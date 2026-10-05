from fastapi import APIRouter
from pydantic import BaseModel
from engine.baseline_calc import calculate_ide, evaluate_mopec_compliance, estimate_thermal_breakdown

router = APIRouter()

class PoolBaselineConfig(BaseModel):
    commune_name: str
    typology: str
    surface_eau_m2: float
    volume_eau_m3: float
    annee_construction: int
    consommation_thermique_kwh: float
    consommation_electrique_kwh: float
    production_chaleur: str
    cta_age: int = 0
    cta_recuperation: bool = False
    filtres_age: int = 0
    pompes_vfd: bool = False

@router.post("/baseline")
def register_baseline(config: PoolBaselineConfig):
    # 1. Calcul de l'IDE global
    total_energy = config.consommation_thermique_kwh + config.consommation_electrique_kwh
    ide = calculate_ide(total_energy, config.surface_eau_m2)

    # 2. Validation centralisée MoPEC
    mopec_status = evaluate_mopec_compliance(config.typology, config.production_chaleur)

    # 3. Ventilation thermodynamique (SIA 385/9)
    breakdown = estimate_thermal_breakdown(config.consommation_thermique_kwh, config.typology)

    return {
        "status": "success",
        "ide_calcul_kwh_m2": round(ide, 2),
        "ofen_target_status": "Dépassement" if ide > 240 else "Conforme",
        "mopec_compliance": mopec_status,
        "thermal_breakdown": breakdown
    }