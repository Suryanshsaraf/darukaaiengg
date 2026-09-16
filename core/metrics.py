"""
Darukaa.Earth: Environmental Metric Definitions, Bounds & Scientific Units
Pedological and ecological quantitative thresholds based on FAO, USDA-NRCS, and IPCC.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional, Tuple


@dataclass(frozen=True)
class MetricDefinition:
    key: str
    display_name: str
    dimension: str
    unit: str
    min_val: float
    max_val: float
    critical_threshold_low: Optional[float]
    critical_threshold_high: Optional[float]
    optimal_range: Tuple[float, float]
    scientific_basis: str


METRIC_REGISTRY: Dict[str, MetricDefinition] = {
    "soil_organic_carbon_pct": MetricDefinition(
        key="soil_organic_carbon_pct",
        display_name="Soil Organic Carbon (SOC)",
        dimension="soil_health",
        unit="%",
        min_val=0.0,
        max_val=15.0,
        critical_threshold_low=0.5,   # Critical FAO threshold: below 0.5% indicates acute soil desertification
        critical_threshold_high=None,
        optimal_range=(2.0, 5.0),
        scientific_basis="FAO Global Assessment of Soil Organic Carbon (2020); Lal (2004) Science 304(5677)"
    ),
    "soil_ph": MetricDefinition(
        key="soil_ph",
        display_name="Soil pH",
        dimension="soil_health",
        unit="pH",
        min_val=3.0,
        max_val=11.0,
        critical_threshold_low=5.2,   # Below 5.2 triggers aluminum/manganese phytotoxicity and AMF suppression
        critical_threshold_high=8.4,  # Above 8.4 triggers micronutrient lockout (Fe, Zn, P precipitation)
        optimal_range=(6.2, 7.2),
        scientific_basis="Slessarev et al. (2016) Nature 540; USDA-NRCS Soil Health Indicators"
    ),
    "soil_bulk_density": MetricDefinition(
        key="soil_bulk_density",
        display_name="Soil Bulk Density",
        dimension="soil_health",
        unit="g/cm³",
        min_val=0.8,
        max_val=2.2,
        critical_threshold_low=None,
        critical_threshold_high=1.55, # >1.55 restricts root penetration, aerotropic microbial respiration
        optimal_range=(1.10, 1.30),
        scientific_basis="USDA Natural Resources Conservation Service Soil Quality Institute (2001)"
    ),
    "soil_moisture_pct": MetricDefinition(
        key="soil_moisture_pct",
        display_name="Volumetric Soil Moisture",
        dimension="soil_health",
        unit="%",
        min_val=0.0,
        max_val=60.0,
        critical_threshold_low=10.0,  # Below permanent wilting point for loams
        critical_threshold_high=45.0, # Anaerobic waterlogging risk
        optimal_range=(20.0, 35.0),
        scientific_basis="Hillel (2004) Introduction to Environmental Soil Physics; FAO Irrigation Paper 56"
    ),
    "rainfall_annual_mm": MetricDefinition(
        key="rainfall_annual_mm",
        display_name="Mean Annual Precipitation",
        dimension="water_climate",
        unit="mm/yr",
        min_val=50.0,
        max_val=4500.0,
        critical_threshold_low=350.0, # Dryland semi-arid threshold (<350-400mm restricts non-irrigated cover crops)
        critical_threshold_high=None,
        optimal_range=(600.0, 1200.0),
        scientific_basis="UNEP World Atlas of Desertification; IPCC Special Report on Climate Change and Land (2019)"
    ),
    "aridity_index": MetricDefinition(
        key="aridity_index",
        display_name="UNEP Aridity Index (P/PET)",
        dimension="water_climate",
        unit="ratio",
        min_val=0.01,
        max_val=2.5,
        critical_threshold_low=0.20,  # <0.20 is Arid; 0.20-0.50 Semi-arid
        critical_threshold_high=None,
        optimal_range=(0.65, 1.50),
        scientific_basis="Middleton & Thomas (1997) World Atlas of Desertification UNEP"
    ),
    "canopy_cover_pct": MetricDefinition(
        key="canopy_cover_pct",
        display_name="Woody Canopy Cover",
        dimension="land_use",
        unit="%",
        min_val=0.0,
        max_val=100.0,
        critical_threshold_low=5.0,   # Landscape bareness, absence of vertical structural diversity
        critical_threshold_high=None,
        optimal_range=(20.0, 45.0),   # Silvopastoral / agroforestry equilibrium
        scientific_basis="Jose (2009) Agroforestry Systems 76(1); IPBES Global Assessment (2019)"
    ),
    "vegetative_ground_cover_pct": MetricDefinition(
        key="vegetative_ground_cover_pct",
        display_name="Living/Residue Ground Cover",
        dimension="land_use",
        unit="%",
        min_val=0.0,
        max_val=100.0,
        critical_threshold_low=30.0,  # <30% triggers catastrophic wind and sheet erosion under Revised Universal Soil Loss Equation (RUSLE)
        critical_threshold_high=None,
        optimal_range=(70.0, 100.0),
        scientific_basis="Renard et al. (1997) USDA RUSLE Handbook; FAO Conservation Agriculture Series"
    ),
    "pollinator_density_index": MetricDefinition(
        key="pollinator_density_index",
        display_name="Pollinator Abundance Proxy",
        dimension="biodiversity",
        unit="index (0-100)",
        min_val=0.0,
        max_val=100.0,
        critical_threshold_low=20.0,
        critical_threshold_high=None,
        optimal_range=(60.0, 95.0),
        scientific_basis="Potts et al. (2016) IPBES Assessment Report on Pollinators, Pollination and Food Production"
    ),
    "shannon_diversity_index": MetricDefinition(
        key="shannon_diversity_index",
        display_name="Shannon Diversity Index (H')",
        dimension="biodiversity",
        unit="H'",
        min_val=0.0,
        max_val=5.0,
        critical_threshold_low=1.0,   # Extreme monoculture homogeneity
        critical_threshold_high=None,
        optimal_range=(2.5, 4.2),
        scientific_basis="Magurran (2004) Measuring Biological Diversity; IPBES (2019)"
    ),
    "mycorrhizal_colonization_pct": MetricDefinition(
        key="mycorrhizal_colonization_pct",
        display_name="Arbuscular Mycorrhizal Fungal (AMF) Colonization",
        dimension="biodiversity",
        unit="%",
        min_val=0.0,
        max_val=100.0,
        critical_threshold_low=15.0,  # Fungal hyphae depletion due to intensive tillage/fungicide
        critical_threshold_high=None,
        optimal_range=(45.0, 85.0),
        scientific_basis="Rillig et al. (2019) Science 366; Smith & Read (2008) Mycorrhizal Symbiosis"
    ),
    "synthetic_nitrogen_kg_ha": MetricDefinition(
        key="synthetic_nitrogen_kg_ha",
        display_name="Synthetic Nitrogen Application",
        dimension="human_impact",
        unit="kg N/ha/yr",
        min_val=0.0,
        max_val=400.0,
        critical_threshold_low=None,
        critical_threshold_high=160.0, # Excessive synthetic N accelerates soil organic matter oxidation and nitrate runoff
        optimal_range=(0.0, 60.0),
        scientific_basis="Mulvaney et al. (2009) J. Environ. Qual. 38; Galloway et al. (2008) Science 320"
    ),
    "pesticide_passes_yr": MetricDefinition(
        key="pesticide_passes_yr",
        display_name="Chemical Pesticide Application Frequency",
        dimension="human_impact",
        unit="passes/yr",
        min_val=0.0,
        max_val=20.0,
        critical_threshold_low=None,
        critical_threshold_high=3.0,  # Repeated broad-spectrum sprays break predatory insect cascades
        optimal_range=(0.0, 1.0),
        scientific_basis="Sánchez-Bayo & Wyckhuys (2019) Biological Conservation 232"
    )
}


def normalize_metric(key: str, value: float) -> float:
    """Normalize metric value to a 0.0 - 1.0 health score where 1.0 is ecologically optimal."""
    if key not in METRIC_REGISTRY:
        return 0.5
    m = METRIC_REGISTRY[key]
    low_opt, high_opt = m.optimal_range

    if low_opt <= value <= high_opt:
        return 1.0

    # Below optimal
    if value < low_opt:
        crit_low = m.critical_threshold_low if m.critical_threshold_low is not None else m.min_val
        if value <= crit_low:
            return 0.15
        span = low_opt - crit_low
        if span <= 0:
            return 0.5
        return 0.15 + 0.85 * ((value - crit_low) / span)

    # Above optimal
    if value > high_opt:
        crit_high = m.critical_threshold_high if m.critical_threshold_high is not None else m.max_val
        if value >= crit_high:
            return 0.15
        span = crit_high - high_opt
        if span <= 0:
            return 0.5
        return 1.0 - 0.85 * ((value - high_opt) / span)

    return 0.5
