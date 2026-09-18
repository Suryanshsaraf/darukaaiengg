"""
Darukaa.Earth: Conversational Intelligence & Multi-Turn Session State Machine
Maintains conversational context, accumulates environmental profile across turns,
detects missing critical variables, and triggers targeted clarifying questions.
"""

from typing import List, Dict, Any, Optional, Tuple, Union
import uuid

from core.models import SiteProfile, ClarificationPrompt, VerifiedResponsePlan
from .extractor import EcologicalEntityExtractor
from .spatial import SpatialEnrichmentService
from reasoning.engine import EcologicalReasoningEngine


class ConversationSession:
    """
    Stateful conversational agent managing multi-turn dialogue.
    Enforces the diagnostic gate: prompts for missing decision-critical variables
    before executing full scientific synthesis.
    """

    def __init__(self, session_id: Optional[str] = None):
        self.session_id = session_id or str(uuid.uuid4())[:8]
        self.profile = SiteProfile(session_id=self.session_id)
        self.history: List[Dict[str, Any]] = []
        self.reasoning_engine = EcologicalReasoningEngine()

    def process_user_message(self, message: str) -> Dict[str, Any]:
        """
        Process incoming user message.
        Returns either a 'clarification' or a 'verified_plan' response.
        """
        self.history.append({"role": "user", "content": message})

        # Check what variables are present in this specific message
        fresh_profile = EcologicalEntityExtractor.extract_from_text(message)
        extracted_vars = fresh_profile.get_critical_variables()

        msg_lower = message.lower().strip()
        vague_keywords = [
            "biodiversity", "declining", "falling", "dropping", "decreasing",
            "loss", "lost", "degraded", "degradation", "dying", "failing",
            "poor", "bad", "damage", "problem", "decline"
        ]
        has_vague_symptom = any(k in msg_lower for k in vague_keywords)

        # Check if the session previously finalized a verified plan
        previous_had_plan = any(h.get("type") == "verified_plan" for h in self.history[:-1])

        # If a previous plan was finalized and the new message does not independently have >= 3 variables,
        # or if the message is an explicit vague problem statement with 0 variables:
        if (previous_had_plan and len(extracted_vars) < 3) or (len(extracted_vars) == 0 and has_vague_symptom):
            # Reset profile for the new inquiry so previous site metrics are not hallucinated/reused
            self.profile = fresh_profile
            self.profile.session_id = self.session_id
        else:
            # Multi-turn clarification continuation: incrementally merge into accumulated profile
            self.profile = EcologicalEntityExtractor.extract_from_text(message, self.profile)

        # 2. Enrich if coordinates exist
        if self.profile.coordinates and not self.profile.enriched_spatially:
            self.profile = SpatialEnrichmentService.enrich_profile(self.profile)

        # 3. Check sufficiency gate (requires >= 3 interacting environmental dimensions)
        present_vars = self.profile.get_critical_variables()
        present_dims = self.profile.get_represented_dimensions()

        if not self.profile.is_sufficient_for_diagnosis():
            # Generate targeted clarifying question
            clarification = self._generate_clarification(present_vars)
            response_payload = {
                "type": "clarification",
                "session_id": self.session_id,
                "current_profile": self.profile.to_dict(),
                "variables_found": list(present_vars.keys()),
                "dimensions_found": list(present_dims.keys()),
                "missing_count": max(1, 3 - len(present_dims)),
                "clarification": clarification.to_dict(),
                "assistant_message": clarification.clarification_question
            }
            self.history.append({
                "role": "assistant",
                "type": "clarification",
                "content": clarification.clarification_question,
                "data": response_payload
            })
            return response_payload

        # 4. Input is complete (>= 3 variables): Run full scientific decision engine
        plan = self.reasoning_engine.process_site_profile(self.profile)
        response_payload = {
            "type": "verified_plan",
            "session_id": self.session_id,
            "current_profile": self.profile.to_dict(),
            "variables_evaluated": list(present_vars.keys()),
            "plan": plan.to_dict(),
            "assistant_message": self._format_plan_summary(plan)
        }
        self.history.append({
            "role": "assistant",
            "type": "verified_plan",
            "content": response_payload["assistant_message"],
            "data": response_payload
        })
        return response_payload

    def _generate_clarification(self, present_vars: Dict[str, Any]) -> ClarificationPrompt:
        """
        Identify the most decision-changing missing variables and generate
        a natural, targeted question.
        Example from Hackathon Brief:
        User: "Biodiversity is declining on my land"
        System: "Can you provide soil organic carbon %, rainfall pattern, and land use type?"
        """
        missing_candidates = []
        
        # Priority order of decision-critical variables
        check_list = [
            ("soil_organic_carbon_pct", "soil organic carbon % (SOC)"),
            ("rainfall_annual_mm", "annual rainfall or rainfall pattern"),
            ("land_use_type", "land use or crop type"),
            ("soil_ph", "soil pH"),
            ("soil_bulk_density", "soil bulk density or tillage practice"),
            ("canopy_cover_pct", "canopy cover % or buffer presence")
        ]

        for key, display in check_list:
            if key not in present_vars and (key != "land_use_type" or "crop_type" not in present_vars):
                missing_candidates.append((key, display))

        needed = missing_candidates[:3]
        needed_keys = [k for k, _ in needed]
        needed_labels = [lbl for _, lbl in needed]

        if len(needed_labels) == 3:
            question = f"To diagnose your site scientifically and formulate an evidence-backed intervention, can you provide {needed_labels[0]}, {needed_labels[1]}, and {needed_labels[2]}?"
        elif len(needed_labels) == 2:
            question = f"To complete the multi-variable diagnosis, could you specify {needed_labels[0]} and {needed_labels[1]}?"
        else:
            question = f"We need one additional metric to pass the causal diagnostic threshold: could you provide {needed_labels[0]}?"

        quick_options = [
            {
                "label": "Benchmark 1: Semi-Arid Monoculture Wheat",
                "text": "Soil organic carbon: 0.3%, Rainfall: low (320mm), Crop: monoculture wheat, Region: semi-arid"
            },
            {
                "label": "Benchmark 2: Degraded Pasture Compaction",
                "text": "Degraded pasture, Soil organic carbon: 0.6%, Bulk density: 1.55 g/cm³, Rainfall: 450mm"
            },
            {
                "label": "Benchmark 3: High-Tillage Intensive Cropland",
                "text": "Conventional deep tillage, Soil pH: 5.8, SOC: 0.8%, Pesticide passes: 4 per year"
            }
        ]

        return ClarificationPrompt(
            is_clarification_needed=True,
            reason=f"System requires at least 3 interacting environmental variables to prevent shallow recommendations. Currently have {len(present_vars)}.",
            missing_critical_variables=needed_keys,
            clarification_question=question,
            suggested_quick_options=quick_options
        )

    def _format_plan_summary(self, plan: VerifiedResponsePlan) -> str:
        diag = plan.diagnosis
        recs = plan.recommendations
        summary_lines = [
            f"**Ecological Diagnosis: {diag.primary_degradation_pathway}**",
            f"*Evaluated interacting variables ({len(diag.interacting_variables)}):* {', '.join(diag.interacting_variables)}",
            f"*Vulnerability Score:* **{diag.vulnerability_score:.1f}/100**",
            "",
            f"**Scientific Causal Analysis:** {diag.compound_risk_analysis}",
            "",
            "### Evidence-Backed Recommended Interventions:",
        ]

        for i, r in enumerate(recs, 1):
            cites = ", ".join([f"{c.authors} ({c.year})" for c in r.citations[:2]])
            deltas = ", ".join([f"{m.metric_name}: {m.projected_delta_min:+.1f}% to {m.projected_delta_max:+.1f}%" for m in r.impacted_metrics[:2]])
            summary_lines.append(
                f"**{i}. {r.title}** ({r.time_horizon})\n"
                f"- **What to do:** {r.what_to_do}\n"
                f"- **Why it works (Science):** {r.why_it_works}\n"
                f"- **Impacted Metrics:** {deltas}\n"
                f"- **Confidence:** {r.confidence_tier} ({r.confidence_score*100:.0f}%) — {r.confidence_rationale}\n"
                f"- **Citations:** {cites} ([DOI/Link]({r.citations[0].doi_or_url}))\n"
            )

        return "\n".join(summary_lines)

    def reset(self):
        """Reset session state for a fresh dialogue."""
        self.profile = SiteProfile(session_id=self.session_id)
        self.history.clear()
