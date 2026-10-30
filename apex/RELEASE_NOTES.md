# Apex Velocity - Release Notes

## Version 1.5.3 - 3D Garage Vehicle Framing, Interactive Inspection & Formula 1 Dynamics

### 1. 3D Garage Vehicle Framing & Card Occlusion Fix
- Resolved issue where vehicles were rendered in the center of the viewport and partially hidden behind the vehicle specifications card.
- Implemented lateral pan framing in the showroom camera (`panOffset = 1.45m`), shifting the rendered car into the open right ~64% of the viewport.
- Supercars (Ferrari 458, Lamborghini Huracán, BMW M4) are now 100% visible from nose to tail without any overlap from the UI card.
- Compacted the specifications card to 370px width with refined padding and glassmorphism backdrop blur.

### 2. Interactive 3D Orbit & Zoom Showroom Inspection
- Enabled full 360-degree interactive camera orbit inspection: click and drag with mouse/touch to rotate around the vehicle at any angle.
- Added vertical elevation adjustment (0.65m to 3.2m) to inspect roof aerodynamics and ground diffuser channels.
- Added mouse wheel zoom (3.8m to 7.8m distance) to inspect detailed alloy wheel spokes, brake calipers, and cockpit interior.
- Added intelligent auto-spin resume with smooth timer pause during manual inspection.

### 3. Formula 1 Aerodynamic Downforce & Precision Controls
- Implemented realistic aerodynamic ground-effect downforce physics ($F_{\text{downforce}} = \frac{1}{2} \rho C_{df} A v^2$).
- Downforce increases tire normal load ($F_N = mg + F_{\text{downforce}}$), providing massive high-speed lateral grip up to 4.5G for glued-down "on-rails" cornering without slide washout or wall collisions.
- Upgraded steering response to Formula 1 race rack calibration: 18.5 s⁻¹ turn-in responsiveness, 24.0 s⁻¹ snap-centering, and direct linear rack response.
- Integrated carbon-composite high-speed aerodynamic braking scaling with downforce, allowing late, aggressive braking into apexes.


## Version 1.5.2 - Supercar Alignment, Per-Gear Speed Limits & Wheel Mesh Fix

### 1. Ferrari 458 Italia Grid & Driving Orientation Correction
- Resolved the critical bug where the green Ferrari 458 Italia (Veloce GT-R) was loaded 180 degrees reversed, facing backwards toward the camera on the starting grid.
- Inspected the internal GLTF coordinate system of `ferrari.glb` (headlights at $Z = -1.84$, taillights at $Z = +0.91$) and applied a 180-degree yaw rotation (`rotation.y = Math.PI`).
- The Ferrari now points forward down the race track along $+Z$ on the starting grid and throughout the race with authentic rear-chase camera perspective.

### 2. Elimination of Floating Overhead Tyres & Duplicate Wheel Meshes
- Resolved the visual glitch where procedural wheel assemblies were flung into the air and floated near overhead track structures.
- Corrected double coordinate transformation in wheel placement by anchoring wheels strictly in local coordinate offsets relative to the vehicle root chassis.
- When loading high-fidelity 3D supercar models (Ferrari 458, Lamborghini Huracán, BMW M4) that feature integrated wheel geometries, procedural wheel meshes are automatically hidden (`w.visible = false`), eliminating duplicate or ghost floating wheels.

### 3. Physical Gear-Specific Speed Limits & Rev Limiter Governor
- Implemented real-world physical transmission mechanics where each individual gear possesses a strict top speed calculated from the drivetrain gear ratio, final drive, tire rolling radius, and engine redline RPM ($v_{\max} = \frac{\text{redlineRpm} \times 2\pi r_{\text{tire}}}{60 \times |R_g| \times F_d} \times 3.6$ km/h).
- In lower gears (such as 1st gear), vehicles can no longer accelerate endlessly into triple-digit speeds:
  - Strada-R: 1st $\le 58.8$ km/h, 2nd $\le 98.5$ km/h, 3rd $\le 139.4$ km/h, 4th $\le 179.5$ km/h, 5th $\le 223$ km/h, 6th $\le 260$ km/h.
  - Veloce GT-R (Ferrari): 1st gear strictly capped at $72.6$ km/h.
  - Reverse (Gear -1): Governed strictly to 42 km/h.
- Added progressive fuel cut power tapering between 90% and 100% of gear redline, realistic rev limiter stutter bounce at 98%, and authentic engine overrun compression braking when downshifting or overspeeding in lower gears.


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
