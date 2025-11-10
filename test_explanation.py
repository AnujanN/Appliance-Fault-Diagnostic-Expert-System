"""
Test the Natural Language Explanation Generator
Shows before/after comparison
"""
from engine import DiagnosticEngine
from experta import Fact
from explanation_generator import generate_explanation

print("🧪 Testing Natural Language Explanation Generator\n")
print("=" * 70)

# Test Case: Washing Machine Won't Drain with Gurgling
print("\n📝 TEST CASE: Washing machine won't drain, gurgling noise")
print("-" * 70)

engine = DiagnosticEngine()
engine.reset()

# Declare facts
engine.declare(Fact(appliance='Washing Machine'))
engine.declare(Fact(symptom='Wont Drain'))
engine.declare(Fact(symptom='Loud Noise'))
engine.declare(Fact(noise_type='Gurgling'))

engine.run()
report = engine.report

# Show BEFORE: Technical output
print("\n❌ BEFORE (Technical Expert System Output):")
print("-" * 70)
if report['best_fit']:
    best = report['best_fit']
    print(f"Diagnosis: {best['diagnosis']}")
    print(f"Confidence: {best['score']}%")
    print(f"Action: {best['action']}")
    print(f"\nRecommendation:")
    print(best['recommendation'])
    print(f"\nReasons:")
    for explanation in report['explanations']:
        print(f"  • {explanation}")

# Show AFTER: Natural language output
print("\n\n✅ AFTER (Friendly Natural Language Output):")
print("-" * 70)
try:
    friendly_explanation = generate_explanation(report)
    print(friendly_explanation)
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 70)
print("✅ Comparison complete!")
print("\nNotice how the AFTER version:")
print("  • Uses conversational language")
print("  • Explains reasoning in simple terms")
print("  • Provides reassurance and practical guidance")
print("  • Sounds like talking to a real technician")
