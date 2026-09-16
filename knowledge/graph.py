"""
Darukaa.Earth: Structured Claim & Intervention Knowledge Graph
Deterministic mapping of ecological interventions, site preconditions,
multi-metric causal pathways, trade-offs, and verified citations.
"""

from typing import List, Dict, Any, Optional


INTERVENTION_GRAPH: List[Dict[str, Any]] = [
    {
        "intervention_id": "INT-LEGUME-COVER-CROPPING",
        "title": "Multi-Species Leguminous Cover Cropping & Green Manuring",
        "category": "Agro-ecological Soil Regeneration",
        "time_horizon": "Short to Medium-Term (18-36 months)",
        "preconditions": {
            "min_rainfall_annual_mm": 280.0,
            "max_soil_organic_carbon_pct": 2.0,
            "compatible_climates": ["semi_arid", "arid", "dry_sub_humid", "temperate", "tropical"],
            "compatible_land_use": ["monoculture_cropland", "intensive_tillage_cropland", "fallow_degraded"]
        },
        "prohibited_conditions": {
            "max_rainfall_annual_mm": 180.0,  # Extreme hyper-arid without irrigation
        },
        "target_variables_addressed": [
            "soil_organic_carbon_pct",
            "mycorrhizal_colonization_pct",
            "soil_bulk_density",
            "vegetative_ground_cover_pct"
        ],
        "what_to_do": (
            "Broadcast or drill a calibrated multi-species cover crop cocktail—combining deep-rooted legumes "
            "(e.g., hairy vetch Vicia villosa, crimson clover, or drought-hardy cowpea Vigna unguiculata) "
            "with brassicas and fibrous-rooted cereals—into post-harvest stubble or fallow gaps. Terminate "
            "mechanically using a roller-crimper or shallow flail mower 15-20 days prior to primary cash crop planting."
        ),
        "why_it_works": (
            "Symbiotic Rhizobium bacteria inside root nodules fix atmospheric nitrogen (60-140 kg N/ha/yr). Continuous "
            "rhizodeposition of labile carbon feeds fungal and bacterial communities, while fine root decay creates "
            "macropores that decompact dense subsoils. The surface residue forms an insulative mulch layer that drops "
            "soil temperature peaks and curtails evaporative moisture loss."
        ),
        "projected_metric_impacts": [
            {
                "metric_key": "soil_organic_carbon_pct",
                "metric_name": "Soil Organic Carbon",
                "projected_delta_min": 18.0,
                "projected_delta_max": 28.0,
                "unit": "%",
                "time_horizon": "2-3 years",
                "causal_mechanism": "Labile root exudates and biomass carbon incorporation into organo-mineral fractions"
            },
            {
                "metric_key": "soil_bulk_density",
                "metric_name": "Soil Bulk Density",
                "projected_delta_min": -6.0,
                "projected_delta_max": -11.0,
                "unit": "%",
                "time_horizon": "18-24 months",
                "causal_mechanism": "Bio-drilling by taproots creating stable vertical macropores"
            },
            {
                "metric_key": "vegetative_ground_cover_pct",
                "metric_name": "Living/Residue Ground Cover",
                "projected_delta_min": 40.0,
                "projected_delta_max": 75.0,
                "unit": "%",
                "time_horizon": "6-12 months",
                "causal_mechanism": "Continuous canopy intercept preventing raindrop detachment and wind shear"
            },
            {
                "metric_key": "mycorrhizal_colonization_pct",
                "metric_name": "Arbuscular Mycorrhizal Colonization",
                "projected_delta_min": 35.0,
                "projected_delta_max": 65.0,
                "unit": "%",
                "time_horizon": "18-36 months",
                "causal_mechanism": "Continuous living host plant roots maintaining active extraradical AMF mycelium"
            }
        ],
        "trade_offs_and_risks": [
            "In strictly rainfed dryland zones (<350 mm), unmanaged cover crop growth can deplete residual seedbed soil moisture.",
            "Must be rolled/crimped before seed maturation to prevent cover crop species from becoming volunteer weeds in the cash crop."
        ],
        "evidence_chunk_ids": ["FAO-GSP-2020-C1", "SCIENCE-MYCO-2020-C1", "PNAS-NCS-2017-C1"]
    },
    {
        "intervention_id": "INT-DRYLAND-AGROFORESTRY",
        "title": "Dryland Agroforestry & Alley Cropping with Nitrogen-Fixing Perennials",
        "category": "Structural Landscape Agroforestry",
        "time_horizon": "Medium to Long-Term (3-6 years)",
        "preconditions": {
            "max_canopy_cover_pct": 12.0,
            "compatible_climates": ["semi_arid", "arid", "dry_sub_humid", "tropical"],
            "compatible_land_use": ["monoculture_cropland", "degraded_pasture", "fallow_degraded"]
        },
        "prohibited_conditions": {},
        "target_variables_addressed": [
            "canopy_cover_pct",
            "soil_organic_carbon_pct",
            "shannon_diversity_index",
            "soil_moisture_pct"
        ],
        "what_to_do": (
            "Establish contour-aligned tree rows (alleys spaced 10-18 meters apart) utilizing indigenous or naturalized "
            "drought-resilient leguminous trees and deep-rooted shrubs (e.g., Faidherbia albida, Prosopis cineraria, "
            "Leucaena leucocephala, or native Acacia species). Annual cereals or pulse crops are cultivated within "
            "the wide inter-row alleys."
        ),
        "why_it_works": (
            "Deep tree roots penetrate subsoil and fractured bedrock, executing hydraulic lift during nocturnal periods "
            "to moisten upper rooting horizons. Species exhibiting reverse phenology (like Faidherbia albida) drop foliage "
            "during crop sowing, contributing high-nitrogen green mulch while avoiding vegetative shade competition. "
            "Woody shelterbelts reduce horizontal wind velocity, slashing crop evapotranspiration by 20-30%."
        ),
        "projected_metric_impacts": [
            {
                "metric_key": "canopy_cover_pct",
                "metric_name": "Woody Canopy Cover",
                "projected_delta_min": 15.0,
                "projected_delta_max": 25.0,
                "unit": "%",
                "time_horizon": "3-5 years",
                "causal_mechanism": "Perennial crown development providing multi-strata structural complexity"
            },
            {
                "metric_key": "soil_organic_carbon_pct",
                "metric_name": "Soil Organic Carbon",
                "projected_delta_min": 22.0,
                "projected_delta_max": 38.0,
                "unit": "%",
                "time_horizon": "3-6 years",
                "causal_mechanism": "Perennial litterfall, root exudation, and root turnover under tree canopies"
            },
            {
                "metric_key": "shannon_diversity_index",
                "metric_name": "Shannon Biodiversity Index",
                "projected_delta_min": 35.0,
                "projected_delta_max": 60.0,
                "unit": "%",
                "time_horizon": "2-4 years",
                "causal_mechanism": "Vertical habitat layering for avian, predatory arthropod, and pollinator taxa"
            },
            {
                "metric_key": "soil_moisture_pct",
                "metric_name": "Subsoil Moisture Retention",
                "projected_delta_min": 15.0,
                "projected_delta_max": 28.0,
                "unit": "%",
                "time_horizon": "3-5 years",
                "causal_mechanism": "Hydraulic redistribution and reduced wind-driven vapor pressure deficits"
            }
        ],
        "trade_offs_and_risks": [
            "Saplings require herbivore fencing and protective irrigation/mulch during initial 12-18 months of establishment.",
            "Requires careful tree alley spacing to accommodate agricultural machinery (seeders, harvesters)."
        ],
        "evidence_chunk_ids": ["IPCC-SRCCL-2019-C1", "NATURE-PLANTS-2021-C1", "ICRAF-DRYLAND-2020-C1"]
    },
    {
        "intervention_id": "INT-CEREAL-LEGUME-INTERCROPPING",
        "title": "Strip Intercropping & Relay Cropping (Cereal-Pulse Niche Complementarity)",
        "category": "Temporal & Spatial Crop Diversification",
        "time_horizon": "Short-Term (6-18 months)",
        "preconditions": {
            "compatible_climates": ["semi_arid", "arid", "temperate", "tropical", "dry_sub_humid"],
            "compatible_land_use": ["monoculture_cropland", "intensive_tillage_cropland"]
        },
        "prohibited_conditions": {},
        "target_variables_addressed": [
            "shannon_diversity_index",
            "soil_organic_carbon_pct",
            "synthetic_nitrogen_kg_ha",
            "pollinator_density_index"
        ],
        "what_to_do": (
            "Transition from continuous sole-crop cereal stands (e.g. wheat, sorghum) to alternating strip intercropping "
            "(4:2 or 6:3 row arrangements) of cereals paired with legumes (e.g., chickpea Cicer arietinum, pigeonpea Cajanus cajan, "
            "or lentils Lens culinaris). In drylands, calibrate row widths to balance solar interception."
        ),
        "why_it_works": (
            "Temporal and spatial niche differentiation between fibrous monocot cereal roots and taproot dicot legumes enables "
            "optimal phosphorus extraction via legume carboxylate root exudates. Legume biological nitrogen fixation reduces "
            "reliance on synthetic nitrogen fertilizer by 30-50%, curtailing soil acidification and nitrate runoff while providing "
            "intermittent nectar flow for beneficial pollinators."
        ),
        "projected_metric_impacts": [
            {
                "metric_key": "shannon_diversity_index",
                "metric_name": "Field-Level Floral/Faunal Diversity",
                "projected_delta_min": 25.0,
                "projected_delta_max": 45.0,
                "unit": "%",
                "time_horizon": "1 season",
                "causal_mechanism": "Breaking monoculture host continuity and diversifying plant-associated microhabitats"
            },
            {
                "metric_key": "synthetic_nitrogen_kg_ha",
                "metric_name": "Synthetic Nitrogen Application",
                "projected_delta_min": -30.0,
                "projected_delta_max": -50.0,
                "unit": "%",
                "time_horizon": "1-2 seasons",
                "causal_mechanism": "Symbiotic nitrogen transfer and reduced baseline crop N demand"
            },
            {
                "metric_key": "pollinator_density_index",
                "metric_name": "Pollinator Abundance",
                "projected_delta_min": 35.0,
                "projected_delta_max": 65.0,
                "unit": "%",
                "time_horizon": "1 season",
                "causal_mechanism": "Staggered flowering duration providing accessible pollen and nectar resources"
            }
        ],
        "trade_offs_and_risks": [
            "Harvesting requires either multi-stage combines or synchronized seed maturity cultivars.",
            "Herbicide chemical weed control options are severely restricted due to broadleaf/monocot coexistence."
        ],
        "evidence_chunk_ids": ["IPCC-AR6-WG2-2022-C1", "NAT-COMM-DIVERSIFY-2021-C1", "FAO-BIODIV-2019-C1"]
    },
    {
        "intervention_id": "INT-CONSERVATION-TILLAGE",
        "title": "Zero-Tillage & Direct Seeding with Stubble Residue Retention",
        "category": "Conservation Pedology & Structural Protection",
        "time_horizon": "Short to Medium-Term (12-36 months)",
        "preconditions": {
            "compatible_climates": ["semi_arid", "temperate", "dry_sub_humid"],
            "compatible_land_use": ["intensive_tillage_cropland", "monoculture_cropland"]
        },
        "prohibited_conditions": {
            "soil_texture": "heavy_unstructured_vertisol_waterlogged"
        },
        "target_variables_addressed": [
            "soil_bulk_density",
            "mycorrhizal_colonization_pct",
            "vegetative_ground_cover_pct",
            "soil_organic_carbon_pct"
        ],
        "what_to_do": (
            "Halt deep moldboard plowing and disk harrowing. Deploy disc-opener no-till direct seeders that place seed "
            "and starter fertilizer directly into untilled soil through standing stubble. Maintain a minimum of 40-70% "
            "crop residue blanket over the soil surface year-round."
        ),
        "why_it_works": (
            "Inversion tillage shears fungal hyphae networks and oxidizes particulate organic matter. Eliminating tillage "
            "protects macroaggregates (>250 μm), preserving arbuscular mycorrhizal fungal networks and glomalin synthesis. "
            "Surface residue protects soil aggregates from droplet kinetic destruction, curtailing crusting and reducing "
            "surface runoff while increasing water infiltration."
        ),
        "projected_metric_impacts": [
            {
                "metric_key": "mycorrhizal_colonization_pct",
                "metric_name": "Mycorrhizal Fungal Colonization",
                "projected_delta_min": 40.0,
                "projected_delta_max": 75.0,
                "unit": "%",
                "time_horizon": "2-3 years",
                "causal_mechanism": "Preservation of perennial underground mycelial architecture and intact hyphal conduits"
            },
            {
                "metric_key": "soil_bulk_density",
                "metric_name": "Soil Bulk Density (10-25cm)",
                "projected_delta_min": -8.0,
                "projected_delta_max": -14.0,
                "unit": "%",
                "time_horizon": "2-4 years",
                "causal_mechanism": "Bio-pores created by earthworm drilosphere and decomposing undisturbed root channels"
            },
            {
                "metric_key": "soil_moisture_pct",
                "metric_name": "Available Soil Water Capacity",
                "projected_delta_min": 15.0,
                "projected_delta_max": 25.0,
                "unit": "%",
                "time_horizon": "1-2 years",
                "causal_mechanism": "Mulch blanket insulating soil surface from direct solar radiation and wind evaporation"
            }
        ],
        "trade_offs_and_risks": [
            "Requires dedicated direct-drill seeding equipment capable of cutting through thick crop residue.",
            "Initial soil cooling in high-latitude spring zones can delay seed germination by 3-5 days."
        ],
        "evidence_chunk_ids": ["FAO-GSP-2020-C2", "SCIENCE-MYCO-2020-C1", "SOIL-TILL-2022-C1"]
    },
    {
        "intervention_id": "INT-BIOCHAR-CO-COMPOST",
        "title": "Co-Composted Biochar & Mycorrhizal Inoculant Amendment",
        "category": "Soil Structural Matrix Rebuilding",
        "time_horizon": "Medium to Long-Term (1-5 years, durable >50 yrs)",
        "preconditions": {
            "max_soil_organic_carbon_pct": 1.2,
            "compatible_climates": ["semi_arid", "arid", "dry_sub_humid", "temperate"]
        },
        "prohibited_conditions": {},
        "target_variables_addressed": [
            "soil_organic_carbon_pct",
            "soil_moisture_pct",
            "soil_bulk_density"
        ],
        "what_to_do": (
            "Apply pyrolyzed woody or crop biomass (biochar) co-composted with manure or fungal inoculant at 5-10 t/ha. "
            "Incorporate into topsoil during strip renovation or targeted band application along crop planting lines."
        ),
        "why_it_works": (
            "Biochar contains highly aromatic, recalcitrant carbon resistant to chemical and enzymatic oxidation. "
            "Its micro-porous structure increases soil specific surface area, dramatically boosting soil cation exchange capacity (CEC) "
            "and water-retention capacity in coarse-textured sandy-loam soils while creating physical micro-refugia for beneficial soil bacteria."
        ),
        "projected_metric_impacts": [
            {
                "metric_key": "soil_organic_carbon_pct",
                "metric_name": "Stable Soil Organic Carbon",
                "projected_delta_min": 30.0,
                "projected_delta_max": 55.0,
                "unit": "%",
                "time_horizon": "1-3 years",
                "causal_mechanism": "Direct addition of aromatic carbon rings plus organo-mineral sorption stabilization"
            },
            {
                "metric_key": "soil_moisture_pct",
                "metric_name": "Volumetric Moisture Retention",
                "projected_delta_min": 18.0,
                "projected_delta_max": 32.0,
                "unit": "%",
                "time_horizon": "1-2 years",
                "causal_mechanism": "Micro-porous capillary water storage within pyrolyzed carbon skeleton"
            }
        ],
        "trade_offs_and_risks": [
            "Biochar must be biologically charged (co-composted); applying raw unconditioned biochar can bind available soil nitrogen temporarily.",
            "Sourcing and transportation costs can be high without localized pyrolysis equipment."
        ],
        "evidence_chunk_ids": ["GCB-BIOCHAR-2018-C1", "RODALE-FST-2020-C1"]
    },
    {
        "intervention_id": "INT-POLLINATOR-HEDGEROWS",
        "title": "Native Flowering Hedgerows & Ecological Buffer Strips",
        "category": "Landscape Connectivity & Conservation Biocontrol",
        "time_horizon": "Short to Medium-Term (12-24 months)",
        "preconditions": {
            "compatible_climates": ["semi_arid", "temperate", "tropical", "dry_sub_humid"],
            "compatible_land_use": ["monoculture_cropland", "intensive_tillage_cropland", "degraded_pasture"]
        },
        "prohibited_conditions": {},
        "target_variables_addressed": [
            "pollinator_density_index",
            "shannon_diversity_index",
            "pesticide_passes_yr"
        ],
        "what_to_do": (
            "Plant 4-6 meter wide perennial hedgerow strips along field boundaries, drainage ditches, and non-arable margins. "
            "Utilize a 70/30 mix of native flowering dicot perennials (providing continuous blooming from spring through autumn) "
            "and native tussock bunchgrasses to provide undisturbed ground-nesting substrates."
        ),
        "why_it_works": (
            "Field perimeters provide permanent floral nectar resources outside of crop flowering intervals and shelter wild solitary bees, "
            "bumblebees, and hoverflies. Simultaneously, hedgerows host parasitic micro-hymenopteran wasps and predatory ground beetles (Carabidae) "
            "that disperse 50-100 meters into adjacent crop fields, actively preying upon cereal aphids and lepidopteran larvae."
        ),
        "projected_metric_impacts": [
            {
                "metric_key": "pollinator_density_index",
                "metric_name": "Wild Pollinator Density",
                "projected_delta_min": 70.0,
                "projected_delta_max": 120.0,
                "unit": "%",
                "time_horizon": "1-2 years",
                "causal_mechanism": "Continuous nectar/pollen resource phenology and ground-nesting habitat protection"
            },
            {
                "metric_key": "pesticide_passes_yr",
                "metric_name": "Chemical Insecticide Spray Frequency",
                "projected_delta_min": -30.0,
                "projected_delta_max": -50.0,
                "unit": "%",
                "time_horizon": "2-3 years",
                "causal_mechanism": "Biological top-down pest suppression by natural predator arthropods"
            },
            {
                "metric_key": "shannon_diversity_index",
                "metric_name": "Macro-invertebrate Shannon Diversity",
                "projected_delta_min": 40.0,
                "projected_delta_max": 75.0,
                "unit": "%",
                "time_horizon": "18-24 months",
                "causal_mechanism": "Reconnection of fragmented agricultural landscape patches into wildlife corridors"
            }
        ],
        "trade_offs_and_risks": [
            "Converts 3-5% of peripheral land area from arable production to conservation buffer.",
            "Requires weed rogueing during initial 12-month establishment phase until native cover closes canopy."
        ],
        "evidence_chunk_ids": ["IPBES-GLOBAL-2019-C1", "AEE-HEDGEROW-2021-C1", "IPBES-POLLINATORS-2016-C1"]
    },
    {
        "intervention_id": "INT-ROTATIONAL-GRAZING",
        "title": "Adaptive Multi-Paddock (AMP) Rotational Grazing & Pasture Recovery",
        "category": "Restorative Rangeland Ecology",
        "time_horizon": "Medium-Term (2-4 years)",
        "preconditions": {
            "compatible_land_use": ["degraded_pasture", "rotational_pasture"],
            "compatible_climates": ["semi_arid", "arid", "temperate", "tropical", "dry_sub_humid"]
        },
        "prohibited_conditions": {
            "compatible_land_use": ["monoculture_cropland"]
        },
        "target_variables_addressed": [
            "vegetative_ground_cover_pct",
            "soil_organic_carbon_pct",
            "shannon_diversity_index"
        ],
        "what_to_do": (
            "Subdivide continuous pasture into smaller paddocks using portable solar electric fencing. Graze livestock at high "
            "stocking density for short durations (1-3 days), followed by extended pasture rest intervals (60-120 days) until "
            "perennial grasses reach full physiological vegetative recovery."
        ),
        "why_it_works": (
            "Brief animal impact tramples unpalatable senescent biomass onto the ground, forming a moisture-retaining organic litter layer. "
            "Extended rest periods allow perennial forage roots to penetrate deep into subsoils, pulsing carbon exudates into the rhizosphere "
            "and breaking pest/parasite life cycles while native seed banks germinate during recovery periods."
        ),
        "projected_metric_impacts": [
            {
                "metric_key": "vegetative_ground_cover_pct",
                "metric_name": "Basal Ground Cover",
                "projected_delta_min": 35.0,
                "projected_delta_max": 65.0,
                "unit": "%",
                "time_horizon": "18-36 months",
                "causal_mechanism": "Spontaneous regeneration of perennial bunchgrasses from stimulated root crowns"
            },
            {
                "metric_key": "soil_organic_carbon_pct",
                "metric_name": "Soil Organic Carbon",
                "projected_delta_min": 20.0,
                "projected_delta_max": 40.0,
                "unit": "%",
                "time_horizon": "2-4 years",
                "causal_mechanism": "Deep root turnover and incorporation of trampled litter into topsoil horizons"
            }
        ],
        "trade_offs_and_risks": [
            "Requires investment in mobile water distribution troughs and solar energizer fencing.",
            "Requires active stockmanship and regular forage monitoring rather than passive continuous grazing."
        ],
        "evidence_chunk_ids": ["IUCN-NBS-2021-C1", "FAO-GSP-2020-C1"]
    }
]


def get_intervention_by_id(intervention_id: str) -> Optional[Dict[str, Any]]:
    for item in INTERVENTION_GRAPH:
        if item["intervention_id"] == intervention_id:
            return item
    return None
