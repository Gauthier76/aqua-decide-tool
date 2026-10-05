import React, { useState } from 'react';
import { runSimulation } from '../services/api';

const SimulationEngine = () => {
    const [inputs, setInputs] = useState({
        area_m2: 1000,
        t_water: 26.0,
        t_air: 12.0,
        rh_air: 65.0,
        wind_speed: 3.0,
        current_energy: 'gaz',
        apply_cover: false,
        apply_isolation: false,
        apply_mcr_night_setback: false,
        apply_vfd_pumps: false,
        heating_system: 'aucun',
        apply_cta_recovery: false
    });

    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleSimulate = async () => {
        setLoading(true);
        try {
            const data = await runSimulation(inputs);
            setResults(data);
        } catch (error) {
            console.error("Erreur API :", error);
        }
        setLoading(false);
    };

    return (
        <div className="simulation-engine">
            <div className="module-header">
                <h2>Module 3 : Moteur de Variantes Multicritère</h2>
                <p>Combinez les leviers Passifs, Opérationnels et Actifs pour piloter la stratégie d'assainissement communal.</p>
            </div>

            <div className="layout-grid">
                {/* 🎛️ PANNEAU DE CONTRÔLE DES 3 FAMILLES DE LEVIERS */}
                <div className="control-panel card">
                    <h3>Matrice des Leviers d'Action</h3>

                    {/* 1. PASSIFS */}
                    <div className="variant-section" style={{marginBottom: '1rem'}}>
                        <h4 style={{color: '#2980b9'}}>1. Leviers Passifs (Structure & Enveloppe)</h4>
                        <label className="toggle" style={{display: 'block', margin: '5px 0'}}>
                            <input type="checkbox" checked={inputs.apply_cover} onChange={e => setInputs({...inputs, apply_cover: e.target.checked})} />
                            Couverture thermique nocturne (Bâche)
                        </label>
                        <label className="toggle" style={{display: 'block', margin: '5px 0'}}>
                            <input type="checkbox" checked={inputs.apply_isolation} onChange={e => setInputs({...inputs, apply_isolation: e.target.checked})} />
                            Isolation des cuves / bassins
                        </label>
                    </div>

                    {/* 2. OPERATIONNELS */}
                    <div className="variant-section" style={{marginBottom: '1rem'}}>
                        <h4 style={{color: '#27ae60'}}>2. Leviers Opérationnels (MCR & Régulation)</h4>
                        <label className="toggle" style={{display: 'block', margin: '5px 0'}}>
                            <input type="checkbox" checked={inputs.apply_mcr_night_setback} onChange={e => setInputs({...inputs, apply_mcr_night_setback: e.target.checked})} />
                            Abaissement nocturne de l'eau (-1°C)
                        </label>
                        <label className="toggle" style={{display: 'block', margin: '5px 0'}}>
                            <input type="checkbox" checked={inputs.apply_vfd_pumps} onChange={e => setInputs({...inputs, apply_vfd_pumps: e.target.checked})} />
                            Variateurs de fréquence sur pompes (VFD)
                        </label>
                    </div>

                    {/* 3. ACTIFS */}
                    <div className="variant-section" style={{marginBottom: '1rem'}}>
                        <h4 style={{color: '#e74c3c'}}>3. Leviers Actifs (Systèmes & Énergies)</h4>
                        <div style={{margin: '5px 0'}}>
                            <label>Substitution de chauffage :</label>
                            <select value={inputs.heating_system} onChange={e => setInputs({...inputs, heating_system: e.target.value})} style={{width: '100%', marginTop: '5px'}}>
                                <option value="aucun">Conserver le vecteur actuel (Gaz/Mazout)</option>
                                <option value="cad">Raccordement Chauffage à Distance (CAD)</option>
                                <option value="pac">Pompe à Chaleur (PAC) géothermique</option>
                            </select>
                        </div>
                        <label className="toggle" style={{display: 'block', margin: '10px 0 5px 0'}}>
                            <input type="checkbox" checked={inputs.apply_cta_recovery} onChange={e => setInputs({...inputs, apply_cta_recovery: e.target.checked})} />
                            Récupération de chaleur CTA (Double flux)
                        </label>
                    </div>

                    <button className="btn-primary" onClick={handleSimulate} disabled={loading} style={{marginTop: '1.5rem', width: '100%'}}>
                        {loading ? 'Calculs multicritères en cours...' : 'Lancer la Simulation Croisée'}
                    </button>
                </div>

                {/* 📊 PANNEAU DE RÉSULTATS */}
                {results && (
                    <div className="results-panel card">
                        <h3>Bilan de la Stratégie de Rénovation</h3>

                        <div className="kpi-grid">
                            <div className="kpi-card">
                                <h4>Énergie Totale Sauvée</h4>
                                <span className="value text-success">-{results.energy_saved_kwh.toLocaleString('fr-CH')} kWh/an</span>
                            </div>
                            <div className={`kpi-card ${results.mopec_compliant ? 'success' : 'danger'}`}>
                                <h4>Validation MoPEC</h4>
                                <span className="value">{results.mopec_compliant ? '✅ Conforme' : '❌ Non-Conforme'}</span>
                            </div>
                        </div>

                        <h4>Analyse Détaillée par Mesure (CAPEX / OPEX / ACV)</h4>
                        {results.measures_evaluation.length === 0 ? (
                            <p style={{color: '#7f8c8d', fontStyle: 'italic'}}>Aucun levier activé.</p>
                        ) : (
                            <table className="analysis-table">
                                <thead>
                                    <tr>
                                        <th>Catégorie</th>
                                        <th>Mesure</th>
                                        <th>Investissement (CAPEX)</th>
                                        <th>Économie (OPEX)</th>
                                        <th>TRI</th>
                                        <th>TRC (Carbone)</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {results.measures_evaluation.map((m, idx) => (
                                        <tr key={idx}>
                                            <td><span className={`badge ${m.category.toLowerCase()}`}>{m.category}</span></td>
                                            <td><strong>{m.name}</strong></td>
                                            <td>{m.capex_chf.toLocaleString('fr-CH')} CHF</td>
                                            <td className="text-success">+{m.savings_chf_year.toLocaleString('fr-CH')} CHF/an</td>
                                            <td><strong>{m.tri_years} ans</strong></td>
                                            <td>{m.trc_years} ans</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
};

export default SimulationEngine;