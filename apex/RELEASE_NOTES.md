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
