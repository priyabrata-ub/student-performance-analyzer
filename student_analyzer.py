import pandas as pd

# Load dataset
df = pd.read_csv("academic_dataset.csv")

# Take roll number as input
roll_number = input("Enter Roll Number: ")

# Find student
student = df[df["Roll_Number"].astype(str) == str(roll_number)]

if student.empty:
    print("Student not found!")

else:
    student = student.iloc[0]

    subjects = [
        "English",
        "Maths",
        "Biology",
        "Chemistry",
        "Physics",
        "Computer_Applications"
    ]

    total_marks = 0

    for subject in subjects:
        total_marks += student[subject]

    percentage = total_marks / len(subjects)

    print("\n===== STUDENT REPORT =====")
    print("Name:", student["Student_Name"])
    print("Roll Number:", student["Roll_Number"])
    print("Attendance:", student["Attendance"], "%")
    print("Total Marks:", total_marks)
    print("Percentage:", round(percentage, 2), "%")

    # Grade Calculation
    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    elif percentage >= 35:
        grade = "D"
    else:
        grade = "F"

    print("Grade:", grade)

    if percentage >= 35:
        print("Result: PASS")
    else:
        print("Result: FAIL")