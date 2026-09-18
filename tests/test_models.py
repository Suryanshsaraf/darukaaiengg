"""
Unit tests for core models and schemas.
"""

import unittest
from core.models import (
    SiteProfile,
    ScientificCitation,
    MetricImpact,
    CausalCompoundDiagnosis,
    InterventionRecommendation
)


class TestModels(unittest.TestCase):

    def test_site_profile_critical_variables_count(self):
        profile = SiteProfile()
        self.assertEqual(profile.present_variables_count(), 0)
        self.assertFalse(profile.is_sufficient_for_diagnosis())

        profile.soil_organic_carbon_pct = 0.3
        profile.rainfall_annual_mm = 320.0
        self.assertEqual(profile.present_variables_count(), 2)
        self.assertFalse(profile.is_sufficient_for_diagnosis())

        profile.crop_type = "monoculture wheat"
        self.assertEqual(profile.present_variables_count(), 3)
        self.assertTrue(profile.is_sufficient_for_diagnosis())

    def test_scientific_citation_to_dict(self):
        cite = ScientificCitation(
            citation_id="FAO-TEST-1",
            authors="FAO Global Soil Partnership",
            year=2021,
            title="Recarbonizing Global Soils",
            publication="FAO Rome",
            doi_or_url="https://doi.org/10.4060/cb6595en",
            exact_excerpt="Cover cropping increases SOC by 0.15% to 0.35%",
            evidence_tier="Tier-1 Institutional Meta-Analysis",
            relevance_score=0.92
        )
        d = cite.to_dict()
        self.assertEqual(d["citation_id"], "FAO-TEST-1")
        self.assertEqual(d["year"], 2021)
        self.assertIn("10.4060", d["doi_or_url"])


if __name__ == "__main__":
    unittest.main()
