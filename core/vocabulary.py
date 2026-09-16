"""
Darukaa.Earth: Ecological Vocabulary & Taxonomies
Controlled scientific constants, biomes, classifications, and thresholds.
Grounded in pedology, FAO soil guidelines, and IPBES ecological frameworks.
"""

from enum import Enum


class BiomeType(str, Enum):
    SEMI_ARID_GRASSLAND = "semi_arid_grassland"
    ARID_SHRUBLAND = "arid_shrubland"
    TEMPERATE_BROADLEAF = "temperate_broadleaf"
    TROPICAL_DRY_FOREST = "tropical_dry_forest"
    TROPICAL_MOIST_FOREST = "tropical_moist_forest"
    MEDITERRANEAN_WOODLAND = "mediterranean_woodland"
    SAVANNA = "savanna"
    BOREAL_TAIGA = "boreal_taiga"


class LandUseType(str, Enum):
    MONOCULTURE_CROPLAND = "monoculture_cropland"
    INTENSIVE_TILLAGE_CROPLAND = "intensive_tillage_cropland"
    DEGRADED_PASTURE = "degraded_pasture"
    ROTATIONAL_PASTURE = "rotational_pasture"
    CONVENTIONAL_ORCHARD = "conventional_orchard"
    AGROFORESTRY_SILVOPASTURE = "agroforestry_silvopasture"
    CONSERVATION_CROPPING = "conservation_cropping"
    FALLOW_DEGRADED = "fallow_degraded"
    RIPARIAN_BUFFER = "riparian_buffer"


class TillagePractice(str, Enum):
    CONVENTIONAL_DEEP = "conventional_deep"
    REDUCED_TILL = "reduced_till"
    NO_TILL_DIRECT_SEED = "no_till_direct_seed"
    STRIP_TILL = "strip_till"


class AridityCategory(str, Enum):
    HYPER_ARID = "hyper_arid"        # AI < 0.05
    ARID = "arid"                    # 0.05 <= AI < 0.20
    SEMI_ARID = "semi_arid"          # 0.20 <= AI < 0.50
    DRY_SUB_HUMID = "dry_sub_humid"  # 0.50 <= AI < 0.65
    HUMID = "humid"                  # AI >= 0.65


class SoilTextureClass(str, Enum):
    SAND = "sand"
    LOAMY_SAND = "loamy_sand"
    SANDY_LOAM = "sandy_loam"
    LOAM = "loam"
    SILT_LOAM = "silt_loam"
    CLAY_LOAM = "clay_loam"
    CLAY = "clay"


class TimeHorizon(str, Enum):
    SHORT_TERM = "short_term"      # 6 - 18 months
    MEDIUM_TERM = "medium_term"    # 2 - 5 years
    LONG_TERM = "long_term"        # 5 - 15 years


class ConfidenceTier(str, Enum):
    HIGH = "high"                  # Multi-site meta-analyses (FAO/IPCC/Nature), empirical match
    MEDIUM = "medium"              # Single-site controlled trials or modeled extrapolations
    LOW = "low"                    # Observational or limited geographical transferability


class EcologicalDimension(str, Enum):
    SOIL_HEALTH = "soil_health"
    LAND_USE = "land_use"
    WATER_CLIMATE = "water_climate"
    BIODIVERSITY = "biodiversity"
    HUMAN_IMPACT = "human_impact"
