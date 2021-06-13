import sqlite3

#set up connection to 'timetable.db'
con = sqlite3.connect('timetable.db')
c = con.cursor()


def add():
	name = input("Enter class name: ")
	start_time = input("Enter class start time in 24 hour format: (HH:MM) ")

	end_time = input("Enter class end time in 24 hour format: (HH:MM) ")

	day = input("Enter day (Monday/Tuesday/Wednesday..etc) : ")

	is_lab = input("Type yes, if lab else type no : ")

	c.execute("INSERT INTO timetable VALUES ('%s','%s','%s','%s','%s')"%(name,start_time,end_time,day, is_lab))

	con.commit()


print("1. View db")
print("2. Insert a data")
print("3. Delete a data")
print("4. Delete all data")
ch = int(input("Enter your choice (1/2/3/4): "))

if(ch == 1):
	for row in c.execute('SELECT * FROM timetable'):
		print(row)
	con.close()
if(ch == 2):
	ch = 1
	while(ch == 1):
		add()
		ch = int(input("Enter 1 for adding more: "))
	con.close()
if(ch == 3):
	name = input("Enter the name of the class to be deleted: ")
	start_time=input("Enter class start time in 24 hour format: (HH:MM) -> ")
	day = input("Enter day (Monday/Tuesday/Wednesday...etc) : ")
	c.execute("DELETE FROM timetable WHERE class  = '%s' AND start_time = '%s' AND day = '%s'"%(name, start_time, day))
	con.commit()
	con.close()
if(ch == 4):
	c.execute("DELETE FROM timetable WHERE 1=1")
	con.commit()
	con.close()
else:
	print("Wrong choice")