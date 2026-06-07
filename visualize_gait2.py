import mujoco
import mujoco.viewer
import numpy as np
import time

# YOUR FINETUNED VALUES
KP = 25.0
KD = 2

def get_walking_targets(sim_time):
    """
    Implements your refined locomotion plan:
    Support: Hip 60 -> 30, Knee 90
    Swing Part 1 (Retract): Hip stays 30, Knee 90 -> 45
    Swing Part 2 (Extend): Hip 30 -> 60, Knee 45 -> 90
    """
    T = 0.6  # SLOW MOTION: 2 seconds per cycle for better analysis
    phase = (sim_time % T) / T
    
    def calculate_angles(p):
        # --- SUPPORT PHASE (0.0 to 0.5) ---
        if p < 0.5:
            s_p = p / 0.5
            # Hip: Starts at 60, reduces to 30 (pushing backward)
            # Using -np.deg2rad as established for your model's orientation
            hip = -np.deg2rad(60 - (30 * s_p))
            knee = np.deg2rad(90)
            
        # --- SWING PHASE (0.5 to 1.0) ---
        else:
            sw_p = (p - 0.5) / 0.5 # Progress within the swing (0 to 1)
            
            # Sub-Phase 1: Retract/Lift (Hip stays still at 30)
            if sw_p < 0.5:
                sub_p = sw_p / 0.5
                hip = -np.deg2rad(30) # Hip stays at 30 per your instruction
                knee = np.deg2rad(90 - (45 * sub_p)) # Knee bends in from 90 to 45
            
            # Sub-Phase 2: Pull Forward (Hip 30->60, Knee 45->90)
            else:
                sub_p = (sw_p - 0.5) / 0.5
                hip = -np.deg2rad(30 + (30 * sub_p)) # Hip pulls forward to 60
                knee = np.deg2rad(45 + (45 * sub_p)) # Knee extends back to 90
        
        return hip, knee

    # Pair 1: Front-Left and Back-Right
    h1, k1 = calculate_angles(phase)
    
    # Pair 2: Front-Right and Back-Left (Opposite Phase)
    h2, k2 = calculate_angles((phase + 0.5) % 1.0)
    
    return {
        "fl_hip_motor": h1, "fl_knee_motor": k1,
        "br_hip_motor": h1, "br_knee_motor": k1,
        "fr_hip_motor": h2, "fr_knee_motor": k2,
        "bl_hip_motor": h2, "bl_knee_motor": k2
    }

def main():
    # Load your dog
    model = mujoco.MjModel.from_xml_path("xml/dog.xml")
    data = mujoco.MjData(model)

    print(model.body_mass)

    # Start the passive viewer
    with mujoco.viewer.launch_passive(model, data) as viewer:
        while viewer.is_running():
            step_start = time.time()

            # 1. Get targets from the staged swing plan
            targets = get_walking_targets(data.time)

            # 2. PD Control Loop
            for i in range(model.nu):
                actuator_name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_ACTUATOR, i)
                joint_idx = model.actuator_trnid[i, 0]
                
                q_adr = model.jnt_qposadr[joint_idx]
                #v_adr = model.jnt_dofadr[joint_idx]
                v_adr = q_adr -1
                
                current_q = data.qpos[q_adr]
                current_v = data.qvel[v_adr]
                #print(current_v)
                
                target_q = targets.get(actuator_name, 0.0)
                
                # Apply PD logic
                error = target_q - current_q
                d_error = 0 - current_v
                
                data.ctrl[i] = (KP * error) + (KD * d_error)


            # 3. Step physics and sync viewer
            mujoco.mj_step(model, data)
            viewer.sync()

            # Maintain real-time sync
            elapsed = time.time() - step_start
            if elapsed < model.opt.timestep:
                time.sleep(model.opt.timestep - elapsed)

if __name__ == "__main__":
    main()