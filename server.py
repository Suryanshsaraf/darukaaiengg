"""
Darukaa.Earth: High-Performance REST API & Full-Stack Web Server
Powers the React Frontend with endpoints for chat dialogue, multi-metric causal diagnosis,
spatial geo-enrichment, hybrid retrieval traces, and benchmark scenarios.
"""

import os
import json
from typing import Dict, Any, Optional

from starlette.applications import Starlette
from starlette.responses import JSONResponse, FileResponse, HTMLResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import uvicorn

from core.models import SiteProfile
from conversation.session import ConversationSession
from conversation.spatial import SpatialEnrichmentService
from reasoning.engine import EcologicalReasoningEngine
from knowledge.sources_data import CURATED_SOURCES


# Global session registry
SESSION_REGISTRY: Dict[str, ConversationSession] = {}
ENGINE = EcologicalReasoningEngine()


def get_session(session_id: Optional[str] = None) -> ConversationSession:
    sid = session_id or "default"
    if sid not in SESSION_REGISTRY:
        SESSION_REGISTRY[sid] = ConversationSession(session_id=sid)
    return SESSION_REGISTRY[sid]


async def api_chat(request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    message = body.get("message", "").strip()
    session_id = body.get("session_id", "default")

    if not message:
        return JSONResponse({"error": "Message cannot be empty"}, status_code=400)

    session = get_session(session_id)
    response = session.process_user_message(message)
    return JSONResponse(response)


async def api_diagnose(request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    profile = SiteProfile()
    for k, v in body.items():
        if hasattr(profile, k) and v is not None:
            if k == "coordinates" and isinstance(v, (list, tuple)) and len(v) == 2:
                setattr(profile, k, (float(v[0]), float(v[1])))
            else:
                setattr(profile, k, v)

    # Check sufficiency gate (>= 3 variables)
    if not profile.is_sufficient_for_diagnosis():
        present = list(profile.get_critical_variables().keys())
        return JSONResponse({
            "error": "Diagnosis gate failed: System requires at least 3 interacting environmental variables.",
            "variables_present": present,
            "missing_count": 3 - len(present)
        }, status_code=422)

    plan = ENGINE.process_site_profile(profile)
    return JSONResponse(plan.to_dict())


async def api_enrich(request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    lat = float(body.get("latitude", 0.0))
    lon = float(body.get("longitude", 0.0))

    profile = SiteProfile(coordinates=(lat, lon))
    enriched = SpatialEnrichmentService.enrich_profile(profile)
    return JSONResponse(enriched.to_dict())


async def api_benchmark(request):
    b_id = int(request.path_params["id"])
    session = ConversationSession(session_id=f"bench_{b_id}")

    if b_id == 1:
        prompt = "Biodiversity is declining on my land"
        res = session.process_user_message(prompt)
        res["prompt"] = prompt
        return JSONResponse(res)

    elif b_id == 2:
        prompt = "Soil organic carbon: 0.3%, Rainfall: low (320mm), Crop: monoculture wheat, Region: semi-arid"
        res = session.process_user_message(prompt)
        res["prompt"] = prompt
        return JSONResponse(res)

    elif b_id == 3:
        profile = SiteProfile(
            coordinates=(31.5, -102.3),
            soil_organic_carbon_pct=0.45,
            soil_bulk_density=1.52,
            land_use_type="monoculture_cropland",
            crop_type="monoculture cotton",
            tillage_practice="conventional_deep",
            rainfall_annual_mm=360.0
        )
        plan = ENGINE.process_site_profile(profile)
        return JSONResponse({
            "type": "verified_plan",
            "prompt": "Coordinates (31.5, -102.3), SOC: 0.45%, BD: 1.52 g/cm³, Cotton Monoculture",
            "plan": plan.to_dict(),
            "assistant_message": session._format_plan_summary(plan)
        })

    return JSONResponse({"error": "Unknown benchmark ID"}, status_code=404)


async def api_sources(request):
    return JSONResponse(CURATED_SOURCES)


async def api_health(request):
    return JSONResponse({
        "status": "healthy",
        "system": "Darukaa.Earth AI Biodiversity Intelligence Decision System",
        "version": "1.0.0",
        "acceptance_gates": "ACTIVE (>= 3 variables, verified citations)"
    })


async def api_download_docx(request):
    doc_path = os.path.join(os.path.dirname(__file__), "Darukaa_Earth_Biodiversity_Intelligence_Submission.docx")
    if os.path.exists(doc_path):
        return FileResponse(
            doc_path,
            filename="Darukaa_Earth_Biodiversity_Intelligence_Submission.docx",
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    return JSONResponse({"error": "Submission document not found"}, status_code=404)


# Frontend static files serving
routes = [
    Route("/api/health", api_health, methods=["GET"]),
    Route("/api/chat", api_chat, methods=["POST"]),
    Route("/api/diagnose", api_diagnose, methods=["POST"]),
    Route("/api/enrich", api_enrich, methods=["POST"]),
    Route("/api/benchmarks/{id:int}", api_benchmark, methods=["GET"]),
    Route("/api/sources", api_sources, methods=["GET"]),
    Route("/api/download-docx", api_download_docx, methods=["GET"]),
]

frontend_dist = os.path.join(os.path.dirname(__file__), "frontend", "dist")

if os.path.exists(frontend_dist):
    routes.append(Mount("/", app=StaticFiles(directory=frontend_dist, html=True), name="static"))
else:
    async def index_fallback(request):
        return HTMLResponse(
            "<html><body style='font-family:sans-serif;text-align:center;padding:50px;background:#0f172a;color:#f8fafc;'>"
            "<h1>🌱 Darukaa.Earth API Active</h1>"
            "<p>React frontend is building or running via Vite on port 5173.</p>"
            "<p><a href='http://localhost:5173' style='color:#10b981;font-weight:bold;'>Open React App (Vite)</a></p>"
            "</body></html>"
        )
    routes.append(Route("/", index_fallback, methods=["GET"]))


middleware = [
    Middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
]

app = Starlette(debug=True, routes=routes, middleware=middleware)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"Starting Darukaa.Earth Server on http://localhost:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
