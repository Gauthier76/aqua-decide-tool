import React, { useState } from 'react';

const BaselineForm = ({ onSubmit, isLoading }) => {
    // État initial basé sur une infrastructure vieillissante standard
    const [formData, setFormData] = useState({
        commune_name: '',
        typology: 'extérieure',
        surface_eau_m2: 1000,
        volume_eau_m3: 2000,
        annee_construction: 1975,
        consommation_thermique_kwh: 450000,
        consommation_electrique_kwh: 120000,
        production_chaleur: 'gaz',
        cta_age: 15,
        cta_recuperation: false,
        filtres_age: 20,
        pompes_vfd: false
    });

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData({
            ...formData,
            [name]: type === 'checkbox' ? checked : (type === 'number' ? parseFloat(value) : value)
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit(formData);
    };

    return (
        <form onSubmit={handleSubmit} className="baseline-form">
            <h3>1. Informations Générales & Géométrie</h3>
            <div className="form-grid">
                <div className="form-group">
                    <label>Nom de la Commune</label>
                    <input type="text" name="commune_name" value={formData.commune_name} onChange={handleChange} required />
                </div>
                <div className="form-group">
                    <label>Typologie</label>
                    <select name="typology" value={formData.typology} onChange={handleChange}>
                        <option value="extérieure">Plein air (Extérieure)</option>
                        <option value="intérieure">Couverte (Intérieure)</option>
                        <option value="mixte">Mixte</option>
                    </select>
                </div>
                <div className="form-group">
                    <label>Surface en eau (m²)</label>
                    <input type="number" name="surface_eau_m2" value={formData.surface_eau_m2} onChange={handleChange} min="10" required />
                </div>
                <div className="form-group">
                    <label>Année de construction</label>
                    <input type="number" name="annee_construction" value={formData.annee_construction} onChange={handleChange} required />
                </div>
            </div>

            <h3>2. Systèmes Actuels (État des lieux)</h3>
            <div className="form-grid">
                <div className="form-group">
                    <label>Production de Chaleur principale</label>
                    <select name="production_chaleur" value={formData.production_chaleur} onChange={handleChange}>
                        <option value="gaz">Gaz Naturel</option>
                        <option value="mazout">Mazout</option>
                        <option value="pac">Pompe à Chaleur (PAC)</option>
                        <option value="cad">Chauffage à Distance (CAD)</option>
                        <option value="solaire">Solaire Thermique (Appoint)</option>
                    </select>
                </div>
                
                {formData.typology !== 'extérieure' && (
                    <>
                        <div className="form-group">
                            <label>Âge de la CTA (années)</label>
                            <input type="number" name="cta_age" value={formData.cta_age} onChange={handleChange} min="0" />
                        </div>
                        <div className="form-group checkbox-group">
                            <label>
                                <input type="checkbox" name="cta_recuperation" checked={formData.cta_recuperation} onChange={handleChange} />
                                CTA avec récupération double flux
                            </label>
                        </div>
                    </>
                )}

                <div className="form-group checkbox-group">
                    <label>
                        <input type="checkbox" name="pompes_vfd" checked={formData.pompes_vfd} onChange={handleChange} />
                        Variateurs de fréquence (Pompes hydrauliques)
                    </label>
                </div>
            </div>

            <h3>3. Données de Consommation Annuelles</h3>
            <div className="form-grid">
                <div className="form-group">
                    <label>Chaleur (kWh/an)</label>
                    <input type="number" name="consommation_thermique_kwh" value={formData.consommation_thermique_kwh} onChange={handleChange} required />
                </div>
                <div className="form-group">
                    <label>Électricité (kWh/an)</label>
                    <input type="number" name="consommation_electrique_kwh" value={formData.consommation_electrique_kwh} onChange={handleChange} required />
                </div>
            </div>

            <div className="form-actions">
                <button type="submit" className="btn-primary" disabled={isLoading}>
                    {isLoading ? 'Calcul en cours...' : 'Générer le Diagnostic Initial'}
                </button>
            </div>
        </form>
    );
};

export default BaselineForm;