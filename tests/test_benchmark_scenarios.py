"""
Comprehensive verification of the Three Core Benchmark Moments
as specified in the Darukaa.Earth Challenge Brief and Shortlist Build Plan:
1. Vague input ("Biodiversity is declining on my land") prompts for smallest set of missing metrics.
2. Semi-arid monoculture wheat with SOC 0.3% produces cited multi-metric intervention portfolio (FAO/IPCC).
3. Structured JSON / coordinate-based profile proves structured input, remembered context, retrieval trace, and uncertainty.
"""

import unittest
from conversation.session import ConversationSession
from core.models import SiteProfile
from reasoning.engine import EcologicalReasoningEngine


class TestBenchmarkScenarios(unittest.TestCase):

    def test_benchmark_1_vague_input_clarification(self):
        """
        Benchmark Moment 1:
        A vague biodiversity-decline message prompts for the smallest useful set of missing metrics.
        Reviewer criterion: Conversational Intelligence (15%).
        """
        session = ConversationSession()
        res = session.process_user_message("Biodiversity is declining on my land")

        self.assertEqual(res["type"], "clarification")
        self.assertEqual(res["missing_count"], 3)
        self.assertIn("clarification", res)
        clarification_text = res["assistant_message"].lower()

        # Must specifically ask for the decision-changing environmental parameters
        self.assertIn("soil organic carbon", clarification_text)
        self.assertIn("rainfall", clarification_text)
        self.assertIn("land use", clarification_text)

    def test_benchmark_2_semi_arid_monoculture_wheat(self):
        """
        Benchmark Moment 2:
        Input:
          - Soil organic carbon: 0.3%
          - Rainfall: low
          - Crop: monoculture wheat
          - Region: semi-arid
        Expected Output:
          - Suggest agroforestry / intercropping / cover crops
          - Explain impact on soil carbon and biodiversity
          - Provide measurable improvement estimates
          - Reference credible sources such as FAO and IPCC
        """
        session = ConversationSession()
        user_input = "Soil organic carbon: 0.3%, Rainfall: low, Crop: monoculture wheat, Region: semi-arid"
        res = session.process_user_message(user_input)

        self.assertEqual(res["type"], "verified_plan")
        plan = res["plan"]

        # 1. Gate check
        self.assertTrue(plan["validation_gate"]["all_gates_passed"])
        diag = plan["diagnosis"]
        self.assertGreaterEqual(diag["interacting_variables_count"], 3)
        self.assertIn("soil_organic_carbon_pct", diag["interacting_variables"])

        # 2. Check recommendations
        recs = plan["recommendations"]
        rec_titles = [r["title"].lower() for r in recs]
        has_agroforestry_or_intercropping = any(
            "agroforestry" in t or "intercropping" in t or "cover crop" in t for t in rec_titles
        )
        self.assertTrue(has_agroforestry_or_intercropping, f"Expected agroforestry/intercropping/cover crop in {rec_titles}")

        # 3. Check measurable improvement estimates
        all_metrics = [m for r in recs for m in r["impacted_metrics"]]
        metric_keys = [m["metric_key"] for m in all_metrics]
        self.assertIn("soil_organic_carbon_pct", metric_keys)

        # Check that quantitative ranges are specified
        for m in all_metrics:
            self.assertTrue(bool(m["projected_delta_range"]))
            self.assertTrue(bool(m["causal_mechanism"]))

        # 4. Check credible source references (FAO, IPCC)
        all_citations = [c for r in recs for c in r["citations"]]
        citation_authors_and_titles = [f"{c['authors']} {c['title']}".lower() for c in all_citations]
        
        has_fao = any("fao" in cat or "food and agriculture organization" in cat for cat in citation_authors_and_titles)
        has_ipcc = any("ipcc" in cat or "intergovernmental panel on climate change" in cat for cat in citation_authors_and_titles)
        self.assertTrue(has_fao or has_ipcc, "Plan must cite FAO or IPCC institutional studies")

        # Verify all citations have DOIs/URLs
        for c in all_citations:
            self.assertTrue(c["doi_or_url"].startswith("http"))
            self.assertTrue(len(c["exact_excerpt"]) > 20)

    def test_benchmark_3_structured_json_and_retrieval_trace(self):
        """
        Benchmark Moment 3:
        A JSON or coordinate-based profile proves structured input, remembered context,
        retrieval trace, and transparent uncertainty.
        """
        profile = SiteProfile(
            coordinates=(31.5, -102.3),  # High Plains Semi-Arid Basin
            soil_organic_carbon_pct=0.45,
            soil_bulk_density=1.52,
            land_use_type="monoculture_cropland",
            crop_type="monoculture cotton",
            tillage_practice="conventional_deep",
            rainfall_annual_mm=360.0
        )

        engine = EcologicalReasoningEngine()
        plan = engine.process_site_profile(profile)

        self.assertTrue(plan.validation_passed)

        # Check retrieval trace
        trace = plan.retrieval_trace
        self.assertGreater(trace.candidate_chunks_evaluated, 10)
        self.assertGreaterEqual(trace.chunks_returned_count, 1)
        self.assertIn("top_chunks", trace.to_dict())

        first_chunk = trace.chunks[0]
        self.assertIn("scores", first_chunk)
        self.assertIn("bm25", first_chunk["scores"])
        self.assertIn("vector_cosine", first_chunk["scores"])
        self.assertIn("composite_relevance", first_chunk["scores"])

        # Check confidence and uncertainty
        for rec in plan.recommendations:
            self.assertIn(rec.confidence_tier, ["High", "Medium", "Conditional"])
            self.assertTrue(bool(rec.confidence_rationale))
            self.assertGreaterEqual(len(rec.trade_offs_and_risks), 1)


if __name__ == "__main__":
    unittest.main()
