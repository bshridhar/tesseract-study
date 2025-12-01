# ...existing code...
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.config import APP_TITLE, APP_VERSION, APP_DESCRIPTION, DOCS_URL, REDOC_URL
from app.algorithms.day1_20251124 import router as day1_router
from app.algorithms.day2_20251124 import router as day2_router
from app.algorithms.day3_20251125 import router as day3_router
from app.algorithms.day4_20251130 import router as day4_router
from app.algorithms.day5_20251201 import router as day5_router

# Create FastAPI application
app = FastAPI(
    title=APP_TITLE,
    version=APP_VERSION,
    description=APP_DESCRIPTION,
    docs_url=DOCS_URL,
    redoc_url=REDOC_URL,  # Disable default redoc (using custom below)
)

# mount static files FIRST
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(day1_router)
app.include_router(day2_router)
app.include_router(day3_router)
app.include_router(day4_router)
app.include_router(day5_router)

# Custom redoc endpoint
@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Algorithm Practice API - ReDoc</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
        <style>
            body {
                margin: 0;
                padding: 0;
            }
        </style>
    </head>
    <body>
        <redoc spec-url="/openapi.json"></redoc>
        <script src="/static/redoc.standalone.js"></script>
    </body>
    </html>
    """)
