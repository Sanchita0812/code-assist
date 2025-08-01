import os
import google.generativeai as genai

# --- Configuration ---
# It's best practice to handle configuration at the start of the script.
try:
    # Load the Gemini API key from an environment variable for security.
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not found.")
    genai.configure(api_key=api_key)

except ValueError as e:
    # If the key isn't set, print a clear error and exit.
    print(f"Configuration Error: {e}")
    exit(1) # Exit the script with a non-zero status code to indicate an error.

# --- Model Definition ---
# Initialize the generative model to be used.
model = genai.GenerativeModel("gemini-pro")

def summarize_code(code: str) -> str:
    """
    Summarizes a given Python code string using the Gemini API.

    This function sends code to the Gemini model, truncates long code blocks
    to stay within API limits, and returns a high-level summary.

    Args:
        code: A string containing the Python code to be summarized.

    Returns:
        A string with the summary, or an error message if summarization fails.
    """
    # Gracefully handle empty or whitespace-only input.
    if not code.strip():
        return "No code provided for summarization."

    # Truncate very long code to avoid exceeding API limits.
    max_length = 4000
    if len(code) > max_length:
        code = code[:max_length] + "\n\n# ... (Code truncated for summary)"

    # This prompt provides clear context and instructions for the model.
    prompt = f"""
    As an expert software engineer, please provide a concise summary of the following Python code.
    Focus on its main purpose, key components, and overall structure in a few bullet points.

    ```python
    {code}
    ```
    """

    try:
        # Generate content using the defined model and prompt.
        response = model.generate_content(prompt)
        # The .text attribute is a convenient shortcut to access the model's text output.
        return response.text.strip()
    except Exception as e:
        # Catch potential API errors (e.g., network issues, authentication problems).
        print(f"[Gemini API Error]: {e}")
        return "Error: The summary could not be generated due to an API issue."

def call_llm(prompt: str) -> str:
    """
    Generic LLM wrapper function that uses Gemini to process prompts.
    
    Args:
        prompt: The prompt to send to the LLM
        
    Returns:
        The LLM's response as a string
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"[Gemini API Error]: {e}")
        return "Error: Could not generate response due to an API issue."

# Alias for backward compatibility
gemini_llm = call_llm

# --- Script Execution ---
# The `if __name__ == "__main__":` block ensures this code only runs
# when the script is executed directly, not when imported as a module.
if __name__ == "__main__":
    # An example code snippet to demonstrate the function.
    example_code_to_summarize = """
import random

class DataProcessor:
    def __init__(self, data_source):
        self.data_source = data_source
        self.data = []
        print(f"Processor initialized for source: {self.data_source}")

    def load_data(self):
        '''Simulates loading data from a source.'''
        self.data = [random.randint(1, 100) for _ in range(20)]
        print("Data loaded successfully.")

    def process(self):
        '''Calculates the mean and standard deviation of the loaded data.'''
        if not self.data:
            print("No data to process. Please load data first.")
            return None
        
        mean = sum(self.data) / len(self.data)
        variance = sum([(x - mean) ** 2 for x in self.data]) / len(self.data)
        std_dev = variance ** 0.5
        
        print(f"Processing complete. Mean: {mean:.2f}, Std Dev: {std_dev:.2f}")
        return {"mean": mean, "std_dev": std_dev}

# Usage
processor = DataProcessor("virtual_api_endpoint")
processor.load_data()
results = processor.process()
"""
    print("--- 👨‍💻 Attempting to summarize the example code... ---\n")
    
    # Call the main function with the example code.
    summary = summarize_code(example_code_to_summarize)
    
    # Print the final result.
    print("--- ✨ Gemini's Summary ---")
    print(summary)
    print("-------------------------")