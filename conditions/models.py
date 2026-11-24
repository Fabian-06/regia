"""Modelos de condiciones. Responsable: persona 3.

PENDIENTE: un modelo para las incidencias que se crean desde el centro de
control. Campos que exige el contrato (core.contracts.Incident): tipo,
estación, línea, minutos extra y descripción. Os conviene añadir además si
está activa y cuándo se creó.

Al crear o cambiar modelos:
    python manage.py makemigrations conditions
    python manage.py migrate
y subid al repositorio la carpeta conditions/migrations/.
"""
