import mujoco
from mujoco import viewer
import numpy as np
import time


def run_simulation(model_path="xml/dog.xml"):
    model = mujoco.MjModel.from_xml_path(model_path)
    data = mujoco.MjData(model)


    sim_viewer = viewer.launch_passive(model, data)
    while True:
        mujoco.mj_step(model, data)
        sim_viewer.sync()
        time.sleep(0.01)  # Control the simulation speed
    

def main():
    model_path = "xml/dog.xml"
    run_simulation(model_path)

if __name__ == "__main__":
    main()
