from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import random
import math
import httpx
import asyncio

app = FastAPI(title="RYVEN Fraud Detection API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Request Model ────────────────────────────────────────────────────────────

class ClaimRequest(BaseModel):
    # Identity
    user_id: str
    device_id: str

    # Location signals
    gps_lat: float
    gps_lon: float
    wifi_lat: Optional[float] = None
    wifi_lon: Optional[float] = None
    cell_lat: Optional[float] = None
    cell_lon: Optional[float] = None

    # Motion sensors
    accel_x: Optional[float] = None
    accel_y: Optional[float] = None
    accel_z: Optional[float] = None
    gyro_x: Optional[float] = None
    gyro_y: Optional[float] = None
    gyro_z: Optional[float] = None

    # Device signals
    is_rooted: Optional[bool] = False
    mock_location_enabled: Optional[bool] = False
    is_emulator: Optional[bool] = False
    vpn_detected: Optional[bool] = False

    # Behavioral signals
    claim_frequency_24h: Optional[int] = 0
    avg_speed_kmh: Optional[float] = 0.0
    route_consistency_score: Optional[float] = 1.0

    # Weather claim
    claimed_weather_event: Optional[str] = "heavy_rain"
    actual_weather: Optional[str] = None

# ─── Scoring Engine ────────────────────────────────────────────────────────────

def haversine_distance(lat1, lon1, lat2, lon2) -> float:
    """Distance in km between two GPS coordinates."""
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))

def score_sensor_fusion(claim: ClaimRequest) -> dict:
    """Layer 1: Check if GPS matches Wi-Fi/cell tower location."""
    flags = []
    score = 0.0

    if claim.wifi_lat and claim.wifi_lon:
        dist = haversine_distance(claim.gps_lat, claim.gps_lon, claim.wifi_lat, claim.wifi_lon)
        if dist > 2.0:
            flags.append(f"GPS vs Wi-Fi mismatch: {dist:.1f}km apart")
            score += min(dist / 10.0, 0.4)

    if claim.cell_lat and claim.cell_lon:
        dist = haversine_distance(claim.gps_lat, claim.gps_lon, claim.cell_lat, claim.cell_lon)
        if dist > 5.0:
            flags.append(f"GPS vs Cell tower mismatch: {dist:.1f}km apart")
            score += min(dist / 20.0, 0.3)

    return {"risk": min(score, 1.0), "flags": flags, "layer": "Sensor Fusion"}

def score_motion(claim: ClaimRequest) -> dict:
    """Layer 2: Check if motion sensors match movement."""
    flags = []
    score = 0.0

    if claim.accel_x is not None:
        total_accel = math.sqrt(claim.accel_x**2 + claim.accel_y**2 + claim.accel_z**2)
        # A delivery worker on a bike/scooter should show motion
        if total_accel < 0.5 and claim.avg_speed_kmh > 10:
            flags.append("Phone stationary but high speed claimed")
            score += 0.4

    if claim.avg_speed_kmh > 120:
        flags.append(f"Impossible speed: {claim.avg_speed_kmh:.0f} km/h")
        score += 0.5

    if claim.route_consistency_score < 0.3:
        flags.append("Erratic/teleporting route detected")
        score += 0.3

    return {"risk": min(score, 1.0), "flags": flags, "layer": "Motion Analysis"}

def score_device_integrity(claim: ClaimRequest) -> dict:
    """Layer 3: Check device for tampering signs."""
    flags = []
    score = 0.0

    if claim.is_rooted:
        flags.append("Device is rooted/jailbroken")
        score += 0.35

    if claim.mock_location_enabled:
        flags.append("Mock location app is active")
        score += 0.5

    if claim.is_emulator:
        flags.append("Running on emulator, not real device")
        score += 0.6

    if claim.vpn_detected:
        flags.append("VPN detected — masking real location")
        score += 0.25

    return {"risk": min(score, 1.0), "flags": flags, "layer": "Device Integrity"}

def score_behavioral(claim: ClaimRequest) -> dict:
    """Layer 4: Check behavioral patterns."""
    flags = []
    score = 0.0

    if claim.claim_frequency_24h > 3:
        flags.append(f"Unusually high claim frequency: {claim.claim_frequency_24h} claims in 24h")
        score += min((claim.claim_frequency_24h - 3) * 0.15, 0.5)

    return {"risk": min(score, 1.0), "flags": flags, "layer": "Behavioral Analysis"}

def score_weather(claim: ClaimRequest) -> dict:
    """Layer 5: Cross-check claimed weather with real weather."""
    flags = []
    score = 0.0

    if claim.actual_weather:
        # Simple matching — in production this would use NLP similarity
        claimed = claim.claimed_weather_event.lower().replace("_", " ")
        actual = claim.actual_weather.lower()

        weather_map = {
            "heavy rain": ["rain", "storm", "shower", "drizzle", "thunderstorm"],
            "storm": ["storm", "thunderstorm", "tornado", "squall"],
            "flood": ["rain", "storm", "flood"],
            "snow": ["snow", "blizzard", "sleet"],
            "hail": ["hail", "storm"],
        }

        matched = False
        for key, keywords in weather_map.items():
            if key in claimed:
                if any(k in actual for k in keywords):
                    matched = True
                    break

        if not matched:
            flags.append(f"Claimed '{claim.claimed_weather_event}' but actual weather is '{claim.actual_weather}'")
            score += 0.5

    return {"risk": min(score, 1.0), "flags": flags, "layer": "Weather Validation"}

def score_fraud_ring(claim: ClaimRequest) -> dict:
    """Layer 6: Simple fraud ring heuristic (in production: graph DB query)."""
    flags = []
    score = 0.0

    # Simulate: device IDs starting with 'shared_' are flagged (demo heuristic)
    if claim.device_id.startswith("shared_"):
        flags.append("Device ID linked to multiple users (fraud ring signal)")
        score += 0.6

    return {"risk": min(score, 1.0), "flags": flags, "layer": "Fraud Ring Detection"}

def compute_ensemble_score(layer_scores: list) -> float:
    """Weighted ensemble of all layer scores."""
    weights = [0.25, 0.20, 0.25, 0.10, 0.10, 0.10]
    total = sum(s["risk"] * w for s, w in zip(layer_scores, weights))
    return round(min(total, 1.0), 4)

def get_decision(score: float) -> dict:
    if score < 0.30:
        return {
            "verdict": "APPROVED",
            "label": "Low Risk",
            "action": "Payout approved instantly.",
            "color": "green",
            "emoji": "✅"
        }
    elif score < 0.65:
        return {
            "verdict": "REVIEW",
            "label": "Medium Risk",
            "action": "Quick verification required — tap confirmation or selfie.",
            "color": "yellow",
            "emoji": "⚠️"
        }
    else:
        return {
            "verdict": "BLOCKED",
            "label": "High Risk",
            "action": "Claim flagged for manual review. User may appeal within 24 hours.",
            "color": "red",
            "emoji": "❌"
        }

# ─── Routes ────────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "RYVEN Fraud Detection API is running", "team": "RYVEN", "version": "1.0.0"}

@app.post("/analyze")
async def analyze_claim(claim: ClaimRequest):
    """Main endpoint: analyze a claim and return fraud risk score."""

    layers = [
        score_sensor_fusion(claim),
        score_motion(claim),
        score_device_integrity(claim),
        score_behavioral(claim),
        score_weather(claim),
        score_fraud_ring(claim),
    ]

    ensemble_score = compute_ensemble_score(layers)
    decision = get_decision(ensemble_score)

    all_flags = []
    for layer in layers:
        all_flags.extend(layer["flags"])

    return {
        "user_id": claim.user_id,
        "trust_score": round(1 - ensemble_score, 4),
        "risk_score": ensemble_score,
        "decision": decision,
        "flags": all_flags,
        "layer_breakdown": [
            {"layer": l["layer"], "risk": round(l["risk"], 4), "flags": l["flags"]}
            for l in layers
        ],
        "total_flags": len(all_flags),
    }

@app.get("/demo/genuine")
def demo_genuine():
    """Returns a sample payload for a genuine claim."""
    return {
        "user_id": "user_001",
        "device_id": "device_abc123",
        "gps_lat": 28.6139, "gps_lon": 77.2090,
        "wifi_lat": 28.6142, "wifi_lon": 77.2088,
        "cell_lat": 28.6135, "cell_lon": 77.2092,
        "accel_x": 2.1, "accel_y": 0.8, "accel_z": 9.5,
        "gyro_x": 0.1, "gyro_y": 0.2, "gyro_z": 0.05,
        "is_rooted": False, "mock_location_enabled": False,
        "is_emulator": False, "vpn_detected": False,
        "claim_frequency_24h": 1, "avg_speed_kmh": 22.0,
        "route_consistency_score": 0.92,
        "claimed_weather_event": "heavy_rain",
        "actual_weather": "heavy rain and thunderstorm"
    }

@app.get("/demo/fraudulent")
def demo_fraudulent():
    """Returns a sample payload for a fraudulent claim."""
    return {
        "user_id": "user_fraud_99",
        "device_id": "shared_device_001",
        "gps_lat": 28.6139, "gps_lon": 77.2090,
        "wifi_lat": 19.0760, "wifi_lon": 72.8777,
        "cell_lat": 19.0750, "cell_lon": 72.8780,
        "accel_x": 0.01, "accel_y": 0.01, "accel_z": 9.8,
        "gyro_x": 0.0, "gyro_y": 0.0, "gyro_z": 0.0,
        "is_rooted": True, "mock_location_enabled": True,
        "is_emulator": False, "vpn_detected": True,
        "claim_frequency_24h": 7, "avg_speed_kmh": 35.0,
        "route_consistency_score": 0.15,
        "claimed_weather_event": "heavy_rain",
        "actual_weather": "clear sky"
    }
