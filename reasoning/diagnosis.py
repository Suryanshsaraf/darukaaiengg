"""
Darukaa.Earth: Multi-Variable Ecological Diagnostic Matrix
Evaluates compound interactions across at least 3 interacting environmental variables:
Soil Health, Water/Climate, Land Use/Cover, Biodiversity, and Human Impact.
Strictly blocks single-variable diagnoses.
"""

from typing import List, Dict, Any, Tuple
from core.models import SiteProfile, CausalCompoundDiagnosis
from core.metrics import normalize_metric


class CausalDiagnosticMatrix:
    """
    Deterministic multi-variable causal analyzer.
    Identifies synergistic ecological degradation loops connecting 3+ variables.
    """

    def diagnose(self, profile: SiteProfile) -> CausalCompoundDiagnosis:
        critical_vars = profile.get_critical_variables()
        var_keys = list(critical_vars.keys())

        if len(var_keys) < 3:
            raise ValueError(
                f"Ecological diagnosis gate failed: System requires at least 3 distinct "
                f"interacting environmental variables, but only {len(var_keys)} were provided: {var_keys}"
            )

        interacting_vars: List[str] = []
        pathways: List[str] = []
        mechanisms: List[str] = []
        limiting_factors: List[str] = []
        vulnerability_penalties: List[float] = []

        soc = profile.soil_organic_carbon_pct
        rain = profile.rainfall_annual_mm
        climate = profile.climate_zone or ("semi_arid" if rain and rain < 500 else None)
        land_use = profile.land_use_type or "monoculture_cropland"
        crop = profile.crop_type or ""
        tillage = profile.tillage_practice
        ph = profile.soil_ph
        bd = profile.soil_bulk_density
        moisture = profile.soil_moisture_pct
        canopy = profile.canopy_cover_pct
        pollinators = profile.pollinator_density_index
        amf = profile.mycorrhizal_colonization_pct
        pesticides = profile.pesticide_passes_yr
        synth_n = profile.synthetic_nitrogen_kg_ha

        # Compound Pattern 1: Semi-arid / Low Rain + Low SOC + Monoculture Cropland
        is_dryland = (climate in ["semi_arid", "arid"]) or (rain is not None and rain <= 500.0)
        is_low_soc = (soc is not None and soc <= 1.2)
        is_monoculture = (
            "monoculture" in land_use.lower() or 
            "wheat" in crop.lower() or 
            "cotton" in crop.lower() or 
            "corn" in crop.lower()
        )

        if is_dryland and is_low_soc and is_monoculture:
            interacting_vars.extend(["soil_organic_carbon_pct", "rainfall_annual_mm/climate_zone", "land_use/crop_type"])
            pathways.append("Accelerated Soil Aggregate Breakdown & Moisture Evaporation Cascade")
            mechanisms.append(
                f"Depleted soil organic carbon ({soc if soc is not None else '<0.8'}%) impairs cation exchange and soil water "
                f"holding capacity. Under semi-arid evapotranspiration regimes ({rain if rain else '<500'} mm rainfall), "
                f"continuous monoculture {crop or 'cereal'} cropping leaves soil devoid of living root exudates during fallow periods. "
                f"The resulting absence of vegetative residue destabilizes soil macroaggregates, accelerating wind erosion and "
                f"limiting rainwater infiltration to shallow subsoils."
            )
            limiting_factors.extend([
                "Acute organic matter deficit limiting microbial glomalin production",
                "Severe surface evaporation under high vapor pressure deficit (VPD)",
                "Lack of multi-species root architecture to scavenge stratified nutrients"
            ])
            vulnerability_penalties.append(42.0)

        # Compound Pattern 2: Deep Tillage + High Pesticides + Suppressed Mutualists
        is_high_tillage = (tillage == "conventional_deep") or (tillage is None and is_monoculture)
        is_high_chem = (pesticides is not None and pesticides >= 2.0) or (synth_n is not None and synth_n >= 120.0)
        is_low_bio = (pollinators is not None and pollinators < 40.0) or (amf is not None and amf < 30.0)

        if is_high_tillage and is_high_chem:
            interacting_vars.extend(["tillage_practice", "pesticide_passes/synthetic_n", "biodiversity_indicators"])
            pathways.append("Trophic Web Disruption & Mycorrhizal Hyphae Shearing")
            mechanisms.append(
                "Mechanical inversion tillage fractures subterranean arbuscular mycorrhizal fungal (AMF) networks. "
                "Simultaneously, frequent chemical inputs decimate predatory ground beetles and native pollinators, "
                "creating pest resurgence vulnerability and degrading internal biological pest suppression loops."
            )
            limiting_factors.extend([
                "Mechanical shearing of fungal mycelia",
                "Agrochemical suppression of parasitoid and pollinator populations"
            ])
            vulnerability_penalties.append(28.0)

        # Compound Pattern 3: Pasture Degradation + High Bulk Density / Compaction + Low Ground Cover
        is_pasture = "pasture" in land_use.lower() or land_use == "degraded_pasture"
        is_compacted = (bd is not None and bd >= 1.45)
        is_bare = (profile.vegetative_ground_cover_pct is not None and profile.vegetative_ground_cover_pct < 50.0)

        if is_pasture and (is_compacted or is_bare):
            interacting_vars.extend(["land_use_type (pasture)", "soil_bulk_density", "ground_cover_pct"])
            pathways.append("Rangeland Sward Degeneration & Hydrological Decoupling")
            mechanisms.append(
                "Continuous selective livestock grazing exhausts root energy reserves of perennial bunchgrasses, "
                "leading to sward thinning and surface crusting. Elevated bulk density severely impedes water infiltration, "
                "causing flash surface runoff during storm events and starving subsoil horizons of recharge."
            )
            limiting_factors.extend([
                "Root-restrictive subsoil compaction",
                "Loss of native bunchgrass seed reserves"
            ])
            vulnerability_penalties.append(34.0)

        # Fallback / General Multi-Metric Synthesis if specific named pattern not fully triggered
        if not interacting_vars:
            # Pick top 3-4 present variables
            top_vars = var_keys[:4]
            interacting_vars.extend(top_vars)
            pathways.append("Coupled Edaphic-Climatic Degradation Dynamic")
            mechanisms.append(
                f"Multi-factorial interaction observed across {', '.join(top_vars)}. "
                f"Suboptimal edaphic conditions interact with local climatic exposure and management disturbances, "
                f"reducing ecological buffer capacity and biological nutrient recycling efficiency."
            )
            limiting_factors.append("Suboptimal balance across structural soil metrics and vegetative cover")
            vulnerability_penalties.append(25.0)

        # Deduplicate variables while preserving order
        deduped_vars: List[str] = []
        for v in interacting_vars:
            if v not in deduped_vars:
                deduped_vars.append(v)

        # Guarantee at least 3 interacting variables
        if len(deduped_vars) < 3:
            for k in var_keys:
                if k not in deduped_vars:
                    deduped_vars.append(k)
                if len(deduped_vars) >= 3:
                    break

        # Compute vulnerability score (0 - 100)
        base_vulnerability = sum(vulnerability_penalties)
        # Factor in normalized metric health
        health_scores = []
        for k, val in critical_vars.items():
            if isinstance(val, (int, float)):
                health_scores.append(normalize_metric(k, float(val)))
        
        if health_scores:
            avg_health = sum(health_scores) / len(health_scores)
            computed_score = min(96.0, max(20.0, base_vulnerability * 0.65 + (1.0 - avg_health) * 50.0))
        else:
            computed_score = min(96.0, max(25.0, base_vulnerability))

        primary_pathway = " & ".join(pathways[:2])

        return CausalCompoundDiagnosis(
            primary_degradation_pathway=primary_pathway,
            interacting_variables=deduped_vars,
            compound_risk_analysis=" ".join(mechanisms),
            vulnerability_score=computed_score,
            limiting_factors=list(dict.fromkeys(limiting_factors)),
            ecological_mechanisms=mechanisms
        )
