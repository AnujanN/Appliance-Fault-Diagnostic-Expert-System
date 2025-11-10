"""
Appliance Fault Diagnostic Expert System - Engine Module
Uses experta for rule-based inference with scoring and explanation capabilities.
"""

from experta import *


class DiagnosticEngine(KnowledgeEngine):
    """
    Expert system engine for diagnosing appliance faults.
    Uses a scoring system to handle uncertainty and provide ranked diagnoses.
    """
    
    def __init__(self):
        super().__init__()
        self.report = {
            "best_fit": None,
            "alternatives": [],
            "explanations": [],
            "scores": {}
        }
    
    def explain(self, message):
        """Add an explanation message to the report."""
        self.report['explanations'].append(message)
    
    def add_score(self, diagnosis, points):
        """Add points to a diagnosis score."""
        if diagnosis not in self.report['scores']:
            self.report['scores'][diagnosis] = 0
        self.report['scores'][diagnosis] += points
    
    # =====================================================================
    # WASHING MACHINE RULES
    # =====================================================================
    
    @Rule(
        Fact(appliance='Washing Machine'),
        Fact(symptom='Wont Start')
    )
    def wm_wont_start(self):
        self.add_score('Power Supply Issue', 25)
        self.add_score('Door Latch Problem', 20)
        self.add_score('Control Board Failure', 15)
        self.explain("Symptom 'Won't Start' suggests a power, door latch, or control issue.")
    
    @Rule(
        Fact(appliance='Washing Machine'),
        Fact(symptom='Wont Start'),
        Fact(power='Not Checked')
    )
    def wm_wont_start_no_power_check(self):
        self.add_score('Power Supply Issue', 20)
        self.explain("Please verify the washing machine is plugged in and the outlet is working.")
    
    @Rule(
        Fact(appliance='Washing Machine'),
        Fact(symptom='Wont Start'),
        Fact(power='Checked')
    )
    def wm_wont_start_power_ok(self):
        self.add_score('Door Latch Problem', 25)
        self.add_score('Control Board Failure', 20)
        self.explain("Since power is confirmed, the door latch or control board is likely faulty.")
    
    @Rule(
        Fact(appliance='Washing Machine'),
        Fact(symptom='Wont Drain')
    )
    def wm_wont_drain(self):
        self.add_score('Clogged Filter', 30)
        self.add_score('Failed Pump', 10)
        self.add_score('Blocked Drain Hose', 15)
        self.explain("Symptom 'Won't Drain' points to a blockage or pump failure.")
    
    @Rule(
        Fact(appliance='Washing Machine'),
        Fact(symptom='Loud Noise'),
        Fact(noise_type='Gurgling')
    )
    def wm_gurgling(self):
        self.add_score('Clogged Filter', 40)
        self.add_score('Blocked Drain Hose', 20)
        self.explain("'Gurgling' noise strongly suggests a drainage blockage.")
    
    @Rule(
        Fact(appliance='Washing Machine'),
        Fact(symptom='Loud Noise'),
        Fact(noise_type='Grinding')
    )
    def wm_grinding(self):
        self.add_score('Failed Pump', 50)
        self.add_score('Worn Bearings', 30)
        self.add_score('Clogged Filter', -10)
        self.explain("'Grinding' noise strongly suggests a motor, pump, or bearing failure.")
    
    @Rule(
        Fact(appliance='Washing Machine'),
        Fact(symptom='Loud Noise'),
        Fact(noise_type='Banging')
    )
    def wm_banging(self):
        self.add_score('Unbalanced Load', 45)
        self.add_score('Worn Bearings', 20)
        self.explain("'Banging' noise often indicates an unbalanced load or worn drum bearings.")
    
    @Rule(
        Fact(appliance='Washing Machine'),
        Fact(symptom='Leaking Water')
    )
    def wm_leaking(self):
        self.add_score('Worn Door Seal', 30)
        self.add_score('Loose Hose Connection', 25)
        self.add_score('Damaged Drain Pump', 15)
        self.explain("Water leaking could be from the door seal, hose connections, or drain pump.")
    
    @Rule(
        Fact(appliance='Washing Machine'),
        Fact(symptom='Not Spinning')
    )
    def wm_not_spinning(self):
        self.add_score('Broken Drive Belt', 35)
        self.add_score('Motor Coupler Failure', 25)
        self.add_score('Control Board Failure', 15)
        self.explain("'Not Spinning' suggests a drive belt, motor coupler, or control issue.")
    
    # =====================================================================
    # WASHING MACHINE COMBINATION RULES (Multiple Symptoms)
    # =====================================================================
    
    @Rule(
        Fact(appliance='Washing Machine'),
        Fact(symptom='Wont Drain'),
        Fact(symptom='Not Spinning')
    )
    def wm_wont_drain_and_spin(self):
        self.add_score('Clogged Filter', 60)
        self.add_score('Failed Pump', 50)
        self.explain("Won't drain AND won't spin together indicates a severely clogged filter or failed pump.")
    
    @Rule(
        Fact(appliance='Washing Machine'),
        Fact(symptom='Leaking Water'),
        Fact(symptom='Not Spinning')
    )
    def wm_leaking_and_not_spinning(self):
        self.add_score('Worn Bearings', 55)
        self.add_score('Damaged Tub Seal', 40)
        self.explain("Leaking with spinning failure strongly suggests worn drum bearings or tub seal damage.")
    
    @Rule(
        Fact(appliance='Washing Machine'),
        Fact(symptom='Wont Drain'),
        Fact(symptom='Leaking Water')
    )
    def wm_wont_drain_and_leaking(self):
        self.add_score('Damaged Drain Pump', 50)
        self.add_score('Blocked Drain Hose', 45)
        self.explain("Won't drain with leaking indicates damaged pump or severely blocked hose.")
    
    @Rule(
        Fact(appliance='Washing Machine'),
        Fact(symptom='Loud Noise'),
        Fact(symptom='Not Spinning')
    )
    def wm_noisy_and_not_spinning(self):
        self.add_score('Worn Bearings', 60)
        self.add_score('Broken Drive Belt', 45)
        self.explain("Noise with spinning failure points to worn bearings or broken drive belt.")
    
    # Additional Washing Machine Rules
    @Rule(
        Fact(appliance='Washing Machine'),
        Fact(symptom='Excessive Vibration')
    )
    def wm_excessive_vibration(self):
        self.add_score('Unbalanced Load', 35)
        self.add_score('Worn Shock Absorbers', 30)
        self.add_score('Unlevel Machine', 25)
        self.explain("Excessive vibration suggests unbalanced load, worn shock absorbers, or machine not level.")
    
    @Rule(
        Fact(appliance='Washing Machine'),
        Fact(symptom='Burning Smell')
    )
    def wm_burning_smell(self):
        self.add_score('Motor Overheating', 40)
        self.add_score('Worn Drive Belt', 30)
        self.add_score('Electrical Short', 20)
        self.explain("Burning smell indicates motor overheating, worn belt friction, or electrical issue.")
    
    @Rule(
        Fact(appliance='Washing Machine'),
        Fact(symptom='Water Not Filling')
    )
    def wm_no_water_fill(self):
        self.add_score('Faulty Water Inlet Valve', 40)
        self.add_score('Clogged Inlet Screen', 30)
        self.add_score('Low Water Pressure', 20)
        self.explain("Water not filling suggests faulty inlet valve, clogged screen, or low pressure.")
    
    @Rule(
        Fact(appliance='Washing Machine'),
        Fact(symptom='Door Wont Lock')
    )
    def wm_door_wont_lock(self):
        self.add_score('Door Latch Problem', 45)
        self.add_score('Control Board Failure', 25)
        self.add_score('Wiring Issue', 15)
        self.explain("Door won't lock indicates faulty latch mechanism or control board issue.")
    
    # =====================================================================
    # FAN RULES
    # =====================================================================
    
    @Rule(
        Fact(appliance='Fan'),
        Fact(symptom='Wont Start')
    )
    def fan_wont_start(self):
        self.add_score('Power Supply Issue', 20)
        self.add_score('Blown Thermal Fuse', 15)
        self.add_score('Broken Switch', 10)
        self.explain("A fan that won't start may have a power, fuse, or switch problem.")
    
    @Rule(
        Fact(appliance='Fan'),
        Fact(symptom='Wont Start'),
        Fact(power='Checked')
    )
    def fan_wont_start_power_ok(self):
        self.add_score('Blown Thermal Fuse', 40)
        self.add_score('Broken Switch', 25)
        self.add_score('Failed Motor', 20)
        self.explain("With power confirmed, a blown thermal fuse or failed motor is most likely.")
    
    @Rule(
        Fact(appliance='Fan'),
        Fact(symptom='Wont Start'),
        Fact(power='Not Checked')
    )
    def fan_no_power_check(self):
        self.add_score('Power Supply Issue', 30)
        self.explain("Please check if the fan is plugged in and the outlet has power.")
    
    @Rule(
        Fact(appliance='Fan'),
        Fact(symptom='Wobbles')
    )
    def fan_wobbles(self):
        self.add_score('Unbalanced Blades', 45)
        self.add_score('Loose Mounting', 25)
        self.add_score('Bent Blade', 20)
        self.explain("Wobbling is typically caused by unbalanced or damaged blades.")
    
    @Rule(
        Fact(appliance='Fan'),
        Fact(symptom='Slow Speed')
    )
    def fan_slow(self):
        self.add_score('Dust Buildup', 35)
        self.add_score('Worn Motor Bearings', 25)
        self.add_score('Capacitor Failure', 20)
        self.explain("Slow speed suggests dust buildup, worn bearings, or capacitor issues.")
    
    @Rule(
        Fact(appliance='Fan'),
        Fact(symptom='Noisy Operation')
    )
    def fan_noisy(self):
        self.add_score('Worn Motor Bearings', 40)
        self.add_score('Loose Parts', 25)
        self.add_score('Blade Obstruction', 15)
        self.explain("Unusual noise indicates worn bearings, loose parts, or obstructions.")
    
    @Rule(
        Fact(appliance='Fan'),
        Fact(symptom='Overheating')
    )
    def fan_overheating(self):
        self.add_score('Motor Overload', 35)
        self.add_score('Dust Buildup', 30)
        self.add_score('Failing Capacitor', 20)
        self.explain("Overheating may result from motor overload or dust restricting airflow.")
    
    # =====================================================================
    # FAN COMBINATION RULES (Multiple Symptoms)
    # =====================================================================
    
    @Rule(
        Fact(appliance='Fan'),
        Fact(symptom='Noisy Operation'),
        Fact(symptom='Wobbles')
    )
    def fan_noisy_and_wobbles(self):
        self.add_score('Worn Motor Bearings', 60)
        self.add_score('Unbalanced Blades', 50)
        self.explain("Noise with wobbling indicates worn motor bearings combined with unbalanced blades.")
    
    @Rule(
        Fact(appliance='Fan'),
        Fact(symptom='Slow Speed'),
        Fact(symptom='Overheating')
    )
    def fan_slow_and_overheating(self):
        self.add_score('Dust Buildup', 65)
        self.add_score('Motor Overload', 50)
        self.explain("Slow speed with overheating indicates severe dust buildup restricting airflow.")
    
    @Rule(
        Fact(appliance='Fan'),
        Fact(symptom='Noisy Operation'),
        Fact(symptom='Slow Speed')
    )
    def fan_noisy_and_slow(self):
        self.add_score('Worn Motor Bearings', 55)
        self.add_score('Capacitor Failure', 45)
        self.explain("Noise with slow speed points to worn bearings or failing capacitor.")
    
    @Rule(
        Fact(appliance='Fan'),
        Fact(symptom='Wobbles'),
        Fact(symptom='Overheating')
    )
    def fan_wobbles_and_overheating(self):
        self.add_score('Loose Mounting', 50)
        self.add_score('Motor Overload', 45)
        self.explain("Wobbling with overheating suggests loose mounting causing motor strain.")
    
    # Additional Fan Rules
    @Rule(
        Fact(appliance='Fan'),
        Fact(symptom='Not Oscillating')
    )
    def fan_no_oscillation(self):
        self.add_score('Broken Oscillating Gear', 40)
        self.add_score('Dry Oscillator Mechanism', 25)
        self.add_score('Motor Issue', 15)
        self.explain("No oscillation indicates broken gear or dry mechanism needing lubrication.")
    
    @Rule(
        Fact(appliance='Fan'),
        Fact(symptom='Sparks')
    )
    def fan_sparks(self):
        self.add_score('Electrical Short', 50)
        self.add_score('Worn Motor Brushes', 30)
        self.add_score('Loose Wiring', 15)
        self.explain("Sparks indicate serious electrical issue requiring immediate attention.")
    
    @Rule(
        Fact(appliance='Fan'),
        Fact(symptom='Intermittent Operation')
    )
    def fan_intermittent(self):
        self.add_score('Loose Connection', 35)
        self.add_score('Failing Capacitor', 30)
        self.add_score('Speed Switch Issue', 20)
        self.explain("Intermittent operation suggests loose connection or failing capacitor.")
    
    # =====================================================================
    # POWER GENERATOR RULES
    # =====================================================================
    
    @Rule(
        Fact(appliance='Power Generator'),
        Fact(symptom='Wont Start')
    )
    def gen_wont_start(self):
        self.add_score('Fuel System Problem', 25)
        self.add_score('Dead Battery', 20)
        self.add_score('Spark Plug Failure', 15)
        self.explain("A generator that won't start often has fuel, battery, or ignition issues.")
    
    @Rule(
        Fact(appliance='Power Generator'),
        Fact(symptom='Wont Start'),
        Fact(fuel='Empty')
    )
    def gen_no_fuel(self):
        self.add_score('Fuel System Problem', 50)
        self.explain("The fuel tank is empty or the fuel line may be clogged.")
    
    @Rule(
        Fact(appliance='Power Generator'),
        Fact(symptom='Wont Start'),
        Fact(fuel='Full')
    )
    def gen_fuel_ok(self):
        self.add_score('Dead Battery', 30)
        self.add_score('Spark Plug Failure', 25)
        self.add_score('Carburetor Issue', 20)
        self.explain("With fuel present, check the battery, spark plug, or carburetor.")
    
    @Rule(
        Fact(appliance='Power Generator'),
        Fact(symptom='Low Power Output')
    )
    def gen_low_power(self):
        self.add_score('Overloaded Circuit', 35)
        self.add_score('Dirty Air Filter', 25)
        self.add_score('Voltage Regulator Failure', 20)
        self.explain("Low power output suggests overload, air filter issues, or voltage regulation problems.")
    
    @Rule(
        Fact(appliance='Power Generator'),
        Fact(symptom='Runs But No Electricity')
    )
    def gen_no_output(self):
        self.add_score('Failed AVR (Voltage Regulator)', 45)
        self.add_score('Faulty Breaker', 25)
        self.add_score('Capacitor Failure', 20)
        self.explain("Generator runs but produces no power indicates AVR or breaker failure.")
    
    @Rule(
        Fact(appliance='Power Generator'),
        Fact(symptom='Excessive Smoke')
    )
    def gen_smoke(self):
        self.add_score('Oil Leak/Overfill', 40)
        self.add_score('Air Filter Clogged', 30)
        self.add_score('Rich Fuel Mixture', 20)
        self.explain("Excessive smoke indicates oil issues, clogged air filter, or fuel mixture problems.")
    
    @Rule(
        Fact(appliance='Power Generator'),
        Fact(symptom='Overheating')
    )
    def gen_overheating(self):
        self.add_score('Low Oil Level', 40)
        self.add_score('Blocked Cooling Vents', 30)
        self.add_score('Overload', 20)
        self.explain("Overheating is often caused by low oil, blocked vents, or overload.")
    
    @Rule(
        Fact(appliance='Power Generator'),
        Fact(symptom='Backfiring')
    )
    def gen_backfiring(self):
        self.add_score('Carburetor Timing Issue', 40)
        self.add_score('Exhaust System Problem', 25)
        self.add_score('Bad Fuel', 20)
        self.explain("Backfiring suggests carburetor timing, exhaust, or fuel quality issues.")
    
    # Additional Generator Rules
    @Rule(
        Fact(appliance='Power Generator'),
        Fact(symptom='Oil Leaking')
    )
    def gen_oil_leak(self):
        self.add_score('Worn Oil Seal', 40)
        self.add_score('Cracked Gasket', 30)
        self.add_score('Overfilled Oil', 20)
        self.explain("Oil leaking indicates worn seal, cracked gasket, or overfilled oil reservoir.")
    
    @Rule(
        Fact(appliance='Power Generator'),
        Fact(symptom='Engine Surging')
    )
    def gen_engine_surging(self):
        self.add_score('Dirty Air Filter', 35)
        self.add_score('Carburetor Adjustment Needed', 30)
        self.add_score('Fuel Flow Problem', 25)
        self.explain("Engine surging suggests restricted air intake or fuel flow irregularities.")
    
    @Rule(
        Fact(appliance='Power Generator'),
        Fact(symptom='High Fuel Consumption')
    )
    def gen_high_fuel_consumption(self):
        self.add_score('Carburetor Adjustment Needed', 35)
        self.add_score('Air Filter Clogged', 25)
        self.add_score('Engine Running Rich', 20)
        self.explain("High fuel consumption suggests carburetor needs adjustment or air filter is clogged.")
    
    @Rule(
        Fact(appliance='Power Generator'),
        Fact(symptom='Battery Not Charging')
    )
    def gen_battery_not_charging(self):
        self.add_score('Faulty Alternator', 45)
        self.add_score('Broken Charging Circuit', 30)
        self.add_score('Dead Battery', 20)
        self.explain("Battery not charging indicates faulty alternator or charging circuit issue.")
    
    # =====================================================================
    # POWER GENERATOR COMBINATION RULES (Multiple Symptoms)
    # =====================================================================
    
    @Rule(
        Fact(appliance='Power Generator'),
        Fact(symptom='Excessive Smoke'),
        Fact(symptom='Overheating')
    )
    def gen_smoke_and_overheating(self):
        self.add_score('Low Oil Level', 70)
        self.add_score('Oil Leak/Overfill', 55)
        self.explain("Smoke with overheating is a CRITICAL sign of oil level problems - check immediately!")
    
    @Rule(
        Fact(appliance='Power Generator'),
        Fact(symptom='Low Power Output'),
        Fact(symptom='Excessive Smoke')
    )
    def gen_low_power_and_smoke(self):
        self.add_score('Air Filter Clogged', 60)
        self.add_score('Rich Fuel Mixture', 45)
        self.explain("Low power with smoke indicates severely clogged air filter or fuel mixture issues.")
    
    @Rule(
        Fact(appliance='Power Generator'),
        Fact(symptom='Backfiring'),
        Fact(symptom='Excessive Smoke')
    )
    def gen_backfire_and_smoke(self):
        self.add_score('Bad Fuel', 55)
        self.add_score('Carburetor Timing Issue', 50)
        self.explain("Backfiring with smoke strongly suggests bad fuel or serious carburetor problems.")
    
    @Rule(
        Fact(appliance='Power Generator'),
        Fact(symptom='Low Power Output'),
        Fact(symptom='Overheating')
    )
    def gen_low_power_and_overheating(self):
        self.add_score('Overload', 60)
        self.add_score('Voltage Regulator Failure', 45)
        self.explain("Low power with overheating indicates generator overload or voltage regulator failure.")
    
    @Rule(
        Fact(appliance='Power Generator'),
        Fact(symptom='Runs But No Electricity'),
        Fact(symptom='Low Power Output')
    )
    def gen_no_output_and_low_power(self):
        self.add_score('Failed AVR (Voltage Regulator)', 75)
        self.explain("No electricity output with low power conclusively points to AVR failure.")
    
    # =====================================================================
    # KITCHEN GRINDER RULES
    # =====================================================================
    
    @Rule(
        Fact(appliance='Kitchen Grinder'),
        Fact(symptom='Wont Start')
    )
    def grinder_wont_start(self):
        self.add_score('Power Supply Issue', 25)
        self.add_score('Thermal Overload Trip', 20)
        self.add_score('Motor Burnout', 15)
        self.explain("A grinder that won't start may have power, overload, or motor issues.")
    
    @Rule(
        Fact(appliance='Kitchen Grinder'),
        Fact(symptom='Wont Start'),
        Fact(power='Checked')
    )
    def grinder_wont_start_power_ok(self):
        self.add_score('Thermal Overload Trip', 40)
        self.add_score('Motor Burnout', 30)
        self.add_score('Switch Failure', 20)
        self.explain("With power confirmed, the thermal overload may have tripped or the motor is burned out.")
    
    @Rule(
        Fact(appliance='Kitchen Grinder'),
        Fact(symptom='Wont Start'),
        Fact(power='Not Checked')
    )
    def grinder_no_power_check(self):
        self.add_score('Power Supply Issue', 35)
        self.explain("Please verify the grinder is plugged in and the outlet is working.")
    
    @Rule(
        Fact(appliance='Kitchen Grinder'),
        Fact(symptom='Weak Grinding')
    )
    def grinder_weak(self):
        self.add_score('Dull Blades', 45)
        self.add_score('Motor Wear', 25)
        self.add_score('Belt Slippage', 15)
        self.explain("Weak grinding performance indicates dull blades or motor wear.")
    
    @Rule(
        Fact(appliance='Kitchen Grinder'),
        Fact(symptom='Excessive Vibration')
    )
    def grinder_vibration(self):
        self.add_score('Unbalanced Blade Assembly', 40)
        self.add_score('Loose Mounting', 30)
        self.add_score('Worn Motor Bearings', 20)
        self.explain("Excessive vibration suggests unbalanced blades or loose mounting.")
    
    @Rule(
        Fact(appliance='Kitchen Grinder'),
        Fact(symptom='Burning Smell')
    )
    def grinder_burning_smell(self):
        self.add_score('Motor Overheating', 45)
        self.add_score('Electrical Short', 30)
        self.add_score('Overloaded Motor', 20)
        self.explain("Burning smell indicates motor overheating or electrical problems - stop using immediately!")
    
    @Rule(
        Fact(appliance='Kitchen Grinder'),
        Fact(symptom='Jamming')
    )
    def grinder_jamming(self):
        self.add_score('Foreign Object in Chamber', 40)
        self.add_score('Overloading', 30)
        self.add_score('Worn Clutch', 15)
        self.explain("Jamming occurs when foreign objects are present or the grinder is overloaded.")
    
    @Rule(
        Fact(appliance='Kitchen Grinder'),
        Fact(symptom='Leaking')
    )
    def grinder_leaking(self):
        self.add_score('Worn Gasket/Seal', 45)
        self.add_score('Loose Assembly', 30)
        self.add_score('Cracked Container', 20)
        self.explain("Leaking indicates worn gaskets, loose assembly, or container damage.")
    
    # Additional Grinder Rules
    @Rule(
        Fact(appliance='Kitchen Grinder'),
        Fact(symptom='Overheating Quickly')
    )
    def grinder_quick_overheat(self):
        self.add_score('Blocked Ventilation', 40)
        self.add_score('Motor Overload', 30)
        self.add_score('Worn Motor Brushes', 20)
        self.explain("Quick overheating suggests blocked ventilation or continuous overloading.")
    
    @Rule(
        Fact(appliance='Kitchen Grinder'),
        Fact(symptom='Lid Not Secure')
    )
    def grinder_lid_issue(self):
        self.add_score('Worn Lid Lock', 40)
        self.add_score('Broken Safety Switch', 30)
        self.add_score('Damaged Threads', 20)
        self.explain("Lid not securing indicates worn lock mechanism or safety switch issue.")
    
    @Rule(
        Fact(appliance='Kitchen Grinder'),
        Fact(symptom='Uneven Grinding')
    )
    def grinder_uneven(self):
        self.add_score('Dull Blades', 40)
        self.add_score('Loose Blade Assembly', 30)
        self.add_score('Unbalanced Load', 20)
        self.explain("Uneven grinding results from dull blades or loose blade assembly.")
    
    @Rule(
        Fact(appliance='Kitchen Grinder'),
        Fact(symptom='Sparks Inside')
    )
    def grinder_sparks(self):
        self.add_score('Worn Motor Brushes', 50)
        self.add_score('Electrical Short', 35)
        self.add_score('Motor Armature Damage', 10)
        self.explain("Sparks indicate worn motor brushes or electrical short requiring immediate attention.")
    
    # =====================================================================
    # KITCHEN GRINDER COMBINATION RULES (Multiple Symptoms)
    # =====================================================================
    
    @Rule(
        Fact(appliance='Kitchen Grinder'),
        Fact(symptom='Burning Smell'),
        Fact(symptom='Excessive Vibration')
    )
    def grinder_burning_and_vibration(self):
        self.add_score('Worn Motor Bearings', 70)
        self.add_score('Motor Overheating', 55)
        self.explain("CRITICAL: Burning smell with vibration indicates worn motor bearings - stop using immediately!")
    
    @Rule(
        Fact(appliance='Kitchen Grinder'),
        Fact(symptom='Weak Grinding'),
        Fact(symptom='Burning Smell')
    )
    def grinder_weak_and_burning(self):
        self.add_score('Motor Overheating', 65)
        self.add_score('Overloaded Motor', 50)
        self.explain("Weak grinding with burning smell indicates motor is overloaded and overheating - reduce load.")
    
    @Rule(
        Fact(appliance='Kitchen Grinder'),
        Fact(symptom='Jamming'),
        Fact(symptom='Excessive Vibration')
    )
    def grinder_jamming_and_vibration(self):
        self.add_score('Foreign Object in Chamber', 60)
        self.add_score('Unbalanced Blade Assembly', 50)
        self.explain("Jamming with vibration strongly indicates foreign object stuck in chamber.")
    
    @Rule(
        Fact(appliance='Kitchen Grinder'),
        Fact(symptom='Weak Grinding'),
        Fact(symptom='Excessive Vibration')
    )
    def grinder_weak_and_vibration(self):
        self.add_score('Dull Blades', 60)
        self.add_score('Unbalanced Blade Assembly', 55)
        self.explain("Weak grinding with vibration indicates dull or unbalanced blades.")
    
    @Rule(
        Fact(appliance='Kitchen Grinder'),
        Fact(symptom='Leaking'),
        Fact(symptom='Excessive Vibration')
    )
    def grinder_leaking_and_vibration(self):
        self.add_score('Worn Gasket/Seal', 60)
        self.add_score('Loose Assembly', 55)
        self.explain("Leaking with vibration indicates loose assembly or worn gasket from vibration.")
    
    @Rule(
        Fact(appliance='Kitchen Grinder'),
        Fact(symptom='Jamming'),
        Fact(symptom='Burning Smell')
    )
    def grinder_jamming_and_burning(self):
        self.add_score('Overloading', 65)
        self.add_score('Foreign Object in Chamber', 50)
        self.explain("STOP: Jamming with burning smell means severe overload or jammed object - turn off now!")
    
    # =====================================================================
    # DEFAULT HANDLING FOR INCOMPLETE INFORMATION
    # =====================================================================
    
    @Rule(
        Fact(appliance=MATCH.appliance),
        NOT(Fact(symptom=W()))
    )
    def no_symptoms_provided(self, appliance):
        self.add_score('Insufficient Information', 100)
        self.explain(f"No specific symptoms were reported for the {appliance}.")
        self.explain("RECOMMENDATION: Start with basic troubleshooting:")
        self.explain("1. Check if the appliance is properly plugged in")
        self.explain("2. Verify the power outlet is working")
        self.explain("3. Look for any obvious damage or loose parts")
        self.explain("4. Check if any safety switches or breakers have tripped")
        self.explain("5. Consult the user manual for basic troubleshooting steps")
    
    # =====================================================================
    # DECISION RULE (LOW PRIORITY - RUNS LAST)
    # =====================================================================
    
    @Rule(
        AS.f1 << Fact(appliance=W()),
        salience=-1000  # Low priority - runs after all other rules
    )
    def make_decision(self, f1):
        """
        Final decision rule that analyzes all scores and determines
        the best-fit diagnosis and alternatives.
        """
        if not self.report['scores']:
            # No scores means no rules fired - provide default advice
            self.report['best_fit'] = {
                'diagnosis': 'Unable to Diagnose - Insufficient Information',
                'score': 0,
                'recommendation': 'DIY: Check power supply and basic connections. If issue persists, contact a professional technician.',
                'action': 'Start with Basic Troubleshooting'
            }
            self.explain("Unable to provide a specific diagnosis with the information provided.")
            return
        
        # Count symptoms to apply confidence adjustment
        symptom_count = sum(1 for fact in self.facts.values() if 'symptom' in fact)
        
        # Convert scores to confidence percentage with symptom-based adjustment
        normalized_scores = {}
        for diagnosis, raw_score in self.report['scores'].items():
            if raw_score <= 0:
                normalized_scores[diagnosis] = 0
            else:
                # Base confidence calculation - decreases with more symptoms
                if symptom_count == 1:
                    # Single symptom: High confidence (80-92%)
                    # Scale: 30 points = 80%, 50 points = 92%
                    confidence = 80 + (raw_score / 50) * 12
                elif symptom_count == 2:
                    # Two symptoms: Medium-High confidence (65-78%)
                    # Scale: 50 points = 65%, 100 points = 78%
                    confidence = 65 + (raw_score / 100) * 13
                elif symptom_count == 3:
                    # Three symptoms: Medium confidence (50-65%)
                    # Scale: 70 points = 50%, 120 points = 65%
                    confidence = 50 + (raw_score / 120) * 15
                elif symptom_count == 4:
                    # Four symptoms: Lower-Medium confidence (40-55%)
                    # Scale: 80 points = 40%, 130 points = 55%
                    confidence = 40 + (raw_score / 130) * 15
                else:
                    # Five or more symptoms: Low confidence (30-45%)
                    # Scale: 100 points = 30%, 150 points = 45%
                    confidence = 30 + (raw_score / 150) * 15
                
                # Cap at 100% and round
                normalized_scores[diagnosis] = round(min(confidence, 100), 1)
        
        # Replace raw scores with normalized scores
        self.report['scores'] = normalized_scores
        
        # Sort diagnoses by normalized score (highest first)
        sorted_diagnoses = sorted(
            normalized_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Get the best fit
        best_diagnosis, best_score = sorted_diagnoses[0]
        
        # Generate recommendation based on diagnosis
        recommendation = self.get_recommendation(best_diagnosis, best_score)
        
        self.report['best_fit'] = {
            'diagnosis': best_diagnosis,
            'score': best_score,
            'recommendation': recommendation['text'],
            'action': recommendation['action']
        }
        
        # Get alternatives (next 2 highest scores, if they exist and are above threshold)
        alternatives = []
        for diagnosis, score in sorted_diagnoses[1:4]:  # Get up to 3 alternatives
            if score > 5:  # Only include scores above 5% to filter out noise
                alt_rec = self.get_recommendation(diagnosis, score)
                alternatives.append({
                    'diagnosis': diagnosis,
                    'score': score,
                    'recommendation': alt_rec['text'],
                    'action': alt_rec['action']
                })
        
        self.report['alternatives'] = alternatives
    
    def get_recommendation(self, diagnosis, score):
        """
        Generate specific recommendations based on the diagnosis.
        Returns a dict with 'text' and 'action' keys.
        """
        # Define DIY-fixable vs professional issues
        diy_issues = {
            'Power Supply Issue': 'DIY: Check the power cord, outlet, and circuit breaker. Try a different outlet.',
            'Clogged Filter': 'DIY: Clean or replace the filter according to the user manual.',
            'Unbalanced Load': 'DIY: Redistribute the load evenly and restart the cycle.',
            'Dust Buildup': 'DIY: Clean all surfaces, especially motor and vents, with compressed air or cloth.',
            'Loose Mounting': 'DIY: Tighten all mounting screws and ensure stable placement.',
            'Unbalanced Blades': 'DIY: Clean blades and check for balance. Adjust blade positions if possible.',
            'Loose Hose Connection': 'DIY: Check and tighten all hose connections.',
            'Foreign Object in Chamber': 'DIY: Remove any foreign objects from the chamber before restarting.',
            'Overloading': 'DIY: Reduce the load size and try again.',
            'Loose Assembly': 'DIY: Reassemble all parts according to the user manual.',
            'Dirty Air Filter': 'DIY: Clean or replace the air filter.',
            'Blocked Drain Hose': 'DIY: Check and clear the drain hose for blockages.',
            'Low Oil Level': 'DIY: Check and refill oil to the recommended level.',
            'Blocked Cooling Vents': 'DIY: Clean all cooling vents and ensure proper ventilation.',
            'Fuel System Problem': 'DIY: Check fuel level, fuel quality, and fuel line for blockages.',
            'Empty Fuel Tank': 'DIY: Refill the fuel tank with fresh, appropriate fuel.',
            'Dull Blades': 'DIY/Professional: Sharpen or replace the blades.',
            'Insufficient Information': 'DIY: Start with basic troubleshooting (power, connections, visual inspection).',
            'Unlevel Machine': 'DIY: Adjust the leveling feet until the machine is perfectly level.',
            'Clogged Inlet Screen': 'DIY: Turn off water supply and clean the inlet screen filter.',
            'Low Water Pressure': 'DIY: Check household water pressure and ensure supply valves are fully open.',
            'Wiring Issue': 'Professional: Electrical wiring issues require a qualified technician.',
            'Dry Oscillator Mechanism': 'DIY: Apply light lubricating oil to oscillator mechanism.',
            'Loose Connection': 'DIY: Check and tighten all electrical connections.',
            'Speed Switch Issue': 'Professional: Speed switch replacement requires electrical expertise.',
            'Broken Oscillating Gear': 'Professional: Gear replacement requires disassembly.',
            'Cracked Gasket': 'DIY: Replace gasket with manufacturer-approved parts.',
            'Overfilled Oil': 'DIY: Drain excess oil to proper level indicated on dipstick.',
            'Fuel Flow Problem': 'DIY: Check fuel line for kinks or blockages. Replace fuel filter.',
            'Engine Running Rich': 'Professional: Carburetor adjustment needed for proper fuel-air mixture.',
            'Blocked Ventilation': 'DIY: Clean all ventilation slots and ensure adequate airflow around appliance.',
            'Unbalanced Load': 'DIY: Distribute contents evenly in the container before grinding.',
            'Damaged Threads': 'Professional: Damaged threads require replacement of affected parts.',
        }
        
        professional_issues = {
            'Failed Pump': 'Professional: The drain pump likely needs replacement. Contact a qualified technician.',
            'Worn Bearings': 'Professional: Bearing replacement requires disassembly. Contact a qualified technician.',
            'Control Board Failure': 'Professional: Electronic control boards require specialized diagnosis and replacement.',
            'Broken Drive Belt': 'DIY/Professional: Drive belt replacement can be DIY for experienced users, or contact a technician.',
            'Motor Coupler Failure': 'Professional: Motor coupler replacement requires internal access. Contact a technician.',
            'Worn Door Seal': 'DIY/Professional: Door seal replacement can be DIY, but ensure proper fit.',
            'Door Latch Problem': 'Professional: Door latch mechanism may need professional adjustment or replacement.',
            'Blown Thermal Fuse': 'Professional: Thermal fuse replacement requires electrical expertise.',
            'Broken Switch': 'Professional: Switch replacement involves electrical work.',
            'Failed Motor': 'Professional: Motor replacement or repair requires a qualified technician.',
            'Worn Motor Bearings': 'Professional: Motor bearing replacement requires specialized skills.',
            'Capacitor Failure': 'Professional: Capacitor replacement involves electrical work and safety risks.',
            'Bent Blade': 'Professional: Bent blades should be replaced to avoid further damage.',
            'Motor Burnout': 'Professional: A burned-out motor requires replacement by a technician.',
            'Thermal Overload Trip': 'DIY: Let the unit cool for 30 minutes, then reset. If it trips again, call a professional.',
            'Switch Failure': 'Professional: Switch replacement requires electrical expertise.',
            'Motor Wear': 'Professional: Worn motor components require professional assessment.',
            'Belt Slippage': 'Professional: Belt adjustment or replacement may be needed.',
            'Unbalanced Blade Assembly': 'Professional: Blade assembly balancing requires proper tools and expertise.',
            'Motor Overheating': 'Professional: If cooling doesn\'t resolve it, motor inspection is needed.',
            'Electrical Short': 'Professional: Electrical shorts are dangerous and require immediate professional attention.',
            'Overloaded Motor': 'DIY: Let cool, then use with smaller loads. If persists, contact a professional.',
            'Worn Clutch': 'Professional: Clutch replacement requires disassembly and expertise.',
            'Worn Gasket/Seal': 'DIY: Replace gasket with manufacturer-specified parts.',
            'Cracked Container': 'DIY/Professional: Replace the container with an OEM part.',
            'Dead Battery': 'DIY: Charge or replace the battery according to specifications.',
            'Spark Plug Failure': 'DIY: Clean or replace the spark plug following the manual.',
            'Carburetor Issue': 'Professional: Carburetor cleaning or adjustment requires expertise.',
            'Overloaded Circuit': 'DIY: Reduce the electrical load on the generator.',
            'Failed AVR (Voltage Regulator)': 'Professional: AVR replacement requires technical knowledge.',
            'Faulty Breaker': 'DIY/Professional: Reset breaker first. If faulty, replace with correct rating.',
            'Oil Leak/Overfill': 'DIY: Check oil level and drain excess. Inspect for leaks and repair if needed.',
            'Air Filter Clogged': 'DIY: Clean or replace the air filter regularly.',
            'Rich Fuel Mixture': 'Professional: Fuel mixture adjustment requires carburetor expertise.',
            'Overload': 'DIY: Reduce the load to within rated capacity.',
            'Carburetor Timing Issue': 'Professional: Carburetor timing requires professional adjustment.',
            'Exhaust System Problem': 'Professional: Exhaust system inspection and repair needed.',
            'Bad Fuel': 'DIY: Drain old fuel and refill with fresh, appropriate fuel.',
            'Damaged Drain Pump': 'Professional: Drain pump replacement requires a qualified technician.',
            'Blade Obstruction': 'DIY: Turn off and unplug, then carefully remove any obstructions.',
            'Motor Overload': 'DIY: Let cool, avoid extended use. If persists, contact a professional.',
            'Failing Capacitor': 'Professional: Capacitor testing and replacement requires expertise.',
            'Voltage Regulator Failure': 'Professional: Voltage regulator diagnosis and replacement needed.',
            'Loose Parts': 'DIY: Identify and tighten any loose screws or components.',
            'Damaged Tub Seal': 'Professional: Tub seal replacement requires disassembly and expertise.',
            'Worn Shock Absorbers': 'Professional: Shock absorber replacement requires disassembly and specialized parts.',
            'Faulty Water Inlet Valve': 'Professional: Water inlet valve replacement requires plumbing and electrical work.',
            'Worn Drive Belt': 'DIY/Professional: Belt replacement can be DIY with proper tools and manual.',
            'Loose Wiring': 'Professional: Electrical wiring repairs require qualified technician for safety.',
            'Worn Oil Seal': 'Professional: Oil seal replacement requires engine disassembly.',
            'Carburetor Adjustment Needed': 'Professional: Carburetor tuning requires technical expertise and tools.',
            'Faulty Alternator': 'Professional: Alternator testing and replacement requires electrical expertise.',
            'Broken Charging Circuit': 'Professional: Electrical circuit diagnosis and repair needed.',
            'Worn Motor Brushes': 'DIY/Professional: Carbon brush replacement can be DIY with proper guidance.',
            'Worn Lid Lock': 'DIY: Replace lid lock mechanism with manufacturer-specified part.',
            'Broken Safety Switch': 'Professional: Safety switch replacement involves electrical components.',
            'Loose Blade Assembly': 'DIY: Tighten blade assembly securely following manual instructions.',
            'Motor Armature Damage': 'Professional: Motor armature damage requires complete motor replacement.',
        }
        
        # Add priority messages for critical combinations
        critical_messages = {
            'Low Oil Level': '⚠️ URGENT: Low oil can cause permanent engine damage. Check immediately!',
            'Oil Leak/Overfill': '⚠️ WARNING: Oil issues can damage the engine. Address promptly.',
            'Worn Oil Seal': '⚠️ WARNING: Oil leak can lead to engine seizure. Address promptly.',
            'Worn Motor Bearings': '⚠️ CRITICAL: Stop using immediately to prevent motor failure.',
            'Motor Overheating': '⚠️ CRITICAL: Continued use may cause permanent motor damage.',
            'Electrical Short': '🔥 DANGER: Electrical short is a fire hazard. Unplug immediately!',
            'Worn Motor Brushes': '⚠️ WARNING: Sparking from worn brushes can damage motor. Replace soon.',
            'Motor Armature Damage': '⚠️ CRITICAL: Do not use. Motor replacement required.',
        }
        
        # Determine if DIY or Professional
        if diagnosis in diy_issues:
            recommendation_text = diy_issues[diagnosis]
            action = 'DIY Fix' if 'DIY:' in recommendation_text else 'DIY or Professional'
        elif diagnosis in professional_issues:
            recommendation_text = professional_issues[diagnosis]
            if 'DIY/Professional:' in recommendation_text:
                action = 'DIY or Call Professional'
            else:
                action = 'Call Professional'
        else:
            # Default recommendation
            if score > 30:
                recommendation_text = 'Professional: This issue likely requires professional diagnosis and repair.'
                action = 'Call Professional'
            else:
                recommendation_text = 'DIY: Start with basic troubleshooting. If issue persists, contact a professional.'
                action = 'DIY Fix'
        
        # Add critical warning if applicable
        if diagnosis in critical_messages:
            recommendation_text = critical_messages[diagnosis] + '\n\n' + recommendation_text
        
        return {
            'text': recommendation_text,
            'action': action
        }
