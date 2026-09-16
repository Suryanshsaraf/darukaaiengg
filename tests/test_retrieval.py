"""
Unit tests for hybrid knowledge retrieval and metadata filtering.
"""

import unittest
from knowledge.retriever import HybridKnowledgeRetriever


class TestRetrieval(unittest.TestCase):

    def setUp(self):
        self.retriever = HybridKnowledgeRetriever()

    def test_retriever_initialization(self):
        self.assertGreater(len(self.retriever.chunks), 10)
        self.assertGreater(self.retriever.doc_count, 0)

    def test_hybrid_search_semi_arid_wheat(self):
        query = "semi-arid monoculture wheat low soil organic carbon agroforestry"
        citations, trace = self.retriever.retrieve(
            query=query,
            climate_zone="semi_arid",
            land_use="monoculture_cropland",
            top_k=4
        )
        self.assertGreaterEqual(len(citations), 1)
        self.assertIsNotNone(trace)
        self.assertGreater(trace.candidate_chunks_evaluated, 5)
        self.assertIn("semi_arid", trace.applied_filters.get("climate_zone", ""))

        # Verify source quality
        top_citation = citations[0]
        self.assertTrue(bool(top_citation.doi_or_url))
        self.assertTrue(bool(top_citation.exact_excerpt))
        self.assertIn(top_citation.evidence_tier, [
            "Tier-1 Institutional Meta-Analysis",
            "Tier-1 Global Assessment",
            "Tier-1 Peer-Reviewed Global Meta-Analysis",
            "Tier-1 Primary Empirical Study",
            "Tier-1 Meta-Synthesis (5,188 studies)",
            "Tier-1 Quantitative Global Assessment",
            "Tier-1 UN Global Synthesis",
            "Tier-1 UN Scientific Assessment",
            "Tier-1 International Standard",
            "Tier-2 Applied Research Trial",
            "Tier-2 Long-Term Controlled Field Experiment",
            "Tier-2 Multi-Site Landscape Field Trial"
        ])

    def test_get_chunk_by_id(self):
        chunk = self.retriever.get_chunk_by_id("FAO-GSP-2020-C1")
        self.assertIsNotNone(chunk)
        self.assertIn("Vicia villosa", chunk.exact_excerpt)


if __name__ == "__main__":
    unittest.main()
