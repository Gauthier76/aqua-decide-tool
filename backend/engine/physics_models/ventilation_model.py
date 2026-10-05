# ==================================================
# FILE: backend\engine\physics_models\ventilation_model.py
# ==================================================

def calculate_cta_power_savings(q_airflow_initial: float, reduction_factor: float) -> float:
    """
    Calcule les économies électriques des ventilateurs d'une Centrale de Traitement d'Air (CTA)
    lors de la réduction de débit (nuit/bâche), basé sur les lois d'affinité hydraulique/aéraulique.

    P_2 = P_1 * (Q_2 / Q_1)^3
    """
    if not (0 < reduction_factor <= 1):
        raise ValueError("Le facteur de réduction doit être entre 0 et 1.")

    # La puissance évolue au cube du débit
    power_ratio = reduction_factor ** 3
    return 1 - power_ratio


def calculate_latent_heat_recovery(m_evap_kg_h: float, efficiency: float = 0.75) -> float:
    """
    Calcule la chaleur latente récupérée par une CTA double flux ou PAC intégrée
    conformément aux exigences de récupération du MoPEC et SIA 382/1.
    """
    # Chaleur latente de l'eau ~ 0.627 kWh/kg
    total_latent_heat_kw = m_evap_kg_h * 0.627
    recovered_kw = total_latent_heat_kw * efficiency
    return recovered_kw