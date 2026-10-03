@echo off
title Veloce Auto Spa - Sistema de Gestion y Fidelizacion
echo ===============================================================
echo   VELOCE AUTO SPA - SISTEMA DE GESTION Y FIDELIZACION
echo ===============================================================
echo.
echo Verificando dependencias...
python -m pip install -r requirements.txt
echo.
echo Iniciando servidor local en http://127.0.0.1:5000 ...
echo Credenciales Administrador: admin / admin123
echo Credenciales Cliente:       carlos_m / cliente123
echo.
python app.py
pause
