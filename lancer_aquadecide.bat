Set-Content -Path "C:\Users\gauthier.demonchy\PycharmProjects\PythonProject1\aqua-decide-tool\lancer_aquadecide.bat" -Value @"
@echo off
echo ===================================================
echo   Lancement d'AquaDecide (HEIG-VD)
echo ===================================================

echo Demarrage du Moteur Python (Backend)...
start "AquaDecide - Backend" cmd /k "cd /d C:\Users\gauthier.demonchy\PycharmProjects\PythonProject1 && (call venv\Scripts\activate.bat 2>nul || call .venv\Scripts\activate.bat 2>nul) && cd aqua-decide-tool\backend && uvicorn main:app --reload"

echo Demarrage de l'Interface React (Frontend)...
start "AquaDecide - Frontend" cmd /k "cd /d C:\Users\gauthier.demonchy\PycharmProjects\PythonProject1\aqua-decide-tool\frontend && npm start"
"@