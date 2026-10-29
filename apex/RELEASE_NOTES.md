# Apex Velocity - Release Notes

## Version 1.4.2 - Supercar Acoustics, Alpine White BMW & AI Race Intelligence

### 1. BMW Strada-R Factory Paint Overhaul
- Updated the default factory finish of the BMW Strada-R sports coupe to authentic Alpine White (`#ffffff`).
- Added contrasting shadow-line gloss black aero trim (`#0f172a`), carbon side splitters, and BMW M-Sport Electric Blue brake calipers (`#0284c7`).
- Updated 3D material shaders to ensure white body paint reflects realistic ambient lighting and environment specular highlights.

### 2. AI Pathfinding, Switchback Isolation & Wrong-Way Recovery
- Resolved issue where bot cars could steer backwards on multi-tier mountain passes (Alpine Pass) and switchbacks.
- Querying track samples now explicitly incorporates 3D elevation altitude and local sample indices, preventing lookahead queries from jumping across vertical tiers.
- Integrated active wrong-way heading detection: if an AI car is spun or knocked off heading by more than 80 degrees, it automatically executes a 180-degree recovery turn back onto the racing line in Gear 1.
- Locked AI drivetrains to forward gears (1..6), preventing bots from ever remaining stuck in reverse gear.

### 3. Eliminate Missing AI Chassis & Floating Wheels Glitch
- Eliminated the glitch where AI bot cars could occasionally render only wheels with a missing chassis body.
- Preserved high-fidelity 3D sculpted supercar/GT procedural bodywork (aerodynamic greenhouse, rear diffuser, splitter, carbon wings, LED lights, interior) for all AI opponents.
- Guaranteed 100% chassis visibility, zero network latency, and zero WebGL instance clipping across the entire grid.

### 4. Continuous Engine Rumble & Deceleration Overrun Acoustics
- Fixed engine sound disappearing when releasing the forward (W/Up) button.
- Designed a dual-architecture hybrid acoustic engine: continuous multi-harmonic mechanical synthesizer coupled with high-fidelity real engine and throttle roar samples.
- When coasting or decelerating with throttle released, authentic engine braking overrun roar (0.35 - 0.85 volume) and exhaust burbles remain prominently audible.
- Stationary idle now delivers a continuous, warm mechanical burble with sub-bass exhaust presence (45 - 120 Hz) that never cuts out.

### 5. Timed Reverse Shift Threshold & Grid Anti-Stall
- Added a 250ms continuous brake-hold threshold before shifting into Reverse (Gear -1) while stationary.
- Eliminates accidental reverse engagement during normal braking to a stop or during race countdown.
- Touching the throttle immediately clears reverse and returns the transmission into 1st gear for instantaneous forward launch.

## Version 1.5.0 - Dynamic Handling Precision, Silky Physics & Photorealistic Circuit Graphics

### 1. Agile Steering Sensitivity & Suspension Jitter Elimination
- Re-calibrated the speed-sensitive steering response: full lock (34 deg) up to 40 km/h, agile turn-in (15 deg) through medium chicanes, and firm high-speed aerodynamic bite (7 deg) for confident apex clipping.
- Boosted steering turn-in responsiveness rate to 12.5 s⁻¹ and flattened input shaping curve for immediate, crisp response on initial keypress.
- Increased physical cornering lateral grip limit to 1.55G, delivering authentic GT3 downforce-assisted handling.
- Replaced laggy suspension spring calculations and hard floor snapping with smooth, critically damped road elevation tracking, eliminating all vertical physics oscillation, stutter, and chattering while moving.

### 2. Camera Angular Oscillation & Wobble Fix
- Replaced mismatched separate position/look-at lerp rates with unified, critically damped camera tracking vectors.
- Camera position and look-at target now track the vehicle in synchronized fluid harmony without micro-jitter or directional fluttering.
