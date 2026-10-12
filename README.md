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

Arivumathi G

GitHub: Artificial Intelligence & Machine Learning

---

## 📄 License

This project is created for **academic/educational purposes**.
# AI-Based Study Planner – Rational Agent → Constraint-Based Adaptive Timetable

An AI study planner built in two stages:

* **IA1 – Rational Agent:** ranks subjects with a utility (priority) rule.
* **IA2 – Final Extension:** turns the planner into a **constraint-based adaptive timetable** using a CSP solver, a syllabus ontology with a rule base, and probability-based re-planning.

---

## 📂 Project Structure

```
FAI.Arivu-IA/
├── src/
│   ├── study_planner.py          # IA1 – rational agent (priority rule)
│   └── study_planner_ia2.py      # IA2 – CSP + ontology + rules + re-planning
├── tests/
│   └── test_study_planner_ia2.py # unit tests for IA2
├── docs/
│   ├── ontology.dot              # ontology graph (Graphviz)
│   ├── ontology.png              # ontology diagram
│   └── *.png                     # output screenshots
├── requirements.txt
├── LICENSE
└── README.md
```

---

## ▶️ How to Run

Requires **Python 3.8+**. No external packages (standard library only).

```bash
# IA1
python src/study_planner.py

# IA2
python src/study_planner_ia2.py
```

IA2 first asks `Use the built-in sample data? (y/n)`.
Type `y` for the demo, or `n` to enter your own subjects (name, deadline, difficulty 1-5, topic weight 1-5, last quiz score, units/topics, prerequisites, study hours per day).

Run the tests:

```bash
python -m unittest discover -s tests -v
```

Optional – draw the ontology diagram (needs [Graphviz](https://graphviz.org/download/)):

```bash
dot -Tpng docs/ontology.dot -o docs/ontology.png
```

---

# IA1 – Rational Agent

The agent takes subjects, deadlines, difficulty, topic weight and daily study hours, then ranks subjects with:

```
Priority = (Difficulty × Topic Weight) / Days Remaining
```

A higher score means the subject needs attention sooner. Days remaining is never allowed to drop below 1 (prevents division by zero). In IA2 this same rule is kept and used as the agent's utility: it prints the priority order, decides which subject the plain solver tries first, and breaks ties in the MRV heuristic.

---

# IA2 – Constraint-Based Adaptive Timetable

## 1. CSP layer

The timetable is formulated as a Constraint Satisfaction Problem.

| Element | Definition |
|---------|-----------|
| **Variables** | One variable per study session (topic sessions, extra sessions, one revision session per subject) |
| **Domains** | `(day, slot)` pairs, only days before the subject's deadline |
| **Daily cap** | Each day has exactly *CAP* slots (= study hours per day), so no day exceeds the cap |
| **All-different** | Two sessions cannot share the same `(day, slot)` |
| **Deadline** | Every session of a subject is finished before its exam day |
| **Prerequisite order** | A topic's session comes after its prerequisite topic's session |
| **No hard back-to-back** | Sessions of two different *Hard* subjects are never in adjacent slots on the same day |
| **Minimum revision gap** | Revision is at least `REV_GAP` day(s) after every other session of that subject |

**Solvers compared**

* **Plain backtracking** – fixed variable order, no heuristics, no propagation.
* **Backtracking + MRV + LCV + AC-3** – *MRV* picks the variable with the fewest remaining values (ties: degree, then IA1 priority), *LCV* tries the value that rules out the fewest options for neighbours, *AC-3* prunes domains before the search and after every assignment (MAC).

The program prints assignments tried and runtime for both.

## 2. Knowledge & reasoning layer

**Ontology:** `Subject → Unit → Topic`, with `prerequisiteOf` relations (stored as triples, drawn as a Graphviz diagram in `docs/`). Prerequisites are always scheduled first.

**Rule base (forward chaining):**

| Rule | Meaning |
|------|---------|
| R1 | `Difficulty(s,High) ∧ LastScore(s)<50 → ExtraSessions(s,2)` |
| R2 | `Difficulty(s,Medium) ∧ LastScore(s)<40 → ExtraSessions(s,1)` |
| R3 | `Difficulty(s,High) → Hard(s)` (no two Hard subjects back-to-back) |
| R4 | `Missed(x) → NeedsReschedule(x)` |
| R5 | `ProbOnTime(s)<0.6 → AtRisk(s)` (fairness guard) |

The program prints which rules fired.

## 3. Applied & responsible AI layer

* **Probability of finishing on time:** each remaining session succeeds with probability *p*. If the number of missed sessions is at most the free buffer slots before the exam, the subject still finishes on time:
  `P(on time) = Σ_{k=0..buffer} C(n,k) (1−p)^k p^(n−k)`
* ***p* is learned** from what actually happened: a Beta prior (by difficulty) updated with sessions done/missed.
* **Fairness:** the program reports every subject's sessions, buffer and P(on time), the Jain fairness index, and flags starved or at-risk subjects.
* **Re-planning:** when sessions are missed, finished sessions are kept fixed, missed ones are re-scheduled, and the plan is re-solved from the next day.

---

## 💻 Sample Output (built-in sample data)

```
CSP LAYER : plain backtracking  vs  MRV + LCV + AC-3
  Method                       assignments tried   runtime (ms)   solved
  Plain backtracking                         121           0.37     True
  MRV + LCV + AC-3 (MAC)                      15          35.75     True
  AC-3 preprocessing shrank total domain size 294 -> 217

Generated timetable:
  Day   Slot 1                Slot 2                Slot 3
  Day 1 Math:Equations        Math:Polynomials      Math:Limits
  Day 2 Math:Derivatives      English:Grammar       Python:Syntax
  Day 3 Math:Extra1           Math:Extra2           English:Essay
  Day 4 Python:ControlFlow    English:Revision      Math:Revision
  Day 5 Python:Functions      Python:OOP            -
  Day 6 -                     -                     -
  Day 7 Python:Revision       -                     -

  Subject      sessions  buffer  p(session)  P(on time)
  Mathematics         7       4        0.85      99.88%
  Python              5       6        0.85     100.00%
  English             3       6        0.95     100.00%
  Jain fairness index over P(on time) = 1.000

RE-PLANNING: student misses Mathematics:Derivatives and English:Grammar on Day 2
  FIRED  R4: Missed(x) -> NeedsReschedule(x)
  Mathematics:Derivatives  Day 2 slot 1  ->  Day 3 slot 1
  English:Grammar          Day 2 slot 2  ->  Day 4 slot 2
  ...
  Mathematics   P(on time) drops 99.88% -> 81.92%
```

**Reading the comparison:** MRV + LCV + AC-3 needs far fewer assignments (15 vs 121). On this small problem plain backtracking is faster in milliseconds because AC-3 has overhead; the advantage of the heuristics grows on tighter, larger problems.

---

## ✅ Tests

`tests/test_study_planner_ia2.py` checks that:

* prerequisites are always scheduled before the topics that need them
* no session is scheduled after its deadline
* no two hard subjects are back-to-back
* the daily cap, slot uniqueness and revision gap hold
* rule R1 gives a hard subject with a low score two extra sessions (and does not fire otherwise)
* a missed session fires rule R4
* re-planning keeps finished sessions fixed and the new plan is still valid
* the probability, posterior and fairness helpers behave correctly

---

## 🚧 Limitations

* Each session is **1 hour**; the solver does not split or merge hours.
* The plan covers a **7-day horizon**; deadlines further away are treated as day 7.
* The timetable is a **feasible** plan, not an optimal one – there is no objective that spreads study evenly or avoids gaps.
* Constraints are fixed (daily cap, revision gap, no hard back-to-back); the user cannot add personal preferences or break times.
* The success probability uses a simple Beta/Binomial model and assumes sessions are independent.
* An impossible input (very close deadlines, too many topics for the hours available) produces *no feasible timetable* instead of a best-effort partial plan.
* Re-planning is triggered by missed sessions entered in the demo scenario; there is no calendar, GUI or reminders.

## 🔮 Future Enhancements

* Variable-length sessions and break times
* An optimisation objective (e.g. maximise coverage of high-priority topics before deadlines)
* Let the user enter which sessions were missed in the console
* Save/load plans from a file, and a GUI
* Automatic extra buffer for subjects flagged *AtRisk*

---

## 👨‍💻 Author

Arivumathi G – Artificial Intelligence & Machine Learning

## 📄 License

MIT – created for academic/educational purposes.