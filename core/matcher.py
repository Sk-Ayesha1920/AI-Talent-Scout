from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class CandidateMatcher:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """Initializes the matcher with a pre-trained sentence transformer model."""
        # Using a lightweight local model perfect for prototyping
        print(f"Loading embedding model {model_name}...")
        self.model = SentenceTransformer(model_name)
        print("Model loaded successfully.")
        
    def generate_embeddings(self, texts):
        """Generates embeddings for a list of texts."""
        if not texts:
            return np.array([])
        return self.model.encode(texts)
        
    def calculate_match_scores(self, jd_text, candidate_embeddings):
        """
        Calculates cosine similarity between the Job Description and candidate embeddings.
        Returns a list of scores between 0 and 100.
        """
        if len(candidate_embeddings) == 0:
            return []
            
        # Encode the Job Description
        jd_embedding = self.model.encode([jd_text])
        
        # Calculate cosine similarity
        # Returns a matrix of shape (1, num_candidates)
        similarities = cosine_similarity(jd_embedding, candidate_embeddings)[0]
        
        # Convert to a 0-100 scale and round
        scores = [round(float(score) * 100, 1) for score in similarities]
        return scores
        
    def get_match_explanation(self, jd_text, candidate):
        """
        Generates a simple rule-based explanation for the match.
        (In a full production system with an API key, this would use an LLM).
        """
        jd_lower = jd_text.lower()
        matched_skills = []
        
        skills = candidate['skills']
        if isinstance(skills, str):
            skills = [s.strip() for s in skills.split(',')]
            
        for skill in skills:
            if skill.lower() in jd_lower:
                matched_skills.append(skill)
                
        if matched_skills:
            return f"Strong match found on key skills: {', '.join(matched_skills)}."
        else:
            return "Matches based on general semantic similarity of experience and role description, though specific keyword overlap is low."
