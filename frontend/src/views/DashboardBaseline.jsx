// ==================================================
// FILE: frontend/src/views/DashboardBaseline.jsx
// ==================================================

import React, { useState } from 'react';
import BaselineForm from '../components/forms/BaselineForm';
import { Chart } from 'react-google-charts';
import { submitBaseline } from '../services/api';

const DashboardBaseline = () => {
    const [result, setResult] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleFormSubmit = async (formData) => {
        setIsLoading(true);
        setError(null); // Réinitialisation des erreurs avant un nouvel appel

        try {
            // APPEL RÉEL À L'API FASTAPI
            // Transmission des données de l'infrastructure vers routes_input.py
            const data = await submitBaseline(formData);

            // Le backend renvoie la structure : ide_calcul_kwh_m2, ofen_target_status, mopec_compliance, thermal_breakdown
            setResult(data);
        } catch (err) {
            console.error("Erreur de calcul Backend :", err);
            setError("Impossible de joindre le moteur thermodynamique (API FastAPI). Vérifiez que le serveur Python est lancé.");
        } finally {
            setIsLoading(false);
        }
    };

    // Configuration dynamique du diagramme de Sankey basé sur les calculs physiques du backend
    const generateSankeyData = () => {
        if (!result || !result.thermal_breakdown) return [];

        const { evaporation_kwh, convection_radiation_kwh, renouvellement_kwh } = result.thermal_breakdown;
        const total_pertes = evaporation_kwh + convection_radiation_kwh + renouvellement_kwh;

        return [
            ["Source", "Déperdition", "Énergie (kWh/an)"],
            ["Production Chaleur", "Chauffage Bassin", total_pertes],
            ["Chauffage Bassin", "Évaporation (Latente)", Math.round(evaporation_kwh)],
            ["Chauffage Bassin", "Convection/Radiation", Math.round(convection_radiation_kwh)],
            ["Chauffage Bassin", "Renouvellement d'Eau Normatif", Math.round(renouvellement_kwh)]
        ];
    };

    return (
        <div className="dashboard-baseline">
            <div className="module-header">
                <h2>Module 1 : Diagnostic de l'Existant (Baseline)</h2>
                <p>Évaluation de la performance énergétique initiale et de la conformité aux exigences MoPEC.</p>
            </div>

            <div className="layout-grid">
                {/* PANNEAU DE SAISIE */}
                <div className="input-section">
                    <BaselineForm onSubmit={handleFormSubmit} isLoading={isLoading} />
                    {error && (
                        <div className="error-alert" style={{ color: 'red', marginTop: '1rem', padding: '1rem', border: '1px solid red', backgroundColor: '#ffe6e6' }}>
                            <strong>⚠️ Erreur Système :</strong> {error}
                        </div>
                    )}
                </div>

                {/* PANNEAU DES RÉSULTATS (Généré après l'appel API) */}
                {result && (
                    <div className="results-section">
                        <h3>Bilan de l'Audit Initial</h3>

                        {/* Indicateurs de performance (KPI) */}
                        <div className="kpi-grid">
                            <div className="kpi-card">
                                <h4>Indice de Dépense Énergétique (IDE)</h4>
                                <span className="value">{result.ide_calcul_kwh_m2} <small>kWh/m²/an</small></span>
                            </div>
                            <div className={`kpi-card ${result.ofen_target_status === 'Conforme' ? 'success' : 'danger'}`}>
                                <h4>Cible OFEN (160 - 240)</h4>
                                <span className="value">{result.ofen_target_status}</span>
                            </div>
                        </div>

                        {/* Validation du cadre légal (MoPEC / LVLEne) */}
                        <div className={`mopec-alerts ${result.mopec_compliance?.is_compliant ? 'compliant' : 'non-compliant'}`}>
                            <h4>Statut Légal (MoPEC)</h4>
                            {result.mopec_compliance?.is_compliant ? (
                                <p style={{ color: 'green' }}>✅ L'infrastructure respecte les exigences de base du MoPEC.</p>
                            ) : (
                                <ul style={{ color: '#d35400' }}>
                                    {result.mopec_compliance?.warnings.map((warning, index) => (
                                        <li key={index}>⚠️ {warning}</li>
                                    ))}
                                </ul>
                            )}
                        </div>

                        {/* Diagramme Thermodynamique */}
                        <div className="sankey-container" style={{ marginTop: '2rem', padding: '1rem', backgroundColor: '#f9f9f9', borderRadius: '8px' }}>
                            <h4>Répartition Thermodynamique Estimée (Norme SIA 385/9)</h4>
                            <p style={{ fontSize: '0.85rem', color: '#666' }}>
                                Visualisation des vecteurs de déperdition thermique basée sur les modèles physiques HEIG-VD.
                            </p>
                            <Chart
                                chartType="Sankey"
                                width="100%"
                                height="280px"
                                data={generateSankeyData()}
                                options={{
                                    sankey: {
                                        node: { width: 20, colors: ['#2c3e50', '#e74c3c', '#3498db', '#f39c12', '#9b59b6'] },
                                        link: { colorMode: 'gradient' }
                                    }
                                }}
                            />
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default DashboardBaseline;