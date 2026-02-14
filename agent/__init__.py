"""
StudyMate Agent Module
"""

from .core import StudyMateAgent
from .tools import (
    analyze_repo_structure,
    extract_code_snippet,
    search_repo_concept,
    generate_socratic_question,
    assess_student_understanding,
    provide_progressive_hint,
    track_learning_progress
)

__all__ = [
    'StudyMateAgent',
    'analyze_repo_structure',
    'extract_code_snippet',
    'search_repo_concept',
    'generate_socratic_question',
    'assess_student_understanding',
    'provide_progressive_hint',
    'track_learning_progress'
]
