"""
Unit tests for multi-variable causal reasoning engine and diagnostic gates.
"""

import unittest
from core.models import SiteProfile
from reasoning.diagnosis import CausalDiagnosticMatrix
from reasoning.engine import EcologicalReasoningEngine


class TestReasoning(unittest.TestCase):

    def setUp(self):
        self.diagnostic_matrix = CausalDiagnosticMatrix()
        self.reasoning_engine = EcologicalReasoningEngine()

    def test_single_variable_rejection_gate(self):
        profile = SiteProfile()
        profile.soil_organic_carbon_pct = 0.3
        # Should raise ValueError because < 3 variables
        with self.assertRaises(ValueError):
            self.diagnostic_matrix.diagnose(profile)

    def test_multi_variable_diagnosis_success(self):
        profile = SiteProfile()
        profile.soil_organic_carbon_pct = 0.3
        profile.rainfall_annual_mm = 310.0
        profile.crop_type = "monoculture wheat"
        profile.land_use_type = "monoculture_cropland"
        profile.climate_zone = "semi_arid"

        diagnosis = self.diagnostic_matrix.diagnose(profile)
        self.assertGreaterEqual(len(diagnosis.interacting_variables), 3)
        self.assertGreater(diagnosis.vulnerability_score, 30.0)
        self.assertTrue(bool(diagnosis.compound_risk_analysis))

    def test_end_to_end_reasoning_pipeline(self):
        profile = SiteProfile()
        profile.soil_organic_carbon_pct = 0.3
        profile.rainfall_annual_mm = 320.0
        profile.crop_type = "monoculture wheat"
        profile.land_use_type = "monoculture_cropland"
        profile.climate_zone = "semi_arid"

        plan = self.reasoning_engine.process_site_profile(profile)
        self.assertTrue(plan.validation_passed)
        self.assertGreaterEqual(len(plan.recommendations), 1)

        for rec in plan.recommendations:
            self.assertGreaterEqual(len(rec.citations), 1)
            self.assertGreaterEqual(len(rec.impacted_metrics), 1)
            self.assertTrue(bool(rec.time_horizon))
            self.assertGreater(rec.confidence_score, 0.0)
            self.assertIn(rec.confidence_tier, ["High", "Medium", "Conditional"])


if __name__ == "__main__":
    unittest.main()
