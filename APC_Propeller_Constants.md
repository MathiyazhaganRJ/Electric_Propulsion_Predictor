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

### Design Guidelines & Physical Constraints

*   **Default Coefficients:** For standard sport/glider setups ($H/D = 0.5$ to $0.6$), baseline fallback values are $C_T \approx 0.113$ and $C_P \approx 0.045$.
*   **Static Blade Stall:** Propellers with $H/D \ge 1.0$ exhibit reduced static thrust and power coefficients due to zero-airspeed stall, despite having higher peak flight efficiency.
*   **Efficiency vs. Pitch:** Peak aerodynamic efficiency ($\eta_{max}$) scales directly with the Pitch/Diameter ratio.
*   **Power Scaling ($D^5$):** Mechanical power and electrical current scale to the 5th power of diameter. A 10% increase in diameter yields a ~61% increase in current draw. Thrust scales to $D^4$.
*   **RPM Structural Limits:** 
    *   APC Slow Flyer (SF): $RPM_{max} = 65,000 / D_{inches}$
    *   APC Thin Electric (E): $RPM_{max} = 145,000 / D_{inches}$
*   **Optimal Advance Ratio:** Peak efficiency is achieved when the propeller's Pitch Speed ($V_{pitch}$) is approximately $1.4\times$ the aircraft's steady-state flight speed.

---

### Standard Aerodynamic Formulas
When you build your solver in Python, remember to convert RPM to RPS ($n$) and inches to meters ($D$) before calculating Thrust and Power.

**Thrust Equation (Newtons):**
`T = Ct * rho * n^2 * D^4`

**Power Equation (Watts):**
`P = Cp * rho * n^3 * D^5`

*Where:*
*   **$T$** = Thrust in Newtons ($N$)
*   **$P$** = Mechanical Power required to turn the propeller in Watts ($W$)
*   **$\rho$** = Air density in $kg/m^3$ (standard sea level is $1.225 \ kg/m^3$)
*   **$n$** = Propeller rotational speed in Revolutions per Second ($n = \frac{RPM}{60}$)
*   **$D$** = Propeller diameter in meters ($D_{meters} = D_{inches} \cdot 0.0254$)
