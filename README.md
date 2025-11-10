# Appliance Fault Diagnostic Expert System

A "Virtual Technician" expert system built with Python, Experta, and Streamlit that diagnoses faults in household appliances.

## Features

This system implements all 6 core requirements:

1. **Asking Questions**: Interactive UI with dynamic, appliance-specific questions
2. **Handling Incomplete Information**: Provides safe default advice when information is limited
3. **Providing Alternative Solutions**: Offers best-fit diagnosis plus 2-3 alternatives
4. **Recommendations Over Exact Answers**: Suggests actionable steps (DIY vs. Professional)
5. **Uncertainty (Confidence Level)**: Uses a points-based scoring system for diagnoses
6. **Explainability**: Provides clear reasoning for all recommendations

## Supported Appliances

- **Washing Machine**: Diagnoses issues like won't start, won't drain, loud noises, leaking, etc.
- **Fan**: Handles problems like won't start, wobbling, slow speed, overheating, etc.
- **Power Generator**: Identifies fuel issues, power output problems, overheating, backfiring, etc.
- **Kitchen Grinder**: Diagnoses motor issues, weak grinding, vibration, burning smell, etc.

## Installation

1. Clone or download this project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## How It Works

### Architecture

- **engine.py**: Contains the Experta-based rule engine with 50+ diagnostic rules
- **app.py**: Streamlit UI that guides users through the diagnostic process
- **requirements.txt**: Python dependencies

### Diagnostic Process

1. **Triage**: User selects the appliance type
2. **Symptom Collection**: Dynamic questions based on appliance type
3. **Rule Execution**: Expert system evaluates symptoms using rule-based inference
4. **Scoring**: Each rule adds points to potential diagnoses
5. **Decision**: System selects best-fit diagnosis and alternatives based on scores
6. **Recommendations**: Provides actionable advice with DIY vs. Professional guidance

### Scoring System

- Rules fire based on symptoms and observations
- Each rule adds/subtracts points to diagnoses
- Higher scores = higher confidence
- Best fit is the highest-scoring diagnosis
- Alternatives are the next 2-3 highest scores

## Example Usage

### Example 1: Washing Machine Won't Drain

**Input:**
- Appliance: Washing Machine
- Symptoms: Won't Drain, Loud Noise (Gurgling)

**Output:**
- **Best-Fit**: Clogged Filter (70 pts)
- **Alternatives**: Blocked Drain Hose (35 pts), Failed Pump (10 pts)
- **Recommendation**: DIY - Clean or replace the filter
- **Explanation**: "Gurgling noise strongly suggests a drainage blockage"

### Example 2: Fan Won't Start

**Input:**
- Appliance: Fan
- Symptoms: Won't Start
- Power: Checked

**Output:**
- **Best-Fit**: Blown Thermal Fuse (40 pts)
- **Alternatives**: Broken Switch (25 pts), Failed Motor (20 pts)
- **Recommendation**: Professional - Requires electrical expertise
- **Explanation**: "With power confirmed, a blown thermal fuse or failed motor is most likely"

## Project Structure

```
Expert System Assignment/
├── app.py              # Streamlit UI application
├── engine.py           # Experta rule engine
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Key Technologies

- **Python 3.x**: Core programming language
- **Experta**: Rule-based expert system framework
- **Streamlit**: Web UI framework for interactive applications

## Safety Notice

This expert system provides diagnostic guidance only. Always:
- Unplug appliances before inspection or repair
- Stop using appliances if you smell burning or see smoke
- Consult professionals for electrical or gas-related issues
- Prioritize safety over cost savings

## Future Enhancements

Potential improvements:
- Add more appliances (refrigerator, microwave, dryer, etc.)
- Implement machine learning to improve scoring over time
- Add image upload for visual diagnosis
- Include video tutorials for common DIY fixes
- Multi-language support
- Mobile-responsive design optimization

## License

This project is created for educational purposes.

## Author

Created as part of an Expert System Assignment demonstrating rule-based AI and knowledge engineering principles.
