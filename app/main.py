# ...existing code...
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.algorithms import day1_20251124

# Create app without redoc initially
app = FastAPI(
    title="Two Sum API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url=None,  # Disable default redoc
)

# mount static files FIRST
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Now add custom redoc endpoint
@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Two Sum API - ReDoc</title>
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

@app.post("/api/two-sum", response_model=day1_20251124.TwoSumResponse)
def api_two_sum(payload: day1_20251124.TwoSumRequest):
    nums = payload.nums
    target = payload.target
    result = day1_20251124.two_sum(nums, target)
    if result is None:
        raise HTTPException(status_code=404, detail="No two sum solution found")
    return {"indices": result}
