import os
import sys

# Add current dir to path
sys.path.append(os.getcwd())

from utils.resume_parser import parse_resume
from utils.scorer import rank_candidates

def test_utils():
    print("Testing Utils...")
    
    # Create a dummy text file
    with open("test_resume.txt", "w") as f:
        f.write("I am a software engineer with python and fastAPI skills.")
    
    # Test Parser
    text = parse_resume("test_resume.txt")
    print(f"Parsed Text: {text}")
    assert "software engineer" in text
    
    # Test Scorer
    job_text = "Looking for a software engineer with python skills."
    cands = [(1, text), (2, "I am a chef with cooking skills.")]
    
    ranked = rank_candidates(job_text, cands)
    print(f"Ranked: {ranked}")
    
    # ID 1 should be higher than ID 2
    assert ranked[0][0] == 1
    
    print("✅ Utils Verified Success!")
    
    # Cleanup
    if os.path.exists("test_resume.txt"):
        os.remove("test_resume.txt")

if __name__ == "__main__":
    test_utils()
