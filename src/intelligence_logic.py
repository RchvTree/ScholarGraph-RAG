# === Discussion ===
# Which LLM?
# Lukas's function -> 'limitations', 'future work' section
# Need to work on 'future work' logic -> (consistencies, contradiction...)
# Normal queries too

import json
import os
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()

# -----------------------------------------
# Prompt Templats
# -----------------------------------------

# Template for expanding user queries into technical search terms
EXPANSION_PROMPT_TEMPLATE = """
You are an Academic Research Assistant. Your goal is to improve retrieval precision.
Original Query: {user_query}

Tasks:
1. Identify the core technical concepts.
2. Generate 3 expanded search queries using professional academic terminology.
3. Focus on methodology, results, and constraints.

IMPORTANT: Output ONLY a valid JSON list of strings.
Example: ["query 1", "query 2", "query 3"]
"""

# Template for synthesizing research gaps from multiple paper sections
GAP_SYNTHESIS_PROMPT_TEMPLATE = """
You are a Research Analyst. Below are "Limitations" and "Future Work" sections from multiple papers.
Context: {context_data}

Tasks:
1. Compare the findings and identify common unaddressed variables.
2. Highlight any contradictions between the papers.
3. Propose a "Research Silence" (a gap) that current literature hasn't covered.

Output format: Structured bullet points.
"""



# -----------------------------------------
# Orchestration Logic
# -----------------------------------------

class ScholarGraphLogic:
    def __init__(self):
        """
        Initialize the Logic Engine and configure the Gemini SDK.
        """
        # Retrieve the API Key from the environment variable
        api_key = os.getenv("GOOGLE_API_KEY")
        
        if not api_key:
            print("[Error] GOOGLE_API_KEY not found. Please check your .env file.")
            return
        
        # Initialize the client
        self.client = genai.Client(api_key=api_key)
        # We use 'gemini-flash-latest' for its high speed and large context window
        self.model_id = "models/gemini-flash-latest"

        print(f"[System] ScholarGraph Logic Engine Initialized with {self.model_id}.")

    def call_llm(self, final_prompt):
        """
        Sends the engineered prompt to the Gemini API and returns the generated text.
        """
        print(f"[System] Calling Gemini API ({self.model_id})...")
        try:
            # Actual API call to Gemini
            response = self.client.models.generate_content(
                model = self.model_id,
                contents = final_prompt
            )
            return response.text
        except Exception as e:
            return f"API Call Failed for {self.model_id}: {str(e)}"

    def expand_query_workflow(self, user_query):
        """
        Step 1: Transform a simple user query into multiple technical variations.
                This improves the retrieval hit rate in the vector database.
              : Transform raw text into a machine-readable Python List.
        """
        print(f"\n[Step 1] Executing Query Expansion & Parsing for: '{user_query}'")

        # Create the specific prompt for expansion
        prompt = EXPANSION_PROMPT_TEMPLATE.format(user_query=user_query)

        # Call the LLM to get the technical variations
        raw_result = self.call_llm(prompt)

        # Sanitization & Parsing
        try:
            # 1. Sanitization: Remove potential markdown backticks
            clean_json = raw_result.replace("```json", "").replace("```", "").strip()

            # 2. Parsing: Convert String to real Python List
            query_list = json.loads(clean_json)

            if isinstance(query_list, list):
                print(f" -> Successfully parsed {len(query_list)} queries.")
                return query_list # Return <class 'list'>
            else:
                raise ValueError("Output is not a list format.")
            
        except Exception as e:
            print(f"[Warning] Parsing failed: {e}")
            # Fallback: Return original query in a list to prevent system crash
            return [user_query]


    
    def gap_synthesis_workflow(self, paper_ids):
        """
        Step 2: Orchestrate cross-paper analysis by synthesizing limitations.
        It aggregates data from Lukas and processes it through the reasoning engine.
        """
        print(f"\n[Step 2] Fetching data for Paper IDs: {paper_ids}")

        # Interface: Fetching mock data representing Lukas's retrieval result
        # In the future, this will call Lukas's search function
        mock_data = [
            "Paper A: Small sample size and lack of diverse demographics.",
            "Paper B: High computational cost and latency in real-time processing."
        ]

        # Refinement: Aggregate text chunks into a single string for the LLM
        raw_context = "\n".join(mock_data)

        # Injection: Combine the raw context with the Gap Synthesis prompt
        final_prompt = GAP_SYNTHESIS_PROMPT_TEMPLATE.format(context_data = raw_context)

        # Execution: Get the final analytical response from the AI
        final_answer = self.call_llm(final_prompt)

        return final_answer



# -----------------------------------------
# Execution Example
# -----------------------------------------
if __name__ == "__main__":
    engine = ScholarGraphLogic()

    # Show Query Expansion
    engine.expand_query_workflow("RAG system efficiency")

    # Show Gap Synthesis
    result = engine.gap_synthesis_workflow(["Arxiv_2301", "Arxiv_2405"])
    print(f"\n[Final Output]\n{result}")