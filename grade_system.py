def grade(marks):
    try:
        marks = int(marks)

        if marks < 0 or marks > 100:
            print("Invalid input. Marks can only be between 0 and 100.")
        else:
            if marks >= 90 and marks <= 100:
                print("Your grade is: 'A'")
            elif marks >= 80 and marks < 90:
                print("Your grade is: 'B'")
            elif marks >= 70 and marks < 80:
                print("Your grade is: 'C'")
            elif marks >= 60 and marks < 70:
                print("Your grade is: 'D'")
            else:
                print("Your grade is: 'F'")
    except ValueError:
        print("Invalid input. Please enter the marks between 0 and 100.")

marks = input("Enter your marks: ")
grade(marks)