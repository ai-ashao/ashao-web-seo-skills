from __future__ import annotations
import importlib.util, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts"/"validate_output.py"
FIXTURES=Path(__file__).resolve().parent/"fixtures"
spec=importlib.util.spec_from_file_location("validate_output",SCRIPT); assert spec and spec.loader
validate_output=importlib.util.module_from_spec(spec); spec.loader.exec_module(validate_output)

class ValidateOutputV2Tests(unittest.TestCase):
    def test_export_led_fixture_passes(self):
        text=(FIXTURES/"export-led-converter-v2.md").read_text(encoding="utf-8")
        self.assertEqual([], validate_output.validate(text))

    def test_strong_demand_allows_supporting_p0_with_missing_serp(self):
        text=(FIXTURES/"export-led-converter-v2.md").read_text(encoding="utf-8")
        errors=validate_output.validate(text)
        self.assertNotIn("SERP-missing P0 cluster md-docx must be the First Batch CORE or move to HOLD.",errors)

    def test_missing_demand_restores_old_serp_gate(self):
        text=(FIXTURES/"export-led-converter-v2.md").read_text(encoding="utf-8")
        start=text.index("## Demand Evidence Map"); end=text.index("## Feature Coverage Map")
        text=text[:start]+text[end:]
        errors=validate_output.validate(text)
        self.assertIn("SERP-missing P0 cluster md-docx must be the First Batch CORE or move to HOLD.",errors)

    def test_dynamic_five_competitor_feature_matrix_passes(self):
        text=(FIXTURES/"export-led-converter-v2.md").read_text(encoding="utf-8")
        self.assertFalse(any("Feature Coverage Map" in e for e in validate_output.validate(text)))

    def test_page_family_unknown_cluster_is_rejected(self):
        text=(FIXTURES/"export-led-converter-v2.md").read_text(encoding="utf-8").replace("md-pdf; md-docx","md-pdf; ghost-cluster",1)
        errors=validate_output.validate(text)
        self.assertIn("Page Family Map row 1 references unknown cluster: ghost-cluster.",errors)

if __name__=="__main__": unittest.main()
