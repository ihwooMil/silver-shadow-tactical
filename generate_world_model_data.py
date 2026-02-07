import jsbsim
import os
import matplotlib.pyplot as plt

def generate_trajectory():
    jsbsim_path = os.path.dirname(jsbsim.__file__)
    fdm = jsbsim.FGFDMExec(jsbsim_path)
    
    # Cessna 172 모델 로드
    fdm.load_model('c172x')
    
    # 초기 조건 설정 (순항 상태)
    fdm.set_property_value('ic/h-agl-ft', 5000.0)
    fdm.set_property_value('ic/vc-kts', 100.0)
    fdm.run_ic()
    
    # 시뮬레이션 설정
    dt = 0.1
    fdm.set_dt(dt)
    
    # 데이터 저장을 위한 리스트
    times = []
    pitches = []
    altitudes = []
    velocities = []
    
    print("Generating 30s flight trajectory...")
    
    for i in range(300): # 30초 시뮬레이션
        t = i * dt
        
        # 엔진 가동 및 스로틀 최대
        fdm.set_property_value('fcs/throttle-cmd-norm', 1.0)
        fdm.set_property_value('fcs/mixture-cmd-norm', 1.0)
        fdm.set_property_value('propulsion/engine[0]/set-running', 1)
        
        # 5초~15초 사이에 엘리베이터를 서서히 당겨서 상승 시도
        if 5.0 <= t < 15.0:
            fdm.set_property_value('fcs/elevator-cmd-norm', -0.2)
        elif 15.0 <= t < 25.0:
            fdm.set_property_value('fcs/elevator-cmd-norm', 0.1) # 다시 기수 숙이기
        else:
            fdm.set_property_value('fcs/elevator-cmd-norm', 0.0)
            
        fdm.run()
        
        # 데이터 수집
        times.append(t)
        pitches.append(fdm.get_property_value('attitude/theta-deg'))
        altitudes.append(fdm.get_property_value('position/h-agl-ft'))
        velocities.append(fdm.get_property_value('velocities/vc-kts'))

    # 결과 플롯 생성
    plt.figure(figsize=(12, 8))
    
    plt.subplot(3, 1, 1)
    plt.plot(times, altitudes, label='Altitude (ft)')
    plt.ylabel('Altitude')
    plt.legend()
    
    plt.subplot(3, 1, 2)
    plt.plot(times, pitches, label='Pitch (deg)', color='orange')
    plt.ylabel('Pitch')
    plt.legend()
    
    plt.subplot(3, 1, 3)
    plt.plot(times, velocities, label='Velocity (kts)', color='green')
    plt.xlabel('Time (s)')
    plt.ylabel('Velocity')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('world_model_trajectory.png')
    print("Trajectory data generated and saved to 'world_model_trajectory.png'")

if __name__ == "__main__":
    generate_trajectory()
