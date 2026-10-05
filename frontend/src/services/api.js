import axios from 'axios';

// Utilisation d'un chemin relatif pour l'environnement de production (Hugging Face)
const API_URL = process.env.REACT_APP_API_URL || '/api/v1';

export const submitBaseline = async (config) => {
    try {
        const response = await axios.post(`${API_URL}/baseline`, config);
        return response.data;
    } catch (error) {
        throw new Error("Erreur lors de l'enregistrement de la baseline : " + error.message);
    }
};

export const runSimulation = async (params) => {
    try {
        const response = await axios.post(`${API_URL}/simulate`, params);
        return response.data;
    } catch (error) {
        throw new Error("Erreur lors du calcul dynamique : " + error.message);
    }
};