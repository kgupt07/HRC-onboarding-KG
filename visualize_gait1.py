import mujoco
import mujoco.viewer
import numpy as np
import time

# Proportional and Derivative gains
Kp = 5.0 
Kd = 0.05

def pd_control(model, data):
    # Target angles (radians)
    # Adjust these to see the dog move to different poses
    targets = {
        "fl_hip_motor": 0.4, "fl_knee_motor": -0.8,
        "fr_hip_motor": 0.4, "fr_knee_motor": -0.8,
        "bl_hip_motor": 0.4, "bl_knee_motor": -0.8,
        "br_hip_motor": 0.4, "br_knee_motor": -0.8,
    }

    for i in range(model.nu):
        actuator_name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_ACTUATOR, i)
        # trnid[0] is the ID of the joint this actuator attached to
        joint_qpos_adr = model.jnt_qposadr[model.actuator_trnid[i, 0]]
        joint_qvel_adr = model.jnt_dofadr[model.actuator_trnid[i, 0]]
        
        current_pos = data.qpos[joint_qpos_adr]
        current_vel = data.qvel[joint_qvel_adr]
        
        target_pos = targets.get(actuator_name, 0.0)
        error = target_pos - current_pos
        derivative = 0.0 - current_vel 
        
        data.ctrl[i] = (Kp * error) + (Kd * derivative)

def main():
    # Load the model
    model = mujoco.MjModel.from_xml_path("xml/dog.xml")
    data = mujoco.MjData(model)

    # Launch the passive viewer
    with mujoco.viewer.launch_passive(model, data) as viewer:
        while viewer.is_running():
            step_start = time.time()

            # Apply our PD control logic
            pd_control(model, data)

            # Step the physics
            mujoco.mj_step(model, data)

            # Pick up any changes from the viewer (like moving the dog with mouse)
            viewer.sync()

            # Maintain real-time timing
            time_until_next_step = model.opt.timestep - (time.time() - step_start)
            if time_until_next_step > 0:
                time.sleep(time_until_next_step)

if __name__ == "__main__":
    main()