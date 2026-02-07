import jsbsim
import os
import matplotlib.pyplot as plt
import numpy as np

def verify_jsbsim_flight():
    jsbsim_path = os.path.dirname(jsbsim.__file__)
    fdm = jsbsim.FGFDMExec(jsbsim_path)
    
    # 안정적인 C172 모델로 테스트
    fdm.load_model('c172x')
    
    # 초기 조건: 3000ft, 100kts
    fdm.set_property_value('ic/h-agl-ft', 3000.0)
    fdm.set_property_value('ic/vc-kts', 100.0)
    fdm.run_ic()
    
    # 엔진 강제 시동 및 스로틀 풀 가동
    fdm.set_property_value('propulsion/engine[0]/set-running', 1)
    fdm.set_property_value('fcs/throttle-cmd-norm', 1.0)
    fdm.set_property_value('fcs/mixture-cmd-norm', 1.0) # 연료 혼합비 최대로
    
    fdm.set_dt(0.01)
    
    traj = []
    print("\n--- Real Flight Verification (Cessna 172) ---")
    
    for i in range(3000): # 30초
        # 5초 후부터 완만하게 기수 들기
        if i > 500:
            fdm.set_property_value('fcs/elevator-cmd-norm', -0.15)
        
        fdm.run()
        
        alt = fdm.get_property_value('position/h-sl-ft')
        thrust = fdm.get_property_value('propulsion/engine[0]/thrust-lbs')
        pitch = fdm.get_property_value('attitude/theta-deg')
        v_fps = fdm.get_property_value('velocities/v-fps')
        
        if i % 200 == 0:
            print(f"Time: {i/100:>4.1f}s | Thrust: {thrust:>6.1f} lbs | Alt: {alt:>6.1f} ft | Pitch: {pitch:>5.1f}° | Speed: {v_fps:>6.1f} fps")
            
        # 좌표 수집 (East-North-Up)
        # 거리를 위도/경도로부터 계산하지 않고 직접 velocity 적분 혹은 JSBSim 내부 거리 속성 사용
        x = fdm.get_property_value('position/distance-from-start-lat-ft') * 0.3048
        y = fdm.get_property_value('position/distance-from-start-lon-ft') * 0.3048
        z = alt * 0.3048
        traj.append([x, y, z])
        
        if alt < 100:
            print("Crash detected!")
            break

    return np.array(traj)

if __name__ == "__main__":
    data = verify_jsbsim_flight()
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(data[:, 1], data[:, 0], data[:, 2], label='C172 Flight Path', color='blue', linewidth=3)
    ax.set_title("JSBSim C172 Flight Path Verification")
    ax.set_xlabel('East (m)')
    ax.set_ylabel('North (m)')
    ax.set_zlabel('Altitude (m)')
    ax.legend()
    
    os.makedirs('world_model_validation', exist_ok=True)
    plt.savefig('world_model_validation/C172_Verified.png')
    print("\nVerified plot saved as world_model_validation/C172_Verified.png")
