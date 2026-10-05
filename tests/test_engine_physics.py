# ==================================================
# FILE: tests\test_engine_physics.py
# ==================================================

import pytest
from backend.engine.physics_models.evaporation_model import calculate_evaporation_loss
from backend.engine.physics_models.ventilation_model import calculate_cta_power_savings

def test_evaporation_loss_positive():
    """L'évaporation doit causer une perte thermique positive"""
    loss = calculate_evaporation_loss(T_water=26, T_air=15, RH_air=60, wind_speed=2, pool_area=1000)
    assert loss > 0

def test_evaporation_cover_impact():
    """La présence d'une bâche doit réduire drastiquement l'évaporation"""
    loss_uncovered = calculate_evaporation_loss(26, 15, 60, 2, 1000, is_covered=False)
    loss_covered = calculate_evaporation_loss(26, 15, 60, 2, 1000, is_covered=True)
    assert loss_covered < loss_uncovered
    assert loss_covered == pytest.approx(loss_uncovered * 0.05, rel=1e-3)

def test_ventilation_affinity_laws():
    """Réduire le débit de 50% doit réduire la puissance de 87.5%"""
    savings = calculate_cta_power_savings(10000, reduction_factor=0.5)
    assert savings == pytest.approx(0.875, rel=1e-3)