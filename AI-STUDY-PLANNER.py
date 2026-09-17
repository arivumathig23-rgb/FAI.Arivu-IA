# AI-Based Study Planner - Rational Agent

from datetime import date

# Get today's date
today = date.today()

# Number of subjects
n = int(input("Enter number of subjects: "))

subjects = []

# Get subject details
for i in range(n):
    print(f"\nSubject {i + 1}")

    name = input("Subject name: ")
    deadline = input("Deadline (YYYY-MM-DD): ")
    difficulty = int(input("Difficulty (1-5): "))
    weight = int(input("Topic weight (1-5): "))

    deadline_date = date.fromisoformat(deadline)

    # Calculate days remaining
    days_left = (deadline_date - today).days

    # Avoid division by zero
    if days_left < 1:
        days_left = 1

    # Rational agent priority rule
    priority = (difficulty * weight) / days_left

    subjects.append({
        "name": name,
        "deadline": deadline,
        "difficulty": difficulty,
        "weight": weight,
        "priority": priority
    })


# Sort subjects by priority
subjects.sort(key=lambda x: x["priority"], reverse=True)

# Available study hours
hours = int(input("\nEnter available study hours per day: "))

# Create weekly timetable
print("\n========== WEEKLY STUDY PLAN ==========")

day = 1
hour_used = 0

for subject in subjects:

    if hour_used >= hours:
        day += 1
        hour_used = 0

    if day > 7:
        break

    print(f"Day {day}: {subject['name']} - 1 hour "
          f"(Priority: {subject['priority']:.2f})")

    hour_used += 1

print("\n========== PRIORITY ORDER ==========")

for i, subject in enumerate(subjects, 1):
    print(
        f"{i}. {subject['name']} | "
        f"Priority = {subject['priority']:.2f}"
    )