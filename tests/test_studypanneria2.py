"""
Tests for the IA2 AI-Based Study Planner (CSP + ontology + rules + re-planning).
Run from the repository root:   python -m unittest discover -s tests -v
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import study_planner_ia2 as sp  # noqa: E402


def solve_sample(solver="mac"):
    """Build the sample problem and solve it. Returns (onto, facts, sessions, csp, solution)."""
    sp.finalize()
    onto = sp.Ontology(sp.SYLLABUS)
    facts = sp.build_facts()
    sp.forward_chain(facts, verbose=False)
    sessions = sp.make_sessions(onto, facts)
    csp = sp.build_csp(sessions, onto, facts)
    if solver == "plain":
        sol, _, _ = sp.plain_backtracking(csp, [s.sid for s in sessions])
    else:
        sol, _, _, _ = sp.mrv_lcv_ac3(csp)
    return onto, facts, sessions, csp, sol


class TestSchedule(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.onto, cls.facts, cls.sessions, cls.csp, cls.sol = solve_sample()

    def test_solution_exists_and_complete(self):
        self.assertIsNotNone(self.sol)
        self.assertEqual(set(self.sol), {s.sid for s in self.sessions})

    def test_prerequisites_scheduled_first(self):
        for s in self.sessions:
            if s.kind != "topic":
                continue
            for p in self.onto.prereqs(s.topic):
                pid = f"{s.subject}:{p}"
                self.assertLess(sp.idx(self.sol[pid]), sp.idx(self.sol[s.sid]),
                                f"{pid} must come before {s.sid}")

    def test_no_session_after_deadline(self):
        for s in self.sessions:
            day = self.sol[s.sid][0]
            self.assertLess(day, sp.SUBJECTS[s.subject]["exam_day"],
                            f"{s.sid} is scheduled on/after its exam day")

    def test_no_two_hard_subjects_back_to_back(self):
        hard = {x[1] for x in self.facts if x[0] == "Hard"}
        self.assertGreaterEqual(len(hard), 2)
        for a in self.sessions:
            for b in self.sessions:
                if a.sid < b.sid and a.subject != b.subject and {a.subject, b.subject} <= hard:
                    (d1, k1), (d2, k2) = self.sol[a.sid], self.sol[b.sid]
                    self.assertFalse(d1 == d2 and abs(k1 - k2) == 1,
                                     f"{a.sid} and {b.sid} are back-to-back")

    def test_daily_cap_and_no_slot_clash(self):
        slots = list(self.sol.values())
        self.assertEqual(len(slots), len(set(slots)), "two sessions share one slot")
        for d, k in slots:
            self.assertLess(k, sp.CAP)

    def test_revision_gap(self):
        for s in self.sessions:
            if s.kind == "revision":
                for o in self.sessions:
                    if o.subject == s.subject and o.kind != "revision":
                        self.assertGreaterEqual(self.sol[s.sid][0] - self.sol[o.sid][0], sp.REV_GAP)

    def test_plain_backtracking_also_solves(self):
        *_, sol = solve_sample("plain")
        self.assertIsNotNone(sol)


class TestRules(unittest.TestCase):
    def setUp(self):
        sp.finalize()
        self.facts = sp.build_facts()
        self.log = sp.forward_chain(self.facts, verbose=False)

    def test_r1_hard_subject_with_low_score_gets_two_extra_sessions(self):
        # Mathematics: difficulty High and last score 40 (< 50)
        self.assertIn(("ExtraSessions", "Mathematics", 2), self.facts)

    def test_r1_does_not_fire_when_score_is_high_enough(self):
        # Python: difficulty High but last score 55 (>= 50)
        self.assertFalse(any(f[0] == "ExtraSessions" and f[1] == "Python" for f in self.facts))

    def test_extra_sessions_are_created(self):
        onto = sp.Ontology(sp.SYLLABUS)
        sessions = sp.make_sessions(onto, self.facts)
        extras = [s for s in sessions if s.kind == "extra" and s.subject == "Mathematics"]
        self.assertEqual(len(extras), 2)

    def test_hard_fact_derived_from_high_difficulty(self):
        self.assertIn(("Hard", "Mathematics"), self.facts)
        self.assertNotIn(("Hard", "English"), self.facts)

    def test_missed_session_triggers_reschedule_rule(self):
        self.facts.add(("Missed", "Mathematics:Derivatives"))
        sp.forward_chain(self.facts, verbose=False)
        self.assertIn(("NeedsReschedule", "Mathematics:Derivatives"), self.facts)


class TestReplanning(unittest.TestCase):
    def test_finished_sessions_stay_fixed_and_new_plan_is_valid(self):
        onto, facts, sessions, _, sol = solve_sample()
        today = 2
        on_day2 = sorted((v, k) for k, v in sol.items() if v[0] == 1)
        missed = [k for _, k in on_day2[:2]]
        done = {sid: v for sid, v in sol.items() if v[0] < today and sid not in missed}

        csp2 = sp.build_csp(sessions, onto, facts, start_day=today, fixed=done)
        new, *_ = sp.mrv_lcv_ac3(csp2)
        self.assertIsNotNone(new)

        for sid, slot in done.items():                      # finished work never moves
            self.assertEqual(new[sid], slot)
        for sid in set(new) - set(done):                    # everything else is in the future
            self.assertGreaterEqual(new[sid][0], today)
        for m in missed:                                    # missed sessions were re-planned
            self.assertGreaterEqual(new[m][0], today)
        for s in sessions:                                  # deadlines + prerequisites still hold
            self.assertLess(new[s.sid][0], sp.SUBJECTS[s.subject]["exam_day"])
            if s.kind == "topic":
                for p in onto.prereqs(s.topic):
                    self.assertLess(sp.idx(new[f"{s.subject}:{p}"]), sp.idx(new[s.sid]))


class TestHelpers(unittest.TestCase):
    def test_probability_is_between_0_and_1_and_grows_with_buffer(self):
        p_small = sp.prob_on_time(5, 0.8, 0)
        p_big = sp.prob_on_time(5, 0.8, 3)
        self.assertTrue(0 <= p_small <= p_big <= 1)
        self.assertAlmostEqual(sp.prob_on_time(5, 0.8, 5), 1.0)

    def test_posterior_drops_after_misses(self):
        before = sp.p_hat("Mathematics", 0, 0)
        after = sp.p_hat("Mathematics", 1, 3)
        self.assertLess(after, before)

    def test_jain_index_perfectly_fair(self):
        self.assertAlmostEqual(sp.jain([0.9, 0.9, 0.9]), 1.0)

    def test_ac3_detects_impossible_problem(self):
        _, _, _, csp, _ = solve_sample()
        csp.domains["Mathematics:Equations"] = []      # empty domain => no solution
        doms = {v: list(d) for v, d in csp.domains.items()}
        doms["Mathematics:Equations"] = [(0, 0)]
        doms["Mathematics:Polynomials"] = [(0, 0)]      # same slot as Equations -> conflict
        self.assertFalse(sp.ac3(csp, doms))


if __name__ == "__main__":
    unittest.main()