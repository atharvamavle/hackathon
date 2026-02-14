"""
Test script for StudyMates Agent
"""

from agent import StudyMateAgent
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def test_agent():
    """Test the agent with a simple conversation."""
    
    print("🧪 Testing StudyMates Agent...\n")
    
    # Check OpenAI key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not set in .env file!")
        return
    
    print("✅ OpenAI key found")
    
    # Initialize agent (without repo for now)
    print("🔧 Initializing agent...")
    agent = StudyMateAgent(repo_path=None)
    print("✅ Agent initialized\n")
    
    # Test 1: Simple greeting
    print("=" * 60)
    print("TEST 1: Ask about Python")
    print("=" * 60)
    
    student_input = "I want to learn about functions in Python"
    print(f"\n👤 Student: {student_input}\n")
    
    response = agent.teach(student_input, session_id="test-session-1")
    print(f"🤖 Agent: {response}\n")
    
    # Test 2: Follow-up question
    print("=" * 60)
    print("TEST 2: Follow-up")
    print("=" * 60)
    
    student_input = "A function is like a reusable piece of code"
    print(f"\n👤 Student: {student_input}\n")
    
    response = agent.teach(student_input, session_id="test-session-1")
    print(f"🤖 Agent: {response}\n")
    
    print("✅ Agent test complete!")

if __name__ == "__main__":
    test_agent()
