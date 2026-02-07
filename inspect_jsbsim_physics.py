import jsbsim
import os

def inspect_physics():
    jsbsim_path = os.path.dirname(jsbsim.__file__)
    fdm = jsbsim.FGFDMExec(jsbsim_path)
    
    # F-16 모델 로드
    fdm.load_model('f16')
    
    # 초기 조건 설정 (BVR/WVR을 고려한 고속 비행 상태)
    fdm.set_property_value('ic/h-agl-ft', 20000.0)
    fdm.set_property_value('ic/vc-kts', 500.0)
    fdm.set_property_value('ic/theta-deg', 0.0) # 수평 자세
    fdm.set_property_value('ic/alpha-deg', 2.0) # 초기 받음각 약간 부여
    
    # 엔진 가동 준비
    fdm.set_property_value('propulsion/engine[0]/set-running', 1)
    fdm.set_property_value('fcs/throttle-cmd-norm', 1.0)
    
    fdm.run_ic()
    
    # JSBSim 기본 정보 및 물리 변수 리스트
    properties = {
        "Initial Speed (kts)": "velocities/vc-kts",
        "Mass (slugs)": "inertia/mass-slugs",
        "Weight (lbs)": "inertia/weight-lbs",
        "Wing Area (sqft)": "metrics/sw-sqft",
        "Timestep (sec)": "simulation/dt",
        "Gravity (ft/s^2)": "accelerations/g-acceleration-ft_sec2",
        "Alpha (AoA deg)": "aero/alpha-deg",
        "Beta (deg)": "aero/beta-deg",
        "Pitch (deg)": "attitude/theta-deg",
        "Roll (deg)": "attitude/phi-deg",
        "Elevator Pos (deg)": "fcs/elevator-pos-deg",
        "Thrust (lbs)": "propulsion/engine[0]/thrust-lbs",
        "Lift Force (lbs)": "forces/lift-lbs",
        "Drag Force (lbs)": "forces/drag-lbs",
        "Side Force (lbs)": "forces/side-lbs",
        "Gravity Force Body-Z (lbs)": "forces/fbz-gravity-lbs",
        "Aero Force Body-Z (lbs)": "forces/fbz-aero-lbs",
    }

    print("\n" + "="*50)
    print("JSBSim Physical Environment & Model Inspection")
    print("="*50)
    
    for label, prop in properties.items():
        try:
            val = fdm.get_property_value(prop)
            print(f"{label:<25}: {val:>10.4f}")
        except:
            print(f"{label:<25}: [Property Not Found]")

    # 좌표계 확인 (NED 기준)
    print("\n--- Coordinate System Check (Local Frame) ---")
    print(f"X-Axis Acceleration (ft/s^2): {fdm.get_property_value('accelerations/udot-ft_sec2'):.4f}")
    print(f"Y-Axis Acceleration (ft/s^2): {fdm.get_property_value('accelerations/vdot-ft_sec2'):.4f}")
    print(f"Z-Axis Acceleration (ft/s^2): {fdm.get_property_value('accelerations/wdot-ft_sec2'):.4f}")

    # 제어 입력 확인 루프 (1초간)
    print("\n--- Control Input Response Test (1s) ---")
    fdm.set_property_value('fcs/elevator-cmd-norm', -0.5) # Pitch Up 명령
    for _ in range(100):
        fdm.run()
    
    print(f"Elevator Cmd Norm      : -0.5")
    print(f"Elevator Final Pos(deg): {fdm.get_property_value('fcs/elevator-pos-deg'):.4f}")
    print(f"Final Pitch Rate (deg/s): {fdm.get_property_value('velocities/q-deg_sec'):.4f}")
    print(f"Final Load Factor (Nz) : {fdm.get_property_value('accelerations/n-pilot-z-norm'):.4f}")

if __name__ == "__main__":
    inspect_physics()
