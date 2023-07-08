from .base import *
# the settings only used in production environments should be here

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:9000",
    "http://153.156.254.150:50828",
    "http://localhost:82",
    "http://153.156.254.150:50090"
]

TIME_ZONE = "Asia/Tokyo"