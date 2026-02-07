import jsbsim
import os

def check_controls_and_thrust():
    jsbsim_path = os.path.dirname(jsbsim.__file__)
    fdm = jsbsim.FGFDMExec(jsbsim_path)
    
    # 안정적인 비행을 위해 C172 모델 선택
    fdm.load_model('c172x')
    
    # 초기 조건: 5000ft에서 120kts로 비행 중인 상태로 시작 시도
    fdm.set_property_value('ic/h-agl-ft', 5000.0)
    fdm.set_property_value('ic/vc-kts', 120.0)
    fdm.run_ic()
    
    fdm.set_dt(0.01)
    
    print(f"{'Time':>5} | {'Thr-Cmd':>7} | {'Thrust':>8} | {'Elv-Cmd':>7} | {'Elv-Pos':>7} | {'Pitch':>6} | {'V-kts':>6}")
    print("-" * 70)
    
    for i in range(1000): # 10초 테스트
        # 1. 엔진 제어
        fdm.set_property_value('fcs/throttle-cmd-norm', 1.0)
        fdm.set_property_value('propulsion/engine[0]/set-running', 1) # 엔진 강제 가동
        fdm.set_property_value('fcs/mixture-cmd-norm', 1.0)
        
        # 2. 엘리베이터 제어 (3초 후부터 당기기)
        if i > 300:
            fdm.set_property_value('fcs/elevator-cmd-norm', -0.5)
        else:
            fdm.set_property_value('fcs/elevator-cmd-norm', 0.0)
            
        fdm.run()
        
        if i % 100 == 0:
            t = i / 100
            thr_cmd = fdm.get_property_value('fcs/throttle-cmd-norm')
            thrust = fdm.get_property_value('propulsion/engine[0]/thrust-lbs')
            elv_cmd = fdm.get_property_value('fcs/elevator-cmd-norm')
            elv_pos = fdm.get_property_value('fcs/elevator-pos-deg') # 실제 표면 각도
            pitch = fdm.get_property_value('attitude/theta-deg')
            v_kts = fdm.get_property_value('velocities/vc-kts')
            
            print(f"{t:5.1f} | {thr_cmd:7.2f} | {thrust:8.1f} | {elv_cmd:7.2f} | {elv_pos:7.2f} | {pitch:6.1f} | {v_kts:6.1f}")

if __name__ == "__main__":
    check_controls_and_thrust()
