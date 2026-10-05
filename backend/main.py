import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from api import routes_simulation, routes_input, routes_export

app = FastAPI(title="AquaDecide API (HEIG-VD)", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ouvert pour Hugging Face
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Inclusion de TOUTES les routes de calcul
app.include_router(routes_input.router, prefix="/api/v1")
app.include_router(routes_simulation.router, prefix="/api/v1")
app.include_router(routes_export.router, prefix="/api/v1")

# 2. Gestion du Frontend React (SPA)
frontend_build_path = os.path.join(os.path.dirname(__file__), "build")

if os.path.exists(frontend_build_path):
    # On sert les assets statiques (CSS, JS, images)
    app.mount("/static", StaticFiles(directory=os.path.join(frontend_build_path, "static")), name="static")


    # Catch-all pour gérer la navigation React Router sans erreur 404
    @app.get("/{full_path:path}")
    def serve_react_app(full_path: str):
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="API route not found")

        filepath = os.path.join(frontend_build_path, full_path)
        if os.path.exists(filepath) and os.path.isfile(filepath):
            return FileResponse(filepath)

        return FileResponse(os.path.join(frontend_build_path, "index.html"))
else:
    @app.get("/")
    def read_root():
        return {"message": "API Thermodynamique active. (Frontend build introuvable)"}