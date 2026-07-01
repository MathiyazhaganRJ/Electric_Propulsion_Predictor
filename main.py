import sys
from pathlib import Path

# Use the local PyThrust modules we extracted
local_path = Path(__file__).parent.absolute()
if str(local_path) not in sys.path:
    sys.path.append(str(local_path))

from pythrust.propellers.database import PropellerDatabase
from pythrust.propulsion.models import MotorSpec, BatterySpec, SystemSpec, PropellerSpec
from pythrust.propulsion.solver import PropulsionSolver, SolverConfig

# =====================================================================
# 1. YOUR MOTOR DATA (Type what you have from the manufacturer here!)
# =====================================================================
V_in = 22.2         # Battery Voltage (e.g., 22.2V for 6S)
Kv = 550.0          # RPM/V
Rm = 0.020          # Internal Resistance (Ohms)
I0 = 1.6            # No-Load Current (Amps)
Max_Amps = 70     # Rated Motor current limit (Amps)

# =====================================================================
# 2. FLIGHT CONDITIONS & PROPELLER
# =====================================================================
CRUISE_SPEED_MPS = 16.0     # The forward flight speed of the drone (m/s)

TARGET_DIA_INCH = 14.0
TARGET_PITCH_INCH = 7.0


# Initialize the PyThrust Database
print("Loading local Propeller Database...")
db = PropellerDatabase()
data_dir = local_path / "data" / "propellers" / "apc_202602"

if not db.load(data_dir):
    print(f"Failed to load propeller database from {data_dir}")
    sys.exit(1)

# Search the database for the closest real-world wind tunnel data
prop_entry = db.find_by_size(TARGET_DIA_INCH, TARGET_PITCH_INCH, blade_count=2, tolerance=0.5)

if not prop_entry:
    print(f"Could not find a propeller close to {TARGET_DIA_INCH}x{TARGET_PITCH_INCH} in the database!")
    sys.exit(1)

print(f"Found Match: {prop_entry.metadata.manufacturer} {prop_entry.metadata.model} ({prop_entry.metadata.diameter_in}x{prop_entry.metadata.pitch_in})")


# =====================================================================
# 3. RUNNING THE SOLVER ENGINE
# =====================================================================
motor = MotorSpec(
    kv_rpm_per_v=Kv,
    resistance_ohm=Rm,
    no_load_current_a=I0,
    current_max_a=Max_Amps,
    # === 2ND ORDER CORRECTIONS ===
    torque_constant_kv_ratio=1.0,  
    resistance_quadratic=0.0,    
)
battery = BatterySpec(voltage_v=V_in)
system = SystemSpec(resistance_ohm=0.01) # Small wire resistance

propeller = PropellerSpec(
    diameter_m=prop_entry.diameter_m, 
    pitch_m=prop_entry.pitch_m
)

solver = PropulsionSolver(SolverConfig())

def print_throttle_sweep(airspeed: float):
    print(f"\n====================================================================================================")
    if airspeed == 0.0:
        print(f" STATIC THRUST TEST (Takeoff / 0 m/s) for {prop_entry.metadata.id}")
    else:
        print(f" DYNAMIC CRUISE FLIGHT ({airspeed:.1f} m/s Airspeed) for {prop_entry.metadata.id}")
        
    print(f"================================================================================================================================")
    print(f"| {'Throttle':<8} | {'RPM':<6} | {'Thrust(kg)':<10} | {'Torque(Nm)':<10} | {'Amps':<8} | {'Elec(W)':<9} | {'Mech(W)':<9} | {'Motor Eff':<9} |")
    print("-" * 110)

    for throttle_pct in range(10, 101, 10):
        throttle = throttle_pct / 100.0
        
        point = solver.solve_operating_point(
            motor=motor,
            battery=battery,
            system=system,
            propeller=propeller,
            prop_entry=prop_entry,
            rho=1.225,           
            airspeed_mps=airspeed,
            throttle=throttle
        )
        
        if point.is_feasible:
            thrust_kg = point.thrust_n / 9.81
            print(f"| {throttle_pct:>6}% | {int(point.rpm):<6} | {thrust_kg:<10.2f} | {point.torque_nm:<10.3f} | {point.motor_current_a:<8.2f} | {point.battery_power_w:<9.1f} | {point.shaft_power_w:<9.1f} | {point.motor_efficiency*100:<7.1f}% |")
        else:
            print(f"| {throttle_pct:>6}% | FAILED: {point.infeasible_reason}")

    print("====================================================================================================")

# Run the sweep for Static Takeoff
print_throttle_sweep(0.0)

# Run the sweep for Forward Cruise Flight
print_throttle_sweep(CRUISE_SPEED_MPS)
