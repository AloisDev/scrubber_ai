from fastapi import Depends, FastAPI
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from routers import documents, users, auth

# import uvicorn

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s %(message)s",
    handlers=[
        RotatingFileHandler("logs/debug.log", maxBytes=100000, backupCount=10),
        logging.StreamHandler(),
        TimedRotatingFileHandler(
            "logs/debug_daily.log", when="D", interval=1, backupCount=7
        ),
    ],
)

app = FastAPI(
    title="Scrubber AI API",
    description="Scrubber AI API documentation",
    version="1.0.0",
)

app.include_router(users.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(documents.router, prefix="/api/v1")

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)

# Request Logging:
# If you want to log every request coming into your application,
# you can create a dependency that does this and add it as a global dependency.
# This way, every request will be logged automatically.

# Rate Limiting: If you want to limit the number of requests a client can make in a certain time period,
# you can create a rate limiting dependency and add it globally.
# This will ensure that all routes in your application are rate-limited.

# CORS Middleware: If you want to handle Cross-Origin Resource Sharing (CORS) in your application,
# you can add a CORS middleware as a global dependency.
# This will apply CORS settings to all routes.

# Common Header Checks: If there are certain headers that should be present in all requests
# (like an API version header), you can create a dependency that checks for these headers and add it globally.
