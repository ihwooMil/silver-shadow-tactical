import jsbsim
import os
import matplotlib.pyplot as plt
import numpy as np

def run_maneuver(name, duration_sec, control_logic):
    jsbsim_path = os.path.dirname(jsbsim.__file__)
    fdm = jsbsim.FGFDMExec(jsbsim_path)
    fdm.load_model('f16')
    
    # 초고속 고고도 초기 조건 (에너지 충분히!)
    fdm.set_property_value('ic/h-agl-ft', 20000.0)
    fdm.set_property_value('ic/vc-kts', 500.0) # 500 kts
    fdm.set_property_value('ic/lat-geod-deg', 37.0)
    fdm.set_property_value('ic/long-gc-deg', 127.0)
    fdm.set_property_value('ic/psi-true-deg', 0.0)
    fdm.set_property_value('propulsion/engine[0]/set-running', 1)
    fdm.set_property_value('fcs/throttle-cmd-norm', 1.0)
    
    fdm.run_ic()
    fdm.set_dt(0.01)
    
    traj = []
    steps = int(duration_sec * 100)
    
    for i in range(steps):
        control_logic(fdm, i)
        fdm.run()
        
        alt = fdm.get_property_value('position/h-sl-ft') * 0.3048
        if alt < 100: # 지면 충돌 시 중단
            break
            
        x = fdm.get_property_value('position/distance-from-start-lat-ft') * 0.3048
        y = fdm.get_property_value('position/distance-from-start-lon-ft') * 0.3048
        traj.append([x, y, alt])
        
    return np.array(traj)

def plot_maneuver(name, data, filename):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    # 궤적 그리기
    ax.plot(data[:, 1], data[:, 0], data[:, 2], label=name, linewidth=3, color='magenta')
    # 시작/끝 점
    ax.scatter(data[0, 1], data[0, 0], data[0, 2], color='green', s=100, label='Start')
    ax.scatter(data[-1, 1], data[-1, 0], data[-1, 2], color='red', s=100, label='End')
    
    ax.set_title(f"Combat Maneuver: {name} (F-16 6DOF)")
    ax.set_xlabel('East-West (m)')
    ax.set_ylabel('North-South (m)')
    ax.set_zlabel('Altitude (m)')
    ax.legend()
    plt.savefig(filename)
    plt.close()

# 1. Loop: 예쁘게 수직 원 그리기
def logic_loop(fdm, step):
    fdm.set_property_value('fcs/throttle-cmd-norm', 1.0)
    if step > 100: # 1초간 수평 비행 후 당기기
        fdm.set_property_value('fcs/elevator-cmd-norm', -0.5) # 적당한 G로 당김

# 2. Level Turn: 고도 유지하며 360도 선회
def logic_turn(fdm, step):
    fdm.set_property_value('fcs/throttle-cmd-norm', 1.0)
    if step > 100:
        fdm.set_property_value('fcs/aileron-cmd-norm', 0.4) # 롤 먼저
        if step > 150: # 롤이 어느 정도 들어가면 피치 당김
            fdm.set_property_value('fcs/elevator-cmd-norm', -0.4)

# 3. High Climb: 급상승
def logic_climb(fdm, step):
    fdm.set_property_value('fcs/throttle-cmd-norm', 1.0)
    if step > 50:
        fdm.set_property_value('fcs/elevator-cmd-norm', -0.3)

if __name__ == "__main__":
    out_dir = "world_model_validation"
    os.makedirs(out_dir, exist_ok=True)
    
    tasks = [
        ("Loop_V2", 20, logic_loop),
        ("Sustained_Turn", 20, logic_turn),
        ("Zoom_Climb", 15, logic_climb)
    ]
    
    for name, dur, logic in tasks:
        print(f"Generating {name}...")
        data = run_maneuver(name, dur, logic)
        plot_maneuver(name, data, os.path.join(out_dir, f"{name}.png"))
