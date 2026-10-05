import React from 'react';

const RoadmapReport = ({ simulationResults }) => {
    if (!simulationResults || simulationResults.measures_evaluation.length === 0) {
        return (
            <div className="roadmap-report empty-state" style={{ padding: '2rem', textAlign: 'center' }}>
                <h2>Feuille de Route non disponible</h2>
                <p>Veuillez d'abord configurer une variante dans le <strong>Module 3</strong>.</p>
            </div>
        );
    }

    const totalCapex = simulationResults.measures_evaluation.reduce((acc, m) => acc + m.capex_chf, 0);
    const totalSavingsYearly = simulationResults.measures_evaluation.reduce((acc, m) => acc + m.savings_chf_year, 0);
    const globalTri = totalSavingsYearly > 0 ? (totalCapex / totalSavingsYearly).toFixed(1) : 'N/A';

    // Estimation des tonnes de CO2 évitées (Facteur moyen gaz ~0.228 kg/kWh)
    const tonnesCO2Evitees = (simulationResults.energy_saved_kwh * 0.228) / 1000;

    return (
        <div className="roadmap-report" style={{ padding: '2rem', backgroundColor: '#fff', color: '#333' }}>

            <div className="report-header" style={{ borderBottom: '3px solid #e74c3c', paddingBottom: '1rem', marginBottom: '2rem' }}>
                <h1 style={{ margin: 0, color: '#2c3e50' }}>Feuille de Route : Décarbonation & Efficacité</h1>
                <h3 style={{ margin: '0.5rem 0', color: '#7f8c8d' }}>Méthodologie HEIG-VD / Norme SIA 385/9</h3>
            </div>

            {/* SYNTHÈSE ÉNERGÉTIQUE ET ÉCOLOGIQUE */}
            <div className="report-section">
                <h2 style={{ color: '#27ae60' }}>1. Bilan Énergétique et Écologique (ACV)</h2>
                <p>L'application des leviers d'optimisation permet une restructuration majeure de l'empreinte environnementale de l'infrastructure.</p>

                <div className="executive-summary" style={{ display: 'flex', gap: '2rem', marginBottom: '2rem', marginTop: '1rem' }}>
                    <div className="summary-box" style={{ flex: 1, padding: '1rem', backgroundColor: '#e8f8f5', borderRadius: '8px', borderLeft: '4px solid #27ae60' }}>
                        <h4>Énergie Sauvée</h4>
                        <p style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#27ae60' }}>
                            {simulationResults.energy_saved_kwh.toLocaleString('fr-CH')} <small>kWh/an</small>
                        </p>
                    </div>
                    <div className="summary-box" style={{ flex: 1, padding: '1rem', backgroundColor: '#ebf5fb', borderRadius: '8px', borderLeft: '4px solid #2980b9' }}>
                        <h4>Émissions Évitées</h4>
                        <p style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#2980b9' }}>
                            - {tonnesCO2Evitees.toFixed(1)} <small>t CO₂-eq/an</small>
                        </p>
                    </div>
                    <div className="summary-box" style={{ flex: 1, padding: '1rem', backgroundColor: '#fef9e7', borderRadius: '8px', borderLeft: '4px solid #f39c12' }}>
                        <h4>Conformité Légale (MoPEC)</h4>
                        <p style={{ fontSize: '1.2rem', fontWeight: 'bold', color: simulationResults.mopec_compliant ? '#27ae60' : '#e74c3c' }}>
                            {simulationResults.mopec_compliant ? '✅ Validée' : '❌ Non Atteinte'}
                        </p>
                    </div>
                </div>
            </div>

            {/* SYNTHÈSE FINANCIÈRE */}
            <div className="report-section">
                <h2 style={{ color: '#2980b9' }}>2. Bilan Économique (CAPEX / OPEX)</h2>
                <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '1rem', textAlign: 'left' }}>
                    <thead>
                        <tr style={{ backgroundColor: '#f2f2f2' }}>
                            <th style={{ padding: '10px', borderBottom: '2px solid #ddd' }}>Indicateur Financier</th>
                            <th style={{ padding: '10px', borderBottom: '2px solid #ddd' }}>Valeur Estimée</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td style={{ padding: '10px', borderBottom: '1px solid #ddd' }}>Investissement Total Requis (CAPEX)</td>
                            <td style={{ padding: '10px', borderBottom: '1px solid #ddd', fontWeight: 'bold' }}>{totalCapex.toLocaleString('fr-CH')} CHF</td>
                        </tr>
                        <tr>
                            <td style={{ padding: '10px', borderBottom: '1px solid #ddd' }}>Réduction de la Facture Énergétique (OPEX)</td>
                            <td style={{ padding: '10px', borderBottom: '1px solid #ddd', color: '#27ae60', fontWeight: 'bold' }}>+ {totalSavingsYearly.toLocaleString('fr-CH')} CHF/an</td>
                        </tr>
                        <tr>
                            <td style={{ padding: '10px', borderBottom: '1px solid #ddd' }}>Temps de Retour sur Investissement (TRI)</td>
                            <td style={{ padding: '10px', borderBottom: '1px solid #ddd', fontWeight: 'bold' }}>{globalTri} ans</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            {/* PHASAGE DÉTAILLÉ */}
            <div className="report-section" style={{ marginTop: '2rem' }}>
                <h2 style={{ color: '#2c3e50' }}>3. Plan d'Action Recommandé (Détail des Mesures)</h2>
                <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '1rem' }}>
                    <thead>
                        <tr style={{ backgroundColor: '#34495e', color: 'white', textAlign: 'left' }}>
                            <th style={{ padding: '10px' }}>Catégorie</th>
                            <th style={{ padding: '10px' }}>Mesure Technique</th>
                            <th style={{ padding: '10px' }}>Budget</th>
                            <th style={{ padding: '10px' }}>TRC (Carbone)</th>
                        </tr>
                    </thead>
                    <tbody>
                        {simulationResults.measures_evaluation.map((m, idx) => (
                            <tr key={idx} style={{ borderBottom: '1px solid #ddd' }}>
                                <td style={{ padding: '10px' }}><strong>{m.category}</strong></td>
                                <td style={{ padding: '10px' }}>{m.name}</td>
                                <td style={{ padding: '10px' }}>{m.capex_chf.toLocaleString('fr-CH')} CHF</td>
                                <td style={{ padding: '10px', color: m.trc_years < 3 ? 'green' : 'orange' }}>
                                    {m.trc_years === 0 ? 'Immédiat' : `${m.trc_years} ans`}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                <p style={{ fontSize: '0.85rem', color: '#7f8c8d', marginTop: '10px' }}>
                    *TRC : Le Temps de Retour Carbone indique la durée nécessaire pour que les émissions de CO₂ évitées en exploitation compensent l'énergie grise (fabrication/pose) du matériel, selon les standards KBOB.
                </p>
            </div>

            <div className="report-footer no-print" style={{ marginTop: '3rem', textAlign: 'center' }}>
                <button onClick={() => window.print()} style={{ padding: '10px 20px', backgroundColor: '#e74c3c', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer', fontWeight: 'bold' }}>
                    🖨️ Exporter la Feuille de Route (PDF)
                </button>
            </div>
        </div>
    );
};

export default RoadmapReport;