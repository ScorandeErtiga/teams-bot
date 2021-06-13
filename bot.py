from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re
import os.path
from os import path
import sqlite3
import schedule
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
import discord_webhook

PATH = "C:/Program Files (x86)/chromedriver.exe"


opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
# opt.add_argument("--headless")
opt.add_argument("--disable-extensions")
opt.add_argument("--disable-gpu")
opt.add_argument("--disable-dev-shm-usage")

# Pass the argument 1 to allow and 2 to block
opt.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 1, 
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 1, 
    "profile.default_content_setting_values.notifications": 1 
  })

# driver = webdriver.Chrome(chrome_options=opt,service_log_path='NUL')
driver = None
URL = "https://teams.microsoft.com"

#put your teams credentials here
CREDS = {'email' : '190110107039@gcet.ac.in','passwd':'Abhi@3900'}



def login():
	global driver
	
	#login required
	print("logging in")
	emailField = driver.find_element_by_xpath('//*[@id="i0116"]')
	emailField.click()
	emailField.send_keys(CREDS['email'])
	time.sleep(2)
	driver.find_element_by_xpath('//*[@id="idSIButton9"]').click() #Next button
	time.sleep(2)
	passwordField = driver.find_element_by_xpath('//*[@id="i0118"]')
	passwordField.click()
	passwordField.send_keys(CREDS['passwd'])
	driver.find_element_by_xpath('//*[@id="idSIButton9"]').click() #Sign in button
	time.sleep(2)
	driver.find_element_by_xpath('//*[@id="idSIButton9"]').click() #remember login
	time.sleep(5)
	# return driver


def isJoinAvail():
	try:
		joinbtn = driver.find_element_by_class_name("ts-calling-join-button")
		return True
	except:
		return False


def joinclass(class_name,start_time,end_time,isLab):

	global driver

	# time.sleep(5)


	'''
	/html/body/div[1]/div[2]/div[1]/div/left-rail/div/div/school-app-left-rail/channel-list/div/div[1]/ul/li/ul/li[16]
	/html/body/div[1]/div[2]/div[1]/div/left-rail/div/div/school-app-left-rail/channel-list/div/div[1]/ul/li/ul/li[16]/div/div/ul/ng-include/li[1]/a/div[1]/span
	/div/div/ul/ng-include/li[4]/a/div[1]/span - jimit
	/html/body/div[1]/div[2]/div[1]/div/left-rail/div/div/school-app-left-rail/channel-list/div/div[1]/ul/li/ul/li[18]/div/div/ul/ng-include/li[4]/a/div[1]/span
	/html/body/div[1]/div[2]/div[1]/div/left-rail/div/div/school-app-left-rail/channel-list/div/div[1]/ul/li/ul/li[18]/div/div/ul/ng-include/li[1]/a/div[1]/span
	'''

	if(class_name == "ex"):
		class_no = '16'
	if(class_name == "ada"):
		class_no = '18'
	if(class_name == "pe"):
		class_no = '19'
	if(class_name == "cn"):
		class_no = '20'
	if(class_name == "se"):
		class_no = '21'
	if(class_name == "pds"):
		class_no = '22'
	if(class_name == "ipdc"):
		class_no = '23'
	if(class_name == "de"):
		class_no = '24'

	driver.implicitly_wait(5) #change parameter here
	team = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/left-rail/div/div/school-app-left-rail/channel-list/div/div[1]/ul/li/ul/li['+class_no+']')

	time.sleep(1)

	isOpen = team.get_attribute('aria-expanded')
	if(isOpen == "false"):
		team.click()

	time.sleep(1)

	if(isLab == "yes"):
		channel=driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/left-rail/div/div/school-app-left-rail/channel-list/div/div[1]/ul/li/ul/li['+class_no+']/div/div/ul/ng-include/li[4]/a/div[1]/span')
	else:
		channel=driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/left-rail/div/div/school-app-left-rail/channel-list/div/div[1]/ul/li/ul/li['+class_no+']/div/div/ul/ng-include/li[1]/a/div[1]/span')
	channel.click()

	time.sleep(2)

	k = 1
	while(not(isJoinAvail()) and k<=2):
		time.sleep(60)
		driver.refresh()
		k+=1

	if(k>2):
		discord_webhook.send_msg(class_name=class_name,status="noclass",start_time=start_time,end_time=end_time)
		return
	else:
		joinbtn = driver.find_element_by_class_name("ts-calling-join-button")
		joinbtn.click()

	time.sleep(3)
	webcam = driver.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[2]/toggle-button[1]/div/button/span[1]')
	if(webcam.get_attribute('title')=='Turn camera off'):
		webcam.click()
	time.sleep(1)

	microphone = driver.find_element_by_xpath('//*[@id="preJoinAudioButton"]/div/button/span[1]')
	if(microphone.get_attribute('title')=='Mute microphone'):
		microphone.click()

	time.sleep(1)
	joinnowbtn = driver.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[1]/div/div/button')
	joinnowbtn.click()

	discord_webhook.send_msg(class_name=class_name,status="joined",start_time=start_time,end_time=end_time)
	
	#now schedule leaving class
	tmp = "%H:%M"

	class_running_time = datetime.strptime(end_time,tmp) - datetime.strptime(start_time,tmp)

	time.sleep(class_running_time.seconds)

	isScreen = False
	try:
		screen = driver.find_element_by_class_name("ts-calling-screen")
		screen.click()
		isScreen = True
	except:
		discord_webhook.send_msg(class_name=class_name,status="left",start_time=start_time,end_time=end_time)


	if(isScreen == True):
		driver.find_element_by_xpath('//*[@id="teams-app-bar"]/ul/li[3]').click() #come back to homepage
		time.sleep(1)

		driver.find_element_by_xpath('//*[@id="hangup-button"]').click()
		print("Class left")
		discord_webhook.send_msg(class_name=class_name,status="left",start_time=start_time,end_time=end_time)


def start_browser():

	global driver
	driver = webdriver.Chrome(PATH, options=opt)
	driver.get(URL)

	WebDriverWait(driver,10000).until(EC.visibility_of_element_located((By.TAG_NAME,'body')))

	if("login.microsoftonline.com" in driver.current_url):
		login()



def sched():
	conn = sqlite3.connect('timetable.db')
	c=conn.cursor()
	for row in c.execute('SELECT * FROM timetable'):
		#schedule all classes
		name = row[0]
		start_time = row[1]
		end_time = row[2]
		day = row[3]
		is_lab = row[4]

		if day.lower()=="monday":
			schedule.every().monday.at(start_time).do(joinclass,name,start_time,end_time,is_lab)
			print("Scheduled class '%s' on %s at %s"%(name,day,start_time))
		if day.lower()=="tuesday":
			schedule.every().tuesday.at(start_time).do(joinclass,name,start_time,end_time,is_lab)
			print("Scheduled class '%s' on %s at %s"%(name,day,start_time))
		if day.lower()=="wednesday":
			schedule.every().wednesday.at(start_time).do(joinclass,name,start_time,end_time,is_lab)
			print("Scheduled class '%s' on %s at %s"%(name,day,start_time))
		if day.lower()=="thursday":
			schedule.every().thursday.at(start_time).do(joinclass,name,start_time,end_time,is_lab)
			print("Scheduled class '%s' on %s at %s"%(name,day,start_time))
		if day.lower()=="friday":
			schedule.every().friday.at(start_time).do(joinclass,name,start_time,end_time,is_lab)
			print("Scheduled class '%s' on %s at %s"%(name,day,start_time))
		if day.lower()=="saturday":
			schedule.every().saturday.at(start_time).do(joinclass,name,start_time,end_time,is_lab)
			print("Scheduled class '%s' on %s at %s"%(name,day,start_time))
		if day.lower()=="sunday":
			schedule.every().sunday.at(start_time).do(joinclass,name,start_time,end_time,is_lab)
			print("Scheduled class '%s' on %s at %s"%(name,day,start_time))


	#Start browser
	start_browser()
	while True:
		# Checks whether a scheduled task
		# is pending to run or not
		schedule.run_pending()
		time.sleep(1)


if __name__=="__main__":

	sched()
	'''
	# joinclass("Maths","15:13","15:15","sunday")
	op = int(input(("1. Modify Timetable\n2. View Timetable\n3. Start Bot\nEnter option : ")))
	
	if(op==1):
		add_timetable()
	if(op==2):
		view_timetable()
	if(op==3):
		sched()

	'''