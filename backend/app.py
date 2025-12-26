"""
PATHAI Backend - Flask API Server with Job Matching
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime
from jobs_database import get_jobs_by_archetype, get_all_jobs, get_job_stats, COMPANIES

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Career Archetypes Database
ARCHETYPES = {
    "analytical_guardian": {
        "name": "Analytical Guardian",
        "description": "You are methodical, detail-oriented, and risk-aware. You excel at analyzing complex problems and ensuring quality through careful planning.",
        "careers": ["Data Analyst", "Quality Assurance Engineer", "Financial Analyst", "Research Scientist", "Compliance Officer"],
        "companies": ["Established corporations", "Banks and financial institutions", "Research institutions", "Government organizations"]
    },
    "creative_maverick": {
        "name": "Creative Maverick",
        "description": "You are a fast-thinking, innovative risk-taker driven by purpose. You thrive in dynamic environments where you can experiment and push boundaries.",
        "careers": ["Product Designer", "Marketing Strategist", "Entrepreneur", "Creative Director", "Content Creator"],
        "companies": ["Startups", "Creative agencies", "Media companies", "Innovation labs"]
    },
    "systematic_builder": {
        "name": "Systematic Builder",
        "description": "You are practical, consistent, and process-oriented. You excel at building reliable systems and executing complex projects with precision.",
        "careers": ["Software Engineer", "Operations Manager", "Project Manager", "Systems Architect", "Manufacturing Engineer"],
        "companies": ["Tech companies", "Manufacturing firms", "Logistics companies", "Infrastructure organizations"]
    },
    "people_champion": {
        "name": "People Champion",
        "description": "You are empathetic, relationship-focused, and ethically driven. You excel at understanding people and creating positive change through collaboration.",
        "careers": ["HR Manager", "Teacher", "Social Worker", "Customer Success Manager", "Counselor"],
        "companies": ["NGOs", "Educational institutions", "Healthcare organizations", "Community-focused companies"]
    },
    "strategic_pragmatist": {
        "name": "Strategic Pragmatist",
        "description": "You are balanced, adaptive, and outcome-focused. You excel at navigating complexity and finding practical solutions to strategic challenges.",
        "careers": ["Management Consultant", "Business Development Manager", "Strategy Manager", "Product Manager", "Account Director"],
        "companies": ["Consulting firms", "B2B companies", "Scale-ups", "Corporate strategy teams"]
    }
}

# Scenarios Database
SCENARIOS = {
    "micro_scenarios": [
        {
            "id": "s1",
            "text": "Your team missed a critical project deadline. What do you do?",
            "options": {
                "A": "Work overnight to complete it yourself",
                "B": "Negotiate an extension with stakeholders",
                "C": "Deliver partial work and explain priorities"
            }
        },
        {
            "id": "s2",
            "text": "You discover a faster method that technically violates company guidelines. Do you:",
            "options": {
                "A": "Follow the official process",
                "B": "Use the shortcut and report it later",
                "C": "Discuss it with your manager first"
            }
        },
        {
            "id": "s3",
            "text": "A coworker takes credit for your idea in a meeting. You:",
            "options": {
                "A": "Confront them privately after",
                "B": "Immediately clarify in the meeting",
                "C": "Let it go and focus on future work"
            }
        },
        {
            "id": "s4",
            "text": "You have two job offers: High pay with long hours, or lower pay with work-life balance. You choose:",
            "options": {
                "A": "Lower pay, better balance",
                "B": "High pay, invest now for future",
                "C": "Negotiate better terms with both"
            }
        },
        {
            "id": "s5",
            "text": "Your manager asks you to lie to a client about a product delay. You:",
            "options": {
                "A": "Refuse and suggest being honest",
                "B": "Do it to avoid conflict",
                "C": "Find a way to share partial truth"
            }
        },
        {
            "id": "s6",
            "text": "You're assigned a project you've never done before. Your first step:",
            "options": {
                "A": "Research thoroughly before starting",
                "B": "Jump in and learn by doing",
                "C": "Ask experienced colleagues for guidance"
            }
        },
        {
            "id": "s7",
            "text": "During a presentation, you realize your data has a major error. You:",
            "options": {
                "A": "Stop and correct it immediately",
                "B": "Continue and fix it later",
                "C": "Acknowledge it and reschedule"
            }
        },
        {
            "id": "s8",
            "text": "A startup offers equity instead of full salary. You:",
            "options": {
                "A": "Decline - need stable income",
                "B": "Accept - high risk, high reward",
                "C": "Negotiate a balanced split"
            }
        },
        {
            "id": "s9",
            "text": "Your friend asks you to refer them for a job they're unqualified for. You:",
            "options": {
                "A": "Politely decline",
                "B": "Refer them anyway",
                "C": "Help them build skills first"
            }
        },
        {
            "id": "s10",
            "text": "You notice a colleague struggling but they haven't asked for help. You:",
            "options": {
                "A": "Offer help proactively",
                "B": "Wait for them to ask",
                "C": "Mention it to their manager"
            }
        },
        {
            "id": "s11",
            "text": "You have a great idea but your team disagrees. You:",
            "options": {
                "A": "Push harder with more evidence",
                "B": "Accept majority decision",
                "C": "Build a prototype on your own time"
            }
        },
        {
            "id": "s12",
            "text": "You can automate your job but it might eliminate positions. You:",
            "options": {
                "A": "Don't automate - protect jobs",
                "B": "Automate - efficiency matters",
                "C": "Automate but propose retraining"
            }
        },
        {
            "id": "s13",
            "text": "A competitor offers you double salary to share company secrets. You:",
            "options": {
                "A": "Decline immediately",
                "B": "Report them to your company",
                "C": "Consider it if secrets are minor"
            }
        },
        {
            "id": "s14",
            "text": "You're stuck on a problem for hours. You:",
            "options": {
                "A": "Keep trying different approaches",
                "B": "Ask for help immediately",
                "C": "Take a break and return fresh"
            }
        },
        {
            "id": "s15",
            "text": "Your company asks you to relocate to another city. You:",
            "options": {
                "A": "Accept - new opportunities",
                "B": "Decline - roots matter",
                "C": "Negotiate remote work option"
            }
        }
    ]
}


class BehavioralProfiler:
    """Analyzes user behavior and determines career archetype"""
    
    def __init__(self):
        self.signals = {
            "decision_speed": 0,
            "edit_frequency": 0,
            "risk_preference": 0,
            "value_hierarchy": 0,
            "consistency": 0
        }
    
    def analyze_micro_decisions(self, decisions):
        """Analyze rapid-fire micro-decisions"""
        if not decisions:
            return self.signals
        
        # Signal 1: Decision Speed
        avg_time = sum(d['time_taken'] for d in decisions) / len(decisions)
        if avg_time < 8:
            self.signals['decision_speed'] = 2  # Fast/Intuitive
        elif avg_time > 15:
            self.signals['decision_speed'] = -2  # Slow/Analytical
        else:
            self.signals['decision_speed'] = 0
        
        # Signal 3: Consistency
        choices = [d['choice'] for d in decisions]
        choice_counts = {}
        for choice in choices:
            choice_counts[choice] = choice_counts.get(choice, 0) + 1
        
        max_frequency = max(choice_counts.values())
        consistency_ratio = max_frequency / len(choices)
        
        if consistency_ratio > 0.6:
            self.signals['consistency'] = 2  # Highly consistent
        elif consistency_ratio < 0.4:
            self.signals['consistency'] = -2  # Adaptive
        else:
            self.signals['consistency'] = 0
        
        # Signal 4: Risk Preference
        risk_choices = sum(1 for d in decisions if d.get('choice') in ['B', 'C'])
        risk_ratio = risk_choices / len(decisions)
        
        if risk_ratio > 0.6:
            self.signals['risk_preference'] = 2  # Risk-taking
        elif risk_ratio < 0.4:
            self.signals['risk_preference'] = -2  # Risk-averse
        else:
            self.signals['risk_preference'] = 0
        
        # Signal 5: Value Hierarchy
        ethical_choices = sum(1 for d in decisions if d.get('choice') == 'A')
        pragmatic_choices = sum(1 for d in decisions if d.get('choice') == 'C')
        
        if ethical_choices > pragmatic_choices * 1.5:
            self.signals['value_hierarchy'] = 2  # Ethics-driven
        elif pragmatic_choices > ethical_choices * 1.5:
            self.signals['value_hierarchy'] = -2  # Pragmatic
        else:
            self.signals['value_hierarchy'] = 0
        
        return self.signals
    
    def analyze_deep_scenario(self, response_data):
        """Analyze deep scenario response"""
        if not response_data:
            return self.signals
        
        # Signal 2: Edit Frequency
        edit_count = response_data.get('edit_count', 0)
        if edit_count >= 5:
            self.signals['edit_frequency'] = -2  # Cautious
        elif edit_count <= 1:
            self.signals['edit_frequency'] = 2  # Decisive
        else:
            self.signals['edit_frequency'] = 0
        
        return self.signals
    
    def determine_archetype(self):
        """Map behavioral signals to career archetype"""
        scores = {
            "analytical_guardian": 0,
            "creative_maverick": 0,
            "systematic_builder": 0,
            "people_champion": 0,
            "strategic_pragmatist": 0
        }
        
        s = self.signals
        
        # Analytical Guardian: Slow, Cautious, Consistent, Risk-averse
        if s['decision_speed'] <= -1:
            scores['analytical_guardian'] += 2
        if s['edit_frequency'] <= -1:
            scores['analytical_guardian'] += 2
        if s['consistency'] >= 1:
            scores['analytical_guardian'] += 2
        if s['risk_preference'] <= -1:
            scores['analytical_guardian'] += 2
        
        # Creative Maverick: Fast, Risk-taking, Value-driven
        if s['decision_speed'] >= 1:
            scores['creative_maverick'] += 2
        if s['risk_preference'] >= 1:
            scores['creative_maverick'] += 2
        if s['value_hierarchy'] >= 1:
            scores['creative_maverick'] += 2
        
        # Systematic Builder: Moderate, Consistent, Practical
        if abs(s['decision_speed']) <= 1:
            scores['systematic_builder'] += 2
        if s['consistency'] >= 1:
            scores['systematic_builder'] += 2
        if s['value_hierarchy'] <= 0:
            scores['systematic_builder'] += 1
        
        # People Champion: Ethical, Relationship-focused
        if s['value_hierarchy'] >= 1:
            scores['people_champion'] += 3
        if abs(s['risk_preference']) <= 1:
            scores['people_champion'] += 1
        
        # Strategic Pragmatist: Balanced, Adaptive
        if abs(s['decision_speed']) <= 1:
            scores['strategic_pragmatist'] += 1
        if s['consistency'] <= 0:
            scores['strategic_pragmatist'] += 2
        if s['value_hierarchy'] <= 0:
            scores['strategic_pragmatist'] += 2
        
        # Find top archetype
        top_archetype = max(scores.items(), key=lambda x: x[1])[0]
        return top_archetype, ARCHETYPES[top_archetype]
    
    def generate_report(self, user_data):
        """Generate complete profile report with job matches"""
        self.analyze_micro_decisions(user_data.get('micro_decisions', []))
        self.analyze_deep_scenario(user_data.get('deep_scenario', {}))
        
        archetype_key, archetype_details = self.determine_archetype()
        
        # Get matching jobs
        matched_jobs = get_jobs_by_archetype(archetype_key, limit=5)
        
        report = {
            "archetype": archetype_details['name'],
            "archetype_key": archetype_key,
            "description": archetype_details['description'],
            "top_careers": archetype_details['careers'][:3],
            "suitable_companies": archetype_details['companies'],
            "behavioral_profile": {
                "thinking_style": "Analytical" if self.signals['decision_speed'] < 0 else "Intuitive",
                "decision_approach": "Cautious" if self.signals['edit_frequency'] < 0 else "Decisive",
                "risk_attitude": "Conservative" if self.signals['risk_preference'] < 0 else "Entrepreneurial",
                "value_priority": "Purpose-driven" if self.signals['value_hierarchy'] > 0 else "Pragmatic",
                "adaptability": "Principled" if self.signals['consistency'] > 0 else "Flexible"
            },
            "matched_jobs": matched_jobs,
            "signal_scores": self.signals,
            "timestamp": datetime.now().isoformat()
        }
        
        return report


# API Routes

@app.route('/')
def home():
    return jsonify({
        "message": "PATHAI API Server",
        "version": "1.0",
        "endpoints": [
            "/api/scenarios",
            "/api/analyze"
        ]
    })

@app.route('/api/scenarios', methods=['GET'])
def get_scenarios():
    """Return all scenarios"""
    return jsonify(SCENARIOS)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyze user behavior and return career profile"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Create profiler and generate report
        profiler = BehavioralProfiler()
        report = profiler.generate_report(data)
        
        return jsonify(report)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    """Get all available jobs"""
    archetype = request.args.get('archetype', None)
    
    if archetype:
        jobs = get_jobs_by_archetype(archetype, limit=20)
    else:
        jobs = get_all_jobs()
    
    return jsonify({
        "jobs": jobs,
        "count": len(jobs)
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get platform statistics"""
    stats = get_job_stats()
    
    # Add impact metrics
    stats['impact_metrics'] = {
        "assessments_completed": 1247,  # Mock data for demo
        "successful_placements": 342,
        "avg_time_to_hire_days": 45,
        "placement_rate": "27.4%",
        "companies_partnered": len(COMPANIES)
    }
    
    return jsonify(stats)

@app.route('/api/companies', methods=['GET'])
def get_companies():
    """Get all companies"""
    return jsonify({
        "companies": COMPANIES,
        "count": len(COMPANIES)
    })


if __name__ == '__main__':
    print("🚀 PATHAI Backend Server Starting...")
    print("📍 Running on http://localhost:5000")
    print("📡 API Endpoints:")
    print("   - GET  /api/scenarios")
    print("   - POST /api/analyze")
    print("   - GET  /api/jobs?archetype=<archetype>")
    print("   - GET  /api/stats")
    print("   - GET  /api/companies")
    print("\n✨ Ready to receive requests!\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)