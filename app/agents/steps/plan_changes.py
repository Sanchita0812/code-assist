def plan_changes(summary: str, prompt: str, llm) -> str:
    plan_prompt = f"""Project Summary:\n{summary}

User Prompt: {prompt}

List the changes you'd make, including which files to edit, what functions to add or modify, and why."""
    return llm(plan_prompt)

#Input: project summary, user prompt
#Action: LLM generates a plan of changes
#Output: Step-by-step change plan
