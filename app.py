from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

try:
    students = pd.read_csv("academic_dataset.csv")
    scholarships = pd.read_csv("scholarship_dataset.csv")
except Exception as e:
    print("Dataset Error:", e)
    students = pd.DataFrame()
    scholarships = pd.DataFrame()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/dataset", methods=["GET", "POST"])
def dataset():

    result = None
    error = None

    if request.method == "POST":

        roll_number = request.form.get("roll_number", "").strip()

        if roll_number == "":
            error = "Please enter a Roll Number."

        elif students.empty:
            error = "Student dataset not available."

        else:

            student_data = students[
                students["Roll_Number"].astype(str) == str(roll_number)
            ]

            if student_data.empty:
                error = "Student not found."

            else:

                student = student_data.iloc[0]

                subjects = [
                    "English",
                    "Maths",
                    "Biology",
                    "Chemistry",
                    "Physics",
                    "Computer_Applications"
                ]

                total_marks = sum(student[sub] for sub in subjects)
                percentage = total_marks / len(subjects)

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

                eligible_scholarships = []

                for _, scholarship in scholarships.iterrows():

                    if (
                        percentage >= scholarship["Min_Percentage"]
                        and student["Family_Income_Per_Annum"] <= scholarship["Max_Income"]
                        and (
                            scholarship["Caste"] == "Any"
                            or scholarship["Caste"] == student["Caste"]
                        )
                    ):

                        eligible_scholarships.append({
                            "name": scholarship["Scholarship_Name"],
                            "amount": scholarship["Amount"]
                        })

                result = {
                    "name": student["Student_Name"],
                    "roll": student["Roll_Number"],
                    "attendance": student["Attendance"],
                    "income": student["Family_Income_Per_Annum"],
                    "caste": student["Caste"],
                    "total": total_marks,
                    "percentage": round(percentage, 2),
                    "grade": grade,
                    "scholarships": eligible_scholarships,
                    "scholarship_count": len(eligible_scholarships)
                }

    return render_template(
        "dataset.html",
        result=result,
        error=error
    )


@app.route("/manual", methods=["GET", "POST"])
def manual():

    result = None
    error = None

    if request.method == "POST":

        try:

            english = int(request.form["english"])
            maths = int(request.form["maths"])
            biology = int(request.form["biology"])
            chemistry = int(request.form["chemistry"])
            physics = int(request.form["physics"])
            computer = int(request.form["computer"])

            income = int(request.form["income"])
            caste = request.form["caste"]

            marks = [
                english,
                maths,
                biology,
                chemistry,
                physics,
                computer
            ]

            if any(mark < 0 or mark > 100 for mark in marks):
                error = "Marks must be between 0 and 100."

            elif income < 0:
                error = "Income cannot be negative."

            else:

                total = sum(marks)
                percentage = total / 6

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

                eligible_scholarships = []

                for _, scholarship in scholarships.iterrows():

                    if (
                        percentage >= scholarship["Min_Percentage"]
                        and income <= scholarship["Max_Income"]
                        and (
                            scholarship["Caste"] == "Any"
                            or scholarship["Caste"] == caste
                        )
                    ):

                        eligible_scholarships.append({
                            "name": scholarship["Scholarship_Name"],
                            "amount": scholarship["Amount"]
                        })

                result = {
                    "percentage": round(percentage, 2),
                    "grade": grade,
                    "scholarships": eligible_scholarships,
                    "scholarship_count": len(eligible_scholarships)
                }

        except Exception:
            error = "Please enter valid values."

    return render_template(
        "manual.html",
        result=result,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)