def calculate_ide(total_energy_kwh: float, pool_area_m2: float) -> float:
    """Calcule l'Indice de Dépense Énergétique (IDE) en kWh/m2/an."""
    if pool_area_m2 <= 0:
        raise ValueError("La surface du bassin doit être supérieure à 0.")
    return total_energy_kwh / pool_area_m2


def evaluate_mopec_compliance(typology: str, production_chaleur: str) -> dict:
    """
    Évalue la conformité de l'état initial par rapport au MoPEC et aux lois cantonales (ex: LVLEne).
    """
    compliance = {
        "is_compliant": True,
        "warnings": []
    }

    fossiles = ["gaz", "mazout"]

    # Règle stricte pour le plein air : 100% renouvelable
    if typology == "extérieure" and production_chaleur in fossiles:
        compliance["is_compliant"] = False
        compliance["warnings"].append(
            "Non-conformité MoPEC : Les piscines extérieures ne peuvent être chauffées aux énergies fossiles."
        )

    # Règle pour l'intérieur : 50% renouvelable / récupération
    if typology in ["intérieure", "mixte"] and production_chaleur in fossiles:
        compliance["warnings"].append(
            "Alerte MoPEC : Les piscines couvertes exigent 50% de couverture par les EnR ou rejets thermiques."
        )

    # Étant dans l'état initial (Baseline), on signale l'absence de bâche
    compliance["is_compliant"] = False
    compliance["warnings"].append(
        "Absence de couverture thermique nocturne (exigence minimale pour limiter l'évaporation).")

    return compliance


def estimate_thermal_breakdown(conso_thermique_kwh: float, typology: str) -> dict:
    """
    Ventile la facture thermique annuelle selon des ratios physiques moyens
    basés sur la norme SIA 385/9 et notre état de l'art (HEIG-VD).
    """
    # En l'absence de modélisation horaire pour la Baseline, nous utilisons
    # des clefs de répartition macroscopiques reconnues pour l'audit.
    if typology == "extérieure":
        # Le vent et l'air libre favorisent massivement l'évaporation
        evap = conso_thermique_kwh * 0.60
        conv_rad = conso_thermique_kwh * 0.30
        eau = conso_thermique_kwh * 0.10  # Chauffage de l'eau de renouvellement (hygiène)
    else:
        # En intérieur, la déshumidification et la CTA modifient l'équilibre
        evap = conso_thermique_kwh * 0.50
        conv_rad = conso_thermique_kwh * 0.15
        eau = conso_thermique_kwh * 0.35  # Inclut l'air neuf de la CTA et l'eau

    return {
        "evaporation_kwh": evap,
        "convection_radiation_kwh": conv_rad,
        "renouvellement_kwh": eau
    }