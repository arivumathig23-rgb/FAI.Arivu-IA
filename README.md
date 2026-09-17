# AI-Based Study Planner – Rational Agent

## 📌 Project Description

The **AI-Based Study Planner** is a Python program that works as a simple **Rational Agent** for creating a study plan.

The program collects information about different subjects, including:

* Subject name
* Deadline
* Difficulty level
* Topic weight
* Available study hours per day

It then calculates a **priority score** for each subject. Subjects with higher priority are scheduled earlier in the weekly study plan.

---

## 🎯 Objective

The main objective of this project is to demonstrate the concept of a **Rational Agent** using Python.

The agent makes a rational decision by assigning study priority based on:

1. **Difficulty** – How difficult the subject is.
2. **Topic Weight** – Importance of the topic.
3. **Days Remaining** – How much time is left before the deadline.

The priority is calculated using:

```text
Priority = (Difficulty × Topic Weight) / Days Remaining
```

A higher priority score means the subject requires more immediate attention.

---

## 🤖 Rational Agent Concept

A rational agent observes the available information and chooses an action that helps achieve its goal.

In this project:

**Percepts / Inputs:**

* Subject name
* Deadline
* Difficulty
* Topic weight
* Available study hours

**Decision Rule:**

```text
Priority = (Difficulty × Weight) / Days Remaining
```

**Action:**

* Sort subjects according to their priority.
* Assign study time to subjects in priority order.
* Generate a weekly study plan.

---

## 🧮 Priority Calculation

For each subject, the program calculates the number of days remaining until the deadline.

The priority is then calculated as:

```text
Priority = (Difficulty × Weight) / Days Remaining
```

### Example

Suppose a subject has:

```text
Difficulty = 5
Weight = 4
Days Remaining = 2
```

Then:

```text
Priority = (5 × 4) / 2
         = 10
```

Therefore, the subject receives a high priority.

---

## 🛠️ Technologies Used

* **Python 3**
* `datetime` module
* Lists
* Dictionaries
* Functions and loops
* Sorting
* Basic mathematical calculations

---

## 📂 Project Structure

```text
AI-Based-Study-Planner/
│
├── src/
│   └── study_planner.py
│
├── tests/
│   └── test_study_planner.py
│
└── README.md
```

> If your Python file is currently in the root folder instead of `src/`, you can move it into the `src` folder to match the required project structure.

---

## ▶️ How to Run

### 1. Install Python

Make sure Python 3 is installed on your computer.

Check the Python version:

```bash
python --version
```

### 2. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 3. Open the Project

```bash
cd AI-Based-Study-Planner
```

### 4. Run the Program

If the file is inside `src`:

```bash
python src/study_planner.py
```

---

## 💻 Sample Input

```text
Enter number of subjects: 3

Subject 1
Subject name: Mathematics
Deadline (YYYY-MM-DD): 2026-09-20
Difficulty (1-5): 5
Topic weight (1-5): 5

Subject 2
Subject name: Python
Deadline (YYYY-MM-DD): 2026-09-25
Difficulty (1-5): 3
Topic weight (1-5): 4

Subject 3
Subject name: English
Deadline (YYYY-MM-DD): 2026-09-28
Difficulty (1-5): 2
Topic weight (1-5): 3

Enter available study hours per day: 2
```

---

## 📤 Sample Output

```text
========== WEEKLY STUDY PLAN ==========

Day 1: Mathematics - 1 hour (Priority: 6.25)
Day 1: Python - 1 hour (Priority: 1.20)
Day 2: English - 1 hour (Priority: 0.50)

========== PRIORITY ORDER ==========

1. Mathematics | Priority = 6.25
2. Python | Priority = 1.20
3. English | Priority = 0.50
```

*The exact priority values and order depend on the current date and the deadlines entered by the user.*

---

## 🔄 Working Process

```text
Start
  ↓
Enter number of subjects
  ↓
Enter subject details
  ↓
Calculate days remaining
  ↓
Calculate priority score
  ↓
Store subject information
  ↓
Sort subjects by priority
  ↓
Enter available study hours
  ↓
Generate weekly study plan
  ↓
Display priority order
  ↓
End
```

---

## ⭐ Features

* Calculates study priority automatically.
* Considers subject difficulty.
* Considers topic importance.
* Considers approaching deadlines.
* Sorts subjects based on priority.
* Generates a simple 7-day study timetable.
* Prevents division by zero when the deadline is today or has passed.
* Uses a simple rational-agent decision rule.

---

## ⚙️ Priority Rules

| Factor         |             Range | Effect                               |
| -------------- | ----------------: | ------------------------------------ |
| Difficulty     |               1–5 | Higher difficulty increases priority |
| Topic Weight   |               1–5 | Higher importance increases priority |
| Days Remaining | Based on deadline | Fewer days increases priority        |

The agent therefore gives greater attention to subjects that are **difficult, important, and close to their deadline**.

---

## 🚧 Limitations

This is a basic rational-agent implementation. Some limitations are:

* Each subject is currently assigned **1 hour** at a time.
* The program does not check whether the total available hours are sufficient for all subjects.
* The timetable is generated for a maximum of 7 days.
* The program does not consider individual study preferences.
* It does not dynamically update the timetable after completing a study session.
* It uses a simple priority formula rather than a machine-learning model.

---

## 🔮 Future Enhancements

Possible improvements include:

* Allow different study durations for each subject.
* Add break times between study sessions.
* Generate a complete timetable for each day.
* Add progress tracking.
* Recalculate priorities automatically each day.
* Add a graphical user interface (GUI).
* Store study plans in a file or database.
* Add notifications and reminders.
* Consider completed and pending topics.
* Use historical study performance to improve scheduling.

---

## 📚 Learning Outcomes

Through this project, the following concepts are demonstrated:

* Python programming
* Lists and dictionaries
* Loops and conditional statements
* Date calculations
* Sorting
* Mathematical formulas
* Problem-solving
* Artificial Intelligence – Rational Agent concept

---

## 👨‍💻 Author

**Your Name**

GitHub: **Your GitHub Username**

---

## 📄 License

This project is created for **academic/educational purposes**.
