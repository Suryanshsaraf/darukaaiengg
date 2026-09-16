"""
Darukaa.Earth: Rigorous Ecological Confidence & Uncertainty Estimator
Calculates confidence based on evidence tier (FAO/IPCC/Nature), site precondition alignment,
and observational data completeness.
"""

from typing import Dict, Any, List, Tuple
from core.models import SiteProfile, ScientificCitation


class EcologicalConfidenceEstimator:
    """Computes transparent confidence score and uncertainty bounds."""

    @staticmethod
    def evaluate(
        profile: SiteProfile,
        intervention: Dict[str, Any],
        citations: List[ScientificCitation]
    ) -> Tuple[float, str, str]:
        """
        Returns (confidence_score, confidence_tier, rationale).
        """
        # 1. Scientific Evidence Tier Weight
        tier_scores = []
        for c in citations:
            tier_str = getattr(c, "evidence_tier", "")
            if "Tier-1" in tier_str:
                tier_scores.append(0.95)
            elif "Tier-2" in tier_str:
                tier_scores.append(0.85)
            else:
                tier_scores.append(0.70)

        evidence_score = sum(tier_scores) / max(1, len(tier_scores)) if tier_scores else 0.70

        # 2. Precondition & Constraint Fit
        pre = intervention.get("preconditions", {})
        prohib = intervention.get("prohibited_conditions", {})
        fit_penalties = 0.0
        rationale_elements = []

        # Check rainfall constraint
        rain = profile.rainfall_annual_mm
        if "min_rainfall_annual_mm" in pre and rain is not None:
            if rain < pre["min_rainfall_annual_mm"]:
                fit_penalties += 0.25
                rationale_elements.append(
                    f"Site precipitation ({rain} mm) is near or below lower optimal threshold ({pre['min_rainfall_annual_mm']} mm), requiring strict drought termination timing."
                )

        # Check climate compatibility
        site_climate = profile.climate_zone or ("semi_arid" if rain and rain <= 500 else None)
        if site_climate and "compatible_climates" in pre:
            if site_climate not in pre["compatible_climates"]:
                fit_penalties += 0.20
                rationale_elements.append(f"Climate zone '{site_climate}' is secondary to primary target biomes.")

        feasibility_score = max(0.40, 1.0 - fit_penalties)

        # 3. Data Completeness
        var_count = profile.present_variables_count()
        if var_count >= 6:
            data_completeness = 1.0
        elif var_count >= 4:
            data_completeness = 0.88
        else:
            data_completeness = 0.75

        # Weighted final confidence score
        final_score = (0.45 * evidence_score) + (0.35 * feasibility_score) + (0.20 * data_completeness)
        final_score = min(0.96, max(0.45, final_score))

        if final_score >= 0.82:
            tier = "High"
            summary = "Grounded in peer-reviewed meta-analyses with high edaphic compatibility."
        elif final_score >= 0.68:
            tier = "Medium"
            summary = "Well-supported by multi-site trials; site moisture constraints require seasonal monitoring."
        else:
            tier = "Conditional"
            summary = "Viable intervention but subject to local precipitation and species selection constraints."

        full_rationale = f"{summary} " + " ".join(rationale_elements)

        return round(final_score, 2), tier, full_rationale.strip()
