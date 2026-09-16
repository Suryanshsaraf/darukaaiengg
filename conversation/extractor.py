"""
Darukaa.Earth: Free-Text Ecological Entity & Metric Extractor
Deterministic parser extracting quantitative environmental metrics and categorical
variables from natural language dialogues and structured text.
"""

import re
from typing import Dict, Any, Optional
from core.models import SiteProfile


class EcologicalEntityExtractor:
    """Extracts pedological, climatic, and ecological variables from user input."""

    @staticmethod
    def extract_from_text(text: str, existing_profile: Optional[SiteProfile] = None) -> SiteProfile:
        profile = existing_profile or SiteProfile()
        text_lower = text.lower()

        # 1. Soil Organic Carbon (SOC)
        # Matches: "soil organic carbon: 0.3%", "SOC: 0.4%", "organic carbon 0.3", "soc is 0.5%"
        soc_match = re.search(r"(?:soil\s+organic\s+carbon|soc|organic\s+carbon)[\s:=]+([0-9]+(?:\.[0-9]+)?)\s*%?", text_lower)
        if soc_match:
            try:
                profile.soil_organic_carbon_pct = float(soc_match.group(1))
            except ValueError:
                pass
        elif "low carbon" in text_lower or "depleted carbon" in text_lower:
            if profile.soil_organic_carbon_pct is None:
                profile.soil_organic_carbon_pct = 0.4

        # 2. Soil pH
        # Matches: "ph: 6.5", "soil ph 5.2", "ph of 7.8"
        ph_match = re.search(r"\b(?:soil\s+)?ph[\s:=]+([0-9]+(?:\.[0-9]+)?)\b", text_lower)
        if ph_match:
            try:
                profile.soil_ph = float(ph_match.group(1))
            except ValueError:
                pass

        # 3. Soil Bulk Density
        # Matches: "bulk density: 1.55", "bd: 1.4"
        bd_match = re.search(r"\b(?:bulk\s+density|bd)[\s:=]+([0-9]+(?:\.[0-9]+)?)\b", text_lower)
        if bd_match:
            try:
                profile.soil_bulk_density = float(bd_match.group(1))
            except ValueError:
                pass

        # 4. Rainfall / Precipitation
        # Matches numeric: "rainfall: 350mm", "rainfall: 400", "precip: 300 mm"
        rain_match = re.search(r"(?:rainfall|precipitation|precip)[\s:=]+([0-9]+(?:\.[0-9]+)?)\s*(?:mm)?", text_lower)
        if rain_match:
            try:
                profile.rainfall_annual_mm = float(rain_match.group(1))
                if profile.rainfall_annual_mm < 500 and not profile.climate_zone:
                    profile.climate_zone = "semi_arid"
            except ValueError:
                pass
        elif "low rainfall" in text_lower or "rainfall: low" in text_lower or "dryland" in text_lower:
            if profile.rainfall_annual_mm is None:
                profile.rainfall_annual_mm = 320.0
            profile.rainfall_pattern = "low_erratic"
            if not profile.climate_zone:
                profile.climate_zone = "semi_arid"

        # 5. Climate Zone / Region
        if "semi-arid" in text_lower or "semi arid" in text_lower:
            profile.climate_zone = "semi_arid"
        elif "arid" in text_lower:
            profile.climate_zone = "arid"
        elif "temperate" in text_lower:
            profile.climate_zone = "temperate"
        elif "tropical" in text_lower:
            profile.climate_zone = "tropical"

        # 6. Land Use & Crop Type
        if "monoculture wheat" in text_lower or "wheat monoculture" in text_lower:
            profile.land_use_type = "monoculture_cropland"
            profile.crop_type = "monoculture wheat"
        elif "monoculture" in text_lower:
            profile.land_use_type = "monoculture_cropland"
            # look for crop after monoculture
            crop_match = re.search(r"monoculture\s+([a-z]+)", text_lower)
            if crop_match:
                profile.crop_type = f"monoculture {crop_match.group(1)}"
        elif "pasture" in text_lower or "rangeland" in text_lower or "grazing" in text_lower:
            profile.land_use_type = "degraded_pasture"
        elif "agroforestry" in text_lower:
            profile.land_use_type = "agroforestry_silvopasture"

        if "crop:" in text_lower or "crop is" in text_lower:
            c_match = re.search(r"crop(?:[\s:=]+|is\s+)([a-z0-9\s\-]+?)(?:,|$|\.|\n)", text_lower)
            if c_match:
                profile.crop_type = c_match.group(1).strip()

        # 7. Tillage Practice
        if "no-till" in text_lower or "no till" in text_lower or "zero tillage" in text_lower:
            profile.tillage_practice = "no_till_direct_seed"
        elif "conventional tillage" in text_lower or "deep plowing" in text_lower or "tillage: conventional" in text_lower or "plowed" in text_lower:
            profile.tillage_practice = "conventional_deep"

        # 8. Ground / Canopy Cover
        cover_match = re.search(r"(?:ground\s+cover|vegetative\s+cover)[\s:=]+([0-9]+(?:\.[0-9]+)?)\s*%", text_lower)
        if cover_match:
            try:
                profile.vegetative_ground_cover_pct = float(cover_match.group(1))
            except ValueError:
                pass

        canopy_match = re.search(r"canopy(?:\s+cover)?[\s:=]+([0-9]+(?:\.[0-9]+)?)\s*%", text_lower)
        if canopy_match:
            try:
                profile.canopy_cover_pct = float(canopy_match.group(1))
            except ValueError:
                pass

        # 9. Human Agrochemical Impact
        pest_match = re.search(r"(?:pesticide|spray)(?:[\s:=]+|passes[\s:=]+)([0-9]+(?:\.[0-9]+)?)", text_lower)
        if pest_match:
            try:
                profile.pesticide_passes_yr = float(pest_match.group(1))
            except ValueError:
                pass

        n_match = re.search(r"(?:nitrogen|synthetic\s+n|n\s+rate)[\s:=]+([0-9]+(?:\.[0-9]+)?)\s*(?:kg)?", text_lower)
        if n_match:
            try:
                profile.synthetic_nitrogen_kg_ha = float(n_match.group(1))
            except ValueError:
                pass

        # 10. Geo-coordinates (e.g. "coords: 31.5, -102.3" or "lat: 31.5, lon: -102.3")
        coord_match = re.search(r"(?:lat|latitude)[\s:=]+([\-0-9\.]+)[,\s]+(?:lon|long|longitude)[\s:=]+([\-0-9\.]+)", text_lower)
        if coord_match:
            try:
                profile.coordinates = (float(coord_match.group(1)), float(coord_match.group(2)))
            except ValueError:
                pass
        else:
            simple_coords = re.search(r"(-?\d+\.\d+)\s*,\s*(-?\d+\.\d+)", text)
            if simple_coords:
                try:
                    profile.coordinates = (float(simple_coords.group(1)), float(simple_coords.group(2)))
                except ValueError:
                    pass

        profile.raw_query = text
        return profile
