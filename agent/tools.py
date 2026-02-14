"""
Agent Tools for StudyMate
"""

from langchain.tools import tool
from langchain_openai import ChatOpenAI
import os
import json
from datetime import datetime
from typing import Optional


@tool
def analyze_repo_structure(repo_path: str) -> dict:
    """
    Analyzes GitHub repository structure to understand project layout.
    
    Args:
        repo_path: Path to the repository directory
        
    Returns:
        Dictionary with repo structure information
    """
    if not os.path.exists(repo_path):
        return {"error": f"Repository path does not exist: {repo_path}"}
    
    structure = {
        "total_files": 0,
        "main_directories": [],
        "key_files": [],
        "languages": {},
        "readme_exists": False
    }
    
    # Walk through repo
    for root, dirs, files in os.walk(repo_path):
        # Skip hidden and cache dirs
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules', 'venv']]
        
        for file in files:
            if file.startswith('.'):
                continue
                
            structure["total_files"] += 1
            ext = os.path.splitext(file)[1]
            if ext:
                structure["languages"][ext] = structure["languages"].get(ext, 0) + 1
            
            # Identify key files
            if file.lower() in ['readme.md', 'readme.txt']:
                structure["key_files"].append(os.path.join(root, file))
                structure["readme_exists"] = True
            elif file in ['requirements.txt', 'setup.py', 'main.py', 'app.py']:
                structure["key_files"].append(os.path.join(root, file))
    
    structure["main_directories"] = [
        d for d in os.listdir(repo_path) 
        if os.path.isdir(os.path.join(repo_path, d)) and not d.startswith('.')
    ]
    
    return structure


@tool
def extract_code_snippet(file_path: str, line_start: int, line_end: int) -> dict:
    """
    Extracts specific code snippets from a file by line numbers.
    
    Args:
        file_path: Path to the code file
        line_start: Starting line number (1-indexed)
        line_end: Ending line number (1-indexed)
        
    Returns:
        Dictionary with extracted code and context
    """
    if not os.path.exists(file_path):
        return {"error": f"File does not exist: {file_path}"}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        return {"error": f"Could not read file: {str(e)}"}
    
    if line_start < 1 or line_end > len(lines):
        return {"error": f"Line numbers out of range (file has {len(lines)} lines)"}
    
    code = ''.join(lines[line_start-1:line_end])
    
    return {
        "file_path": file_path,
        "file_name": os.path.basename(file_path),
        "code": code,
        "start_line": line_start,
        "end_line": line_end,
        "total_lines": len(lines)
    }


@tool
def search_repo_concept(query: str, repo_path: str) -> str:
    """
    Searches repository for code related to a specific concept.
    Simple keyword search through Python files.
    
    Args:
        query: The concept to search for
        repo_path: Path to repository
        
    Returns:
        String with relevant file paths and snippets
    """
    results = []
    query_lower = query.lower()
    
    try:
        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                            if query_lower in content.lower():
                                lines = content.split('\n')
                                for i, line in enumerate(lines):
                                    if query_lower in line.lower():
                                        start = max(0, i-2)
                                        end = min(len(lines), i+3)
                                        snippet = '\n'.join(lines[start:end])
                                        results.append({
                                            "file": file_path,
                                            "line": i+1,
                                            "snippet": snippet
                                        })
                                        break
                    except:
                        continue
            
            if len(results) >= 3:
                break
        
        if not results:
            return f"No code found related to '{query}' in the repository."
        
        formatted = f"Found {len(results)} file(s) related to '{query}':\n\n"
        for i, result in enumerate(results[:3], 1):
            formatted += f"{i}. **{os.path.basename(result['file'])}** (Line {result['line']})\n"
            formatted += f"```python\n{result['snippet']}\n```\n\n"
        
        return formatted
        
    except Exception as e:
        return f"Error searching repository: {str(e)}"


@tool
def generate_socratic_question(concept: str, student_level: str) -> str:
    """
    Generates a Socratic question to guide student learning.
    
    Args:
        concept: The concept being taught
        student_level: Student's knowledge level (beginner/intermediate/advanced)
        
    Returns:
        A Socratic question string
    """
    llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0.7)
    
    prompt = f"""Generate ONE Socratic question to teach this programming concept.

Concept: {concept}
Student level: {student_level}

The question should:
1. Guide discovery (don't give the answer)
2. Build on their knowledge level
3. Be specific and focused
4. Encourage critical thinking

Return ONLY the question, no explanation."""

    try:
        question = llm.predict(prompt)
        return question.strip()
    except Exception as e:
        return f"What do you think is the main purpose of {concept}?"


@tool
def assess_student_understanding(student_response: str, expected_concept: str) -> dict:
    """
    Assesses student's response to determine understanding level.
    
    Args:
        student_response: What the student said
        expected_concept: The concept being taught
        
    Returns:
        Dictionary with assessment results
    """
    llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0.3)
    
    prompt = f"""Analyze this student's response about {expected_concept}.

Student said: "{student_response}"

Respond in this EXACT JSON format:
{{
    "understanding_level": "poor/partial/good/excellent",
    "correct_points": ["point1", "point2"],
    "misconceptions": ["misconception1"],
    "next_action": "hint/rephrase_question/advance/show_code",
    "reasoning": "brief explanation"
}}"""

    try:
        response = llm.predict(prompt)
        assessment = json.loads(response)
        return assessment
    except:
        return {
            "understanding_level": "partial",
            "correct_points": ["Attempting to engage"],
            "misconceptions": [],
            "next_action": "rephrase_question",
            "reasoning": "Continue dialogue"
        }


@tool
def provide_progressive_hint(concept: str, student_struggle_count: int) -> str:
    """
    Provides hints that get progressively more explicit.
    
    Args:
        concept: The concept the student is struggling with
        student_struggle_count: How many times they've struggled (1-3+)
        
    Returns:
        A hint string
    """
    llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0.6)
    
    hint_styles = {
        1: "very subtle - just nudge their thinking",
        2: "moderate - point toward the right direction",
        3: "explicit - nearly give the answer but make them take final step"
    }
    
    hint_level = min(student_struggle_count, 3)
    
    prompt = f"""Provide a hint about {concept}.

Hint level: {hint_level}/3 ({hint_styles[hint_level]})

Return ONLY the hint, no extra text."""

    try:
        hint = llm.predict(prompt)
        return hint.strip()
    except:
        return f"Think about what problem {concept} is trying to solve."


@tool
def track_learning_progress(session_id: str, concept: str, mastery_level: str) -> dict:
    """
    Tracks what concepts the student has learned.
    
    Args:
        session_id: Unique session identifier
        concept: The concept learned
        mastery_level: Level of mastery (poor/partial/good/excellent)
        
    Returns:
        Progress summary
    """
    progress_dir = "data/progress"
    os.makedirs(progress_dir, exist_ok=True)
    
    progress_file = os.path.join(progress_dir, f"progress_{session_id}.json")
    
    try:
        with open(progress_file, 'r') as f:
            progress = json.load(f)
    except:
        progress = {
            "session_id": session_id,
            "start_time": datetime.now().isoformat(),
            "concepts_covered": []
        }
    
    progress["concepts_covered"].append({
        "concept": concept,
        "mastery": mastery_level,
        "timestamp": datetime.now().isoformat()
    })
    
    progress["last_updated"] = datetime.now().isoformat()
    
    with open(progress_file, 'w') as f:
        json.dump(progress, f, indent=2)
    
    return {
        "success": True,
        "total_concepts": len(progress["concepts_covered"]),
        "latest_concept": concept,
        "mastery": mastery_level
    }
