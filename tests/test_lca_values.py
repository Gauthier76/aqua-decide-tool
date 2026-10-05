# ==================================================
# FILE: tests\test_lca_values.py
# ==================================================

from backend.engine.lca_calculator import calculate_carbon_roi, KBOB_DB


def test_carbon_roi_calculation():
    """Test du calcul du Temps de Retour Carbone (TRC)"""
    # Dette: 1000 m2 de bâche * 2.1 kgCO2 = 2100 kgCO2
    # Gain: 50,000 kWh/an sauvés * 0.029 kgCO2 = 1450 kgCO2/an
    # ROI: 2100 / 1450 = ~1.44 années

    roi = calculate_carbon_roi(energy_saved_kwh_per_year=50000, material_type="bache_thermique", material_quantity=1000)
    expected_roi = (1000 * KBOB_DB["bache_thermique"]) / (50000 * KBOB_DB["mix_electrique_ch"])
    assert roi == expected_roi


def test_carbon_roi_no_savings():
    """Si aucune économie n'est réalisée, le ROI doit être infini"""
    roi = calculate_carbon_roi(0, "bache_thermique", 1000)
    assert roi == float('inf')