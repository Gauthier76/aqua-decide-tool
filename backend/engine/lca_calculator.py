# Base de données KBOB simplifiée (kg CO2-eq / unité) - Données Suisses
KBOB_DB = {
    # Énergie Grise (Matériaux et Installations)
    "bache_thermique": 2.1,  # kg CO2-eq / m2
    "isolation_cuve": 15.5,  # kg CO2-eq / m2 (ex: XPS + étanchéité)
    "pac_geothermique": 250.0,  # kg CO2-eq / kW (Forage + Machine)
    "raccordement_cad": 1500.0,  # kg CO2-eq forfaitaire (Sous-station)
    "variation_frequence": 120.0,  # kg CO2-eq (Électronique de puissance)
    "recuperation_cta": 800.0,  # kg CO2-eq (Échangeur à plaques / rotatif)
    "optimisation_mcr": 0.0,  # Pur logiciel (Dette carbone nulle)

    # Facteurs d'émissions (Exploitation)
    "mix_electrique_ch": 0.029,  # kg CO2-eq / kWh (Mix de consommation CH)
    "gaz_naturel": 0.228,  # kg CO2-eq / kWh (PCI)
    "mazout": 0.301,  # kg CO2-eq / kWh (PCI)
    "mix_cad": 0.045  # kg CO2-eq / kWh (Moyenne réseaux CAD EnR)
}


def calculate_carbon_roi(energy_saved_kwh_per_year: float, measure_key: str, dimension_unit: float,
                         current_energy: str = "gaz") -> float:
    """
    Calcule le Temps de Retour Carbone (TRC) en années.
    """
    # 1. Calcul de la dette carbone initiale (Fabrication / Installation)
    carbon_debt = KBOB_DB.get(measure_key, 0) * dimension_unit

    # 2. Gain carbone annuel (Émissions évitées)
    # L'énergie économisée l'est sur le vecteur actuel (généralement fossile pour la baseline)
    emission_factor = KBOB_DB.get(current_energy, KBOB_DB["gaz_naturel"])
    carbon_saved_per_year = energy_saved_kwh_per_year * emission_factor

    if carbon_saved_per_year <= 0:
        return float('inf')

    return carbon_debt / carbon_saved_per_year


def calculate_total_emissions_avoided(energy_saved_kwh: float, current_energy: str, new_energy: str = None) -> float:
    """
    Calcule la réduction totale des émissions annuelles (en tonnes de CO2-eq).
    """
    emission_factor_old = KBOB_DB.get(current_energy, 0.228)

    # Si on change de vecteur (ex: Gaz -> PAC), l'économie est double :
    # baisse des besoins ET décarbonation du vecteur restant.
    if new_energy and new_energy != "aucun":
        emission_factor_new = KBOB_DB.get(new_energy, 0.029)  # PAC utilise le mix CH
        # Simplification macroscopique pour le prototype
        tons_avoided = (energy_saved_kwh * emission_factor_old) / 1000.0
    else:
        tons_avoided = (energy_saved_kwh * emission_factor_old) / 1000.0

    return tons_avoided