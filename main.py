from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI(title="IP Lookup API", version="1.0")

# Optional: Add your own domain in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_URL = "http://ip-api.com/json/{ip}?fields=status,message,continent,country,regionName,city,zip,lat,lon,timezone,isp,org,as,query"

@app.get("/iplookup")
async def ip_lookup(request: Request, ip: str = Query(default=None)):
    client_ip = request.client.host if ip is None else ip
    async with httpx.AsyncClient() as client:
        res = await client.get(API_URL.format(ip=client_ip))
        data = res.json()
        if data["status"] != "success":
            return {"error": "Invalid IP or lookup failed"}
        return data