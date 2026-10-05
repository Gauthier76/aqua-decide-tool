# ==================================================
# FILE: backend\api\routes_export.py
# ==================================================

from fastapi import APIRouter
from fastapi.responses import JSONResponse
import datetime

router = APIRouter()


@router.post("/export/roadmap")
def export_roadmap(data: dict):
    """
    Génère une feuille de route exportable pour la commune.
    Dans une version de production, ceci pourrait générer un PDF avec reportlab.
    """
    report = {
        "title": "Feuille de Route - Optimisation Énergétique (MoPEC)",
        "date_generated": datetime.datetime.now().isoformat(),
        "baseline_ide": data.get("baseline_ide", 0),
        "target_ide": data.get("target_ide", 0),
        "recommended_measures": data.get("measures", []),
        "financial_summary": {
            "total_capex_chf": data.get("capex", 0),
            "yearly_savings_chf": data.get("savings", 0)
        }
    }

    return JSONResponse(content={"status": "success", "report": report})