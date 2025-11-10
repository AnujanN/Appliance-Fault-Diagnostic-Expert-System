"""
Appliance Fault Diagnostic Expert System - Streamlit UI
With LLM-powered Natural Language Processing
"""

import streamlit as st
from engine import DiagnosticEngine
from experta import Fact
import os

# Try to import LLM extractor, fall back to manual mode if not configured
try:
    from llm_extractor import extract_facts_from_text
    LLM_AVAILABLE = True
except Exception as e:
    LLM_AVAILABLE = False
    print(f"LLM not available: {e}")

st.set_page_config(page_title="🔧 Virtual Technician", layout="centered")

st.title("🔧 Appliance Fault Diagnostic Expert System")
st.markdown("### 🤖 AI-Powered Diagnosis with Natural Language Understanding")

# Check for API key
api_key_configured = os.getenv("GROQ_API_KEY") is not None

if not api_key_configured:
    st.warning("⚠️ **Groq API key not found.** Get your free key from [console.groq.com](https://console.groq.com/keys) and set it as environment variable `GROQ_API_KEY`")
    st.info("💡 **Temporary Solution:** You can still use the system in manual mode (checkboxes) below.")

# Input mode selector
input_mode = st.radio(
    "How would you like to describe the problem?",
    ["🤖 Natural Language (AI)", "☑️ Manual Selection (Checkboxes)"],
    index=0 if (LLM_AVAILABLE and api_key_configured) else 1
)

appliance = None
symptoms = []
observations = {}
extracted_facts = []

if input_mode == "🤖 Natural Language (AI)":
    # =====================================================================
    # NLP MODE - Natural Language Input
    # =====================================================================
    st.markdown("---")
    st.markdown("### 💬 Describe Your Problem")
    
    # Optional appliance hint
    appliance_hint = st.selectbox(
        "Appliance type (optional - AI can detect this):",
        ["Auto-detect", "Washing Machine", "Fan", "Power Generator", "Kitchen Grinder"]
    )
    appliance = appliance_hint if appliance_hint != "Auto-detect" else None
    
    # Natural language input
    user_description = st.text_area(
        "Tell me what's wrong in your own words:",
        placeholder="Example: My washing machine won't drain and it's making a loud grinding sound",
        height=120,
        help="Describe the problem naturally - the AI will extract the relevant information"
    )
    
    # Show examples
    with st.expander("💡 See example descriptions"):
        st.markdown("""
        **Good examples:**
        - "My washing machine won't start and the door won't lock"
        - "Fan is wobbling and making a squealing noise"
        - "Generator producing lots of smoke and overheating"
        - "Kitchen grinder is jamming and smells like burning"
        - "Washer won't drain, water stays inside, checked power already"
        """)

else:
    # =====================================================================
    # MANUAL MODE - Traditional Checkboxes
    # =====================================================================
    st.markdown("---")
    st.markdown("### ☑️ Select Symptoms Manually")
    
    appliance = st.selectbox(
        "Appliance type:",
        ["", "Washing Machine", "Fan", "Power Generator", "Kitchen Grinder"]
    )

    if appliance:
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
    # Handle based on input mode
    if input_mode == "🤖 Natural Language (AI)":
        if not user_description.strip():
            st.warning("⚠️ Please describe the problem first")
            st.stop()
        
        if not LLM_AVAILABLE or not api_key_configured:
            st.error("❌ LLM extractor not available. Please use Manual Selection mode or configure Groq API key.")
            st.stop()
        
        # Extract facts using LLM
        with st.spinner("🤖 Analyzing your description with AI..."):
            extracted_facts = extract_facts_from_text(user_description, preferred_appliance=appliance)
        
        # Show what was extracted (for transparency)
        with st.expander("🔍 What the AI understood from your description"):
            if extracted_facts:
                for fact in extracted_facts:
                    st.write(f"• {fact}")
            else:
                st.warning("Could not extract any facts from the description")
                st.stop()
    else:
        # Manual mode - convert to facts
        if not appliance:
            st.warning("⚠️ Please select an appliance type")
            st.stop()
        if not symptoms:
            st.warning("⚠️ Please select at least one symptom")
            st.stop()
    
    # Run diagnosis engine
    engine = DiagnosticEngine()
    engine.reset()
    
    # Declare facts
    if input_mode == "🤖 Natural Language (AI)":
        # Use LLM-extracted facts
        for fact in extracted_facts:
            engine.declare(fact)
    else:
        # Use manual facts
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
        
        # Count symptoms based on input mode
        if input_mode == "🤖 Natural Language (AI)":
            symptom_count = sum(1 for f in extracted_facts if hasattr(f, 'as_dict') and 'symptom' in str(f))
        else:
            symptom_count = len(symptoms)
        
        # === NEW: Natural Language Explanation ===
        try:
            from explanation_generator import generate_explanation
            
            with st.spinner("🤖 Generating friendly explanation..."):
                friendly_explanation = generate_explanation(report)
            
            # Show natural language explanation
            st.markdown("### 💬 Here's What I Found")
            st.markdown(friendly_explanation)
            
            # Expandable technical details
            with st.expander("🔍 View Technical Details"):
                st.markdown(f"**Primary Diagnosis:** {best['diagnosis']}")
                st.markdown(f"**Confidence Level:** {confidence}%")
                st.markdown(f"**Action Type:** {best['action']}")
                
                if report.get('explanations'):
                    st.markdown("**Reasoning:**")
                    for explanation in report['explanations']:
                        st.write(f"• {explanation}")
        
        except Exception as e:
            # Fallback to original technical display
            st.markdown(f"#### {confidence}% chance this is caused by {best['diagnosis']}")
        
        st.markdown("---")
        # Show action type badge
   #     action = best['action']
   #     if 'DIY' in action and 'Professional' not in action:
   #         st.success(f"🔧 **Action Required:** {action}")
   #     elif 'Professional' in action and 'DIY' not in action:
   #         st.error(f"👨‍🔧 **Action Required:** {action}")
   #     else:
   #         st.warning(f"🔧👨‍🔧 **Action Required:** {action}")
        
            
        # Detailed recommendation (kept for critical warnings)
        if '⚠️' in best['recommendation'] or '🔥' in best['recommendation']:
            st.error(best['recommendation'])
        
        # Alternative diagnoses - only show when confidence is not high (< 80%)
        if report['alternatives'] and confidence < 80:
            with st.expander("🔄 See Other Possible Causes"):
                for i, alt in enumerate(report['alternatives'], 1):
                    st.markdown(f"**{i}. {alt['diagnosis']}** ({alt['score']}% confidence)")
                    st.caption(f"Action: {alt['action']}")
                    st.write(alt['recommendation'])
                    if i < len(report['alternatives']):
                        st.markdown("---")
        
        st.markdown("---")
        st.caption("⚠️ Always unplug appliances before repair. Consult a professional for electrical issues.")
    else:
        st.warning("No diagnosis generated. Please select an appliance and symptoms.")
   #     st.caption("⚠️ Feature: Handling Incomplete Information - System provides guidance even with minimal input")
