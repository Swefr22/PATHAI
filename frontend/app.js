// PATHAI Frontend JavaScript

// Configuration
const API_URL = 'http://localhost:5000/api'; // Change this when deploying

// State Management
let scenarios = [];
let currentScenarioIndex = 0;
let sessionData = {
    micro_decisions: [],
    deep_scenario: {}
};
let scenarioStartTime = null;
let deepScenarioStartTime = null;
let editCount = 0;
let lastKeystrokeTime = null;
let keystrokePauses = [];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadScenarios();
    setupDeepScenarioTracking();
});

// Load scenarios from backend
async function loadScenarios() {
    try {
        const response = await fetch(`${API_URL}/scenarios`);
        const data = await response.json();
        scenarios = data.micro_scenarios;
        console.log('Scenarios loaded:', scenarios.length);
    } catch (error) {
        console.error('Error loading scenarios:', error);
        // Fallback to embedded scenarios if API fails
        loadFallbackScenarios();
    }
}

// Fallback scenarios if backend is not available
function loadFallbackScenarios() {
    scenarios = [
        {
            id: "s1",
            text: "Your team missed a critical project deadline. What do you do?",
            options: {
                A: "Work overnight to complete it yourself",
                B: "Negotiate an extension with stakeholders",
                C: "Deliver partial work and explain priorities"
            }
        },
        {
            id: "s2",
            text: "You discover a faster method that technically violates company guidelines. Do you:",
            options: {
                A: "Follow the official process",
                B: "Use the shortcut and report it later",
                C: "Discuss it with your manager first"
            }
        },
        {
            id: "s3",
            text: "A coworker takes credit for your idea in a meeting. You:",
            options: {
                A: "Confront them privately after",
                B: "Immediately clarify in the meeting",
                C: "Let it go and focus on future work"
            }
        },
        {
            id: "s4",
            text: "You have two job offers: High pay with long hours, or lower pay with work-life balance. You choose:",
            options: {
                A: "Lower pay, better balance",
                B: "High pay, invest now for future",
                C: "Negotiate better terms with both"
            }
        },
        {
            id: "s5",
            text: "Your manager asks you to lie to a client about a product delay. You:",
            options: {
                A: "Refuse and suggest being honest",
                B: "Do it to avoid conflict",
                C: "Find a way to share partial truth"
            }
        },
        {
            id: "s6",
            text: "You're assigned a project you've never done before. Your first step:",
            options: {
                A: "Research thoroughly before starting",
                B: "Jump in and learn by doing",
                C: "Ask experienced colleagues for guidance"
            }
        },
        {
            id: "s7",
            text: "During a presentation, you realize your data has a major error. You:",
            options: {
                A: "Stop and correct it immediately",
                B: "Continue and fix it later",
                C: "Acknowledge it and reschedule"
            }
        },
        {
            id: "s8",
            text: "A startup offers equity instead of full salary. You:",
            options: {
                A: "Decline - need stable income",
                B: "Accept - high risk, high reward",
                C: "Negotiate a balanced split"
            }
        },
        {
            id: "s9",
            text: "Your friend asks you to refer them for a job they're unqualified for. You:",
            options: {
                A: "Politely decline",
                B: "Refer them anyway",
                C: "Help them build skills first"
            }
        },
        {
            id: "s10",
            text: "You notice a colleague struggling but they haven't asked for help. You:",
            options: {
                A: "Offer help proactively",
                B: "Wait for them to ask",
                C: "Mention it to their manager"
            }
        },
        {
            id: "s11",
            text: "You have a great idea but your team disagrees. You:",
            options: {
                A: "Push harder with more evidence",
                B: "Accept majority decision",
                C: "Build a prototype on your own time"
            }
        },
        {
            id: "s12",
            text: "You can automate your job but it might eliminate positions. You:",
            options: {
                A: "Don't automate - protect jobs",
                B: "Automate - efficiency matters",
                C: "Automate but propose retraining"
            }
        },
        {
            id: "s13",
            text: "A competitor offers you double salary to share company secrets. You:",
            options: {
                A: "Decline immediately",
                B: "Report them to your company",
                C: "Consider it if secrets are minor"
            }
        },
        {
            id: "s14",
            text: "You're stuck on a problem for hours. You:",
            options: {
                A: "Keep trying different approaches",
                B: "Ask for help immediately",
                C: "Take a break and return fresh"
            }
        },
        {
            id: "s15",
            text: "Your company asks you to relocate to another city. You:",
            options: {
                A: "Accept - new opportunities",
                B: "Decline - roots matter",
                C: "Negotiate remote work option"
            }
        }
    ];
}

// Start the test
function startTest() {
    document.getElementById('landing').classList.add('hidden');
    document.getElementById('scenarioScreen').style.display = 'block';
    currentScenarioIndex = 0;
    sessionData.micro_decisions = [];
    showScenario(currentScenarioIndex);
}

// Display a scenario
function showScenario(index) {
    if (index >= scenarios.length) {
        showDeepScenario();
        return;
    }

    const scenario = scenarios[index];
    scenarioStartTime = Date.now();

    // Update progress
    const progress = ((index + 1) / scenarios.length) * 100;
    document.getElementById('progressFill').style.width = progress + '%';
    document.getElementById('progressText').textContent = `Question ${index + 1} of ${scenarios.length}`;

    // Display scenario
    document.getElementById('scenarioText').textContent = scenario.text;

    // Create choice buttons
    const choicesContainer = document.getElementById('choices');
    choicesContainer.innerHTML = '';

    Object.keys(scenario.options).forEach(choice => {
        const button = document.createElement('button');
        button.className = 'choice-btn';
        button.textContent = `${choice}. ${scenario.options[choice]}`;
        button.onclick = () => recordChoice(scenario.id, choice);
        choicesContainer.appendChild(button);
    });
}

// Record user choice
function recordChoice(scenarioId, choice) {
    const timeTaken = (Date.now() - scenarioStartTime) / 1000;

    sessionData.micro_decisions.push({
        scenario_id: scenarioId,
        choice: choice,
        time_taken: timeTaken,
        timestamp: new Date().toISOString()
    });

    currentScenarioIndex++;
    showScenario(currentScenarioIndex);
}

// Show deep scenario
function showDeepScenario() {
    document.getElementById('scenarioScreen').style.display = 'none';
    document.getElementById('deepScreen').style.display = 'block';

    const deepScenarioText = "You are leading the launch of your company's flagship product tomorrow. At 6 PM today, you discover: (1) A critical bug that affects 30% of users, (2) Your marketing team already sent press releases, (3) Investors are attending the launch event, (4) Fixing the bug needs 48 hours, (5) Your team is exhausted from months of work. What do you do and why?";
    
    document.getElementById('deepScenarioText').textContent = deepScenarioText;
    deepScenarioStartTime = Date.now();
    editCount = 0;
    keystrokePauses = [];
    lastKeystrokeTime = Date.now();
}

// Setup deep scenario tracking
function setupDeepScenarioTracking() {
    const textarea = document.getElementById('deepResponse');
    
    // Track edits (backspace/delete)
    textarea.addEventListener('keydown', (e) => {
        if (e.key === 'Backspace' || e.key === 'Delete') {
            editCount++;
        }

        // Track keystroke pauses
        const now = Date.now();
        if (lastKeystrokeTime) {
            const pause = (now - lastKeystrokeTime) / 1000;
            if (pause > 2) {
                keystrokePauses.push(pause);
            }
        }
        lastKeystrokeTime = now;
    });

    // Update word count
    textarea.addEventListener('input', () => {
        const text = textarea.value.trim();
        const words = text.split(/\s+/).filter(word => word.length > 0);
        document.getElementById('wordCount').textContent = words.length;
    });
}

// Submit deep scenario
async function submitDeepScenario() {
    const textarea = document.getElementById('deepResponse');
    const text = textarea.value.trim();
    
    // Validate
    const wordCount = text.split(/\s+/).filter(word => word.length > 0).length;
    if (wordCount < 40) {
        alert('Please write at least 40 words to complete your response.');
        return;
    }

    // Calculate time taken
    const timeTaken = (Date.now() - deepScenarioStartTime) / 1000;

    // Store deep scenario data
    sessionData.deep_scenario = {
        text: text,
        time_taken: timeTaken,
        edit_count: editCount,
        word_count: wordCount,
        keystroke_pauses: keystrokePauses
    };

    // Show loading
    document.getElementById('deepScreen').style.display = 'none';
    document.getElementById('loading').style.display = 'block';

    // Submit to backend
    try {
        const response = await fetch(`${API_URL}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(sessionData)
        });

        if (!response.ok) {
            throw new Error('Analysis failed');
        }

        const result = await response.json();
        displayResults(result);
    } catch (error) {
        console.error('Error analyzing data:', error);
        // Show error message
        alert('Unable to connect to server. Please ensure the backend is running.');
        document.getElementById('loading').style.display = 'none';
        document.getElementById('deepScreen').style.display = 'block';
    }
}

// Display results
function displayResults(report) {
    document.getElementById('loading').style.display = 'none';
    document.getElementById('resultsScreen').style.display = 'block';

    // Archetype
    document.getElementById('archetypeName').textContent = report.archetype;
    document.getElementById('archetypeDesc').textContent = report.description;

    // Careers
    const careerList = document.getElementById('careerList');
    careerList.innerHTML = '';
    report.top_careers.forEach(career => {
        const div = document.createElement('div');
        div.className = 'career-item';
        div.textContent = career;
        careerList.appendChild(div);
    });

    // Behavioral Profile
    const profileGrid = document.getElementById('profileGrid');
    profileGrid.innerHTML = '';
    Object.entries(report.behavioral_profile).forEach(([key, value]) => {
        const div = document.createElement('div');
        div.className = 'profile-item';
        div.innerHTML = `<strong>${formatKey(key)}</strong>${value}`;
        profileGrid.appendChild(div);
    });

    // Companies
    const companyList = document.getElementById('companyList');
    companyList.innerHTML = '';
    report.suitable_companies.forEach(company => {
        const div = document.createElement('div');
        div.className = 'career-item';
        div.textContent = company;
        companyList.appendChild(div);
    });

    // Store report for download
    window.currentReport = report;
}

// Format key names
function formatKey(key) {
    return key.split('_').map(word => 
        word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ') + ': ';
}

// Download report
function downloadReport() {
    if (!window.currentReport) return;

    const report = window.currentReport;
    const text = `
PATHAI Career Assessment Report
Generated: ${new Date().toLocaleString()}

========================================
YOUR CAREER ARCHETYPE
========================================
${report.archetype}

${report.description}

========================================
TOP CAREER MATCHES
========================================
${report.top_careers.map((c, i) => `${i + 1}. ${c}`).join('\n')}

========================================
YOUR BEHAVIORAL PROFILE
========================================
${Object.entries(report.behavioral_profile).map(([k, v]) => `${formatKey(k)}${v}`).join('\n')}

========================================
SUITABLE COMPANY TYPES
========================================
${report.suitable_companies.map((c, i) => `${i + 1}. ${c}`).join('\n')}

========================================
NEXT STEPS
========================================
1. Research the suggested career paths
2. Connect with professionals in these fields
3. Explore internships or projects in these areas
4. Continue developing your strengths

For more information, visit: www.pathai.in
    `.trim();

    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'PATHAI_Career_Report.txt';
    a.click();
    URL.revokeObjectURL(url);
}

// Restart test
function restartTest() {
    location.reload();
}