"""
LLM-based fact extractor using Groq (FREE Llama 3.1 API)
Get free API key from: https://console.groq.com/keys
"""
from groq import Groq
import json
from experta import Fact
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class GroqFactExtractor:
    def __init__(self):
        """
        Initialize Groq client.
        Set GROQ_API_KEY in .env file or as environment variable.
        """
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found. Get free key from https://console.groq.com/keys")
        self.client = Groq(api_key=api_key)
    
    def extract_facts(self, user_text, preferred_appliance=None):
        """
        Extract structured facts from natural language using Groq's Llama 3.1
        
        Args:
            user_text: User's natural language description
            preferred_appliance: Optional appliance hint from selectbox
        
        Returns:
            List of experta.Fact objects
        """
        
        system_prompt = """You are a fact extractor for an appliance diagnostic expert system.
Extract ONLY this JSON structure from user descriptions:

{
  "appliance": "Washing Machine" | "Fan" | "Power Generator" | "Kitchen Grinder",
  "symptoms": ["symptom1", "symptom2"],
  "observations": {"key": "value"}
}

Standard Symptoms (use EXACTLY these terms):
- Wont Start
- Wont Drain
- Not Spinning
- Leaking Water
- Loud Noise
- Excessive Vibration
- Burning Smell
- Water Not Filling
- Door Wont Lock
- Wobbles
- Slow Speed
- Overheating
- Not Oscillating
- Sparks
- Intermittent Operation
- Wont Turn On
- No Power Output
- Low Power Output
- Excessive Smoke
- Backfiring
- Oil Leaking
- Engine Surging
- High Fuel Consumption
- Battery Not Charging
- Weak Grinding
- Vibration
- Jamming
- Leaking
- Overheating Quickly
- Lid Not Secure
- Uneven Grinding
- Sparks Inside

Observations (optional):
- noise_type: "Gurgling" | "Grinding" | "Banging" | "Squealing"
- power: "Checked" | "Not Checked"
- fuel: "Empty" | "Full"

Rules:
1. Map casual language to standard terms (e.g., "won't turn on" → "Wont Start")
2. Detect multiple symptoms if mentioned
3. Extract noise type if described
4. Return ONLY valid JSON, no explanation or markdown

Examples:
Input: "My washing machine won't drain and makes a grinding noise"
Output: {"appliance": "Washing Machine", "symptoms": ["Wont Drain", "Loud Noise"], "observations": {"noise_type": "Grinding"}}

Input: "Fan is wobbling and getting too hot"
Output: {"appliance": "Fan", "symptoms": ["Wobbles", "Overheating"], "observations": {}}

Input: "Generator producing smoke and smells like fuel"
Output: {"appliance": "Power Generator", "symptoms": ["Excessive Smoke"], "observations": {}}
"""

        user_prompt = f"""User description: "{user_text}"
"""
        
        if preferred_appliance:
            user_prompt += f"Preferred appliance (if ambiguous): {preferred_appliance}\n"
        
        user_prompt += "\nReturn JSON only:"

        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",  # Fast & free tier available
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,  # Low temperature for consistent extraction
                max_tokens=300
            )
            
            llm_output = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            if llm_output.startswith("```"):
                llm_output = llm_output.split("```")[1]
                if llm_output.startswith("json"):
                    llm_output = llm_output[4:]
            
            # Parse JSON
            extracted = json.loads(llm_output)
            
            # Convert to experta Facts
            facts = []
            
            # Appliance fact
            appliance = extracted.get('appliance')
            if appliance and appliance in ["Washing Machine", "Fan", "Power Generator", "Kitchen Grinder"]:
                facts.append(Fact(appliance=appliance))
            elif preferred_appliance:
                facts.append(Fact(appliance=preferred_appliance))
            
            # Symptom facts
            for symptom in extracted.get('symptoms', []):
                if symptom:  # Only add non-empty symptoms
                    facts.append(Fact(symptom=symptom))
            
            # Observation facts
            observations = extracted.get('observations', {})
            for key, value in observations.items():
                if value:  # Only add non-empty values
                    facts.append(Fact(**{key: value}))
            
            return facts
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing failed: {e}")
            print(f"LLM output: {llm_output}")
            return self._fallback_extraction(user_text, preferred_appliance)
        
        except Exception as e:
            print(f"❌ LLM extraction failed: {e}")
            return self._fallback_extraction(user_text, preferred_appliance)
    
    def _fallback_extraction(self, text, preferred_appliance):
        """Simple keyword-based fallback if LLM fails"""
        facts = []
        text_lower = text.lower()
        
        # Appliance detection
        if preferred_appliance:
            facts.append(Fact(appliance=preferred_appliance))
        elif "washing" in text_lower or "washer" in text_lower:
            facts.append(Fact(appliance="Washing Machine"))
        elif "fan" in text_lower:
            facts.append(Fact(appliance="Fan"))
        elif "generator" in text_lower:
            facts.append(Fact(appliance="Power Generator"))
        elif "grinder" in text_lower:
            facts.append(Fact(appliance="Kitchen Grinder"))
        
        # Basic symptom detection
        if "won't start" in text_lower or "wont start" in text_lower or "won't turn on" in text_lower:
            facts.append(Fact(symptom="Wont Start"))
        if "drain" in text_lower and "won" in text_lower:
            facts.append(Fact(symptom="Wont Drain"))
        if "leak" in text_lower:
            facts.append(Fact(symptom="Leaking Water"))
        if "noise" in text_lower or "loud" in text_lower or "noisy" in text_lower:
            facts.append(Fact(symptom="Loud Noise"))
        if "spin" in text_lower and ("not" in text_lower or "won't" in text_lower):
            facts.append(Fact(symptom="Not Spinning"))
        if "smoke" in text_lower:
            facts.append(Fact(symptom="Excessive Smoke"))
        if "wobbl" in text_lower:
            facts.append(Fact(symptom="Wobbles"))
        if "overheat" in text_lower or "hot" in text_lower:
            facts.append(Fact(symptom="Overheating"))
        
        return facts


# Convenience function
def extract_facts_from_text(user_text, preferred_appliance=None):
    """
    Main function to extract facts from natural language.
    
    Usage:
        facts = extract_facts_from_text("My washing machine won't drain", "Washing Machine")
    """
    try:
        extractor = GroqFactExtractor()
        return extractor.extract_facts(user_text, preferred_appliance)
    except ValueError as e:
        print(f"⚠️ {e}")
        print("Using fallback keyword extraction instead.")
        extractor = GroqFactExtractor.__new__(GroqFactExtractor)
        return extractor._fallback_extraction(user_text, preferred_appliance)
