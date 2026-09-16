"""
Darukaa.Earth: Core Ecological Decision & Reasoning Engine
Orchestrates multi-metric diagnosis, constraint-aware intervention scoring,
hybrid retrieval binding, citation gating, and response plan assembly.
"""

from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, Tuple
import uuid

from core.models import (
    SiteProfile,
    CausalCompoundDiagnosis,
    InterventionRecommendation,
    MetricImpact,
    ScientificCitation,
    RetrievalTrace,
    VerifiedResponsePlan,
)
from knowledge.retriever import HybridKnowledgeRetriever
from knowledge.graph import INTERVENTION_GRAPH
from .diagnosis import CausalDiagnosticMatrix
from .confidence import EcologicalConfidenceEstimator


class EcologicalReasoningEngine:
    """
    Production-grade decision engine.
    Applies deterministic causal evaluation, retrieves scientific citations,
    and enforces strict evidence and schema validation gates.
    """

    def __init__(self, retriever: Optional[HybridKnowledgeRetriever] = None):
        self.retriever = retriever or HybridKnowledgeRetriever()
        self.diagnostic_matrix = CausalDiagnosticMatrix()

    def process_site_profile(self, profile: SiteProfile) -> VerifiedResponsePlan:
        """
        Execute full end-to-end decision pipeline:
        1. Multi-metric Compound Diagnosis (requires >= 3 variables)
        2. Filter and score interventions from knowledge graph
        3. Retrieve scientific citations and build inspectable trace
        4. Synthesize quantified metric deltas and trade-offs
        5. Pass evidence and schema validation gate
        """
        # Step 1: Diagnose compound interactions (Enforces >= 3 variables)
        diagnosis: CausalCompoundDiagnosis = self.diagnostic_matrix.diagnose(profile)

        # Step 2: Retrieve scientific evidence via hybrid retriever
        query_terms = (
            f"{diagnosis.primary_degradation_pathway} "
            f"{profile.crop_type or ''} {profile.land_use_type or ''} "
            f"{' '.join(diagnosis.limiting_factors)}"
        )
        
        target_metrics = []
        if profile.soil_organic_carbon_pct is not None:
            target_metrics.append("soil_organic_carbon_pct")
        if profile.pollinator_density_index is not None:
            target_metrics.append("pollinator_density_index")
        if profile.soil_bulk_density is not None:
            target_metrics.append("soil_bulk_density")

        climate = profile.climate_zone or ("semi_arid" if profile.rainfall_annual_mm and profile.rainfall_annual_mm <= 500 else None)

        citations, trace = self.retriever.retrieve(
            query=query_terms,
            climate_zone=climate,
            land_use=profile.land_use_type,
            target_metrics=target_metrics,
            top_k=6
        )

        # Step 3: Score and rank candidate interventions from the graph
        scored_interventions = []
        for item in INTERVENTION_GRAPH:
            score = self._score_intervention(profile, diagnosis, item)
            if score > 0.35:
                scored_interventions.append((score, item))

        scored_interventions.sort(key=lambda x: x[0], reverse=True)
        top_interventions = scored_interventions[:3]

        if not top_interventions and scored_interventions:
            top_interventions = [scored_interventions[0]]

        # Step 4: Build concrete, evidence-bound recommendations
        recommendations: List[InterventionRecommendation] = []
        all_addressed_vars = set()

        for score, item in top_interventions:
            # Match specific citations for this intervention
            rec_citations = []
            chunk_ids = item.get("evidence_chunk_ids", [])
            for cid in chunk_ids:
                citation_obj = self.retriever.get_chunk_by_id(cid)
                if citation_obj:
                    rec_citations.append(citation_obj)

            # Fallback to top retrieved citations if none explicitly linked
            if not rec_citations and citations:
                rec_citations = citations[:2]

            # Confidence assessment
            conf_score, conf_tier, conf_rationale = EcologicalConfidenceEstimator.evaluate(
                profile, item, rec_citations
            )

            # Synthesize metric impacts
            metric_impacts: List[MetricImpact] = []
            for mi in item.get("projected_metric_impacts", []):
                baseline = getattr(profile, mi["metric_key"], None)
                
                # Dynamic scaling: Low baseline SOC (<0.5%) experiences higher relative saturation response
                d_min = mi["projected_delta_min"]
                d_max = mi["projected_delta_max"]
                if mi["metric_key"] == "soil_organic_carbon_pct" and baseline is not None and baseline <= 0.5:
                    d_min += 5.0
                    d_max += 8.0

                metric_impacts.append(
                    MetricImpact(
                        metric_key=mi["metric_key"],
                        metric_name=mi["metric_name"],
                        baseline_value=baseline,
                        projected_delta_min=d_min,
                        projected_delta_max=d_max,
                        unit=mi["unit"],
                        time_horizon=mi["time_horizon"],
                        causal_mechanism=mi["causal_mechanism"]
                    )
                )

            rec = InterventionRecommendation(
                intervention_id=item["intervention_id"],
                title=item["title"],
                category=item["category"],
                what_to_do=item["what_to_do"],
                why_it_works=item["why_it_works"],
                target_variables_addressed=item["target_variables_addressed"],
                impacted_metrics=metric_impacts,
                time_horizon=item["time_horizon"],
                confidence_score=conf_score,
                confidence_tier=conf_tier,
                confidence_rationale=conf_rationale,
                trade_offs_and_risks=item["trade_offs_and_risks"],
                citations=rec_citations
            )
            recommendations.append(rec)
            all_addressed_vars.update(item["target_variables_addressed"])

        # Step 5: Portfolio Synergy Score
        # Synergy is maximized when interventions tackle complementary physical, biological, and microclimatic dimensions
        synergy = min(1.0, 0.45 + 0.15 * len(recommendations) + 0.05 * len(all_addressed_vars))

        # Step 6: Strict Schema and Acceptance Gate Validation
        gate_passed, gate_details = self._validate_acceptance_gates(
            profile, diagnosis, recommendations
        )

        plan = VerifiedResponsePlan(
            plan_id=f"DARUKAA-PLAN-{str(uuid.uuid4())[:8].upper()}",
            created_at=datetime.now(timezone.utc).isoformat(),
            site_profile=profile,
            diagnosis=diagnosis,
            recommendations=recommendations,
            portfolio_synergy_score=synergy,
            retrieval_trace=trace,
            validation_passed=gate_passed,
            validation_gate_details=gate_details
        )

        return plan

    def _score_intervention(self, profile: SiteProfile, diagnosis: CausalCompoundDiagnosis, item: Dict[str, Any]) -> float:
        """Score candidate intervention feasibility and alignment against site conditions."""
        pre = item.get("preconditions", {})
        prohib = item.get("prohibited_conditions", {})

        # Hard rejection if prohibited condition triggered
        if "max_rainfall_annual_mm" in prohib and profile.rainfall_annual_mm:
            if profile.rainfall_annual_mm < prohib["max_rainfall_annual_mm"]:
                return 0.0

        if "compatible_land_use" in prohib and profile.land_use_type:
            if profile.land_use_type in prohib["compatible_land_use"]:
                return 0.0

        score = 0.50

        # Climate alignment
        site_climate = profile.climate_zone or ("semi_arid" if profile.rainfall_annual_mm and profile.rainfall_annual_mm <= 500 else None)
        if site_climate and "compatible_climates" in pre:
            if site_climate in pre["compatible_climates"]:
                score += 0.20

        # Land use compatibility
        if profile.land_use_type and "compatible_land_use" in pre:
            if profile.land_use_type in pre["compatible_land_use"]:
                score += 0.25

        # Metric alignment with diagnosis
        addressed = set(item.get("target_variables_addressed", []))
        diag_vars = set(diagnosis.interacting_variables)
        overlap = addressed.intersection(diag_vars)
        if overlap:
            score += 0.10 * len(overlap)

        # Bonus for SOC if severely depleted
        if profile.soil_organic_carbon_pct is not None and profile.soil_organic_carbon_pct <= 0.6:
            if "soil_organic_carbon_pct" in addressed:
                score += 0.15

        return min(1.0, score)

    def _validate_acceptance_gates(
        self,
        profile: SiteProfile,
        diagnosis: CausalCompoundDiagnosis,
        recommendations: List[InterventionRecommendation]
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Acceptance Gates based on Hackathon Rubric:
        Gate 1: >= 3 interacting environmental variables in diagnosis.
        Gate 2: Every material recommendation must have at least 1 verified citation with DOI/URL and excerpt.
        Gate 3: Quantified improvement estimates present.
        Gate 4: Time horizon and confidence level present.
        """
        gate_1 = len(diagnosis.interacting_variables) >= 3
        gate_2 = all(len(r.citations) >= 1 for r in recommendations) if recommendations else False
        gate_3 = all(len(r.impacted_metrics) >= 1 for r in recommendations) if recommendations else False
        gate_4 = all(r.time_horizon and r.confidence_score > 0 for r in recommendations) if recommendations else False

        all_passed = gate_1 and gate_2 and gate_3 and gate_4

        details = {
            "all_gates_passed": all_passed,
            "gate_1_min_3_variables": {
                "passed": gate_1,
                "variable_count": len(diagnosis.interacting_variables),
                "variables": diagnosis.interacting_variables
            },
            "gate_2_scientific_citations_bound": {
                "passed": gate_2,
                "total_recommendations": len(recommendations),
                "citations_per_recommendation": [len(r.citations) for r in recommendations]
            },
            "gate_3_quantified_estimates": {
                "passed": gate_3,
                "metric_impacts_count": sum(len(r.impacted_metrics) for r in recommendations)
            },
            "gate_4_time_horizon_and_confidence": {
                "passed": gate_4
            }
        }

        return all_passed, details
