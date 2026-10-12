"""
AI-Based Study Planner – Rational Agent (IA1 → IA2 Final Project)

Covers:
1. CSP timetable: variables, domains, constraints, backtracking, MRV, LCV,
   forward checking and AC-3-style arc consistency.
2. Knowledge/reasoning: prerequisite rules, forward chaining, inference trace,
   and a simple uncertainty estimate.
3. Applied/responsible AI: transparent explanations, fairness checks, and
   privacy/accountability notes in the report.

Run from repository root:
    python src/study_planner.py
    python src/study_planner.py --demo
"""

from __future__ import annotations
import argparse
import copy
import json
from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List, Optional, Tuple

Slot = Tuple[int, int]  # (day_index, session_index)


@dataclass
class Subject:
    name: str
    deadline: str
    difficulty: int
    weight: int
    hours_needed: int
    prerequisites: List[str] = field(default_factory=list)
    completed_hours: int = 0

    def __post_init__(self):
        self.name = self.name.strip()
        self.deadline = self.deadline.strip()
        self.difficulty = int(self.difficulty)
        self.weight = int(self.weight)
        self.hours_needed = int(self.hours_needed)
        self.completed_hours = int(self.completed_hours)
        if not self.name:
            raise ValueError("Subject name cannot be empty.")
        date.fromisoformat(self.deadline)
        if not 1 <= self.difficulty <= 5:
            raise ValueError("Difficulty must be between 1 and 5.")
        if not 1 <= self.weight <= 5:
            raise ValueError("Importance/weight must be between 1 and 5.")
        if self.hours_needed < 1:
            raise ValueError("Required study hours must be at least 1.")
        if not 0 <= self.completed_hours <= self.hours_needed:
            raise ValueError("Completed hours must be between 0 and required hours.")
        self.prerequisites = [p.strip() for p in self.prerequisites if p.strip()]

    @property
    def days_left(self) -> int:
        return max(1, (date.fromisoformat(self.deadline) - date.today()).days)

    @property
    def remaining_hours(self) -> int:
        return self.hours_needed - self.completed_hours

    @property
    def priority(self) -> float:
        # Preserved from IA1: (difficulty × weight) / days_left.
        return (self.difficulty * self.weight) / self.days_left


class StudyPlanner:
    def __init__(self, subjects: List[Subject], days: int = 7,
                 sessions_per_day: int = 3):
        self.subjects = {s.name: copy.deepcopy(s) for s in subjects}
        if len(self.subjects) != len(subjects):
            raise ValueError("Subject names must be unique.")
        self.days = max(1, int(days))
        self.sessions_per_day = max(1, int(sessions_per_day))
        self.nodes = 0
        self.backtracks = 0
        self.ac3_revisions = 0
        self._validate_knowledge()

    def _validate_knowledge(self):
        names = set(self.subjects)
        for s in self.subjects.values():
            missing = set(s.prerequisites) - names
            if missing:
                raise ValueError(f"{s.name}: unknown prerequisite(s): {', '.join(sorted(missing))}")
            if s.name in s.prerequisites:
                raise ValueError(f"{s.name} cannot be its own prerequisite.")
        self._topological_order()  # also detects cycles

    def _topological_order(self):
        order, visiting, visited = [], set(), set()

        def visit(name):
            if name in visiting:
                raise ValueError("Prerequisite cycle detected.")
            if name in visited:
                return
            visiting.add(name)
            for pre in self.subjects[name].prerequisites:
                visit(pre)
            visiting.remove(name)
            visited.add(name)
            order.append(name)

        for name in self.subjects:
            visit(name)
        return order

    def forward_chain(self):
        """Simple rule engine with an auditable inference trace."""
        facts = set()
        trace = []
        for name, subject in self.subjects.items():
            if subject.completed_hours >= subject.hours_needed:
                facts.add(f"completed({name})")
                trace.append(f"FACT: completed({name}) because all required hours are complete.")
        changed = True
        while changed:
            changed = False
            for name, subject in self.subjects.items():
                prereq_facts = [f"completed({p})" for p in subject.prerequisites]
                if prereq_facts and all(f in facts for f in prereq_facts):
                    fact = f"prerequisites_satisfied({name})"
                    if fact not in facts:
                        facts.add(fact)
                        trace.append(
                            f"RULE: prerequisites_satisfied({name}) because "
                            + " AND ".join(prereq_facts) + "."
                        )
                        changed = True
                elif not subject.prerequisites:
                    fact = f"prerequisites_satisfied({name})"
                    if fact not in facts:
                        facts.add(fact)
                        trace.append(f"FACT/RULE: {name} has no prerequisites.")
                        changed = True
        return facts, trace

    def _make_variables(self):
        variables = []
        for name, s in self.subjects.items():
            for hour in range(s.remaining_hours):
                variables.append((name, hour))
        return variables

    def _initial_domains(self, variables):
        today = date.today()
        domains = {}
        for variable in variables:
            name, _ = variable
            deadline = date.fromisoformat(self.subjects[name].deadline)
            days_to_deadline = max(0, (deadline - today).days)
            last_day = min(self.days - 1, days_to_deadline)
            domains[variable] = [
                (d, session)
                for d in range(last_day + 1)
                for session in range(self.sessions_per_day)
            ]
        return domains

    def _consistent(self, variable, slot, assignment):
        name, _ = variable
        subject = self.subjects[name]
        if slot in assignment.values():
            return False

        # Fairness rule: avoid consecutive sessions for the same subject on a day.
        for (other_name, _), other_slot in assignment.items():
            if other_name == name and other_slot[0] == slot[0]:
                if abs(other_slot[1] - slot[1]) <= 1:
                    return False

        # Knowledge rule: prerequisite must be completed already, or scheduled
        # in an earlier slot than the dependent subject.
        for prerequisite in subject.prerequisites:
            pre_subject = self.subjects[prerequisite]
            if pre_subject.remaining_hours == 0:
                continue
            pre_slots = [v for (n, _), v in assignment.items() if n == prerequisite]
            if len(pre_slots) < pre_subject.remaining_hours:
                return False
            if max(pre_slots) >= slot:
                return False
        return True

    def _legal_values(self, variable, domains, assignment):
        return [slot for slot in domains[variable]
                if self._consistent(variable, slot, assignment)]

    def _select_mrv(self, domains, assignment):
        unassigned = [v for v in domains if v not in assignment]
        if not unassigned:
            return None
        # Knowledge-aware eligibility: assign prerequisite hours before a
        # dependent subject, so MRV does not choose a variable with zero legal
        # values merely because its prerequisite has not been scheduled yet.
        eligible = []
        for variable in unassigned:
            name = variable[0]
            ready = True
            for prerequisite in self.subjects[name].prerequisites:
                required = self.subjects[prerequisite].remaining_hours
                assigned = sum(1 for (n, _h) in assignment if n == prerequisite)
                if assigned < required:
                    ready = False
                    break
            if ready:
                eligible.append(variable)
        candidates = eligible or unassigned
        return min(
            candidates,
            key=lambda v: (
                len(self._legal_values(v, domains, assignment)),
                -self.subjects[v[0]].priority,
                v[0], v[1]
            )
        )

    def _lcv_values(self, variable, domains, assignment):
        # Least-constraining value: prefer the slot that removes the fewest
        # alternatives from other unassigned variables.
        def impact(slot):
            return sum(
                1 for peer in domains
                if peer != variable and peer not in assignment and slot in domains[peer]
            )
        return sorted(domains[variable], key=lambda slot: (impact(slot), slot[0], slot[1]))

    def _revise(self, xi, xj, domains):
        # Arc consistency for the binary all-different slot constraint:
        # if xj has one possible slot, remove it from xi's domain.
        if len(domains[xj]) != 1:
            return False
        fixed = domains[xj][0]
        if fixed in domains[xi] and len(domains[xi]) > 1:
            domains[xi].remove(fixed)
            return True
        return False

    def _ac3(self, domains, variables):
        queue = [(xi, xj) for xi in variables for xj in variables if xi != xj]
        while queue:
            xi, xj = queue.pop(0)
            if self._revise(xi, xj, domains):
                self.ac3_revisions += 1
                if not domains[xi]:
                    return False
                for xk in variables:
                    if xk != xi and xk != xj:
                        queue.append((xk, xi))
        return all(domains[v] for v in variables)

    def _search(self, domains, assignment, improved=True):
        self.nodes += 1
        if len(assignment) == len(domains):
            return dict(assignment)
        variable = self._select_mrv(domains, assignment) if improved else next(
            (v for v in domains if v not in assignment), None
        )
        if variable is None:
            return None
        values = self._lcv_values(variable, domains, assignment) if improved else list(domains[variable])
        for slot in values:
            if not self._consistent(variable, slot, assignment):
                continue
            new_assignment = dict(assignment)
            new_assignment[variable] = slot
            new_domains = {v: list(vals) for v, vals in domains.items()}
            new_domains[variable] = [slot]
            failed = False
            for peer in new_domains:
                if peer not in new_assignment and slot in new_domains[peer]:
                    new_domains[peer].remove(slot)
                    if not new_domains[peer]:
                        failed = True
                        break
            if failed:
                self.backtracks += 1
                continue
            remaining = [v for v in new_domains if v not in new_assignment]
            if improved and remaining and not self._ac3(new_domains, remaining):
                self.backtracks += 1
                continue
            result = self._search(new_domains, new_assignment, improved)
            if result is not None:
                return result
        self.backtracks += 1
        return None

    def generate_timetable(self, improved=True):
        self.nodes = self.backtracks = self.ac3_revisions = 0
        variables = self._make_variables()
        if not variables:
            return {d: [] for d in range(self.days)}
        domains = self._initial_domains(variables)
        if any(not domain for domain in domains.values()):
            return None
        result = self._search(domains, {}, improved)
        if result is None:
            return None
        timetable = {d: [] for d in range(self.days)}
        for (name, hour), (day, session) in result.items():
            timetable[day].append({
                "session": session + 1,
                "subject": name,
                "hour_number": hour + 1,
                "priority": round(self.subjects[name].priority, 2)
            })
        for day in timetable:
            timetable[day].sort(key=lambda item: item["session"])
        return timetable

    def completion_likelihood(self, subject_name):
        s = self.subjects[subject_name]
        available = min(self.days, max(0, (date.fromisoformat(s.deadline) - date.today()).days) + 1)
        slots = available * self.sessions_per_day
        if s.remaining_hours == 0:
            probability = 1.0
            explanation = "All required hours are marked complete."
        else:
            capacity = min(1.0, slots / s.remaining_hours)
            difficulty_factor = 1 - (s.difficulty - 1) * 0.08
            urgency_factor = min(1.0, 0.60 + s.priority / 20)
            probability = max(0.05, min(0.98, capacity * difficulty_factor * urgency_factor))
            explanation = (
                f"{s.remaining_hours} hour(s) remain, {slots} possible slot(s) exist "
                f"before the deadline, difficulty is {s.difficulty}/5, and priority is "
                f"{s.priority:.2f}. This is a heuristic estimate, not a calibrated probability."
            )
        return {"percent": round(probability * 100, 1), "explanation": explanation}

    def replan_after_missed_session(self, missed_day, missed_session, completed_subjects=None):
        """Rebuild a timetable after a missed slot; completed subjects are excluded."""
        completed_subjects = set(completed_subjects or [])
        remaining = [
            copy.deepcopy(s) for name, s in self.subjects.items()
            if name not in completed_subjects and s.remaining_hours > 0
        ]
        if not remaining:
            return {"success": True, "timetable": {}, "message": "No remaining study hours."}
        # Replanning begins from today; record missed session in the explanation.
        revised_planner = StudyPlanner(remaining, days=self.days, sessions_per_day=self.sessions_per_day)
        plan = revised_planner.generate_timetable(improved=True)
        return {
            "success": plan is not None,
            "timetable": plan,
            "message": (
                f"Missed day {int(missed_day) + 1}, session {int(missed_session)}. "
                + ("A revised timetable was generated." if plan is not None
                   else "No feasible timetable; increase available sessions/days or revise deadlines.")
            )
        }


def demo_subjects():
    today = date.today()
    return [
        Subject("Python", (today.replace(day=today.day)).isoformat(), 3, 5, 2),
        Subject("Mathematics", (today.replace(day=today.day)).isoformat(), 5, 5, 2),
        Subject("AI Basics", (today.replace(day=today.day)).isoformat(), 4, 4, 1, ["Python"]),
    ]


def make_demo_subjects():
    from datetime import timedelta
    today = date.today()
    return [
        Subject("Python", (today + timedelta(days=6)).isoformat(), 3, 5, 2),
        Subject("Mathematics", (today + timedelta(days=4)).isoformat(), 5, 5, 2),
        Subject("AI Basics", (today + timedelta(days=6)).isoformat(), 4, 4, 1, ["Python"]),
        Subject("Database", (today + timedelta(days=6)).isoformat(), 2, 3, 2),
    ]


def print_timetable(plan, days):
    if plan is None:
        print("No feasible timetable found. Try more sessions or later deadlines.")
        return
    labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for day in range(days):
        print(f"\n{labels[day] if day < 7 else f'Day {day + 1}'}:")
        entries = plan.get(day, [])
        if not entries:
            print("  Free / buffer time")
        for item in entries:
            print(f"  Session {item['session']}: {item['subject']} "
                  f"(priority {item['priority']})")


def main():
    parser = argparse.ArgumentParser(description="IA2 Adaptive Study Planner")
    parser.add_argument("--demo", action="store_true", help="run sample data")
    args = parser.parse_args()
    print("=== AI-Based Study Planner – Rational Agent (IA2) ===")

    if args.demo:
        subjects = make_demo_subjects()
        sessions = 3
    else:
        count = int(input("Number of subjects: "))
        subjects = []
        for i in range(count):
            print(f"\nSubject {i + 1}")
            name = input("Subject name: ").strip()
            deadline = input("Deadline (YYYY-MM-DD): ").strip()
            difficulty = int(input("Difficulty (1-5): "))
            weight = int(input("Importance/weight (1-5): "))
            hours = int(input("Required study hours: "))
            prereq = input("Prerequisites, comma-separated (or blank): ")
            subjects.append(Subject(name, deadline, difficulty, weight, hours,
                                    [p.strip() for p in prereq.split(",") if p.strip()]))
        sessions = int(input("Study sessions available per day: "))

    try:
        planner = StudyPlanner(subjects, days=7, sessions_per_day=sessions)
        plan = planner.generate_timetable(improved=True)
    except ValueError as exc:
        print(f"Input/knowledge error: {exc}")
        return

    print("\n=== CSP TIMETABLE (MRV + LCV + propagation) ===")
    print_timetable(plan, 7)

    print("\n=== KNOWLEDGE BASE / FORWARD-CHAINING TRACE ===")
    facts, trace = planner.forward_chain()
    for line in trace:
        print("-", line)
    print("Derived facts:", ", ".join(sorted(facts)) if facts else "(none yet)")

    print("\n=== UNCERTAINTY / COMPLETION-LIKELIHOOD ESTIMATES ===")
    for name in planner.subjects:
        estimate = planner.completion_likelihood(name)
        print(f"{name}: {estimate['percent']}%")
        print("  Explanation:", estimate["explanation"])

    print("\n=== BASELINE VS IMPROVED SEARCH ===")
    baseline = StudyPlanner(subjects, days=7, sessions_per_day=sessions)
    baseline_plan = baseline.generate_timetable(improved=False)
    improved = StudyPlanner(subjects, days=7, sessions_per_day=sessions)
    improved_plan = improved.generate_timetable(improved=True)
    print(f"Plain backtracking: {'success' if baseline_plan is not None else 'no solution'}, "
          f"nodes={baseline.nodes}, backtracks={baseline.backtracks}")
    print(f"MRV + LCV + forward checking + AC-3: "
          f"{'success' if improved_plan is not None else 'no solution'}, "
          f"nodes={improved.nodes}, backtracks={improved.backtracks}, "
          f"AC-3 revisions={improved.ac3_revisions}")

    print("\n=== ADAPTIVE REPLANNING DEMO ===")
    revised = planner.replan_after_missed_session(0, 1)
    print(revised["message"])
    if revised["success"]:
        print_timetable(revised["timetable"], 7)

    print("\n=== RESPONSIBLE AI NOTE ===")
    print("Explanations show priority, deadline, difficulty, and remaining workload.")
    print("Review recommendations yourself; the score may reflect inaccurate inputs.")
    print("Avoid entering private student identifiers or sensitive personal information.")


if __name__ == "__main__":
    main()
