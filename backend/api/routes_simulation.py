from fastapi import APIRouter
from pydantic import BaseModel
from engine.physics_models.evaporation_model import calculate_evaporation_loss
from engine.lca_calculator import calculate_carbon_roi
from engine.finance_calculator import calculate_measure_financials

router = APIRouter()


class MultiVariantInput(BaseModel):
    area_m2: float
    t_water: float
    t_air: float
    rh_air: float
    wind_speed: float
    current_energy: str = "gaz"

    # 1. Leviers Passifs
    apply_cover: bool = False
    apply_isolation: bool = False

    # 2. Leviers Opérationnels
    apply_mcr_night_setback: bool = False
    apply_vfd_pumps: bool = False

    # 3. Leviers Actifs
    heating_system: str = "aucun"  # "pac", "cad", "solaire"
    apply_cta_recovery: bool = False


@router.post("/simulate")
def run_simulation(data: MultiVariantInput):
    # Baseline énergétique annuelle estimée (simplifiée 8760h)
    q_loss_base_kw = calculate_evaporation_loss(data.t_water, data.t_air, data.rh_air, data.wind_speed, data.area_m2,
                                                False)
    baseline_energy_kwh = q_loss_base_kw * 8760

    # Simulation de l'état modifié
    t_water_sim = data.t_water
    if data.apply_mcr_night_setback:
        t_water_sim -= 1.0  # Abaissement de 1°C

    q_loss_sim_kw = calculate_evaporation_loss(
        t_water_sim, data.t_air, data.rh_air, data.wind_speed, data.area_m2,
        is_covered=data.apply_cover
    )

    simulated_energy_kwh = q_loss_sim_kw * 8760

    # Bonus d'économie si isolation ou récupération CTA activées
    if data.apply_isolation:
        simulated_energy_kwh *= 0.90  # -10% de pertes par conduction
    if data.apply_cta_recovery:
        simulated_energy_kwh *= 0.85  # -15% sur la charge thermique globale

    energy_saved_kwh = max(0, baseline_energy_kwh - simulated_energy_kwh)

    measures_evaluation = []

    # Évaluation des mesures sélectionnées pour le rapport
    if data.apply_cover:
        finances = calculate_measure_financials("bache_thermique", data.area_m2, energy_saved_kwh * 0.6,
                                                data.current_energy)
        trc = calculate_carbon_roi(energy_saved_kwh * 0.6, "bache_thermique", data.area_m2)
        measures_evaluation.append({
            "category": "Passif",
            "name": "Bâche Thermique Nocturne",
            "capex_chf": finances["capex_chf"],
            "savings_chf_year": finances["yearly_savings_chf"],
            "tri_years": finances["tri_years"],
            "trc_years": round(trc, 2)
        })

    if data.apply_isolation:
        finances = calculate_measure_financials("isolation_cuve", data.area_m2, energy_saved_kwh * 0.1,
                                                data.current_energy)
        measures_evaluation.append({
            "category": "Passif",
            "name": "Isolation / Cuvelage",
            "capex_chf": finances["capex_chf"],
            "savings_chf_year": finances["yearly_savings_chf"],
            "tri_years": finances["tri_years"],
            "trc_years": 3.5
        })

    if data.apply_mcr_night_setback:
        finances = calculate_measure_financials("optimisation_mcr", 1, energy_saved_kwh * 0.15, data.current_energy)
        measures_evaluation.append({
            "category": "Opérationnel",
            "name": "Optimisation MCR & Abaissement Nocturne",
            "capex_chf": finances["capex_chf"],
            "savings_chf_year": finances["yearly_savings_chf"],
            "tri_years": finances["tri_years"],
            "trc_years": 0.0
        })

    if data.apply_vfd_pumps:
        finances = calculate_measure_financials("variation_frequence", 1, 15000, data.current_energy)  # gain électrique
        measures_evaluation.append({
            "category": "Opérationnel",
            "name": "Variateurs de Fréquence (Pompes VFD)",
            "capex_chf": finances["capex_chf"],
            "savings_chf_year": finances["yearly_savings_chf"],
            "tri_years": finances["tri_years"],
            "trc_years": 0.5
        })

    if data.heating_system == "cad":
        finances = calculate_measure_financials("raccordement_cad", 1, energy_saved_kwh, data.current_energy)
        measures_evaluation.append({
            "category": "Actif",
            "name": "Raccordement Chauffage à Distance (CAD)",
            "capex_chf": finances["capex_chf"],
            "savings_chf_year": finances["yearly_savings_chf"],
            "tri_years": finances["tri_years"],
            "trc_years": 1.2
        })
    elif data.heating_system == "pac":
        finances = calculate_measure_financials("pac_geothermique", 200, energy_saved_kwh, data.current_energy)
        measures_evaluation.append({
            "category": "Actif",
            "name": "Pompe à Chaleur (PAC) Géothermique",
            "capex_chf": finances["capex_chf"],
            "savings_chf_year": finances["yearly_savings_chf"],
            "tri_years": finances["tri_years"],
            "trc_years": 2.0
        })

    if data.apply_cta_recovery:
        finances = calculate_measure_financials("recuperation_cta", 1, energy_saved_kwh * 0.2, data.current_energy)
        measures_evaluation.append({
            "category": "Actif",
            "name": "Récupération de Chaleur CTA (Double Flux)",
            "capex_chf": finances["capex_chf"],
            "savings_chf_year": finances["yearly_savings_chf"],
            "tri_years": finances["tri_years"],
            "trc_years": 1.0
        })

    mopec_compliant = data.apply_cover and (data.heating_system in ["cad", "pac"] or data.current_energy == "cad")

    return {
        "status": "success",
        "thermal_loss_kw": round(q_loss_sim_kw, 2),
        "energy_saved_kwh": round(energy_saved_kwh, 0),
        "mopec_compliant": mopec_compliant,
        "measures_evaluation": measures_evaluation
    }