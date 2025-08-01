def plan_changes(summary: str, prompt: str, llm) -> str:
    """
    Generate a plan for code changes based on project summary and user prompt.
    
    Args:
        summary: Project summary from analyze_repo
        prompt: User's request for changes
        llm: LLM function to call for generating the plan
        
    Returns:
        Detailed plan of changes to make
    """
    plan_prompt = f"""Project Summary:
{summary}

User Request: {prompt}

Please create a detailed plan for implementing the requested changes. For each file that needs to be modified, specify:
1. The file path (e.g., app/main.py)
2. What specific changes need to be made
3. Why these changes are necessary

Format your response as:
- filename.py: Description of changes needed
  - Specific modification 1
  - Specific modification 2

Example:
- app/main.py: Add new endpoint for user authentication
  - Import authentication modules
  - Add POST /auth/login route
  - Add authentication middleware
"""
    
    return llm(plan_prompt)