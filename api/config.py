import os
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "database": os.getenv("DB_NAME", "labdb"),
    "user": os.getenv("DB_USER", "labuser"),
    "password": os.getenv("DB_PASSWORD", "labpassword123")
}
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
