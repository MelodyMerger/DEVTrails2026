"""
ml/models.py
Simulated ML models for the fraud detection pipeline.
In production, these would be trained on real labeled data.
"""

import random
import math


def random_forest_predict(features: dict) -> float:
    """
    Simulated Random Forest classifier.
    Returns fraud probability between 0 and 1.
    In production: load a trained sklearn RandomForestClassifier.
    """
    score = 0.0

    if features.get("mock_location_enabled"):
        score += 0.45
    if features.get("is_rooted"):
        score += 0.30
    if features.get("vpn_detected"):
        score += 0.20
    if features.get("claim_frequency_24h", 0) > 3:
        score += 0.25
    if features.get("route_consistency_score", 1.0) < 0.4:
        score += 0.30
    if features.get("avg_speed_kmh", 0) > 100:
        score += 0.40

    # Add small random noise to simulate model variance
    score += random.uniform(-0.05, 0.05)
    return round(min(max(score, 0.0), 1.0), 4)


def isolation_forest_predict(features: dict) -> float:
    """
    Simulated Isolation Forest anomaly detector.
    Returns anomaly score between 0 (normal) and 1 (highly anomalous).
    In production: load a trained sklearn IsolationForest.
    """
    anomaly_signals = 0

    accel = features.get("total_accel", 9.8)
    if accel < 1.0:
        anomaly_signals += 1

    if features.get("route_consistency_score", 1.0) < 0.3:
        anomaly_signals += 1

    if features.get("claim_frequency_24h", 0) > 5:
        anomaly_signals += 1

    score = anomaly_signals / 3.0
    score += random.uniform(-0.05, 0.05)
    return round(min(max(score, 0.0), 1.0), 4)


def graph_fraud_score(device_id: str, user_id: str) -> float:
    """
    Simulated graph-based fraud ring detection.
    In production: query a Neo4j graph database for shared nodes.
    """
    if device_id.startswith("shared_"):
        return 0.85
    if user_id.endswith("_fraud"):
        return 0.70
    return random.uniform(0.0, 0.1)


def ensemble_ml_score(features: dict, device_id: str, user_id: str) -> dict:
    """
    Combines all ML models into a single ensemble score.
    """
    rf_score = random_forest_predict(features)
    iso_score = isolation_forest_predict(features)
    graph_score = graph_fraud_score(device_id, user_id)

    # Weighted ensemble
    final = (rf_score * 0.5) + (iso_score * 0.25) + (graph_score * 0.25)

    return {
        "random_forest": rf_score,
        "isolation_forest": iso_score,
        "graph_analysis": graph_score,
        "ensemble": round(final, 4),
    }
