import jsbsim
import os
import matplotlib.pyplot as plt
import numpy as np

def debug_maneuver(name, duration_sec):
    jsbsim_path = os.path.dirname(jsbsim.__file__)
    fdm = jsbsim.FGFDMExec(jsbsim_path)
    fdm.load_model('f16')
    
    # 확실한 에너지 확보: 20,000ft, 600kts (초고속)
    fdm.set_property_value('ic/h-agl-ft', 20000.0)
    fdm.set_property_value('ic/vc-kts', 600.0)
    fdm.set_property_value('ic/lat-geod-deg', 37.0)
    fdm.set_property_value('ic/long-gc-deg', 127.0)
    fdm.set_property_value('ic/psi-true-deg', 0.0)
    
    # 엔진 강제 가동
    fdm.set_property_value('propulsion/engine[0]/set-running', 1)
    fdm.set_property_value('fcs/throttle-cmd-norm', 1.0)
    
    fdm.run_ic()
    fdm.set_dt(0.01)
    
    traj = []
    print(f"\n--- Debugging Maneuver: {name} ---")
    
    for i in range(int(duration_sec * 100)):
        # 2초간 안정화 후, 아주 부드럽게 기수를 들어올림
        if i > 200:
            # F-16 FBW 모델에서는 pitch-trim이나 elevator-cmd의 부호를 확인해야 함
            # 여기서는 부드러운 상승을 위해 -0.1부터 시작
            fdm.set_property_value('fcs/elevator-cmd-norm', -0.2) 
        
        fdm.run()
        
        alt = fdm.get_property_value('position/h-sl-ft')
        pitch = fdm.get_property_value('attitude/theta-deg')
        
        if i % 100 == 0:
            print(f"Time: {i/100:.1f}s, Alt: {alt:.0f}ft, Pitch: {pitch:.1f}°")
            
        x = fdm.get_property_value('position/distance-from-start-lat-ft') * 0.3048
        y = fdm.get_property_value('position/distance-from-start-lon-ft') * 0.3048
        z = alt * 0.3048 # m
        traj.append([x, y, z])
        
        if alt < 500: break # 추락 방지

    return np.array(traj)

if __name__ == "__main__":
    data = debug_maneuver("Gentle_Climb_Test", 20)
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(data[:, 1], data[:, 0], data[:, 2], label='Climb Path', color='green', linewidth=3)
    ax.set_title("F-16 Steady Climb Validation")
    ax.set_xlabel('East (m)')
    ax.set_ylabel('North (m)')
    ax.set_zlabel('Altitude (m)')
    
    # 시작점 강조 (20,000ft)
    ax.scatter(data[0,1], data[0,0], data[0,2], color='blue', s=100, label='Start (20,000ft)')
    
    plt.savefig('world_model_validation/Climb_Test.png')
    print("Test plot saved to world_model_validation/Climb_Test.png")
