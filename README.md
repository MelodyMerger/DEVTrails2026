# DEVTrails2026
🚚 WeatherShield — Parametric Insurance Platform for Gig Delivery Workers
📌 Project Overview
WeatherShield is an AI-powered parametric insurance platform designed to protect gig delivery workers during severe weather events. When a delivery partner is caught in a red-alert weather zone, the system automatically verifies their situation and triggers instant payouts — no paperwork, no delays.
The Problem:
Delivery workers have zero income protection during extreme weather. They either risk their safety to earn, or stay home and lose money.
Our Solution:
Real-time weather data + GPS location + AI verification = automatic, fair, instant insurance payouts.

🎯 How It Works

Worker opens the app during their shift
System monitors real-time weather conditions at their GPS location
If a severe weather alert is detected at their location → claim is auto-triggered
AI verifies the claim using multi-layer checks
Payout is approved and transferred within minutes


🛡️ Adversarial Defense & Anti-Spoofing Strategy
The Threat
A coordinated syndicate of 500 delivery workers was discovered using GPS-spoofing apps to fake their locations inside red-alert weather zones — while sitting safely at home. They exploited a parametric insurance platform by triggering false weather claims and draining its liquidity pool.
Simple GPS verification is no longer sufficient. Our platform uses a multi-layer defense system.

1. 🔍 Differentiating a Genuine Stranded Worker from a Bad Actor
Our system uses sensor fusion — combining multiple data sources to confirm a worker is truly at a location, not just spoofing GPS coordinates.
Verification LayerHow It WorksMock Location DetectionApp checks if Android "Developer Options / Mock Location" or iOS location simulation is enabled. If ON → instant fraud flag.Accelerometer + Gyroscope CheckA real person in a weather zone shows natural movement data (walking, shaking, vibration). A person at home spoofing GPS will show zero or unnatural sensor activity.Barometric Pressure SensorReal weather events cause measurable air pressure changes. The phone's barometer is cross-checked with the claimed weather event. GPS spoofers cannot fake this.Cell Tower + WiFi TriangulationGPS coordinates are cross-verified with the nearest cell tower ID and WiFi BSSID location. If GPS says "flood zone" but cell tower places the device in a residential area → flag raised.Hyperlocal Weather API MatchWorker's GPS location is matched against real-time weather APIs (e.g., OpenWeatherMap, IMD). If no actual weather event exists at that pinpoint → claim rejected.Historical Route AnalysisWe compare the claimed location against the worker's last 30 days of delivery routes. A worker suddenly appearing in a new zone only during weather alerts is flagged as suspicious.Speed Impossibility CheckIf GPS shows the worker "moved" 50 km in 2 minutes → physically impossible → spoofing detected.

2. 📊 Data Points Used to Detect a Coordinated Fraud Ring
Beyond individual GPS checks, our system detects group/ring fraud using behavioral pattern analysis:
Data PointWhat It RevealsDevice ID / IMEI fingerprintMultiple accounts operating from the same physical deviceClaim timestamp clusteringIf 50+ claims are submitted within a 10-minute window from the same city → coordinated attack signalIdentical GPS coordinatesMultiple workers claiming the exact same latitude/longitude simultaneously → impossible in real-world scenariosBank account linkageMultiple worker accounts routing payouts to the same bank accountIP Address analysisMultiple accounts logging in from the same network or IP addressAccount creation spike detectionSudden surge of new accounts registered just before a predicted weather eventTelegram / Social Metadata (indirect)Unusual claim spikes that match known group coordination patterns (without accessing private messages)Shared referral chainsFraud rings often recruit via referrals — abnormal referral clusters are flagged
Ring Detection Rule: If 3 or more of the above signals fire simultaneously for a cluster of workers → system classifies it as a coordinated fraud ring, not individual fraud, and escalates to a full investigation hold.

3. ⚖️ UX Balance — Protecting Honest Workers Without Punishing Them
Our core principle: Innocent until proven guilty.
We use a 3-Tier Trust System to ensure genuine workers are never wrongly blocked:

🟢 Tier 1 — Clean (Auto-Approve)

All verification layers pass
Worker has a trust score above 85%
No fraud signals detected
Action: Payout released automatically within 5 minutes
Worker receives: "✅ Claim approved. Payout on the way!"


🟡 Tier 2 — Soft Flag (Quick Verification Required)

1–2 suspicious signals detected (could be network drop, cheap phone with weak sensors, or genuine GPS drift in bad weather)
Action: Worker receives an in-app prompt:

"We need a quick check. Please share a 10-second live selfie video or a photo with your surroundings."


If verification passes → payout released within 2 hours
Worker is NOT penalized or marked as fraudster
Worker receives: "⚠️ Quick check needed — tap to verify in 30 seconds"

Why this matters: Bad weather causes real GPS drift. Cheap Android phones have weaker sensors. A hard rejection here would punish honest workers. Soft verification gives them a fair chance.

🔴 Tier 3 — High Risk (Hold + Manual Review)

3+ fraud signals detected, or part of a flagged cluster
Action: Claim is held for up to 24-hour manual review
Worker can submit an appeal with photo/video evidence
If found innocent → full payout released + ₹50 compensation for the inconvenience
If confirmed fraud → account suspended, case flagged for further action
Worker receives: "🔴 Your claim is under review. Expected resolution: 24 hours."


📣 Appeals Process
Every flagged worker has the right to appeal. The appeals portal allows:

Uploading photo/video proof
Submitting delivery app activity logs
Contacting support within 48 hours

No worker is permanently banned without a completed appeal review.

🧠 AI/ML Architecture Summary

Anomaly Detection Model: Trained on historical delivery patterns to flag location outliers
Fraud Ring Graph Model: Network graph analysis to detect connected accounts
Trust Score Engine: Dynamic scoring updated after every shift based on behavior
Real-Time Weather Verification: API integration with IMD + OpenWeatherMap for hyperlocal data


🛠️ Tech Stack (Planned)

Frontend: React Native (iOS + Android)
Backend: Node.js + FastAPI
ML Models: Python (scikit-learn, NetworkX for graph analysis)
Database: PostgreSQL + Redis (real-time caching)
Weather APIs: OpenWeatherMap, IMD (India Meteorological Department)
Payments: Razorpay / UPI integration


👥 Team name-RYVEN
Team member:-
Ankit kumar
Bhoomi gupta
sarthak verma
Aniket Krishnet
Bhawna gupta



Submission Date: March 20, 2026
