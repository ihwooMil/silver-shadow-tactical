import jsbsim
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def generate_sample_trajectory():
    # JSBSim 실행 환경 설정
    fdm = jsbsim.FGFDMExec(os.path.dirname(jsbsim.__file__))
    
    # 전투기 모델 로드 (F-16 또는 유사 기종)
    # 기본 설치된 f16 모델 사용 시도
    try:
        fdm.load_model('f16')
    except:
        # F-16이 없을 경우 성능이 좋은 다른 기종이나 C172로 대체하여 궤적만 확인
        fdm.load_model('c172x')
    
    fdm.load_ic('reset00', True)
    fdm.run_ic()
    
    # 100Hz 설정 (0.01초)
    fdm.set_dt(0.01)
    
    positions = []
    
    print("Generating a 3D maneuver (High-G Turn + Climb)...")
    
    # 약 10초간의 기동 (1000스텝)
    for i in range(1000):
        # 다이내믹한 궤적을 위해 조종 입력 추가
        if i < 200:
            # 초기 가속 및 피치 업
            fdm.set_property_value('fcs/elevator-cmd-norm', -0.5)
            fdm.set_property_value('fcs/throttle-cmd-norm', 1.0)
        elif i < 600:
            # 급선회 (롤 + 피치)
            fdm.set_property_value('fcs/aileron-cmd-norm', 0.6)
            fdm.set_property_value('fcs/elevator-cmd-norm', -0.8)
        else:
            # 회복 기동
            fdm.set_property_value('fcs/aileron-cmd-norm', -0.3)
            fdm.set_property_value('fcs/elevator-cmd-norm', 0.2)
            
        fdm.run()
        
        # 위치 데이터 수집 (위도, 경도, 고도 기반으로 상대적 X, Y, Z 계산)
        # 단순화를 위해 ft 단위를 m로 변환하여 상대 좌표로 시각화
        x = fdm.get_property_value('position/distance-from-start-mag-ft') * 0.3048
        alt = fdm.get_property_value('position/h-sl-ft') * 0.3048
        psi = fdm.get_property_value('attitude/psi-deg')
        
        # 궤적 계산용 간단한 변환
        positions.append([
            x * np.cos(np.radians(psi)),
            x * np.sin(np.radians(psi)),
            alt
        ])

    pos_array = np.array(positions)
    
    # 3D 그래프 생성
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    ax.plot(pos_array[:, 0], pos_array[:, 1], pos_array[:, 2], label='Fighter Trajectory', color='cyan', linewidth=2)
    ax.scatter(pos_array[0, 0], pos_array[0, 1], pos_array[0, 2], color='green', label='Start')
    ax.scatter(pos_array[-1, 0], pos_array[-1, 1], pos_array[-1, 2], color='red', label='End')
    
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Altitude (m)')
    ax.set_title('Sample Maneuver Trajectory (6DOF)')
    ax.legend()
    
    # 그리드 및 배경 설정
    ax.grid(True)
    
    # 이미지 저장
    plt.savefig('sample_trajectory.png')
    print("Trajectory plot saved as sample_trajectory.png")

if __name__ == "__main__":
    generate_sample_trajectory()
