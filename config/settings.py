"""Configuración de Django para Regia.

Responsable: persona 6 (coordinación). Si necesitas un ajuste nuevo, pídelo
en el grupo en lugar de editarlo por tu cuenta: este archivo lo comparten
todos los módulos.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Carga las variables de .env si el archivo existe (ver .env.example).
load_dotenv(BASE_DIR / ".env")

# --- Seguridad -------------------------------------------------------------
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "solo-desarrollo-no-usar-en-produccion")
DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if host.strip()
]

# --- Aplicaciones ----------------------------------------------------------
# "routing" y "core" no aparecen aquí a propósito: son paquetes de Python
# puro, sin modelos ni plantillas, y se importan directamente.
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "network",     # persona 1
    "conditions",  # persona 3
    "assistant",   # persona 4
    "web",         # persona 5
    "api",         # persona 6
    "lab",         # persona 6
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# --- Base de datos ---------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- Idioma y hora ---------------------------------------------------------
# La hora local del proyecto es la de Monterrey: django.utils.timezone.localtime()
# devuelve directamente la hora del metro, sea cual sea el ordenador.
LANGUAGE_CODE = "es"
TIME_ZONE = "America/Monterrey"
USE_I18N = True
USE_TZ = True

# --- Archivos estáticos ----------------------------------------------------
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Ajustes propios de Regia ----------------------------------------------
# Módulo assistant (persona 4). Sin clave, el asistente debe usar el modo sin LLM.
LLM_API_KEY = os.environ.get("LLM_API_KEY", "")
LLM_MODEL = os.environ.get("LLM_MODEL", "")
