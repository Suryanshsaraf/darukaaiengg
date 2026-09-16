"""
Darukaa.Earth: Typed Domain Models and Decision Contracts
Strict machine-readable schemas ensuring scientific grounding, multi-metric interaction,
transparent citation lineage, and schema validation.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import uuid


@dataclass
class ScientificCitation:
    citation_id: str
    authors: str
    year: int
    title: str
    publication: str
    doi_or_url: str
    exact_excerpt: str
    evidence_tier: str  # "Tier-1 Meta-Analysis", "Tier-2 Institutional Report", "Tier-3 Controlled Field Trial"
    relevance_score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "citation_id": self.citation_id,
            "authors": self.authors,
            "year": self.year,
            "title": self.title,
            "publication": self.publication,
            "doi_or_url": self.doi_or_url,
            "exact_excerpt": self.exact_excerpt,
            "evidence_tier": self.evidence_tier,
            "relevance_score": round(self.relevance_score, 3)
        }


@dataclass
class MetricImpact:
    metric_key: str
    metric_name: str
    baseline_value: Optional[float]
    projected_delta_min: float
    projected_delta_max: float
    unit: str
    time_horizon: str
    causal_mechanism: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric_key": self.metric_key,
            "metric_name": self.metric_name,
            "baseline_value": self.baseline_value,
            "projected_delta_range": f"{'+' if self.projected_delta_min > 0 else ''}{self.projected_delta_min:.1f}% to {'+' if self.projected_delta_max > 0 else ''}{self.projected_delta_max:.1f}%",
            "unit": self.unit,
            "time_horizon": self.time_horizon,
            "causal_mechanism": self.causal_mechanism
        }


@dataclass
class SiteProfile:
    session_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    location_name: Optional[str] = None
    coordinates: Optional[Tuple[float, float]] = None  # (lat, lon)
    
    # Soil Health
    soil_organic_carbon_pct: Optional[float] = None
    soil_ph: Optional[float] = None
    soil_bulk_density: Optional[float] = None
    soil_moisture_pct: Optional[float] = None
    soil_texture: Optional[str] = None

    # Water & Climate
    climate_zone: Optional[str] = None  # "semi_arid", "arid", "temperate", "tropical", "humid"
    rainfall_annual_mm: Optional[float] = None
    rainfall_pattern: Optional[str] = None  # "low_erratic", "seasonal", "bimodal", "uniform"
    aridity_index: Optional[float] = None

    # Land Use & Land Cover
    land_use_type: Optional[str] = None  # "monoculture_cropland", "degraded_pasture", "orchard", etc.
    crop_type: Optional[str] = None       # "wheat", "cotton", "corn", "soybean", etc.
    tillage_practice: Optional[str] = None  # "conventional_deep", "reduced_till", "no_till"
    canopy_cover_pct: Optional[float] = None
    vegetative_ground_cover_pct: Optional[float] = None

    # Biodiversity Indicators
    species_richness_observed: Optional[int] = None
    shannon_diversity_index: Optional[float] = None
    pollinator_density_index: Optional[float] = None
    mycorrhizal_colonization_pct: Optional[float] = None
    habitat_fragmentation_level: Optional[str] = None  # "high", "moderate", "low"

    # Human Impact & Disturbance
    synthetic_nitrogen_kg_ha: Optional[float] = None
    pesticide_passes_yr: Optional[float] = None
    irrigation_source: Optional[str] = None

    # Metadata & Raw Prompt
    raw_query: Optional[str] = None
    enriched_spatially: bool = False

    def get_critical_variables(self) -> Dict[str, Any]:
        """Return dict of populated critical decision variables."""
        vars_dict = {}
        for k in [
            "soil_organic_carbon_pct", "soil_ph", "soil_bulk_density", "soil_moisture_pct",
            "climate_zone", "rainfall_annual_mm", "rainfall_pattern", "aridity_index",
            "land_use_type", "crop_type", "tillage_practice", "canopy_cover_pct",
            "vegetative_ground_cover_pct", "pollinator_density_index",
            "shannon_diversity_index", "mycorrhizal_colonization_pct",
            "habitat_fragmentation_level", "synthetic_nitrogen_kg_ha", "pesticide_passes_yr"
        ]:
            val = getattr(self, k)
            if val is not None:
                vars_dict[k] = val
        return vars_dict

    def present_variables_count(self) -> int:
        return len(self.get_critical_variables())

    def is_sufficient_for_diagnosis(self) -> bool:
        """System gate: requires at least 3 distinct interacting environmental variables."""
        return self.present_variables_count() >= 3

    def to_dict(self) -> Dict[str, Any]:
        d = {}
        for k, v in self.__dict__.items():
            if v is not None:
                d[k] = v
        return d


@dataclass
class CausalCompoundDiagnosis:
    primary_degradation_pathway: str
    interacting_variables: List[str]  # Must have len >= 3
    compound_risk_analysis: str
    vulnerability_score: float         # 0.0 (pristine) to 100.0 (acute collapse)
    limiting_factors: List[str]
    ecological_mechanisms: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "primary_degradation_pathway": self.primary_degradation_pathway,
            "interacting_variables_count": len(self.interacting_variables),
            "interacting_variables": self.interacting_variables,
            "compound_risk_analysis": self.compound_risk_analysis,
            "vulnerability_score": round(self.vulnerability_score, 1),
            "limiting_factors": self.limiting_factors,
            "ecological_mechanisms": self.ecological_mechanisms
        }


@dataclass
class InterventionRecommendation:
    intervention_id: str
    title: str
    category: str
    what_to_do: str
    why_it_works: str
    target_variables_addressed: List[str]
    impacted_metrics: List[MetricImpact]
    time_horizon: str  # "Short-term (6-18 months)", "Medium-term (2-4 years)", "Long-term (5-10 years)"
    confidence_score: float  # 0.0 - 1.0
    confidence_tier: str    # "High", "Medium", "Conditional"
    confidence_rationale: str
    trade_offs_and_risks: List[str]
    citations: List[ScientificCitation]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "intervention_id": self.intervention_id,
            "title": self.title,
            "category": self.category,
            "what_to_do": self.what_to_do,
            "why_it_works": self.why_it_works,
            "target_variables_addressed": self.target_variables_addressed,
            "impacted_metrics": [m.to_dict() for m in self.impacted_metrics],
            "time_horizon": self.time_horizon,
            "confidence": {
                "score": round(self.confidence_score, 2),
                "tier": self.confidence_tier,
                "rationale": self.confidence_rationale
            },
            "trade_offs_and_risks": self.trade_offs_and_risks,
            "citations": [c.to_dict() for c in self.citations]
        }


@dataclass
class RetrievalTrace:
    retrieval_query: str
    applied_filters: Dict[str, Any]
    candidate_chunks_evaluated: int
    chunks_returned_count: int
    chunks: List[Dict[str, Any]]
    execution_time_ms: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "retrieval_query": self.retrieval_query,
            "applied_filters": self.applied_filters,
            "candidate_chunks_evaluated": self.candidate_chunks_evaluated,
            "chunks_returned_count": self.chunks_returned_count,
            "execution_time_ms": round(self.execution_time_ms, 2),
            "top_chunks": self.chunks
        }


@dataclass
class VerifiedResponsePlan:
    plan_id: str
    created_at: str
    site_profile: SiteProfile
    diagnosis: CausalCompoundDiagnosis
    recommendations: List[InterventionRecommendation]
    portfolio_synergy_score: float
    retrieval_trace: RetrievalTrace
    validation_passed: bool
    validation_gate_details: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "created_at": self.created_at,
            "site_profile": self.site_profile.to_dict(),
            "diagnosis": self.diagnosis.to_dict(),
            "recommendations": [r.to_dict() for r in self.recommendations],
            "portfolio_synergy_score": round(self.portfolio_synergy_score, 2),
            "validation_gate": self.validation_gate_details,
            "retrieval_trace": self.retrieval_trace.to_dict()
        }


@dataclass
class ClarificationPrompt:
    is_clarification_needed: bool
    reason: str
    missing_critical_variables: List[str]
    clarification_question: str
    suggested_quick_options: List[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_clarification_needed": self.is_clarification_needed,
            "reason": self.reason,
            "missing_critical_variables": self.missing_critical_variables,
            "clarification_question": self.clarification_question,
            "suggested_quick_options": self.suggested_quick_options
        }
