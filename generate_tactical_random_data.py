import jsbsim
import os
import matplotlib.pyplot as plt
import numpy as np
import random

def generate_tactical_stable_data(duration_sec=60, dt=0.01):
    jsbsim_path = os.path.dirname(jsbsim.__file__)
    fdm = jsbsim.FGFDMExec(jsbsim_path)
    
    # F-16 모델 로드
    fdm.load_model('f16')
    
    # 1. 초기 조건 설정 (IC)
    fdm.set_property_value('ic/h-agl-ft', 20000.0)
    fdm.set_property_value('ic/vc-kts', 450.0)
    fdm.set_property_value('ic/theta-deg', 0.0) # 수평 피치
    fdm.set_property_value('ic/alpha-deg', 2.0) # 살짝 받음각 부여
    fdm.run_ic()
    
    # 2. 엔진 강제 기동 및 초기 안정화
    fdm.set_property_value('propulsion/engine[0]/set-running', 1)
    fdm.set_property_value('fcs/throttle-cmd-norm', 0.8) # 순항 추력
    fdm.set_property_value('fcs/mixture-cmd-norm', 1.0)
    
    fdm.set_dt(dt)
    
    # 초기 안정화를 위해 5초간 그냥 흘려보냄 (Pre-run)
    print("Stabilizing flight...")
    for _ in range(int(5.0/dt)):
        fdm.run()

    steps = int(duration_sec / dt)
    data = {
        'time': [], 'alt': [], 'pitch': [], 'roll': [], 'vel': [], 'gload': [],
        'elevator': [], 'aileron': []
    }
    
    curr_el = 0.0
    curr_ai = 0.0
    target_el = 0.0
    target_ai = 0.0
    
    print(f"Generating {duration_sec}s of Tactical Trajectory...")
    
    for i in range(steps):
        t = i * dt
        
        # 전술적 랜덤 기동 (3초마다 변경)
        if i % int(3.0/dt) == 0:
            # BVR/WVR 상황을 모사하여 피치와 롤을 과감하게 사용
            target_el = random.uniform(-0.5, 0.2) # -0.5는 꽤 강하게 당기는 기동
            target_ai = random.uniform(-0.4, 0.4)
            
        # 조종 입력 평활화 (Smoothing)
        curr_el += (target_el - curr_el) * 0.05
        curr_ai += (target_ai - curr_ai) * 0.05
        
        fdm.set_property_value('fcs/elevator-cmd-norm', curr_el)
        fdm.set_property_value('fcs/aileron-cmd-norm', curr_ai)
        fdm.set_property_value('fcs/throttle-cmd-norm', 0.9)
        
        fdm.run()
        
        # 고도가 너무 낮아지면 강제로 기수 올리기 (Safety)
        alt = fdm.get_property_value('position/h-agl-ft')
        if alt < 5000:
            target_el = -0.8 # Pull up!
            
        if i % 10 == 0: # 100Hz 데이터를 10Hz로 기록
            data['time'].append(t)
            data['alt'].append(alt)
            data['pitch'].append(fdm.get_property_value('attitude/theta-deg'))
            data['roll'].append(fdm.get_property_value('attitude/phi-deg'))
            data['vel'].append(fdm.get_property_value('velocities/vc-kts'))
            data['gload'].append(fdm.get_property_value('accelerations/n-pilot-z-norm'))
            data['elevator'].append(curr_el)
            data['aileron'].append(curr_ai)

    # 시각화
    fig, axes = plt.subplots(4, 1, figsize=(12, 14))
    axes[0].plot(data['time'], data['alt'], label='Altitude (ft)')
    axes[0].set_title('Tactical Flight Data (Initialized & Stable)')
    
    axes[1].plot(data['time'], data['pitch'], label='Pitch (deg)', color='orange')
    axes[1].plot(data['time'], data['roll'], label='Roll (deg)', color='red', alpha=0.5)
    
    axes[2].plot(data['time'], data['vel'], label='Velocity (kts)', color='green')
    axes[2].plot(data['time'], [v*10 for v in data['gload']], label='G-Load (x10)', color='purple', linestyle='--')
    
    axes[3].plot(data['time'], data['elevator'], label='Elevator Input')
    axes[3].plot(data['time'], data['aileron'], label='Aileron Input', alpha=0.7)
    
    for ax in axes: ax.legend(); ax.grid(True)
    plt.tight_layout()
    plt.savefig('tactical_stable_trajectory.png')
    print("Stable tactical data generated: 'tactical_stable_trajectory.png'")

if __name__ == "__main__":
    generate_tactical_stable_data()
