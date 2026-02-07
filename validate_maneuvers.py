import jsbsim
import os
import matplotlib.pyplot as plt
import numpy as np

def run_maneuver(name, duration_sec, control_logic):
    fdm = jsbsim.FGFDMExec(os.path.dirname(jsbsim.__file__))
    fdm.load_model('f16')
    
    # Standard IC
    fdm.set_property_value('ic/h-agl-ft', 10000.0)
    fdm.set_property_value('ic/vc-kts', 450.0)
    fdm.set_property_value('ic/lat-geod-deg', 37.0)
    fdm.set_property_value('ic/long-gc-deg', 127.0)
    fdm.set_property_value('ic/psi-true-deg', 0.0)
    fdm.run_ic()
    
    fdm.set_dt(0.01)
    
    traj = []
    steps = int(duration_sec * 100)
    
    for i in range(steps):
        control_logic(fdm, i)
        fdm.run()
        
        # Check for crash
        if fdm.get_property_value('position/h-agl-ft') < 100:
            print(f"[{name}] Warning: Ground proximity/crash detected.")
            break
            
        x = fdm.get_property_value('position/distance-from-start-lat-ft') * 0.3048
        y = fdm.get_property_value('position/distance-from-start-lon-ft') * 0.3048
        z = fdm.get_property_value('position/h-sl-ft') * 0.3048
        traj.append([x, y, z])
        
    return np.array(traj)

def plot_maneuver(name, data, filename):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(data[:, 1], data[:, 0], data[:, 2], label=name, linewidth=2, color='blue')
    ax.scatter(data[0, 1], data[0, 0], data[0, 2], color='green', label='Start')
    ax.scatter(data[-1, 1], data[-1, 0], data[-1, 2], color='red', label='End')
    ax.set_title(f"Maneuver: {name}")
    ax.set_xlabel('East (m)')
    ax.set_ylabel('North (m)')
    ax.set_zlabel('Alt (m)')
    ax.legend()
    plt.savefig(filename)
    plt.close()

# Maneuvers
def logic_loop(fdm, step):
    fdm.set_property_value('fcs/throttle-cmd-norm', 1.0)
    if step > 50: fdm.set_property_value('fcs/elevator-cmd-norm', -0.8)

def logic_barrel_roll(fdm, step):
    fdm.set_property_value('fcs/throttle-cmd-norm', 0.8)
    if step > 50:
        fdm.set_property_value('fcs/elevator-cmd-norm', -0.3)
        fdm.set_property_value('fcs/aileron-cmd-norm', 0.4)

def logic_split_s(fdm, step):
    fdm.set_property_value('fcs/throttle-cmd-norm', 0.5)
    if step < 100: # Half roll
        fdm.set_property_value('fcs/aileron-cmd-norm', 1.0)
    else: # Pull up (downwards)
        fdm.set_property_value('fcs/aileron-cmd-norm', 0.0)
        fdm.set_property_value('fcs/elevator-cmd-norm', -0.9)

if __name__ == "__main__":
    out_dir = "maneuver_validation"
    os.makedirs(out_dir, exist_ok=True)
    
    maneuvers = [
        ("Loop", 15, logic_loop),
        ("Barrel_Roll", 12, logic_barrel_roll),
        ("Split_S", 10, logic_split_s)
    ]
    
    for name, dur, logic in maneuvers:
        print(f"Generating {name}...")
        data = run_maneuver(name, dur, logic)
        plot_maneuver(name, data, os.path.join(out_dir, f"{name}.png"))
