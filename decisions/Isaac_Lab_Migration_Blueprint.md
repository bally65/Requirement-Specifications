# Migration Blueprint: Transitioning to NVIDIA Isaac Lab 🌌

**Subject**: Moving Archimedes' Hand from MuJoCo to Isaac Lab for Photorealistic Multi-Terrain Simulation.

## 1. Why Isaac Lab?
- **Scale**: Ability to simulate 1000+ robots in parallel on a single GPU.
- **Visuals**: RTX-based rendering for realistic water, mud, and light interaction.
- **Terrains**: Native support for Procedural Terrain Generation (Forests, Dunes, Rocky ground).

## 2. Migration Phases

### Phase 1: Asset Conversion 🛠️
- Convert our `archimedes_hand_mujoco.xml` into **URDF** or **USD (Universal Scene Description)** format.
- **Action Item**: Use `mujoco_to_usd` tools or manual URDF mapping.

### Phase 2: Locomotion Logic Porting ⚙️
- Port the screw propulsion physics (torque-to-displacement) into **PhysX 5**.
- Adapt the reward function from `WholeBodyEnv.py` to Isaac Lab's `Manager-based` environment structure.

### Phase 3: Perceptive Training 👁️
- Add RTX-Lidar and Depth Cameras.
- Train the "Terrain Prediction" model using raw visual pixels instead of just numeric height maps.

## 3. Current Progress
- [ ] Researching Isaac Lab URDF importer.
- [ ] Identifying hardware requirements (RTX 3080+ recommended).
- [ ] Initializing environment config file.

---
*Blueprint curated by Antigravity Agent • 2026-02-13*
