"""
LLM-based explanation generator using Groq
Converts technical diagnostic reports into user-friendly explanations
"""
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

class ExplanationGenerator:
    def __init__(self):
        """Initialize Groq client for generating natural language explanations"""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found")
        self.client = Groq(api_key=api_key)
    
    def generate_friendly_explanation(self, report):
        """
        Convert technical expert system report into friendly, natural language
        
        Args:
            report: Dictionary with best_fit, alternatives, explanations
        
        Returns:
            String with user-friendly explanation
        """
        
        if not report.get('best_fit'):
            return "I couldn't determine the exact problem. Please provide more details about the symptoms."
        
        best = report['best_fit']
        
        # Build technical report for LLM
        technical_report = f"""Diagnostic Report:

PRIMARY DIAGNOSIS: {best['diagnosis']}
CONFIDENCE LEVEL: {best['score']}%
RECOMMENDED ACTION: {best['action']}
RECOMMENDATION: {best['recommendation']}

REASONING:
"""
        
        # Add explanations
        if report.get('explanations'):
            for i, explanation in enumerate(report['explanations'], 1):
                technical_report += f"{i}. {explanation}\n"
        
        # Add alternatives if any
        if report.get('alternatives'):
            technical_report += f"\nALTERNATIVE POSSIBILITIES:\n"
            for alt in report['alternatives']:
                technical_report += f"- {alt['diagnosis']} ({alt['score']}%): {alt['action']}\n"
        
        # Create prompt for LLM
        system_prompt = """You are a friendly, knowledgeable appliance repair technician talking to a homeowner. Your job is to:

1. Summarize the diagnostic report in simple, conversational language
2. Explain what's likely wrong in terms anyone can understand
3. Be reassuring and helpful, not alarming
4. Clearly explain whether this is DIY-fixable or needs a professional
5. Give practical next steps
6. Use analogies or simple explanations when helpful
7. Keep the tone warm and supportive

RULES:
- DO NOT add information not in the report
- DO NOT make up new diagnoses or recommendations
- DO use the confidence level to set expectations
- DO explain the reasoning in simple terms
- Keep it conversational but informative (2-3 paragraphs)
- If confidence is low, acknowledge uncertainty
- If critical warnings present (⚠️, 🔥), emphasize urgency"""

        user_prompt = f"""Please explain this diagnostic report to a homeowner in friendly, simple language:

{technical_report}

Remember: Be friendly, clear, and practical. Help them understand what's wrong and what to do next."""

        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,  # Higher temperature for more natural language
                max_tokens=500
            )
            
            friendly_explanation = response.choices[0].message.content.strip()
            return friendly_explanation
            
        except Exception as e:
            print(f"⚠️ LLM explanation generation failed: {e}")
            # Fallback to basic explanation
            return self._fallback_explanation(best, report)
    
    def _fallback_explanation(self, best, report):
        """Simple fallback if LLM fails"""
        confidence = best['score']
        diagnosis = best['diagnosis']
        action = best['action']
        
        # Determine confidence wording
        if confidence >= 70:
            confidence_text = "fairly confident"
        elif confidence >= 50:
            confidence_text = "moderately confident"
        else:
            confidence_text = "not very confident, but my best guess is"
        
        explanation = f"Based on the symptoms you described, I'm {confidence_text} ({confidence}%) that the issue is: **{diagnosis}**.\n\n"
        
        if "DIY" in action:
            explanation += "Good news! This is typically something you can fix yourself. "
        elif "Professional" in action:
            explanation += "This issue typically requires professional repair. "
        
        explanation += f"\n\n{best['recommendation']}"
        
        return explanation


def explain_alternative(alternative_diagnosis, confidence, recommendation):
    """
    Generate natural language explanation for an alternative diagnosis.
    Converts bullet-point recommendations into friendly, conversational explanations.
    
    Args:
        alternative_diagnosis: Name of the alternative diagnosis
        confidence: Confidence percentage
        recommendation: Technical recommendation text
    
    Returns:
        String with friendly explanation for this alternative
    """
    try:
        generator = ExplanationGenerator()
        
        system_prompt = """You are a helpful appliance repair technician explaining an alternative diagnosis to a homeowner.

Your job is to:
1. Explain why this could also be the problem (in simple terms)
2. Translate technical recommendations into friendly, actionable advice
3. Be concise but clear (2-3 sentences)
4. Use conversational language

RULES:
- DO NOT add information not in the recommendation
- DO make it sound natural and friendly
- DO keep it brief and practical
- If it mentions safety concerns, emphasize them
- If it's DIY, make that clear; if professional, say so"""

        user_prompt = f"""Alternative Diagnosis: {alternative_diagnosis}
Confidence: {confidence}%
Technical Recommendation: {recommendation}

Explain this alternative possibility in friendly, simple language (2-3 sentences):"""

        response = generator.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"⚠️ LLM explanation for alternative failed: {e}")
        # Fallback to original recommendation
        return recommendation


def explain_why_recommendation(diagnosis, confidence, explanations_list):
    """
    Generate natural language explanation for "Why this recommendation?" section.
    Converts technical expert system explanations (bullet points) into friendly narrative.
    
    Args:
        diagnosis: The primary diagnosis name
        confidence: Confidence percentage
        explanations_list: List of technical explanation strings from expert system
    
    Returns:
        String with friendly explanation of the reasoning
    """
    try:
        generator = ExplanationGenerator()
        
        # Build the technical reasoning
        reasoning_bullets = "\n".join([f"- {exp}" for exp in explanations_list])
        
        system_prompt = """You are a knowledgeable appliance repair expert explaining your diagnostic reasoning to a homeowner.

Your job is to translate technical expert system reasoning into natural, friendly language that explains WHY you reached this diagnosis.

RULES:
1. Convert the bullet points into a smooth, natural paragraph (2-3 sentences)
2. Explain how the symptoms connect to the diagnosis
3. Use simple language and helpful analogies if appropriate
4. Be conversational but informative
5. DO NOT add new information not in the reasoning
6. DO NOT repeat the diagnosis name or confidence (they already see it above)
7. Focus on explaining the "why" - the logical connection between symptoms and diagnosis

Keep it concise, friendly, and educational."""

        user_prompt = f"""Diagnosis: {diagnosis}
Confidence: {confidence}%

Technical Reasoning (from expert system):
{reasoning_bullets}

Explain WHY these symptoms point to this diagnosis in friendly, natural language (2-3 sentences):"""

        response = generator.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"⚠️ LLM explanation for 'why recommendation' failed: {e}")
        # Fallback to bullet points
        return "Based on the following factors:\n" + "\n".join([f"✓ {exp}" for exp in explanations_list])


def generate_explanation(report):
    """
    Convenience function to generate friendly explanation from report
    
    Usage:
        friendly_text = generate_explanation(engine.report)
    """
    try:
        generator = ExplanationGenerator()
        return generator.generate_friendly_explanation(report)
    except ValueError as e:
        print(f"⚠️ {e}")
        # Return technical report as-is
        if report.get('best_fit'):
            best = report['best_fit']
            return f"**Diagnosis:** {best['diagnosis']} ({best['score']}% confidence)\n\n{best['recommendation']}"
        return "Unable to generate diagnosis."
