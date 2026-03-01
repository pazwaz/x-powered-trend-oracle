import os
import hashlib
import json
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from openai import OpenAI
import redis

load_dotenv()
app = FastAPI(title="X-Powered Trend Oracle")

client = OpenAI(
    api_key=os.getenv("GROK_API_KEY"),
    base_url="https://api.x.ai/v1"
)

r = redis.from_url(os.getenv("UPSTASH_REDIS_URL"), decode_responses=True)

@app.post("/oracle")
async def oracle(request: Request):
    payload = await request.json()
    cache_key = hashlib.md5(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    cached = r.get(cache_key)
    if cached:
        return JSONResponse(content=json.loads(cached))
    
    topic = payload.get("topic")
    signals = payload.get("signals", [])
    
    prompt = f"""You are the X-Powered Trend Oracle. Analyze real-time X data for topic: '{topic}'. 
Focus ONLY on: {', '.join(signals)}. 
Return STRICT JSON only. No text. Example: {{"sentiment_delta": "+23%", "whale_moves": ["0xabc bought 2.4M SOL"], "trend_alpha": "bullish breakout in 6h"}}"""
    
    response = client.chat.completions.create(
        model="grok-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.1
    )
    
    try:
        result = eval(response.choices[0].message.content)
        r.setex(cache_key, 300, json.dumps(result))
        return JSONResponse(content=result)
    except:
        return JSONResponse(content={"error": "parse failed"}, status_code=500)

@app.get("/")
async def root():
    return JSONResponse(content={"status": "live", "message": "Ready for paid agent queries"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)