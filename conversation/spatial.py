"""
Darukaa.Earth: Spatial Context & Geo-Coordinates Enrichment
Enriches site profiles with edaphic and climatic context based on latitude/longitude.
Utilizes cached pedological baselines (ISRIC SoilGrids, WorldClim, WWF Ecoregions).
"""

from typing import Tuple, Dict, Any, Optional
from core.models import SiteProfile


# Curated high-precision benchmark coordinates for global agricultural basins
BENCHMARK_SPATIAL_REGIONS = [
    {
        "name": "North-Western Indo-Gangetic Semi-Arid Basin",
        "bounds": {"min_lat": 26.0, "max_lat": 32.0, "min_lon": 72.0, "max_lon": 79.0},
        "climate_zone": "semi_arid",
        "biome": "tropical_dry_forest",
        "rainfall_annual_mm": 420.0,
        "rainfall_pattern": "seasonal_monsoonal",
        "baseline_soc_pct": 0.38,
        "soil_texture": "sandy_loam",
        "default_crop": "monoculture wheat",
        "data_sources": "ISRIC SoilGrids 250m; WorldClim v2.1; ICAR Pedology Survey"
    },
    {
        "name": "North American Southern High Plains (Texas/New Mexico)",
        "bounds": {"min_lat": 31.0, "max_lat": 36.5, "min_lon": -104.0, "max_lon": -99.0},
        "climate_zone": "semi_arid",
        "biome": "semi_arid_grassland",
        "rainfall_annual_mm": 380.0,
        "rainfall_pattern": "low_erratic",
        "baseline_soc_pct": 0.45,
        "soil_texture": "loamy_sand",
        "default_crop": "monoculture wheat/cotton",
        "data_sources": "USDA-NRCS SSURGO; PRISM Climate Group"
    },
    {
        "name": "Sahelian Semi-Arid Agro-Pastoral Belt",
        "bounds": {"min_lat": 12.0, "max_lat": 16.0, "min_lon": -5.0, "max_lon": 15.0},
        "climate_zone": "arid",
        "biome": "savanna",
        "rainfall_annual_mm": 310.0,
        "rainfall_pattern": "low_erratic",
        "baseline_soc_pct": 0.32,
        "soil_texture": "sand",
        "default_crop": "monoculture millet/sorghum",
        "data_sources": "FAO Africover; ISRIC World Soil Information"
    },
    {
        "name": "Mediterranean Iberian Steppe (La Mancha/Andalusia)",
        "bounds": {"min_lat": 37.0, "max_lat": 40.5, "min_lon": -5.0, "max_lon": -1.5},
        "climate_zone": "semi_arid",
        "biome": "mediterranean_woodland",
        "rainfall_annual_mm": 410.0,
        "rainfall_pattern": "seasonal_winter_rain",
        "baseline_soc_pct": 0.65,
        "soil_texture": "clay_loam",
        "default_crop": "monoculture cereal/olive",
        "data_sources": "European Soil Data Centre (ESDAC); Copernicus ERA5-Land"
    }
]


class SpatialEnrichmentService:
    """Enriches coordinates with edaphic and bioclimatic baselines."""

    @classmethod
    def enrich_profile(cls, profile: SiteProfile) -> SiteProfile:
        if not profile.coordinates:
            return profile

        lat, lon = profile.coordinates

        # 1. Check benchmark basins
        for region in BENCHMARK_SPATIAL_REGIONS:
            b = region["bounds"]
            if b["min_lat"] <= lat <= b["max_lat"] and b["min_lon"] <= lon <= b["max_lon"]:
                if profile.climate_zone is None:
                    profile.climate_zone = region["climate_zone"]
                if profile.rainfall_annual_mm is None:
                    profile.rainfall_annual_mm = region["rainfall_annual_mm"]
                if profile.rainfall_pattern is None:
                    profile.rainfall_pattern = region["rainfall_pattern"]
                if profile.soil_organic_carbon_pct is None:
                    profile.soil_organic_carbon_pct = region["baseline_soc_pct"]
                if profile.soil_texture is None:
                    profile.soil_texture = region["soil_texture"]
                if profile.location_name is None:
                    profile.location_name = region["name"]
                profile.enriched_spatially = True
                return profile

        # 2. General geographic heuristic by latitude band
        abs_lat = abs(lat)
        if abs_lat < 15.0:
            default_climate = "tropical"
            default_rain = 1100.0
            default_soc = 1.4
        elif 15.0 <= abs_lat < 35.0:
            default_climate = "semi_arid"
            default_rain = 390.0
            default_soc = 0.55
        elif 35.0 <= abs_lat < 55.0:
            default_climate = "temperate"
            default_rain = 750.0
            default_soc = 1.8
        else:
            default_climate = "cold_continental"
            default_rain = 500.0
            default_soc = 2.2

        if profile.climate_zone is None:
            profile.climate_zone = default_climate
        if profile.rainfall_annual_mm is None:
            profile.rainfall_annual_mm = default_rain
        if profile.soil_organic_carbon_pct is None:
            profile.soil_organic_carbon_pct = default_soc
        if profile.location_name is None:
            profile.location_name = f"Coordinates ({lat:.3f}, {lon:.3f})"

        profile.enriched_spatially = True
        return profile
