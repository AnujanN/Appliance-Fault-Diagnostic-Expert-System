"""
Appliance Fault Diagnostic Expert System - Streamlit UI
"""

import streamlit as st
from engine import DiagnosticEngine
from experta import Fact

st.set_page_config(page_title="🔧 Virtual Technician", layout="centered")

st.title("🔧 Appliance Fault Diagnostic Expert System")

# --- User Inputs ---
# st.caption("❓ Feature: Asking Questions - Interactive symptom collection")
appliance = st.selectbox(
    "Appliance type:",
    ["", "Washing Machine", "Fan", "Power Generator", "Kitchen Grinder"]
)

symptoms = []
observations = {}

if appliance:
    # =====================================================================
    # WASHING MACHINE
    # =====================================================================
    if appliance == 'Washing Machine':
        if st.checkbox("Won't Start", key="wm_wont_start"):
            symptoms.append("Wont Start")
        if st.checkbox("Won't Drain", key="wm_wont_drain"):
            symptoms.append("Wont Drain")
        if st.checkbox("Not Spinning", key="wm_not_spinning"):
            symptoms.append("Not Spinning")
        if st.checkbox("Leaking Water", key="wm_leaking"):
            symptoms.append("Leaking Water")
        
        noise = st.radio("Any unusual noise?", ["None", "Gurgling", "Grinding", "Banging"], key="wm_noise")
        if noise != "None":
            symptoms.append("Loud Noise")
            observations['noise_type'] = noise
        
        if "Wont Start" in symptoms:
            power_checked = st.radio("Power supply checked?", ["Not Checked", "Checked"], key="wm_power")
            observations['power'] = power_checked
    
    # =====================================================================
    # FAN QUESTIONS
    # =====================================================================
    elif appliance == 'Fan':
        if st.checkbox("Won't Start", key="fan_wont_start"):
            symptoms.append("Wont Start")
        if st.checkbox("Wobbles", key="fan_wobbles"):
            symptoms.append("Wobbles")
        if st.checkbox("Slow Speed", key="fan_slow"):
            symptoms.append("Slow Speed")
        if st.checkbox("Noisy Operation", key="fan_noisy"):
            symptoms.append("Noisy Operation")
        if st.checkbox("Overheating", key="fan_overheat"):
            symptoms.append("Overheating")
        
        if "Wont Start" in symptoms:
            power_checked = st.radio("Power supply checked?", ["Not Checked", "Checked"], key="fan_power")
            observations['power'] = power_checked
    
    # =====================================================================
    # POWER GENERATOR QUESTIONS
    # =====================================================================
    elif appliance == 'Power Generator':
        if st.checkbox("Won't Start", key="gen_wont_start"):
            symptoms.append("Wont Start")
        if st.checkbox("Low Power Output", key="gen_low_power"):
            symptoms.append("Low Power Output")
        if st.checkbox("Runs But No Electricity", key="gen_no_output"):
            symptoms.append("Runs But No Electricity")
        if st.checkbox("Excessive Smoke", key="gen_smoke"):
            symptoms.append("Excessive Smoke")
        if st.checkbox("Overheating", key="gen_overheat"):
            symptoms.append("Overheating")
        if st.checkbox("Backfiring", key="gen_backfire"):
            symptoms.append("Backfiring")
        
        if "Wont Start" in symptoms:
            fuel_status = st.radio("Fuel status?", ["Unknown", "Empty", "Full"], key="gen_fuel")
            if fuel_status != "Unknown":
                observations['fuel'] = fuel_status
    
    # =====================================================================
    # KITCHEN GRINDER QUESTIONS
    # =====================================================================
    elif appliance == 'Kitchen Grinder':
        if st.checkbox("Won't Start", key="grinder_wont_start"):
            symptoms.append("Wont Start")
        if st.checkbox("Weak Grinding", key="grinder_weak"):
            symptoms.append("Weak Grinding")
        if st.checkbox("Excessive Vibration", key="grinder_vibration"):
            symptoms.append("Excessive Vibration")
        if st.checkbox("Burning Smell", key="grinder_burning"):
            symptoms.append("Burning Smell")
        if st.checkbox("Jamming", key="grinder_jamming"):
            symptoms.append("Jamming")
        if st.checkbox("Leaking", key="grinder_leaking"):
            symptoms.append("Leaking")
        
        if "Wont Start" in symptoms:
            power_checked = st.radio("Power supply checked?", ["Not Checked", "Checked"], key="grinder_power")
            observations['power'] = power_checked

if st.button("Get Diagnosis"):
    engine = DiagnosticEngine()
    engine.reset()
    
    # Declare facts
    if appliance:
        engine.declare(Fact(appliance=appliance))
    
    for symptom in symptoms:
        engine.declare(Fact(symptom=symptom))
    
    for key, value in observations.items():
        engine.declare(Fact(**{key: value}))
    
    engine.run()
    report = engine.report
    
    st.markdown("---")

    if report['best_fit']:
        best = report['best_fit']
        confidence = best['score']  # Store confidence for later use
        symptom_count = len(symptoms)  # Count symptoms
        
   #     st.subheader("Diagnosis")
        st.markdown(f"#### {confidence}% chance this is caused by {best['diagnosis']}")
       #     st.caption("🎯 Feature: Recommendations Over Exact Answers")
   #     st.caption("⚡ Feature: Uncertainty (Confidence Level)")
        st.markdown("---")
        # Show action type badge
   #     action = best['action']
   #     if 'DIY' in action and 'Professional' not in action:
   #         st.success(f"🔧 **Action Required:** {action}")
   #     elif 'Professional' in action and 'DIY' not in action:
   #         st.error(f"👨‍🔧 **Action Required:** {action}")
   #     else:
   #         st.warning(f"🔧👨‍🔧 **Action Required:** {action}")
        
            
        # Show recommendation with proper formatting
        if '⚠️' in best['recommendation'] or '🔥' in best['recommendation']:
            st.error(best['recommendation'])
        else:
            st.info(best['recommendation'])
        # Alternative diagnoses - only show when confidence is not high (< 80%) or multiple symptoms selected
        if report['alternatives'] and (confidence < 80):
            st.markdown("---")
            st.markdown(f"#### 🔄 Alternative Possibilities")
   #         st.write("**🔄 Alternative Possibilities:**")
   #         st.caption("🔄 Feature: Providing Alternative Solutions")
            for i, alt in enumerate(report['alternatives'], 1):
                st.markdown(f"**{i}. {alt['diagnosis']}** ({alt['score']}%)")
               # st.write(f"**Action:** {alt['action']}")
                st.write(f"{alt['recommendation']}")
        
        # Explanation - only show when confidence is not high (< 80%)
            st.markdown("---")
   #         st.caption("📖 Feature: Explainability")
            st.markdown(f"#### 📖 Why this recommendation?")
   #         st.write("**💡 Why this recommendation?**")
            for explanation in report['explanations']:
                st.write(f"✓ {explanation}")
        
        st.markdown("---")
        st.caption("⚠️ Always unplug appliances before repair. Consult a professional for electrical issues.")
    else:
        st.warning("No diagnosis generated. Please select an appliance and symptoms.")
   #     st.caption("⚠️ Feature: Handling Incomplete Information - System provides guidance even with minimal input")
