"""
Darukaa.Earth: Hybrid Metadata-Filtered Knowledge Retriever
Combines BM25 lexical ranking, semantic cosine vector similarity, and categorical
ecological metadata filtering. Produces full inspectable retrieval traces.
"""

import math
import re
import time
from typing import List, Dict, Any, Optional, Tuple

from .sources_data import CURATED_SOURCES
from core.models import ScientificCitation, RetrievalTrace


def tokenize(text: str) -> List[str]:
    """Extract lowercase alphanumeric tokens."""
    return re.findall(r"\b[a-z0-9_\-]+\b", text.lower())


class HybridKnowledgeRetriever:
    """
    Self-contained, production-grade hybrid retrieval engine.
    Applies metadata constraints (climate, land-use, target metrics),
    then computes unified ranking: BM25 Lexical + TF-IDF Vector Cosine + Metadata Alignment.
    """

    def __init__(self, sources: Optional[List[Dict[str, Any]]] = None):
        self.sources = sources or CURATED_SOURCES
        self.chunks: List[Dict[str, Any]] = []
        self._build_index()

    def _build_index(self):
        self.chunks.clear()
        doc_count = 0
        all_tokens: List[List[str]] = []

        for src in self.sources:
            for chunk in src.get("chunks", []):
                combined_text = (
                    f"{src['title']} {src['authors']} {chunk['content']} "
                    f"{' '.join(chunk.get('intervention_tags', []))} "
                    f"{' '.join(chunk.get('metric_tags', []))} "
                    f"{' '.join(chunk.get('ecosystem', []))} "
                    f"{' '.join(chunk.get('climate_zones', []))} "
                    f"{chunk.get('conditions', '')}"
                )
                tokens = tokenize(combined_text)
                all_tokens.append(tokens)

                chunk_entry = {
                    "chunk_id": chunk["chunk_id"],
                    "source_id": src["source_id"],
                    "source_title": src["title"],
                    "authors": src["authors"],
                    "year": src["year"],
                    "publication": src["publication"],
                    "doi_or_url": src["doi_or_url"],
                    "evidence_tier": src["evidence_tier"],
                    "content": chunk["content"],
                    "ecosystem": chunk.get("ecosystem", []),
                    "climate_zones": chunk.get("climate_zones", []),
                    "intervention_tags": chunk.get("intervention_tags", []),
                    "metric_tags": chunk.get("metric_tags", []),
                    "conditions": chunk.get("conditions", ""),
                    "time_horizon": chunk.get("time_horizon", ""),
                    "quantitative_delta": chunk.get("quantitative_delta", ""),
                    "tokens": tokens,
                    "doc_len": len(tokens)
                }
                self.chunks.append(chunk_entry)
                doc_count += 1

        self.doc_count = doc_count
        self.avg_doc_len = sum(len(t) for t in all_tokens) / max(1, doc_count)

        # Build Term Frequencies and Inverted Index
        self.doc_freqs: Dict[str, int] = {}
        for tokens in all_tokens:
            unique_terms = set(tokens)
            for t in unique_terms:
                self.doc_freqs[t] = self.doc_freqs.get(t, 0) + 1

        # Precompute IDF
        self.idf: Dict[str, float] = {}
        for t, df in self.doc_freqs.items():
            self.idf[t] = math.log(1.0 + (self.doc_count - df + 0.5) / (df + 0.5))

    def _bm25_score(self, query_tokens: List[str], chunk: Dict[str, Any], k1: float = 1.5, b: float = 0.75) -> float:
        score = 0.0
        doc_len = chunk["doc_len"]
        doc_tokens = chunk["tokens"]
        len_norm = (1.0 - b) + b * (doc_len / max(1.0, self.avg_doc_len))

        tf_map: Dict[str, int] = {}
        for t in doc_tokens:
            tf_map[t] = tf_map.get(t, 0) + 1

        for qt in query_tokens:
            if qt in tf_map:
                tf = tf_map[qt]
                idf = self.idf.get(qt, 0.5)
                term_score = idf * (tf * (k1 + 1.0)) / (tf + k1 * len_norm)
                score += term_score

        return score

    def _cosine_similarity(self, query_tokens: List[str], chunk: Dict[str, Any]) -> float:
        """Compute cosine similarity over TF-IDF vector space."""
        if not query_tokens or not chunk["tokens"]:
            return 0.0

        q_tf: Dict[str, int] = {}
        for t in query_tokens:
            q_tf[t] = q_tf.get(t, 0) + 1

        d_tf: Dict[str, int] = {}
        for t in chunk["tokens"]:
            d_tf[t] = d_tf.get(t, 0) + 1

        dot = 0.0
        q_norm = 0.0
        d_norm = 0.0

        for t, count in q_tf.items():
            w_q = count * self.idf.get(t, 0.5)
            q_norm += w_q * w_q
            if t in d_tf:
                w_d = d_tf[t] * self.idf.get(t, 0.5)
                dot += w_q * w_d

        for t, count in d_tf.items():
            w_d = count * self.idf.get(t, 0.5)
            d_norm += w_d * w_d

        if q_norm <= 0 or d_norm <= 0:
            return 0.0

        return dot / (math.sqrt(q_norm) * math.sqrt(d_norm))

    def retrieve(
        self,
        query: str,
        climate_zone: Optional[str] = None,
        land_use: Optional[str] = None,
        target_metrics: Optional[List[str]] = None,
        top_k: int = 4
    ) -> Tuple[List[ScientificCitation], RetrievalTrace]:
        """
        Execute metadata-filtered hybrid retrieval.
        Returns top ScientificCitation items and an inspectable RetrievalTrace.
        """
        start_time = time.perf_counter()
        query_tokens = tokenize(query)
        applied_filters = {}

        if climate_zone:
            applied_filters["climate_zone"] = climate_zone
        if land_use:
            applied_filters["land_use"] = land_use
        if target_metrics:
            applied_filters["target_metrics"] = target_metrics

        scored_candidates = []

        for chunk in self.chunks:
            # Metadata matching checks
            metadata_bonus = 0.0
            
            # Climate zone filter / alignment
            if climate_zone:
                if climate_zone in chunk["climate_zones"]:
                    metadata_bonus += 0.25
                elif "semi_arid" in chunk["climate_zones"] and climate_zone in ["arid", "dry_sub_humid"]:
                    metadata_bonus += 0.10

            # Land use alignment
            if land_use and chunk["ecosystem"]:
                if any(land_use.lower() in eco.lower() or eco.lower() in land_use.lower() for eco in chunk["ecosystem"]):
                    metadata_bonus += 0.20

            # Target metric alignment
            if target_metrics:
                overlap = set(target_metrics).intersection(set(chunk.get("metric_tags", [])))
                if overlap:
                    metadata_bonus += 0.15 * len(overlap)

            bm25 = self._bm25_score(query_tokens, chunk)
            cos_sim = self._cosine_similarity(query_tokens, chunk)

            # Combined hybrid score (normalized)
            # BM25 is typically in 0 - 25 range, scale to ~0-1
            bm25_norm = min(1.0, bm25 / 15.0)
            combined_score = 0.45 * cos_sim + 0.35 * bm25_norm + 0.20 * min(1.0, metadata_bonus)

            scored_candidates.append({
                "chunk": chunk,
                "bm25_score": round(bm25, 3),
                "cosine_similarity": round(cos_sim, 3),
                "metadata_bonus": round(metadata_bonus, 3),
                "total_score": round(combined_score, 3)
            })

        # Rank descending
        scored_candidates.sort(key=lambda x: x["total_score"], reverse=True)
        top_candidates = scored_candidates[:top_k]

        citations: List[ScientificCitation] = []
        trace_chunks: List[Dict[str, Any]] = []

        for cand in top_candidates:
            c = cand["chunk"]
            citation = ScientificCitation(
                citation_id=c["chunk_id"],
                authors=c["authors"],
                year=c["year"],
                title=c["source_title"],
                publication=c["publication"],
                doi_or_url=c["doi_or_url"],
                exact_excerpt=c["content"],
                evidence_tier=c["evidence_tier"],
                relevance_score=cand["total_score"]
            )
            citations.append(citation)

            trace_chunks.append({
                "chunk_id": c["chunk_id"],
                "source_title": c["source_title"],
                "authors_year": f"{c['authors']} ({c['year']})",
                "doi_or_url": c["doi_or_url"],
                "scores": {
                    "bm25": cand["bm25_score"],
                    "vector_cosine": cand["cosine_similarity"],
                    "metadata_bonus": cand["metadata_bonus"],
                    "composite_relevance": cand["total_score"]
                },
                "matched_climate": c["climate_zones"],
                "matched_metrics": c["metric_tags"],
                "excerpt": c["content"]
            })

        latency_ms = (time.perf_counter() - start_time) * 1000.0

        trace = RetrievalTrace(
            retrieval_query=query,
            applied_filters=applied_filters,
            candidate_chunks_evaluated=len(self.chunks),
            chunks_returned_count=len(citations),
            chunks=trace_chunks,
            execution_time_ms=latency_ms
        )

        return citations, trace

    def get_chunk_by_id(self, chunk_id: str) -> Optional[ScientificCitation]:
        """Retrieve a specific chunk as a ScientificCitation."""
        for c in self.chunks:
            if c["chunk_id"] == chunk_id:
                return ScientificCitation(
                    citation_id=c["chunk_id"],
                    authors=c["authors"],
                    year=c["year"],
                    title=c["source_title"],
                    publication=c["publication"],
                    doi_or_url=c["doi_or_url"],
                    exact_excerpt=c["content"],
                    evidence_tier=c["evidence_tier"],
                    relevance_score=1.0
                )
        return None
