from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="X-Powered Trend Oracle")

@app.post("/oracle")
async def oracle(request: Request):
    return JSONResponse(content={
        "sentiment_delta": "+22%",
        "whale_moves": ["0xdeadbeef bought 3.4M SOL", "0xabc sold 1.1M"],
        "trend_alpha": "bullish momentum detected"
    })

@app.get("/")
async def root():
    return JSONResponse(content={"status": "live", "message": "Ready for paid agent queries"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)