import jsbsim
import time
import os

def benchmark_jsbsim(num_steps=10000):
    # JSBSim root directory (where models are)
    # The pip installed version usually has these in a specific location
    # but for a quick benchmark, we can initialize without a full aircraft if needed, 
    # or use the default ones if we can find them.
    
    # Try to find JSBSim data path
    fdm = jsbsim.FGFDMExec(os.path.dirname(jsbsim.__file__))
    
    # Load a default aircraft (Cessna 172 is standard)
    fdm.load_model('c172x')
    fdm.load_ic('reset00', True) # Initial condition
    
    fdm.run_ic()
    
    print(f"Starting benchmark for {num_steps} steps...")
    start_time = time.time()
    
    for _ in range(num_steps):
        fdm.run()
        
    end_time = time.time()
    total_time = end_time - start_time
    avg_time_per_step = (total_time / num_steps) * 1000 # in ms
    
    print(f"Total time: {total_time:.4f} s")
    print(f"Average time per step: {avg_time_per_step:.6f} ms")
    
    # 1 hour simulation logic:
    # Default DT is 1/120s
    dt = fdm.get_delta_t()
    steps_for_1_hour = int(3600 / dt)
    estimated_1_hour_sim_time = (steps_for_1_hour * avg_time_per_step) / 1000
    
    print(f"Simulation DT: {dt} s")
    print(f"Steps for 1 hour: {steps_for_1_hour}")
    print(f"Estimated real time for 1 hour sim: {estimated_1_hour_sim_time:.2f} s")

if __name__ == "__main__":
    try:
        benchmark_jsbsim()
    except Exception as e:
        print(f"Error: {e}")
