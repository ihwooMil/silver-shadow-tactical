import jsbsim
import os
import matplotlib.pyplot as plt
import numpy as np
import random

def generate_tactical_data(duration_sec=60, dt=0.1):
    jsbsim_path = os.path.dirname(jsbsim.__file__)
    fdm = jsbsim.FGFDMExec(jsbsim_path)
    
    # 고기동 전투기 모델 F-16 로드
    try:
        fdm.load_model('f16')
    except:
        print("F-16 model not found, falling back to c172x for structure check.")
        fdm.load_model('c172x')
    
    # 초기 조건: 고공 고속 상태 (BVR 시작 상황 가정)
    fdm.set_property_value('ic/h-agl-ft', 20000.0)
    fdm.set_property_value('ic/vc-kts', 450.0)
    fdm.run_ic()
    
    fdm.set_dt(dt)
    
    steps = int(duration_sec / dt)
    data = {
        'time': [], 'alt': [], 'pitch': [], 'roll': [], 'yaw': [], 'vel': [],
        'elevator': [], 'aileron': [], 'rudder': [], 'throttle': []
    }
    
    # 제어값 변화를 위한 상태
    curr_el = 0.0
    curr_ai = 0.0
    curr_ru = 0.0
    
    print(f"Generating {duration_sec}s of Randomized Tactical Trajectory...")
    
    for i in range(steps):
        t = i * dt
        
        # 2~3초마다 조종 입력을 랜덤하게 변경 (전술적 기동 모사)
        if i % int(2.5/dt) == 0:
            target_el = random.uniform(-0.8, 0.4) # Elevator: 주로 당기는(Pull) 기동이 많음
            target_ai = random.uniform(-0.6, 0.6) # Aileron: 급격한 롤
            target_ru = random.uniform(-0.2, 0.2) # Rudder: 보조
        
        # 입력을 부드럽게 변화 (Smoothing)
        curr_el += (target_el - curr_el) * 0.1
        curr_ai += (target_ai - curr_ai) * 0.1
        curr_ru += (target_ru - curr_ru) * 0.1
        
        fdm.set_property_value('fcs/elevator-cmd-norm', curr_el)
        fdm.set_property_value('fcs/aileron-cmd-norm', curr_ai)
        fdm.set_property_value('fcs/rudder-cmd-norm', curr_ru)
        fdm.set_property_value('fcs/throttle-cmd-norm', 1.0) # 전투 시에는 보통 Full Power
        fdm.set_property_value('propulsion/engine[0]/set-running', 1)
        
        fdm.run()
        
        # 데이터 추출
        data['time'].append(t)
        data['alt'].append(fdm.get_property_value('position/h-agl-ft'))
        data['pitch'].append(fdm.get_property_value('attitude/theta-deg'))
        data['roll'].append(fdm.get_property_value('attitude/phi-deg'))
        data['yaw'].append(fdm.get_property_value('attitude/psi-deg'))
        data['vel'].append(fdm.get_property_value('velocities/vc-kts'))
        data['elevator'].append(curr_el)
        data['aileron'].append(curr_ai)

    # 시각화
    fig, axes = plt.subplots(4, 1, figsize=(12, 12))
    axes[0].plot(data['time'], data['alt'], label='Altitude (ft)')
    axes[1].plot(data['time'], data['pitch'], label='Pitch (deg)', color='orange')
    axes[1].plot(data['time'], data['roll'], label='Roll (deg)', color='red', alpha=0.5)
    axes[2].plot(data['time'], data['vel'], label='Velocity (kts)', color='green')
    axes[3].plot(data['time'], data['elevator'], label='Elevator Input')
    axes[3].plot(data['time'], data['aileron'], label='Aileron Input', alpha=0.7)
    
    for ax in axes: ax.legend(); ax.grid(True)
    plt.tight_layout()
    plt.savefig('tactical_random_trajectory.png')
    print("Randomized tactical data generated: 'tactical_random_trajectory.png'")

if __name__ == "__main__":
    generate_tactical_data()
