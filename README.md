AI-Powered Talent Scouting & Engagement Agent

This is a prototype of an AI recruitment system designed to automate and improve how companies find and evaluate candidates. It uses semantic matching to compare a Job Description (JD) against candidate profiles and simulates a conversational outreach to assess their interest level.

## Features
- **Semantic Matching (Match Score)**: Uses `sentence-transformers` (`all-MiniLM-L6-v2`) to convert text into embeddings and calculate cosine similarity between the JD and candidate profiles.
- **Conversational Intelligence (Interest Score)**: Simulates a dialogue with the candidate to assess their engagement and interest level, factoring this into a secondary score.
- **Combined Ranking**: Outputs a final list of candidates ranked by a weighted combination of Match and Interest scores.
- **Explainability**: Provides human-readable reasoning for why a candidate matched and summarizes their engagement.
- **UI Dashboard**: Built with Streamlit for a fast, responsive user interface.

## Architecture

![alt text]("A:\Architecture.png")


## Setup Instructions


1. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

4. **Usage**:
   - The app will open in your browser (usually `http://localhost:8501`).
   - Paste a sample Job Description in the text area (e.g., "Looking for a Senior Python developer with AWS and Docker experience").
   - Click "Run AI Scouting Pipeline".
   - Review the ranked candidates, match explanations, and simulated conversation transcripts.

## Data
The `data/candidates.json` file contains a mock dataset of 10 candidates with diverse skills and hidden "interest" indicators to demonstrate the scoring logic effectively.
