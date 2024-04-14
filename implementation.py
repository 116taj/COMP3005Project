import psycopg2 as pg2
import datetime as dt
conn = pg2.connect(database="COMP3005", user="postgres", password="postgres", host="127.0.0.1", port="5432")
cur = conn.cursor()

def menu():
   while True:
    print("Who are you?")
    print("1. Member")
    print("2. Trainer")
    print("3. Admin")
    print("0. Exit")
    choice = int(input("Type a Number: "))
    if choice == 1:
        while True:
            print("What would you like to do?")
            print("1. Register Member")
            print("2. Manage Member Profile")
            print("3. Display Dashboard")
            print("4. Manage Your Schedule")
            print("0. Go back")
            choice = int(input("Type a Number: "))
            if choice == 1:
                registerMember()
            elif choice == 2:
                manageMemberProfile()
            elif choice == 3:
                displayDashboard()
            elif choice == 4:
                manageMemberSchedule()
            else:
               break
    elif choice == 2:
        print("What would you like to do?")
        print("1. Manage Your Schedule")
        print("2. View Member Profile")
        choice = int(input("Type a Number: "))
        if choice == 1:
            manageTrainerSchedule()
        elif choice == 2:
            viewMemberProfile()
        else:
            break
    elif choice == 3:
        print("What would you like to do?")
        print("1. Manage Room Bookings")
        print("2. Monitor Equipment Maintenence")
        print("3. Update Class Schedules")
        print("4. Payment Processing")
        choice = int(input("Type a Number: "))
        if choice == 1:
            roomManagement()
        elif choice == 2:
            equipmentMaintenence()
        elif choice == 3:
            classScheduling()
        elif choice == 4:
            billing()
        else:
            break
    else:
       break
    
def registerMember():
    print("Welcome to the Health and Fitness Club!")
    print("To register, we need some information from you.")
    while True:
        fname = input("First name: ")
        lname = input("Last name: ")
        phone = input("Phone number (xxx-xxx-xxxx): ")
        email = input("Email: ")
        try:
            weight = int(input("Weight (in pounds): "))
            height = int(input("Height (in inches): "))
        except ValueError: 
            print("Weight and/or height must be integers. Please try again.")
            continue
        payment = input("Payment information: ")
        if fname == '' or lname == '' or phone == '' or email == '' or weight == '' or height == '' or payment == '' :
            print("No field can be empty. Please try again.")
        else:
            print("Thank you.")
            try:
                cur.execute("INSERT INTO Members (first_name, last_name, phone_number, email, weight, height, payment_info) VALUES (%s, %s, %s, %s, %s, %s, %s);", (fname, lname, phone, email, weight, height, payment))
                conn.commit()
                break
            except Exception as e:
                print(e)
                print("This email already exists. You cannot have multiple accounts under the same email.")
                conn.rollback()
    print("Registration Success. Welcome!")

def manageMemberProfile():
    email = input("Enter your email: ")
    cur.execute("SELECT EXISTS(SELECT 1 FROM Members WHERE email = %s);", (email,))
    exists = cur.fetchone()[0]
    if not exists:
        print("This account doesn't exist. Are you sure this is the right email?")
        return
    print("What would you like to change?")
    print("1. Update Personal Information")
    print("2. Set Fitness Goals")
    print("3. Update Health Metrics")
    print("0. Nothing")
    choice = int(input("Type a Number: "))
    if choice == 1:
        cur.execute("SELECT first_name,last_name,phone_number,email,payment_info,member_id FROM Members WHERE email =%s;",(email,))
        info = cur.fetchall()
        info = info[0]
        id = info[5]
        print("Here is your current information: ")
        print("First name: "+info[0])
        print("Last name: "+info[1])
        print("Phone number: "+info[2])
        print("Email: "+info[3])
        print("Payment Information: "+info[4])
        print("Would you like to change this information? ")
        print("1. Yes")
        print("0. No")
        choice = int(input("Type a Number: "))
        if choice == 1:
            while True:
                fname = input("First name: ")
                lname = input("Last name: ")
                phone = input("Phone number (xxx-xxx-xxxx): ")
                new_email = input("Email: ")
                payment = input("Payment information: ")
                if fname == '' or lname == '' or phone == '' or new_email == '' or payment == '':
                    print("No field can be empty. Please try again.")
                try:
                    cur.execute("UPDATE Members SET first_name = %s, last_name = %s, phone_number = %s, email = %s, payment_info = %s WHERE member_id = %s;", (fname, lname, phone, new_email, payment, id))
                    conn.commit()
                    break
                except Exception as e:
                    print(e)
                    print("This email already exists. Please try another email.")
                    conn.rollback()
            print("Information successfully updated.")
    elif choice == 2:
        print("Let's make a new fitness goal.")
        cur.execute("SELECT weight,member_id FROM Members WHERE email =%s;",(email,))
        info = cur.fetchall()[0]
        id = info[1]
        print("Your current weight is "+str(info[0]))
        goalw = input("Enter your goal weight: ")
        current = dt.datetime.now().date()
        print("The current date is "+str(current))
        goaltime = int(input("How many days will you allocate for this goal? "))
        goaldate = dt.datetime.now().date()+dt.timedelta(days=goaltime)
        print("Then your goal date is "+str(goaldate)+".")
        print("Are you okay with this? ")
        print("1. Yes")
        print("0. No")
        choice = int(input("Type a Number: "))
        if choice == 1:
            cur.execute("INSERT INTO FitnessGoals (starting_weight,goal_weight,start_time,end_time,member_id) VALUES(%s,%s,%s,%s,%s);",(info[0],goalw,current,goaldate,id))
            conn.commit()
    elif choice == 3:
        cur.execute("SELECT weight,height,member_id FROM Members WHERE email =%s;",(email,))
        info = cur.fetchall()
        info = info[0]
        id = info[2]
        print("Here is your current health information: ")
        print("Weight: "+str(info[0]))
        print("Height: "+str(info[1]))
        print("Would you like to change this information? ")
        print("1. Yes")
        print("0. No")
        choice = int(input("Type a Number: "))
        if choice == 1:
            while True:
                    try:
                        weight = int(input("Weight (in pounds): "))
                        height = int(input("Height (in inches): "))
                    except ValueError: 
                        print("Weight and/or height must be integers. Please try again.")
                        continue
                    cur.execute("UPDATE Members SET weight = %s, height = %s WHERE member_id = %s;", (weight,height,id))
                    conn.commit()
                    break
            print("Information successfully updated.")

def displayDashboard():
    email = input("Enter your email: ")
    cur.execute("SELECT EXISTS(SELECT 1 FROM Members WHERE email = %s);", (email,))
    exists = cur.fetchone()[0]
    if not exists:
        print("This account doesn't exist. Are you sure this is the right email?")
        return
    cur.execute("SELECT weight,member_id FROM Members WHERE email =%s;",(email,))
    info = cur.fetchall()[0]
    id = info[1]
    print("Your current weight is "+str(info[0])+".")
    print("Today's date is "+str(dt.datetime.now().date())+".")
    cur.execute("SELECT goal_weight,end_time FROM FitnessGoals WHERE member_id = %s",(id,))
    goals = cur.fetchall()
    print("You have "+str(len(goals))+" fitness goals.")
    for goal in goals: 
        gw = goal[0]
        time = goal[1]
        print("Goal: Weight "+str(gw)+" by time "+str(time))
    cur.execute("SELECT name,description,length FROM ExerciseRoutines")
    routines = cur.fetchall()
    print("Here are some routines you can try!")
    for r in routines:
        print(r[0]+": "+r[1]+". It takes "+str(r[2])+" minutes to do.")

def manageMemberSchedule():
    email = input("Enter your email: ")
    cur.execute("SELECT EXISTS(SELECT 1 FROM Members WHERE email = %s);", (email,))
    exists = cur.fetchone()[0]
    if not exists:
        print("This account doesn't exist. Are you sure this is the right email?")
        return
    print("Would you like to register in a class or personal session with a trainer?")
    print("1. Class")
    print("2. Personal")
    print("0. Never mind")
    choice = int(input("Type a Number: "))
    if choice == 1:
        pass
    elif choice == 2:
        day = input("Enter the day you'd like your session: ")
        if day not in ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']:
            print("Bad data. Try again")
            return
        start = input("Enter the start time (HH:MM): ")
        end = input("Enter the end time (HH:MM): ")
        cur.execute("SELECT foreign_id FROM Schedules WHERE schedule_type IN ('Classes','Sessions') AND day_of_week = %s AND (start_time>=%s)AND (end_time<=%s);", (day,start,end))
        print("Here are our trainers:")
        cur.execute("SELECT first_name,last_name,trainer_id FROM Trainers")
        trainers = cur.fetchall()
        for trainer in trainers:
            print(str(trainer[0])+" "+str(trainer[1]))
        choice = input("Which trainer interests you? ")
        tfname, tlname = choice.split()
        


def manageTrainerSchedule():
    email = input("Enter your email: ")
    cur.execute("SELECT EXISTS(SELECT 1 FROM Trainers WHERE email = %s);", (email,))
    exists = cur.fetchone()[0]
    if not exists:
        print("This account doesn't exist. Are you sure this is the right email?")
        return
    cur.execute("SELECT trainer_id FROM Trainers WHERE email = %s",(email,))
    id = cur.fetchone()[0]
    print("Your schedule is the following: ")
    cur.execute("SELECT start_time,end_time,day_of_week FROM Schedules WHERE foreign_id = %s AND schedule_type = %s",(id,'Trainers'))
    schedules = cur.fetchall()
    for s in schedules:
        start = s[0]
        end = s[1]
        day = s[2]
        print(str(start)+" to "+str(end)+" on "+day)
    print("Would you like to adjust your schedule?")
    print("1. Yes")
    print("0. No")
    choice = int(input("Type a Number: "))
    if choice == 1:
        day = input("What day would you like to change? ")
        if day not in ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']:
            print("Bad data. Try again")
            return
        start = input("Enter your beginning hour (HH:MM): ")
        end = input("Enter your end hour (HH:MM): ")
        cur.execute("SELECT EXISTS(SELECT 1 FROM Schedules WHERE foreign_id = %s AND schedule_type = %s AND day_of_week = %s);", (id,'Trainers',day))
        exists = cur.fetchone()[0]
        if exists:
            cur.execute("UPDATE Schedules SET start_time = %s, end_time = %s WHERE foreign_id = %s AND schedule_type = %s AND day_of_week = %s;", (start,end,id,'Trainers',day))
        else:
            cur.execute("INSERT INTO Schedules(start_time,end_time,day_of_week,schedule_type,foreign_id) VALUES(%s,%s,%s,%s,%s)",(start,end,day,'Trainers',id))
        conn.commit()

def viewMemberProfile():
    email = input("Enter your email: ")
    cur.execute("SELECT EXISTS(SELECT 1 FROM Trainers WHERE email = %s);", (email,))
    exists = cur.fetchone()[0]
    if not exists:
        print("This account doesn't exist. Are you sure this is the right email?")
        return
    fname = input("Enter member's first name: ")
    lname = input("Enter member's last name: ")
    cur.execute("SELECT phone_number,email FROM Members WHERE first_name = %s AND last_name =%s",(fname,lname))
    info = cur.fetchall()
    print("There are "+str(len(info))+" matches for this name.")
    for i in info:
        print(fname+" "+lname+" with phone number "+i[0]+" and email "+i[1])
    
def roomManagement():
    email = input("Enter your email: ")
    cur.execute("SELECT EXISTS(SELECT 1 FROM AdministrativeStaff WHERE email = %s);", (email,))
    exists = cur.fetchone()[0]
    if not exists:
        print("This account doesn't exist. Are you sure this is the right email?")
        return
    cur.execute("SELECT start_time,end_time,day_of_week,foreign_id FROM Schedules WHERE schedule_type = %s",('Rooms',))
    rooms = cur.fetchall()
    for r in rooms:
        cur.execute("SELECT name,capacity FROM Rooms WHERE room_id = %s",(r[3],))
        name, capacity = cur.fetchall()[0]
        print("Room "+name+" with capacity "+str(capacity)+" has a class planned.")
        print("This is on "+r[2]+" from "+str(r[0])+" to "+str(r[1]))
        print("Would you like to modify this booking? ")
        print("1. Yes")
        print("0. No")
        choice = int(input("Type a Number: "))
        if choice == 1:
            day = input("Enter new day: ")
            if day not in ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']:
                print("Bad data. Try again")
                return
            start = input("Enter the start time (HH:MM): ")
            end = input("Enter the end time (HH:MM): ")
            cur.execute("UPDATE Schedules SET start_time = %s, end_time = %s, day_of_week = %s WHERE foreign_id = %s AND schedule_type = %s;", (start,end,day,r[3],'Rooms'))
            conn.commit()
                    
def classScheduling():
    email = input("Enter your email: ")
    cur.execute("SELECT EXISTS(SELECT 1 FROM AdministrativeStaff WHERE email = %s);", (email,))
    exists = cur.fetchone()[0]
    if not exists:
        print("This account doesn't exist. Are you sure this is the right email?")
        return
    cur.execute("SELECT name FROM Classes")
    classes = cur.fetchall()
    print("Classes: ")
    for c in classes:
        print(c[0])
    name = input("Choose which class you'd like to modify: ")
    cur.execute("SELECT * FROM Classes WHERE name = %s",(name,))
    c = cur.fetchone()
    cur.execute("SELECT name,capacity FROM Rooms WHERE room_id = %s",(c[3],))
    rname, capacity = cur.fetchall()[0]
    cur.execute("SELECT first_name,last_name FROM Trainers WHERE trainer_id = %s",(c[4],))
    tfname, tlname = cur.fetchall()[0]
    cur.execute("SELECT start_time,end_time,day_of_week FROM Schedules WHERE foreign_id = %s AND schedule_type = %s",(c[0],'Classes'))
    sched = cur.fetchall()[0]
    print(c[1]+" at room "+rname+" with capacity "+str(capacity))
    print("The trainer in charge is "+tfname+" "+tlname)
    print("The class is scheduled to be from "+str(sched[0])+" to "+str(sched[1])+" every "+sched[2]+".")
    print("Would you like to change this?")
    print("1. Yes")
    print("0. No")
    choice = int(input("Type a Number: "))
    if choice == 1:
        day = input("Enter new day: ")
        if day not in ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']:
            print("Bad data. Try again")
            return
        start = input("Enter the start time (HH:MM): ")
        end = input("Enter the end time (HH:MM): ")
        cur.execute("UPDATE Schedules SET start_time = %s, end_time = %s, day_of_week = %s WHERE foreign_id = %s AND schedule_type = %s;", (start,end,day,c[0],'Classes'))
        conn.commit()

def equipmentMaintenence():
    email = input("Enter your email: ")
    cur.execute("SELECT EXISTS(SELECT 1 FROM AdministrativeStaff WHERE email = %s);", (email,))
    exists = cur.fetchone()[0]
    if not exists:
        print("This account doesn't exist. Are you sure this is the right email?")
        return
    cur.execute("SELECT name, needs_maintenence, equipment_id FROM Equipments")
    equipments = cur.fetchall()
    for e in equipments:
        flag = e[1]
        if flag:
            print(e[0]+" needs maintenence.")
        else:
            print(e[0]+" is functional.")
        print("Is this accurate?")
        print("1. Yes")
        print("0. No")
        choice = int(input("Type a Number: "))
        if choice == 0:
            new = e[1]
            cur.execute("UPDATE Equipments SET needs_maintenence = %s WHERE equipment_id = %s",(new,e[2]))
            conn.commit()

def billing():
    email = input("Enter your email: ")
    cur.execute("SELECT EXISTS(SELECT 1 FROM AdministrativeStaff WHERE email = %s);", (email,))
    exists = cur.fetchone()[0]
    if not exists:
        print("This account doesn't exist. Are you sure this is the right email?")
        return
    try:
        fee = float(input("Enter fee: "))
    except ValueError: 
        print("Fee must be float. Please try again.")
        return
    cur.execute("SELECT member_id from Members")
    members = cur.fetchall()
    date = dt.datetime.now()
    for m in members:
        cur.execute("INSERT INTO Bills(date,amount,member_id) VALUES (%s,%s,%s)",(date,fee,m[0]))
    conn.commit()
    
menu()