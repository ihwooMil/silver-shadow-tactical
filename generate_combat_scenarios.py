import jsbsim
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def run_simulation(name, ic_h, ic_v, throttle, maneuvers):
    jsbsim_path = os.path.dirname(jsbsim.__file__)
    fdm = jsbsim.FGFDMExec(jsbsim_path)
    fdm.load_model('f16')
    
    fdm.set_property_value('simulation/dt', 1.0/120.0)
    fdm.set_property_value('ic/h-agl-ft', ic_h)
    fdm.set_property_value('ic/vc-kts', ic_v)
    fdm.set_property_value('ic/theta-deg', 0.0)
    fdm.set_property_value('ic/alpha-deg', 2.0)
    
    fdm.run_ic()
    for _ in range(10): fdm.run() # Warmup
    
    fdm.set_property_value('propulsion/engine[0]/set-running', 1)
    fdm.set_property_value('fcs/throttle-cmd-norm', throttle)
    
    data = {'t': [], 'x': [], 'y': [], 'z': [], 'v': [], 'pitch': []}
    x, y = 0.0, 0.0
    
    duration = 20.0
    while fdm.get_sim_time() < duration:
        t = fdm.get_sim_time()
        
        # Apply maneuvers
        for m_t, m_cmd, m_val in maneuvers:
            if t > m_t:
                fdm.set_property_value(m_cmd, m_val)
        
        fdm.run()
        
        # Calculate local position (simplified integration)
        vt = fdm.get_property_value('velocities/v-true-fps')
        psi = fdm.get_property_value('attitude/psi-rad')
        theta = fdm.get_property_value('attitude/theta-rad')
        
        dt = 1.0/120.0
        x += vt * np.cos(theta) * np.cos(psi) * dt
        y += vt * np.cos(theta) * np.sin(psi) * dt
        
        data['t'].append(t)
        data['x'].append(x)
        data['y'].append(y)
        data['z'].append(fdm.get_property_value('position/h-agl-ft'))
        data['v'].append(fdm.get_property_value('velocities/vc-kts'))
        data['pitch'].append(fdm.get_property_value('attitude/theta-deg'))
        
    return data

def plot_and_save(data, title, filename):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(data['x'], data['y'], data['z'], label=title, lw=2, color='blue')
    ax.set_title(title)
    ax.set_xlabel('X (ft)')
    ax.set_ylabel('Y (ft)')
    ax.set_zlabel('Altitude (ft)')
    ax.legend()
    plt.savefig(filename)
    plt.close()

if __name__ == "__main__":
    os.makedirs('combat_trajectories', exist_ok=True)
    
    # 1. BVR: High Altitude Intercept (Straight, High Speed, Slight Climb)
    print("Generating BVR Trajectory...")
    bvr_maneuvers = [(2.0, 'fcs/elevator-cmd-norm', -0.05)]
    bvr_data = run_simulation('BVR Intercept', 35000, 600, 1.0, bvr_maneuvers)
    plot_and_save(bvr_data, 'BVR High-Altitude Intercept', 'combat_trajectories/bvr_intercept.png')
    
    # 2. WVR: Defensive Break (Hard Turn & Dive)
    print("Generating WVR Defensive Break...")
    wvr_maneuvers = [
        (1.0, 'fcs/aileron-cmd-norm', 0.6),  # Roll
        (2.0, 'fcs/elevator-cmd-norm', 0.8), # Pull hard (into dive since rolled)
        (4.0, 'fcs/aileron-cmd-norm', 0.0)   # Stop roll
    ]
    wvr_data = run_simulation('WVR Defensive Break', 15000, 400, 1.0, wvr_maneuvers)
    plot_and_save(wvr_data, 'WVR Defensive Break Turn', 'combat_trajectories/wvr_break.png')

    # 3. WVR: High-Yoyo / Pitch back
    print("Generating WVR Combat Turn...")
    yoyo_maneuvers = [
        (1.0, 'fcs/elevator-cmd-norm', -0.6), # Pitch up
        (3.0, 'fcs/aileron-cmd-norm', 0.4),   # Bank
    ]
    yoyo_data = run_simulation('WVR Combat Maneuver', 10000, 450, 1.0, yoyo_maneuvers)
    plot_and_save(yoyo_data, 'WVR Combat Maneuver (Climb & Bank)', 'combat_trajectories/wvr_maneuver.png')

    print("All combat trajectories generated in combat_trajectories/")
