# Étape 1 : Compilation du Frontend (React)
FROM node:18 AS build-stage
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Étape 2 : Assemblage et Serveur Backend (FastAPI)
FROM python:3.10-slim
WORKDIR /app

# Installation des librairies de calcul
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie des scripts scientifiques
COPY backend/ ./backend/
COPY data/ ./data/

# Transfert du front compilé vers le backend
COPY --from=build-stage /app/frontend/build ./backend/build

# Port standard pour Render
EXPOSE 10000

# Lancement du serveur depuis le dossier backend
WORKDIR /app/backend
CMD uvicorn main:app --host 0.0.0.0 --port 10000