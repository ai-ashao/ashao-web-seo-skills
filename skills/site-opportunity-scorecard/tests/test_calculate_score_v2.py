from pathlib import Path
import importlib.util, unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("calc",ROOT/"scripts"/"calculate_score.py"); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
BASE={
"opportunity_scores":{"independent_primary_keyword":5,"serp_breakability":4,"long_tail_expansion":5,"user_use_case_difference":3,"homepage_workflow_difference":1,"independent_brand_reason":4,"link_distribution_potential":4,"independent_content_system":5,"development_maintenance_economics":5,"monetization_fit":4},
"risk_scores":{"keyword_overlap":1,"search_intent_overlap":1,"product_workflow_overlap":2,"content_template_overlap":1,"brand_positioning_ambiguity":1,"link_authority_fragmentation":1,"development_maintenance_fragmentation":1},
"hard_gates":[],"overall_confidence":"HIGH"}
class Tests(unittest.TestCase):
    def test_seo_utility_does_not_require_novel_workflow(self):
        d={**BASE,"decision_profile":"seo_first_utility"}; self.assertEqual("INDEPENDENT_SITE",mod.calculate(d)["recommendation"])
    def test_product_led_keeps_workflow_gate(self):
        d={**BASE,"decision_profile":"product_led"}; self.assertNotEqual("INDEPENDENT_SITE",mod.calculate(d)["recommendation"])
    def test_downloader_uses_seo_first_decision_behavior(self):
        d={**BASE,"decision_profile":"downloader"}; self.assertEqual("INDEPENDENT_SITE",mod.calculate(d)["recommendation"])
    def test_block_product_wins(self):
        d={**BASE,"decision_profile":"seo_first_utility","hard_gates":[{"reason":"policy blocker","scope":"BLOCK_PRODUCT"}]}; self.assertEqual("OBSERVE_OR_REJECT",mod.calculate(d)["recommendation"])
    def test_legacy_json_fields_remain_available(self):
        d={**BASE,"hard_gates":["unresolved host overlap"]}
        result=mod.calculate(d)
        self.assertEqual(result["hard_gates"], ["unresolved host overlap"])
        self.assertEqual(result["hard_gate_scopes"], [{"reason":"unresolved host overlap","scope":"SITE_ONLY"}])
        self.assertEqual(result["subtotals"], {"search_opportunity":36.0,"product_differentiation":17.2,"independent_growth":17.0,"site_economics":9.0})
        self.assertEqual(result["recommendation"], "EXISTING_SITE_SECTION")
    def test_legacy_recommendation_call_defaults_to_generic(self):
        result=mod.calculate(BASE)
        recommendation,_=mod.choose_recommendation(result["opportunity_score"],result["separation_risk"],BASE["opportunity_scores"],[],"HIGH")
        self.assertEqual(recommendation,result["recommendation"])
if __name__=="__main__": unittest.main()
