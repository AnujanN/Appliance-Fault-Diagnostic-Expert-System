"""
Flask Frontend for Appliance Fault Diagnostic Expert System
Professional, Simple, Light Theme
"""
from flask import Flask, render_template, request, jsonify
from engine import DiagnosticEngine
from experta import Fact
from llm_extractor import extract_facts_from_text

app = Flask(__name__)

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/diagnose', methods=['POST'])
def diagnose():
    """Process diagnosis request"""
    try:
        data = request.get_json()
        input_mode = data.get('input_mode', 'manual')
        
        # Initialize engine
        engine = DiagnosticEngine()
        engine.reset()
        
        if input_mode == 'natural':
            # Natural language mode
            text = data.get('text', '')
            appliance_hint = data.get('appliance_hint')
            
            if not text.strip():
                return jsonify({'error': 'Please describe your problem'}), 400
            
            # Extract facts using LLM
            try:
                hint = None if appliance_hint == 'auto' else appliance_hint
                extracted_facts = extract_facts_from_text(text, hint)
                
                if not extracted_facts:
                    return jsonify({'error': 'Could not extract facts from your description'}), 400
                
                # Declare extracted facts
                for fact in extracted_facts:
                    engine.declare(fact)
                
                # Store extracted facts for display
                extracted_facts_display = [str(f) for f in extracted_facts]
            except Exception as e:
                return jsonify({'error': f'AI extraction failed: {str(e)}'}), 500
        else:
            # Manual mode
            appliance = data.get('appliance')
            symptoms = data.get('symptoms', [])
            observations = data.get('observations', {})
            
            if not appliance:
                return jsonify({'error': 'Please select an appliance'}), 400
            if not symptoms:
                return jsonify({'error': 'Please select at least one symptom'}), 400
            
            # Declare facts
            engine.declare(Fact(appliance=appliance))
            for symptom in symptoms:
                engine.declare(Fact(symptom=symptom))
            for key, value in observations.items():
                if value:
                    engine.declare(Fact(**{key: value}))
            
            extracted_facts_display = None
        
        # Run diagnosis
        engine.run()
        report = engine.report
        
        if not report['best_fit']:
            return jsonify({'error': 'Unable to generate diagnosis'}), 400
        
        # Generate LLM explanation for "Why this recommendation?"
        friendly_explanation = None
        if report['explanations']:
            try:
                from explanation_generator import explain_why_recommendation
                friendly_explanation = explain_why_recommendation(
                    diagnosis=report['best_fit']['diagnosis'],
                    confidence=report['best_fit']['score'],
                    explanations_list=report['explanations']
                )
            except Exception as e:
                print(f"LLM explanation failed: {e}")
                friendly_explanation = None
        
        # Prepare response
        response = {
            'success': True,
            'diagnosis': report['best_fit']['diagnosis'],
            'confidence': report['best_fit']['score'],
            'recommendation': report['best_fit']['recommendation'],
            'alternatives': report['alternatives'],
            'explanations': report['explanations'],
            'friendly_explanation': friendly_explanation,
            'extracted_facts': extracted_facts_display
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
