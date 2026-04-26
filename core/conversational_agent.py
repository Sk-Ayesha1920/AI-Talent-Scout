import random
import time

class ConversationalAgent:
    def __init__(self):
        """Initializes the mock conversational agent."""
        # Pre-defined templates for simulation
        self.questions = [
            "Hi {name}, we have an exciting {role} position. Would you be open to a quick chat about it?",
            "What interests you most about a new opportunity right now?",
            "Can you tell me briefly about a recent project you are proud of?"
        ]
        
    def simulate_outreach(self, candidate, jd_summary=""):
        """
        Simulates an outreach conversation with a candidate.
        Returns a dialogue history and an Interest Score (0-100).
        """
        name = candidate.get('name', 'Candidate')
        role = candidate.get('role', 'position')
        base_interest = candidate.get('interest_level_indicator', 'Medium')
        
        dialogue = []
        
        # Q1: Initial Outreach
        q1 = self.questions[0].format(name=name, role=role)
        dialogue.append({"speaker": "Agent", "text": q1})
        
        # Simulate thinking time in real usage, but fast for the app
        time.sleep(0.1) 
        
        # Determine engagement based on their hidden indicator
        if base_interest == "High":
            interest_score = random.randint(85, 100)
            a1 = f"Hi! Yes, I am actively looking and this {role} role sounds very aligned with my goals. I'd love to chat."
            a2 = "I'm looking for a place where I can utilize my skills to solve complex problems and grow into a leadership role."
        elif base_interest == "Medium":
            interest_score = random.randint(50, 84)
            a1 = f"Hello. I am not actively looking, but I am open to hearing more about the {role} role."
            a2 = "I'd be interested if it offers good work-life balance and interesting technical challenges."
        else: # Low
            interest_score = random.randint(10, 49)
            a1 = f"Hi, thanks for reaching out. I'm quite happy in my current role, but maybe we can connect for the future."
            a2 = "I'm not really looking to move unless it's an extraordinary offer."
            
        dialogue.append({"speaker": "Candidate", "text": a1})
        
        # If they are somewhat interested, continue the chat
        if interest_score >= 50:
            dialogue.append({"speaker": "Agent", "text": self.questions[1]})
            dialogue.append({"speaker": "Candidate", "text": a2})
            
            # Simple summarization for the explanation
            explanation = f"Candidate showed positive engagement and articulated clear goals. Computed Interest Score: {interest_score}/100."
        else:
            explanation = f"Candidate is currently passive and not looking for immediate moves. Computed Interest Score: {interest_score}/100."
            
        return {
            "interest_score": interest_score,
            "dialogue": dialogue,
            "explanation": explanation
        }
