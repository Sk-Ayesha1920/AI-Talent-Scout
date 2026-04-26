import json
import os
import pandas as pd

def load_candidates(filepath="data/candidates.json"):
    """Loads candidate data from a JSON file and returns a pandas DataFrame."""
    try:
        if not os.path.exists(filepath):
            # Fallback path if running from a different working directory
            fallback_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'candidates.json')
            if os.path.exists(fallback_path):
                filepath = fallback_path
            else:
                return pd.DataFrame() # Return empty if not found
                
        with open(filepath, 'r') as f:
            data = json.load(f)
        return pd.DataFrame(data)
    except Exception as e:
        print(f"Error loading candidates: {e}")
        return pd.DataFrame()

def prepare_candidate_text_for_embedding(df):
    """Combines candidate attributes into a single text string for better semantic matching."""
    if df.empty:
        return []
        
    texts = []
    for _, row in df.iterrows():
        # Create a rich text representation of the candidate
        skills_str = ", ".join(row['skills']) if isinstance(row['skills'], list) else row['skills']
        text = f"Role: {row['role']}. Experience: {row['experience_years']} years. Skills: {skills_str}. Summary: {row['summary']}"
        texts.append(text)
    return texts
