"""
Unit tests for multi-turn conversation, entity extraction, and clarifying question state machine.
"""

import unittest
from conversation.extractor import EcologicalEntityExtractor
from conversation.spatial import SpatialEnrichmentService
from conversation.session import ConversationSession
from core.models import SiteProfile


class TestConversation(unittest.TestCase):

    def test_entity_extractor_from_free_text(self):
        text = "My farm has soil organic carbon: 0.3%, rainfall: 320mm, and crop: monoculture wheat in a semi-arid zone."
        profile = EcologicalEntityExtractor.extract_from_text(text)
        self.assertEqual(profile.soil_organic_carbon_pct, 0.3)
        self.assertEqual(profile.rainfall_annual_mm, 320.0)
        self.assertEqual(profile.climate_zone, "semi_arid")
        self.assertIn("wheat", profile.crop_type)

    def test_vague_input_triggers_clarification(self):
        session = ConversationSession()
        # Vague input from Hackathon Brief
        response = session.process_user_message("Biodiversity is declining on my land")
        self.assertEqual(response["type"], "clarification")
        self.assertIn("soil organic carbon", response["assistant_message"].lower())
        self.assertIn("rainfall", response["assistant_message"].lower())
        self.assertIn("land use", response["assistant_message"].lower())

    def test_multi_turn_accumulation(self):
        session = ConversationSession()
        # Turn 1: Vague input
        r1 = session.process_user_message("Biodiversity is declining on my land")
        self.assertEqual(r1["type"], "clarification")

        # Turn 2: User answers with missing variables
        r2 = session.process_user_message("Soil organic carbon: 0.3%, rainfall: low (310mm), crop: monoculture wheat")
        self.assertEqual(r2["type"], "verified_plan")
        self.assertIn("plan", r2)
        self.assertTrue(r2["plan"]["validation_gate"]["all_gates_passed"])

    def test_spatial_enrichment(self):
        profile = SiteProfile()
        profile.coordinates = (28.4, 77.2)  # Indo-Gangetic Basin
        enriched = SpatialEnrichmentService.enrich_profile(profile)
        self.assertTrue(enriched.enriched_spatially)
        self.assertEqual(enriched.climate_zone, "semi_arid")
        self.assertIsNotNone(enriched.rainfall_annual_mm)


if __name__ == "__main__":
    unittest.main()
