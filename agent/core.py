"""
Core Agent Logic for StudyMate - Simplified Version
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from .tools import (
    analyze_repo_structure,
    extract_code_snippet,
    search_repo_concept,
    generate_socratic_question,
    assess_student_understanding,
    provide_progressive_hint,
    track_learning_progress
)
from .prompts import SYSTEM_PROMPT
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class StudyMateAgent:
    """
    Main teaching agent that uses Socratic method to guide learning.
    Simplified version without LangChain Agent framework.
    """
    
    def __init__(self, repo_path: str = None):
        """
        Initialize the StudyMate agent.
        
        Args:
            repo_path: Path to the cloned repository
        """
        self.repo_path = repo_path
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model=self.model,
            temperature=0.7
        )
        
        # Simple chat history
        self.chat_history = [SystemMessage(content=SYSTEM_PROMPT)]
    
    def teach(self, student_input: str, session_id: str = None) -> str:
        """
        Main teaching interaction.
        
        Args:
            student_input: What the student said
            session_id: Session identifier for progress tracking
            
        Returns:
            Agent's response
        """
        try:
            # Add repo path context if available
            if self.repo_path:
                enhanced_input = f"[Repository at: {self.repo_path}]\n\nStudent: {student_input}"
            else:
                enhanced_input = student_input
            
            # Add student message to history
            self.chat_history.append(HumanMessage(content=enhanced_input))
            
            # Get response from LLM
            response = self.llm.invoke(self.chat_history)
            
            # Add AI response to history
            self.chat_history.append(AIMessage(content=response.content))
            
            # Keep only last 12 messages (system + 5 exchanges)
            if len(self.chat_history) > 12:
                self.chat_history = [self.chat_history[0]] + self.chat_history[-11:]
            
            return response.content
            
        except Exception as e:
            print(f"Agent error: {str(e)}")
            return "I encountered an issue. Could you rephrase your question?"
    
    def reset_memory(self):
        """Clears conversation history."""
        self.chat_history = [SystemMessage(content=SYSTEM_PROMPT)]
