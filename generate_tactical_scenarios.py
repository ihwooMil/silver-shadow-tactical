import jsbsim
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def run_simulation(name, ic_h, ic_v, throttle, maneuvers):
    jsbsim_path = os.path.dirname(jsbsim.__file__)
    fdm = jsbsim.FGFDMExec(jsbsim_path)
    fdm.load_model('f16')
    
    dt = 1.0/120.0
    fdm.set_property_value('simulation/dt', dt)
    
    fdm.set_property_value('ic/h-agl-ft', ic_h)
    fdm.set_property_value('ic/vc-kts', ic_v)
    fdm.set_property_value('ic/theta-deg', 3.0)
    fdm.set_property_value('ic/alpha-deg', 3.0)
    
    fdm.run_ic()
    
    for _ in range(100):
        fdm.run()
    
    fdm.set_property_value('propulsion/engine[0]/set-running', 1)
    fdm.set_property_value('fcs/throttle-cmd-norm', throttle)
    
    data = {'t': [], 'x': [], 'y': [], 'z': [], 'v': [], 'pitch': []}
    x, y, z = 0.0, 0.0, ic_h
    
    duration = 40.0
    while fdm.get_sim_time() < duration:
        t = fdm.get_sim_time()
        
        # Default trim
        fdm.set_property_value('fcs/elevator-cmd-norm', -0.06) 
        
        # Apply maneuvers
        for m_t, m_cmd, m_val in maneuvers:
            if t > m_t:
                fdm.set_property_value(m_cmd, m_val)
        
        fdm.run()
        
        vt = fdm.get_property_value('velocities/v-true-fps')
        psi = fdm.get_property_value('attitude/psi-rad')
        theta = fdm.get_property_value('attitude/theta-rad')
        
        dx = vt * np.cos(theta) * np.cos(psi) * dt
        dy = vt * np.cos(theta) * np.sin(psi) * dt
        
        x += dx
        y += dy
        
        data['t'].append(t)
        data['x'].append(x)
        data['y'].append(y)
        data['z'].append(fdm.get_property_value('position/h-agl-ft'))
        
    return data

def plot_and_save(data, title, filename):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    ax.plot(data['x'], data['y'], data['z'], label=title, lw=2.5, color='royalblue')
    ax.scatter(data['x'][0], data['y'][0], data['z'][0], color='green', s=100, label='Start')
    ax.scatter(data['x'][-1], data['y'][-1], data['z'][-1], color='red', s=100, label='End')
    
    ax.set_title(title, fontsize=15)
    ax.set_xlabel('North (ft)')
    ax.set_ylabel('East (ft)')
    ax.set_zlabel('Altitude (ft)')
    
    max_range = np.array([np.max(data['x'])-np.min(data['x']), 
                          np.max(data['y'])-np.min(data['y']), 
                          np.max(data['z'])-np.min(data['z'])]).max() / 2.0
    mid_x = (np.max(data['x'])+np.min(data['x']))/2.0
    mid_y = (np.max(data['y'])+np.min(data['y']))/2.0
    mid_z = (np.max(data['z'])+np.min(data['z']))/2.0
    
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)
    
    ax.legend()
    plt.savefig(filename)
    plt.close()

if __name__ == "__main__":
    os.makedirs('combat_trajectories', exist_ok=True)
    
    # 1. Split-S Maneuver (Evasive/Dive)
    print("Generating Split-S...")
    splits_man = [
        (2.0, 'fcs/aileron-cmd-norm', 1.0),   # Half roll
        (3.5, 'fcs/aileron-cmd-norm', 0.0),   # Stop roll
        (4.0, 'fcs/elevator-cmd-norm', -0.8)  # Pull through loop
    ]
    splits_data = run_simulation('Split-S Maneuver', 25000, 350, 0.4, splits_man)
    plot_and_save(splits_data, 'Split-S Dive', 'combat_trajectories/split_s.png')
    
    # 2. Immelmann Turn (Climb & Reverse)
    print("Generating Immelmann Turn...")
    immel_man = [
        (2.0, 'fcs/elevator-cmd-norm', -0.7), # Half loop up
        (8.0, 'fcs/aileron-cmd-norm', 1.0),   # Half roll at top
        (9.5, 'fcs/aileron-cmd-norm', 0.0)    # Level out
    ]
    immel_data = run_simulation('Immelmann Turn', 10000, 500, 1.0, immel_man)
    plot_and_save(immel_data, 'Immelmann Turn (Vertical Reversal)', 'combat_trajectories/immelmann.png')

    # 3. High-G Barrel Roll
    print("Generating Barrel Roll...")
    barrel_man = [
        (2.0, 'fcs/aileron-cmd-norm', 0.4),
        (2.0, 'fcs/elevator-cmd-norm', -0.5)
    ]
    barrel_data = run_simulation('Barrel Roll', 15000, 400, 0.8, barrel_man)
    plot_and_save(barrel_data, 'High-G Barrel Roll', 'combat_trajectories/barrel_roll.png')

    print("Success: New tactical trajectories saved.")
