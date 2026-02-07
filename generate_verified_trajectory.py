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
    fig = plt.figure(figsize=(15, 10))
    
    # 2D 서브플롯들
    ax1 = fig.add_subplot(2, 2, 1)
    ax1.plot(times, altitudes, color='blue')
    ax1.set_title('Altitude (ft)')
    ax1.grid(True)
    
    ax2 = fig.add_subplot(2, 2, 2)
    ax2.plot(times, speeds, color='green')
    ax2.set_title('Airspeed (kts)')
    ax2.grid(True)
    
    ax3 = fig.add_subplot(2, 2, 4)
    ax3.plot(times, pitches, color='red')
    ax3.set_title('Pitch Angle (deg)')
    ax3.grid(True)
    
    # 3D 궤적 그래프 (NED 좌표계를 고려하여 가시화)
    # 실제 이동 거리를 계산하기 위해 속도를 적분하는 대신, 
    # 간단한 가시화를 위해 위도/경도/고도 변화를 사용하거나 
    # 로컬 좌표계(X, Y, Z)가 있다면 그것을 사용합니다.
    # 여기서는 고도 변화와 시간 흐름에 따른 가상의 X축 이동으로 3D 궤적을 표현합니다.
    
    ax4 = fig.add_subplot(2, 2, 3, projection='3d')
    # 단순 가시화를 위해 X축은 시간*속도, Y축은 0, Z축은 고도로 설정
    x_pos = [t * speeds[0] * 1.68781 for t in times] # kts to ft/s approx
    y_pos = [0] * len(times)
    
    ax4.plot(x_pos, y_pos, altitudes, label='Flight Path', color='purple', lw=2)
    ax4.set_xlabel('Downrange (ft)')
    ax4.set_ylabel('Crossrange (ft)')
    ax4.set_zlabel('Altitude (ft)')
    ax4.set_title('3D Flight Trajectory')
    ax4.legend()
    
    plt.tight_layout()
    plt.savefig('verified_flight_trajectory_3d.png')
    print("3D Trajectory generated: verified_flight_trajectory_3d.png")

if __name__ == "__main__":
    generate_flight_data()
