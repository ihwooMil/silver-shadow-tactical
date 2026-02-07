import jsbsim
import os
import matplotlib.pyplot as plt

def generate_flight_data():
    jsbsim_path = os.path.dirname(jsbsim.__file__)
    fdm = jsbsim.FGFDMExec(jsbsim_path)
    fdm.load_model('f16')
    
    # 시간 스텝 설정 (권장값 0.0083s ~ 120Hz)
    dt = 1.0/120.0
    fdm.set_property_value('simulation/dt', dt)
    
    # 초기 조건 설정
    fdm.set_property_value('ic/h-agl-ft', 20000.0)
    fdm.set_property_value('ic/vc-kts', 500.0)
    fdm.set_property_value('ic/theta-deg', 0.0)
    fdm.set_property_value('ic/alpha-deg', 2.0)
    
    # 엔진 가동
    fdm.set_property_value('propulsion/engine[0]/set-running', 1)
    fdm.set_property_value('fcs/throttle-cmd-norm', 0.8)
    
    fdm.run_ic()
    
    # 해결책 1: 워밍업 스텝 (5회 호출)
    for _ in range(5):
        fdm.run()
        
    # 데이터 수집 (10초 비행)
    time_limit = 10.0
    times = []
    altitudes = []
    speeds = []
    pitches = []
    lifts = []
    
    print("\n--- Starting Data Collection (Warmed up) ---")
    
    while fdm.get_sim_time() < time_limit:
        # 기동 시뮬레이션: 2초에 Pitch Up 시작
        if fdm.get_sim_time() > 2.0:
            fdm.set_property_value('fcs/elevator-cmd-norm', -0.2)
            
        fdm.run()
        
        times.append(fdm.get_sim_time())
        altitudes.append(fdm.get_property_value('position/h-agl-ft'))
        speeds.append(fdm.get_property_value('velocities/vc-kts'))
        pitches.append(fdm.get_property_value('attitude/theta-deg'))
        lifts.append(fdm.get_property_value('forces/lift-lbs'))

    # 그래프 생성
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    axes[0, 0].plot(times, altitudes)
    axes[0, 0].set_title('Altitude (ft)')
    axes[0, 0].grid(True)
    
    axes[0, 1].plot(times, speeds)
    axes[0, 1].set_title('Airspeed (kts)')
    axes[0, 1].grid(True)
    
    axes[1, 0].plot(times, pitches)
    axes[1, 0].set_title('Pitch Angle (deg)')
    axes[1, 0].grid(True)
    
    axes[1, 1].plot(times, lifts)
    axes[1, 1].set_title('Lift Force (lbs)')
    axes[1, 1].grid(True)
    
    plt.tight_layout()
    plt.savefig('verified_flight_trajectory.png')
    print("Trajectory generated: verified_flight_trajectory.png")

if __name__ == "__main__":
    generate_flight_data()
