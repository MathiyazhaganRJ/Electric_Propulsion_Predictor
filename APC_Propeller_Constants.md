# APC Electric Propellers: Empirical Constants

The following data was derived by parsing the complete UIUC aerodynamic database for APC-E (Thin Electric) and APC-SF (Slow Flyer) propellers. 

## Averaged Static Coefficients & Peak Efficiency
The Static Thrust ($C_T$) and Power ($C_P$) coefficients are extracted at an Advance Ratio of $J = 0.0$. The Peak Flight Efficiency ($\eta_{max}$) represents the absolute highest mechanical efficiency the propeller achieves at its optimal flight speed.

| Pitch/Dia (H/D) | Avg Static $C_T$ | Avg Static $C_P$ | Peak Flight Efficiency ($\eta_{max}$) | Sample Size |
| :--- | :--- | :--- | :--- | :--- |
| **0.3** | 0.0840 | 0.0275 | 52.1% | 70 test points |
| **0.4** | 0.0973 | 0.0335 | 61.4% | 368 test points |
| **0.5** | 0.1131 | 0.0432 | 67.1% | 649 test points |
| **0.6** | 0.1137 | 0.0454 | 71.4% | 544 test points |
| **0.7** | 0.1313 | 0.0570 | 74.4% | 406 test points |
| **0.8** | 0.1448 | 0.0708 | 74.9% | 412 test points |
| **0.9** | 0.1585 | 0.0866 | 75.1% | 404 test points |
| **1.0** | 0.1383 | 0.0771 | 77.7% | 440 test points |

### Key Observations for Digital Twin Solvers:
1. **The H/D = 0.5 to 0.6 Sweet Spot:** This is the most common range for sport RC aircraft. A highly reliable baseline fallback for an unknown APC-E propeller in this range is **$C_T \approx 0.113$** and **$C_P \approx 0.045$**.
2. **Static Stall:** At very high pitch ratios ($H/D \ge 1.0$), the static thrust and power coefficients begin to *drop*. This proves that "square" propellers (like a 10x10) experience blade stall at zero forward airspeed, despite being highly efficient (77.7%) once in fast forward flight.
3. **Efficiency Curve:** Peak flight efficiency scales aggressively with Pitch/Diameter ratio. Low-pitch propellers waste significant energy regardless of flight speed.
4. **Power Scales by $D^5$ (The ESC Fire Rule):** Because aerodynamic power math relies on Diameter to the fifth power ($D^5$), increasing your propeller diameter by just 10% (e.g., swapping a 10x5 for an 11x5) will increase your motor's current draw by roughly **61%**! Always re-check your ESC/Motor limits when stepping up diameter. Thrust, by comparison, only scales by $D^4$.
5. **RPM Limits (APC-E vs APC-SF):** Do not mix up Slow Flyer and Thin Electric props in your database logic. APC explicitly limits Slow Flyer (SF) props to a maximum safe RPM of `65,000 / Diameter (in)`. Thin Electric (E) props are much stiffer and can safely spin up to `145,000 / Diameter (in)`.
6. **The Pitch Speed Match:** To hit the Peak Efficiency ($\eta_{max}$) listed in the table above, the aircraft's forward flight speed must be carefully matched to the propeller's pitch speed. As a rule of thumb, **Pitch Speed ($V_{pitch}$) should be roughly 1.4x the target flight speed**.

---

### Standard Aerodynamic Formulas
When you build your solver in Python, remember to convert RPM to RPS ($n$) and inches to meters ($D$) before calculating Thrust and Power.

**Thrust Equation (Newtons):**
$$
T = C_T \cdot \rho \cdot n^2 \cdot D^4
$$

**Power Equation (Watts):**
$$
P = C_P \cdot \rho \cdot n^3 \cdot D^5
$$

*Where:*
*   **$T$** = Thrust in Newtons ($N$)
*   **$P$** = Mechanical Power required to turn the propeller in Watts ($W$)
*   **$\rho$** = Air density in $kg/m^3$ (standard sea level is $1.225 \ kg/m^3$)
*   **$n$** = Propeller rotational speed in Revolutions per Second ($n = \frac{RPM}{60}$)
*   **$D$** = Propeller diameter in meters ($D_{meters} = D_{inches} \cdot 0.0254$)
