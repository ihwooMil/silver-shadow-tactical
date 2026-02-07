import jsbsim
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def generate_working_trajectory():
    # 데이터 경로 설정
    jsbsim_path = os.path.dirname(jsbsim.__file__)
    fdm = jsbsim.FGFDMExec(jsbsim_path)
    
    # 모델 로드
    fdm.load_model('f16')
    
    # 초기 조건 직접 설정 (파일 없이)
    fdm.set_property_value('ic/h-agl-ft', 5000.0)
    fdm.set_property_value('ic/vc-kts', 350.0)
    fdm.set_property_value('ic/long-gc-deg', 127.0)
    fdm.set_property_value('ic/lat-geod-deg', 37.0)
    fdm.set_property_value('ic/psi-true-deg', 0.0)
    
    # 초기화 실행
    fdm.run_ic()
    fdm.set_dt(0.01) # 100Hz
    
    positions = []
    
    print("Simulating a dynamic Fighter maneuver...")
    
    # 30초 시뮬레이션 (3000스텝)
    for i in range(3000):
        # 1초 후부터 기동 시작
        if i > 100:
            # Full Throttle + Hard Bank + Pull Up (High-G Turn)
            fdm.set_property_value('fcs/throttle-cmd-norm', 1.0)
            fdm.set_property_value('fcs/aileron-cmd-norm', 0.3)  # 오른쪽으로 롤
            fdm.set_property_value('fcs/elevator-cmd-norm', -0.7) # 기수 들기 (선회 가속)
            
        fdm.run()
        
        # NED 좌표계 또는 거리를 직접 계산
        # JSBSim의 distance-from-start-lat/lon 속성 활용
        x = fdm.get_property_value('position/distance-from-start-lat-ft') * 0.3048
        y = fdm.get_property_value('position/distance-from-start-lon-ft') * 0.3048
        z = fdm.get_property_value('position/h-sl-ft') * 0.3048
        
        positions.append([x, y, z])

    pos_array = np.array(positions)
    
    # 3D 시각화
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # 궤적 (보라색 계열로 섹시하게!)
    ax.plot(pos_array[:, 1], pos_array[:, 0], pos_array[:, 2], color='#ff00ff', linewidth=3, label='F-16 Combat Turn')
    
    # 포인트 표시
    ax.scatter(pos_array[0, 1], pos_array[0, 0], pos_array[0, 2], color='green', s=100, label='Start (5000ft)')
    ax.scatter(pos_array[-1, 1], pos_array[-1, 0], pos_array[-1, 2], color='red', s=100, label='End')
    
    ax.set_xlabel('East (m)')
    ax.set_ylabel('North (m)')
    ax.set_zlabel('Altitude (m)')
    ax.set_title('F-16 High-G Turning Maneuver (6DOF)')
    ax.legend()
    
    # 배경 그리드 강조
    ax.grid(True, linestyle='--', alpha=0.6)
    
    plt.savefig('fighter_turn.png')
    print("Maneuver plot saved as fighter_turn.png")

if __name__ == "__main__":
    generate_working_trajectory()
