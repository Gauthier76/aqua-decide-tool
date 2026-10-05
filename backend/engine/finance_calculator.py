# Base de données des coûts d'investissement macroscopiques (CAPEX) - Estimations Suisses
CAPEX_DB = {
    "bache_thermique": 150.0,  # CHF / m2 de bassin (Passif)
    "isolation_cuve": 200.0,  # CHF / m2 de bassin (Passif)
    "optimisation_mcr": 8000.0,  # CHF forfaitaire (Opérationnel)
    "variation_frequence": 12000.0,  # CHF forfaitaire (Opérationnel - VFD)
    "pac_geothermique": 1800.0,  # CHF / kW thermique installé (Actif)
    "raccordement_cad": 50000.0,  # CHF forfaitaire sous-station (Actif)
    "solaire_thermique": 850.0,  # CHF / m2 de capteur (Actif)
    "recuperation_cta": 25000.0  # CHF forfaitaire double flux / échangeur (Actif)
}

# Prix de l'énergie (OPEX) - CHF / kWh
OPEX_DB = {
    "gaz": 0.12,
    "mazout": 0.11,
    "electricite": 0.22,
    "cad": 0.14
}


def calculate_measure_financials(measure_key: str, dimension_unit: float, energy_saved_kwh: float,
                                 current_energy_type: str) -> dict:
    """
    Calcule le CAPEX et le TRI (Temps de Retour sur Investissement en années).
    """
    capex_chf = CAPEX_DB.get(measure_key, 0) * dimension_unit
    if measure_key in ["optimisation_mcr", "variation_frequence", "raccordement_cad", "recuperation_cta"]:
        capex_chf = CAPEX_DB.get(measure_key, 0)  # Forfaitaire

    energy_price = OPEX_DB.get(current_energy_type, 0.12)
    yearly_savings_chf = energy_saved_kwh * energy_price

    if yearly_savings_chf <= 0:
        tri_years = float('inf')
    else:
        tri_years = capex_chf / yearly_savings_chf

    return {
        "capex_chf": round(capex_chf, 2),
        "yearly_savings_chf": round(yearly_savings_chf, 2),
        "tri_years": round(tri_years, 1)
    }