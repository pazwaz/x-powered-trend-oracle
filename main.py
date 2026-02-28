from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="X-Powered Trend Oracle")

@app.get("/")
async def root():
    return JSONResponse(content={"status": "live", "message": "Ready for paid agent queries"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
