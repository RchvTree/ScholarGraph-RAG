# === Discussion ===
# Which LLM?
# Lukas's function -> 'limitations', 'future work' section
# Need to work on 'future work' logic -> (consistencies, contradiction...)
# Normal queries too

import json
import os
from dotenv import load_dotenv
from google import genai
import re

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
You are a Senior Research Strategist specialized in identifying "Research Silences" in academic literatue.
Below are retrieved sections (Limitations/Future Work) from multiple research papers.

[Context Data]
{context_data}

[Your Analysis Tasks]
1. Consistency & Addressal: Analyze if Paper B addresses any specific limitations mentioned in Paper A.
2. Technical Contradictions: Highlight any conflicting claims regarding methodology, performance, or experimental results between the papers.
3. Synergy Discovery: Combine the "Future Work" suggestions from both papers to propose a multi-disciplinary research direction that neither paper suggested individually.
4. Research Silence (The Gap): Identify one specific technical or theoretical "Silence"-a gap that is conspicuously missing or ignored by ALL provided papers.

[Output Guidelines]
- Use professional academic English.
- Use structured bullet points with bold headers.
- Be specific and technical; avoid generic summaries.
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
            # -> [Fix] Use Regex to find the JSON list even if there is extra text
            match = re.search(r'\[.*\]', raw_result, re.DOTALL)
            if match:
                clean_json = match.group(0)
                # 2. Parsing: Convert String to real Python List
                query_list = json.loads(clean_json)
                print(f" -> Successfully parsed {len(query_list)} queries.")
                return query_list # Return <class 'list'>

            else:
                raise ValueError("No JSON list found in response.")
            
        except Exception as e:
            print(f"[Warning] Parsing failed: {e}")
            # Fallback: Return original query in a list to prevent system crash
            return [user_query]


    
    def gap_synthesis_workflow(self, context_data_list):
        """
        Step 3: Orchestrate cross-paper analysis by synthesizing research gaps.

        Why 'context_data_list' instead of 'paper_ids'?
        The identifiers (Who to find) are handled by the Retrieval layer (Lukas),
        while this Reasoning layer focuses purely on the actual content (What to analyze).

        It aggregates data from Lukas and processes it through the reasoning engine.
        """

        # Updated to Step 3 and changed to reflect the actual data being processed
        print(f"\n[Step 3] Synthesizing Research Gaps from {len(context_data_list)} retrieved sections...")

        # Aggregate text chunks for the LLM
        raw_context = "\n".join(context_data_list)

        # Combine the raw context with the Gap Synthesis prompt
        final_prompt = GAP_SYNTHESIS_PROMPT_TEMPLATE.format(context_data = raw_context)

        # Execution: Get the final analytical response from the AI
        final_answer = self.call_llm(final_prompt)

        return final_answer
    


    def run_full_pipeline(self, user_query):
        """
        The Main Orchestrator: Connects Expansion, Retrieval, and Synthesis.
        """

        print(f"\n=== Starting Full ScholarGraph Pipeline ===")

        # 1. Expansion Phase
        expanded_queries = self.expand_query_workflow(user_query)

        # 2. Retrieval Phase (Interface for Lukas Integration)
        # In the future, this will call: retrieved_docs = Lukas.search(expanded_queries)
        print(f"\n[Step 2] Ready to pass {len(expanded_queries)} queries to Lukas's DB.")

        # Current Mock Data simulating Lukas's DB result
        mock_retrieved_data = [
            "Paper A: Scalability issues in vector search latency for 1M+ documents.",
            "Paper B: Latency is secondary to semantic drift in long-form embeddings."
        ]

        # 3. Synthesis Phase
        final_analysis = self.gap_synthesis_workflow(mock_retrieved_data)

        print(f"\n=== Pipeline Execution Completed ===")
        return final_analysis


# -----------------------------------------
# Execution Example
# -----------------------------------------
if __name__ == "__main__":
    engine = ScholarGraphLogic()

    # Run the entire pipeline with a single entry point
    final_report = engine.run_full_pipeline("RAG system efficiency")

    print(f"\n[Final Analytical Report]\n{final_report}")