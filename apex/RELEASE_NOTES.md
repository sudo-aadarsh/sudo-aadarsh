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

## Version 1.5.1 - Gantry Structural Alignment, Pure Alpine White BMW M4 & Realistic Circuit Lighting

### 1. Overhead Gantry Structural Orientation & Pitch-Black Monolith Elimination
- Resolved the critical bug where start/finish and sponsor gantry crossbars were rotated 90 degrees longitudinally along the track.
- Replaced angular rotation calculations with exact 3D orthonormal basis matrices (`makeBasis(binormal, normal, tangent)`), guaranteeing crossbars cleanly span from the left pillar to the right pillar across the exact road width on all banked, climbing, and winding track segments.
- Completely eliminated the floating 25-meter black slab that previously cast unwanted shadows and obstructed overhead driver visibility.
- Upgraded gantry truss materials to high-grade galvanized motorsport steel (`0x94a3b8`) with reflective metallic PBR shading.
- Mounted 5 red FIA starting lamps directly onto the front face of the start/finish crossbar facing the starting grid.
- Integrated high-output downward-pointing LED track illuminator strips beneath every gantry, bathing the start straight and sector checkpoints in radiant race lighting.
- Installed double-sided sponsor banners facing both oncoming and exiting traffic across sectors.

### 2. Full Pure Alpine White BMW M4 Body Recolor
- Resolved issue where baked diffuse textures kept the rear quarter panels, trunk lid, and rear bumper of the BMW M4 dark.
- Stripped baked diffuse maps from bodywork shaders and recolored all exterior panels (`white41`, `body151`, `black161`, `black151`, `ff41`, `tail71`, `zx1`, `livery`) to pure glossy Alpine White (`#ffffff` / `0xf8fafc`) with multi-coat automotive clear coat (`roughness: 0.16, metalness: 0.84`).
- Preserved authentic contrasting shadow-line details: gloss-black kidney grilles, tinted glass, red LED taillight clusters, chrome quad exhaust tips, and iconic blue/white BMW roundel emblems.
- Added dynamic body paint recoloring for Lamborghini models (`Mt_Body`).


### 1. Agile Steering Sensitivity & Suspension Jitter Elimination
- Re-calibrated the speed-sensitive steering response: full lock (34 deg) up to 40 km/h, agile turn-in (15 deg) through medium chicanes, and firm high-speed aerodynamic bite (7 deg) for confident apex clipping.
- Boosted steering turn-in responsiveness rate to 12.5 s⁻¹ and flattened input shaping curve for immediate, crisp response on initial keypress.
- Increased physical cornering lateral grip limit to 1.55G, delivering authentic GT3 downforce-assisted handling.
- Replaced laggy suspension spring calculations and hard floor snapping with smooth, critically damped road elevation tracking, eliminating all vertical physics oscillation, stutter, and chattering while moving.

### 2. Camera Angular Oscillation & Wobble Fix
- Replaced mismatched separate position/look-at lerp rates with unified, critically damped camera tracking vectors.
- Camera position and look-at target now track the vehicle in synchronized fluid harmony without micro-jitter or directional fluttering.

### 3. Glowing Carbon-Ceramic Brake Rotors & Dynamic Exhaust Flames
- Fixed brake detection logic in vehicle physics so brake lights and brake rotor effects activate reliably during high-speed deceleration.
- Carbon-ceramic brake rotors glow with incandescent molten cherry-red / orange emissive heat (up to 2.2 intensity) under hard braking and dissipate heat naturally through corner exits.
- Added dynamic 3D exhaust backfire flame cones erupting with cyan-blue core and orange outer bursts during high-rev downshifts and overrun pops.

### 4. Realistic Circuit Architecture, Braking Boards & Overhead Sponsor Gantries
- Added 3D corner braking distance countdown boards (150m, 100m, 50m) approaching every heavy braking zone with bold high-contrast FIA styling.
- Installed high-resolution black-and-white checkered start/finish line spanning the entire road width alongside painted grid boxes (1 to 6).
- Built overhead illuminated race sponsor gantries (Apex Velocity Grand Prix, Brembo, Pirelli, Shell V-Power, Motul) across circuit sectors with glowing LED telemetry backlighting.
- Installed stacked red-and-white motorsport tire walls (Tecpro) along high-curvature corner runoff zones.
