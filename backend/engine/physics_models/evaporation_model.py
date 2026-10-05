import numpy as np


def calculate_saturation_pressure(T_water_celsius):
    """Calcule la pression de vapeur saturante (Pa) selon la formule de Magnus."""
    return 611.2 * np.exp(17.67 * T_water_celsius / (T_water_celsius + 243.5))


def calculate_evaporation_loss(T_water, T_air, RH_air, wind_speed, pool_area, is_covered=False):
    """
    Calcule les pertes thermiques par évaporation (SIA 385/9 / ASHRAE).
    Retourne la puissance de perte en kW.
    """
    # Pressions partielles
    P_water_sat = calculate_saturation_pressure(T_water)
    P_air = calculate_saturation_pressure(T_air) * (RH_air / 100.0)
    Delta_P_kPa = max(0, P_water_sat - P_air) / 1000.0

    # Flux massique d'évaporation (kg / m2.h)
    m_evap = (0.089 + 0.0782 * wind_speed) * Delta_P_kPa

    # Impact de la bâche (réduit l'évaporation de 95%)
    if is_covered:
        m_evap *= 0.05

    # Chaleur latente de vaporisation (approx 0.627 kWh/kg)
    Q_evap_kW = m_evap * pool_area * 0.627
    return Q_evap_kW