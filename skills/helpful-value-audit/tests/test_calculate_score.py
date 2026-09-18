from pathlib import Path
import importlib.util, unittest
ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location("calc",ROOT/"scripts"/"calculate_score.py"); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
def payload():
    return {"ratings":{k:{"rating":4,"evidence":"TESTED"} for k in m.WEIGHTS},"gates":[]}
class Tests(unittest.TestCase):
    def test_perfect(self): self.assertEqual(100.0,m.calculate(payload())["helpful_strength"])
    def test_task_failure_cap(self):
        p=payload(); p["gates"]=[{"id":"core_task_failure","triggered":True}]; self.assertEqual(49.0,m.calculate(p)["helpful_strength"])
    def test_claimed_function_cannot_score_four(self):
        p=payload(); p["ratings"]["functional_completion"]={"rating":4,"evidence":"CLAIMED"}
        with self.assertRaises(m.InputError): m.calculate(p)
if __name__=="__main__": unittest.main()
