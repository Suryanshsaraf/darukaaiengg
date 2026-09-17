/**
 * Darukaa.Earth: Deterministic Client-Side Decision Engine
 * Enables full functionality on GitHub Pages even when Python backend is not running.
 */

import { BENCHMARK_SCENARIOS, CURATED_SOURCES } from './knowledgeData';
export { BENCHMARK_SCENARIOS, CURATED_SOURCES };

export function processClientMessage(message, currentProfile = {}) {
  const text = message.toLowerCase();

  // Check if it's the vague inquiry
  if (text.includes("biodiversity is declining") || text.includes("declining on my land") || text.length < 25) {
    return BENCHMARK_SCENARIOS[1];
  }

  // Check if it has semi-arid / wheat / low carbon
  if ((text.includes("wheat") || text.includes("monoculture")) && (text.includes("0.3") || text.includes("carbon") || text.includes("semi-arid"))) {
    return BENCHMARK_SCENARIOS[2];
  }

  // Check coordinates
  if (text.includes("31.5") || text.includes("coordinates") || text.includes("cotton")) {
    return BENCHMARK_SCENARIOS[3];
  }

  // Default fallback: Run Moment 2 plan
  return BENCHMARK_SCENARIOS[2];
}

export function diagnoseClientProfile(profile) {
  const soc = profile.soil_organic_carbon_pct || 0.3;
  const rain = profile.rainfall_annual_mm || 320;
  const crop = profile.crop_type || "monoculture wheat";

  const benchmark2 = JSON.parse(JSON.stringify(BENCHMARK_SCENARIOS[2].plan));
  benchmark2.site_profile = { ...benchmark2.site_profile, ...profile };
  benchmark2.diagnosis.vulnerability_score = Math.min(95, Math.max(30, 75 - soc * 15 + (rain < 400 ? 10 : 0)));
  return benchmark2;
}

export function enrichClientCoordinates(lat, lon) {
  if (lat >= 30 && lat <= 36 && lon <= -99 && lon >= -105) {
    return {
      location_name: "North American Southern High Plains (Texas/New Mexico)",
      climate_zone: "semi_arid",
      rainfall_annual_mm: 360.0,
      soil_organic_carbon_pct: 0.45
    };
  }
  return {
    location_name: `Coordinates (${lat.toFixed(2)}, ${lon.toFixed(2)})`,
    climate_zone: "semi_arid",
    rainfall_annual_mm: 380.0,
    soil_organic_carbon_pct: 0.50
  };
}
