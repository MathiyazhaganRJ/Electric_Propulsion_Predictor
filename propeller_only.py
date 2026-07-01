import sys
import math
from pathlib import Path

# Use the local PyThrust modules
local_path = Path(__file__).parent.absolute()
if str(local_path) not in sys.path:
    sys.path.append(str(local_path))

from pythrust.propellers.database import PropellerDatabase

# =====================================================================
# 1. YOUR TARGET CONDITIONS
# =====================================================================
TARGET_DIA_INCH = 15.0
TARGET_PITCH_INCH = 8.0

AIRSPEED_MPS = 16.0    # Forward flight speed (m/s)
TARGET_RPM = 5000    # The RPM you want to test
RHO = 1.225            # Air density (kg/m^3) at sea level

# =====================================================================
# 2. LOAD DATABASE & FIND PROPELLER
# =====================================================================
print("Loading local Propeller Database...")
db = PropellerDatabase()
data_dir = local_path / "data" / "propellers" / "apc_202602"

if not db.load(data_dir):
    print(f"Failed to load propeller database from {data_dir}")
    sys.exit(1)

prop_entry = db.find_by_size(TARGET_DIA_INCH, TARGET_PITCH_INCH, blade_count=2, tolerance=0.5)

if not prop_entry:
    print(f"Could not find a propeller close to {TARGET_DIA_INCH}x{TARGET_PITCH_INCH}!")
    sys.exit(1)

print(f"Found Match: {prop_entry.metadata.manufacturer} {prop_entry.metadata.model} ({prop_entry.metadata.diameter_in}x{prop_entry.metadata.pitch_in})")

# =====================================================================
# 3. AERODYNAMIC CALCULATIONS
# =====================================================================
D = prop_entry.diameter_m
n = TARGET_RPM / 60.0

# Calculate Advance Ratio (J)
if n > 0:
    J = AIRSPEED_MPS / (n * D)
else:
    J = 0.0

# Interpolate Ct and Cp from the wind tunnel data
try:
    ct, cp = prop_entry.get_coefficients(TARGET_RPM, J)
except Exception as e:
    print(f"\nERROR: At {TARGET_RPM} RPM and {AIRSPEED_MPS} m/s, the Advance Ratio J is {J:.3f}.")
    print(f"This is outside the wind tunnel data limits for this propeller (it is windmilling/braking).")
    sys.exit(1)

# Calculate Physical Forces
thrust_n = ct * RHO * (n**2) * (D**4)
thrust_kg = thrust_n / 9.81

power_w = cp * RHO * (n**3) * (D**5)
torque_nm = power_w / (2 * math.pi * n)

# Propeller Aerodynamic Efficiency
prop_eff = (J * ct / cp) * 100 if cp > 0 and J > 0 else 0.0

print(f"\n==================================================================================================")
print(f" AERODYNAMIC PREDICTION: {prop_entry.metadata.id} at {TARGET_RPM} RPM")
print(f"==================================================================================================")
print(f" Flight Speed : {AIRSPEED_MPS:.1f} m/s")
print(f" Advance Ratio: J = {J:.3f}")
print(f" Thrust       : {thrust_kg:.2f} kg  ({thrust_n:.1f} N)")
print(f" Mech Power   : {power_w:.1f} W")
print(f" Torque       : {torque_nm:.3f} Nm")
print(f" Prop Effic   : {prop_eff:.1f} %")
print(f"==================================================================================================")
