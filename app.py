import mysql.connector as MSQC

try:
    print("Enter host")
    hname, uname, pname = input("Host: "), input("User: "), input("Password: ")
    connection = MSQC.connect(host=hname, user=uname, password=pname, database='academic_insti')
    print("Database connected")
except MSQC.Error as error:
    print("Failed to connect to the database: {}".format(error))

cursor = connection.cursor()


def update_course():
    print("Enter Department Id")
    dept_id = input()
    print("Enter Course Id")
    course_id = input()
    print("Enter Employee Id")
    teacher_id = input()
    print("Enter Valid Classroom")
    class_Room = input()
    print()

    cursor.execute("SELECT * FROM course WHERE courseId = '{}' AND deptNo = '{}'".format(course_id, dept_id))
    if cursor.fetchone() is None:
        print("Course, deptNo combination not found")
        return
    
    cursor.execute("SELECT * FROM professor WHERE empId = '{}' AND deptNo = '{}'".format(teacher_id, dept_id))
    if cursor.fetchone() is None:
        print("Professor, deptNo combination not found")
        return
    
    cursor.execute("SELECT * FROM teaching WHERE courseId = '{}' AND empId = '{}' AND year = 2006 AND sem = 'Even'".format(course_id, teacher_id))
    if cursor.fetchone() is not None:
        print("Course is already being taken, Would you like to update? (y/n)")
        choice = input()
        if choice == 'y':
            cursor.execute("UPDATE teaching SET classRoom = '{}' WHERE courseId = '{}' AND empId = '{}' AND year = 2006 AND sem = 'Even'".format(class_Room, course_id, teacher_id))
            print("Successfully Updated in teaching table")
        else:
            print("No changes made")
    else:
        cursor.execute("INSERT INTO teaching VALUES ('{}', '{}', 'Even', 2006, '{}')".format(teacher_id, course_id, class_Room))
        print("Successfully Inserted in teaching table")
    
    connection.commit()


def check_prerequisites(course_id, roll_no):
    cursor.execute("SELECT * FROM prerequisite AS p WHERE p.courseId = '{}' AND ((p.prereqCourse IN (SELECT courseId FROM enrollment WHERE rollNo = '{}' AND year < 2006 AND grade = 'U')) OR (p.preReqCourse NOT IN (SELECT courseId FROM enrollment WHERE rollNo = '{}' AND year < 2006)))".format(course_id, roll_no, roll_no))
    return cursor.fetchone() is None

def enroll_student():
    print("Enter Course Id")
    course_id = input()
    print("Enter Roll No")
    roll_no = input()
    print()

    cursor.execute("SELECT * FROM student WHERE rollNo = '{}'".format(roll_no))
    if cursor.fetchone() is None:
        print("Roll No not found")
        return
    
    cursor.execute("SELECT * FROM course WHERE courseId = '{}'".format(course_id))
    if cursor.fetchone() is None:
        print("Course Id not found")
        return

    cursor.execute("SELECT * FROM enrollment WHERE rollNo = '{}' AND courseId = '{}' AND year <= 2006 AND grade <> 'U'".format(roll_no, course_id))
    query_result=cursor.fetchone()
    if query_result is not None:
        if query_result[4]=='':
            print("Student already enrolled in course, No changes made")
        else:
            print("Student has already completed the course")
        return
    
    if not check_prerequisites(course_id, roll_no):
        print("Prerequisites not met, student can't be enrolled in this course, No changes made.")
        return
    
    cursor.execute("INSERT INTO enrollment VALUES ('{}', '{}', 'Even', 2006, '')".format(roll_no, course_id))
    print("Successfully enrolled student in the course")
    connection.commit()

print("Program To add courses or to enroll students in the academic_insti database")

while True:
    print()
    print("Enter your option:")
    print("1. Addition of courses")
    print("2. Student enrollment")
    print("3. Exit program")
    option = input()
    print()
    
    if option == "1":
        update_course()
    elif option == "2":
        enroll_student()
    else:  
        connection.commit()
        print("Exiting program")
        break

connection.close()
