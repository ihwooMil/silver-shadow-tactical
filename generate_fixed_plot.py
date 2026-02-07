import jsbsim
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def generate_accurate_trajectory():
    fdm = jsbsim.FGFDMExec(os.path.dirname(jsbsim.__file__))
    
    try:
        fdm.load_model('f16')
    except:
        fdm.load_model('c172x')
    
    # 초기 조건 설정: 공중에서 시작 (5000ft, 350kts)
    fdm.set_property_value('ic/h-agl-ft', 5000)
    fdm.set_property_value('ic/vc-kts', 350)
    fdm.set_property_value('ic/gamma-deg', 0)
    fdm.load_ic('reset00', False) # IC 로드 시 초기화 보존
    fdm.run_ic()
    
    fdm.set_dt(0.01) # 100Hz
    
    # 초기 좌표 저장
    start_lat = fdm.get_property_value('position/lat-geod-rad')
    start_lon = fdm.get_property_value('position/long-gc-rad')
    
    positions = []
    
    print("Simulating a High-G 360-degree Turn...")
    
    # 20초간 시뮬레이션 (2000스텝)
    for i in range(2000):
        # 기동 명령: 60도 뱅크 넣고 팍 당기기
        if i < 100: # 준비
            fdm.set_property_value('fcs/throttle-cmd-norm', 1.0)
        else:
            # 강한 롤(Aileron)과 피치(Elevator)를 주어 급선회 유도
            fdm.set_property_value('fcs/aileron-cmd-norm', 0.4) 
            fdm.set_property_value('fcs/elevator-cmd-norm', -0.6)
            
        fdm.run()
        
        # 현재 좌표 추출
        curr_lat = fdm.get_property_value('position/lat-geod-rad')
        curr_lon = fdm.get_property_value('position/long-gc-rad')
        alt = fdm.get_property_value('position/h-sl-ft') * 0.3048
        
        # 라디안 차이를 미터로 변환 (대략적 계산)
        x = (curr_lat - start_lat) * 6378137.0
        y = (curr_lon - start_lon) * 6378137.0 * np.cos(start_lat)
        
        positions.append([x, y, alt])

    pos_array = np.array(positions)
    
    # 3D 그래프
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # 궤적 그리기
    ax.plot(pos_array[:, 1], pos_array[:, 0], pos_array[:, 2], label='F-16 Maneuver', color='magenta', linewidth=3)
    
    # 시작/끝점
    ax.scatter(pos_array[0, 1], pos_array[0, 0], pos_array[0, 2], color='green', s=100, label='Start')
    ax.scatter(pos_array[-1, 1], pos_array[-1, 0], pos_array[-1, 2], color='red', s=100, label='End')
    
    ax.set_xlabel('East-West (m)')
    ax.set_ylabel('North-South (m)')
    ax.set_zlabel('Altitude (m)')
    ax.set_title('F-16 High-G 360° Turn Trajectory')
    ax.legend()
    
    # 시점 조정 (더 잘 보이게)
    ax.view_init(elev=30, azim=45)
    
    plt.savefig('fixed_trajectory.png')
    print("Fixed plot saved as fixed_trajectory.png")

if __name__ == "__main__":
    generate_accurate_trajectory()
