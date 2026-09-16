"""
Darukaa.Earth: CLI Scientific Interface
Command-line decision runner for terminal verification and automated evaluation.
Usage:
    python run_cli.py --benchmark 1
    python run_cli.py --benchmark 2
    python run_cli.py --benchmark 3
    python run_cli.py --query "Soil organic carbon: 0.3%, Rainfall: low, Crop: monoculture wheat"
"""

import argparse
import json
import sys
from conversation.session import ConversationSession
from core.models import SiteProfile
from reasoning.engine import EcologicalReasoningEngine


def run_benchmark(benchmark_id: int):
    session = ConversationSession()
    print("=" * 80)
    print(f"DARUKAA.EARTH: RUNNING BENCHMARK SCENARIO {benchmark_id}")
    print("=" * 80)

    if benchmark_id == 1:
        prompt = "Biodiversity is declining on my land"
        print(f"USER QUERY: \"{prompt}\"\n")
        res = session.process_user_message(prompt)
        print(f"STATUS: {res['type'].upper()}")
        print(f"ASSISTANT RESPONSE:\n{res['assistant_message']}\n")
        print("MISSING CRITICAL VARIABLES DETECTED:")
        for v in res["clarification"]["missing_critical_variables"]:
            print(f"  - {v}")

    elif benchmark_id == 2:
        prompt = "Soil organic carbon: 0.3%, Rainfall: low, Crop: monoculture wheat, Region: semi-arid"
        print(f"USER QUERY: \"{prompt}\"\n")
        res = session.process_user_message(prompt)
        print(f"STATUS: {res['type'].upper()}\n")
        plan = res["plan"]
        diag = plan["diagnosis"]
        print(f"DIAGNOSIS PATHWAY: {diag['primary_degradation_pathway']}")
        print(f"INTERACTING VARIABLES ({diag['interacting_variables_count']}): {', '.join(diag['interacting_variables'])}")
        print(f"VULNERABILITY SCORE: {diag['vulnerability_score']}/100\n")
        print("RECOMMENDED INTERVENTIONS:")
        for i, rec in enumerate(plan["recommendations"], 1):
            print(f"\n[{i}] {rec['title']} ({rec['time_horizon']})")
            print(f"    Confidence: {rec['confidence']['tier']} ({int(rec['confidence']['score']*100)}%) — {rec['confidence']['rationale']}")
            print(f"    What To Do: {rec['what_to_do'][:140]}...")
            print(f"    Why It Works: {rec['why_it_works'][:140]}...")
            print("    Impacted Metrics:")
            for m in rec["impacted_metrics"]:
                print(f"      * {m['metric_name']}: {m['projected_delta_range']} ({m['time_horizon']})")
            print("    Verified Citations:")
            for c in rec["citations"]:
                print(f"      * {c['authors']} ({c['year']}) - {c['title']}. DOI: {c['doi_or_url']}")

    elif benchmark_id == 3:
        profile = SiteProfile(
            coordinates=(31.5, -102.3),
            soil_organic_carbon_pct=0.45,
            soil_bulk_density=1.52,
            land_use_type="monoculture_cropland",
            crop_type="monoculture cotton",
            tillage_practice="conventional_deep",
            rainfall_annual_mm=360.0
        )
        print(f"INPUT STRUCTURED PROFILE: Coordinates (31.5, -102.3), SOC: 0.45%, BD: 1.52 g/cm³, Cotton Monoculture\n")
        engine = EcologicalReasoningEngine()
        plan = engine.process_site_profile(profile)
        print(f"DIAGNOSIS: {plan.diagnosis.primary_degradation_pathway}")
        print(f"INTERACTING VARIABLES ({len(plan.diagnosis.interacting_variables)}): {', '.join(plan.diagnosis.interacting_variables)}")
        print(f"VULNERABILITY SCORE: {plan.diagnosis.vulnerability_score}/100\n")
        print(f"RETRIEVAL TRACE: Evaluated {plan.retrieval_trace.candidate_chunks_evaluated} candidates, returned {plan.retrieval_trace.chunks_returned_count} passages in {plan.retrieval_trace.execution_time_ms:.1f}ms")
        for chunk in plan.retrieval_trace.chunks:
            print(f"  - [{chunk['chunk_id']}] {chunk['source_title']} (Composite Score: {chunk['scores']['composite_relevance']:.3f})")

    print("\n" + "=" * 80)


def main():
    parser = argparse.ArgumentParser(description="Darukaa.Earth Ecological Decision Engine CLI")
    parser.add_argument("--benchmark", type=int, choices=[1, 2, 3], help="Run benchmark scenario 1, 2, or 3")
    parser.add_argument("--query", type=str, help="Process natural language or structured query")
    parser.add_argument("--json", action="store_true", help="Output full response as JSON")
    args = parser.parse_args()

    if args.benchmark:
        run_benchmark(args.benchmark)
    elif args.query:
        session = ConversationSession()
        res = session.process_user_message(args.query)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print(res["assistant_message"])
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
