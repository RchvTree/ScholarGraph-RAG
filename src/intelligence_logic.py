# === Discussion ===
# Which LLM?
# Lukas's function -> 'limitations', 'future work' section
# Need to work on 'future work' logic -> (consistencies, contradiction...)
# Normal queries too

import json
# import llm_model_api_connection_library

# -----------------------------------------
# Prompt Templats
# -----------------------------------------

# Query Expansion Prompt
EXPANSION_PROMPT_TEMPLATE = """
You are an Academic Research Assistant. Your goal is to improve retrieval precision.
Original Query: {user_query}

Tasks:
1. Identify the core technical concepts.
2. Generate 3 expanded search queries using professional academic terminology.
3. Focus on methodology, results, and constraints.

Ouput format: JSON list of strings.
"""

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
        # This is where you would configure your API key
        # self.client = ___(api_key="YOUR_KEY")
        print("[System] ScholarGraph Logic Engine Initialized.")

    def call_llm(self, mock_final_prompt):
        """
        This is where the LLM call happens.
        It takes the final engineered prompt and returns the AI's response.
        """
        print("[System] Calling LLM API...")
        # Mock API response
        return "AI Response: Based on the provided sections, the research gap is..."


    def expand_query_workflow(self, user_query):
        """Step 1: Transform user query for Role B's Search Engine"""
        print(f"\n[Step 1] Executing Query Expansion for: '{user_query}'")

        # In a real app, this calls the LLM with EXPANSION_PROMPT_TEMPLATE
        mock_expanded_queries = [
            f"Technical evaluation of {user_query} in distributed systems",
            f"Performance bottlenecks and scalability of {user_query}",
            f"Comparative analysis of {user_query} vs state-of-the-art"
        ]

        print(f" -> Generated Variations: {mock_expanded_queries}")
        return mock_expanded_queries
    
    def gap_synthesis_workflow(self, paper_ids):
        """Step 2: Orchestrate cross-paper analysis"""
        print(f"\n[Step 2] Fetching data for Paper IDs: {paper_ids}")

        # This is where I call Lukas's function
        mock_data = Lukas.search_by_metadata(paper_ids, section="Limitations") # Lukas.get_limitations(paper_ids) # ex. ["Paper A: small sample size", "Paper B: High computational cost"]
        # Aggregate text chuncks into a single context string
        mock_raw_context = "\n".join(mock_data)

        # Inject the aggregated context into the prompt template
        mock_final_prompt = GAP_SYNTHESIS_PROMPT_TEMPLATE.format(context_data=mock_raw_context)

        # Send the finalized prompt to the LLM and receive the final answer
        mock_final_answer = self.call_llm(mock_final_prompt)

        return mock_final_answer



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