# ScholarGraph-RAG
**ScholarGraph** is a high-precision RAG (Retrieval-Augmented Generation) system designed for rigorous academic literature analysis.
Unlike standard "chat-with-PDF" tools, ScholarGraph focuses on document structure and cross-paper synthesis to help researchers identify unaddressed research gaps.

## ⭐️ Key Featrues
- **Structure-Aware Q&A**

    : Recognizes functional sections (Abstract, Methodology, Results) for contextually accurate retrieval.

- **Discussion ToC Generator**

    : Automatically crafts structured table of contents for research discussions.

- **The Gap Finder**

    : A reasoning engine that cross-references "Limitations" and "Future Work" across multiple papers to highlight research "silences".

- **pgvector Hybrid Search**

    : Combines semantic vector embeddings with PostgreSQL Full-Text Search for technical precision.

## 🛠️ Tech Stack
- **Language**

    : Python

- **Database**

    : PostgreSQL with pgvector

- **Environment**

    : Nuvolos (Cloud Research Workspace)

- **Parsing**

    : Docling / Grobid

- **LLM**

    :

    : Orchestrated without framework like LangChain

## 🧠 My Role: Intelligence & Logic Lead
As the **Intelligence & Logic Lead**, I am responsible for the "Brain" of the system-designing the reasoning workflows and the orchestration layer that transforms raw data into academic insights.

### Core Contributions
#### 1. Query Expansion Logic
- 
- **Impact**

#### 2. Gap Synthesis Workflow
-
- **Impact**

#### 3. Table of Contents (ToC) Generation Engine
-
- **Impact**

#### 4. Python Orchestration Layer
-
- **Impact**

## 🤖 Model Selection & Troubleshooting

### Why Gemini Flash Latest?
After evaluating several LLMs, I selected **'gemini-flash-latest'** as the primary engine for ScholarGraph for the following reasons:

- **Large Context Window**

    : Essential for processing dense academic papers and cross-referencing multiple "Limitations" sections.

- **Inference Speed**

    : Provides the near-instant response times required for interactive query expansion and ToC generation.

- **Quota Efficiency**

    : Offers the most stable rate limits within the free-tier, ensuring the RAP pipeline remains functional during heavy testing.

### Troubleshooting Model Availability
During the integration phase, I encountered persistent '404 Not Found' and '429 Resource Exhausted' errors with specific model versions (e.g., 1-5flash, 2.0-flash).

To resolve this, I developed a diagnostic script, 'check_models.py', to programmatically list all models available to my specific API key. This allowed me to identify the exact model identifiers supported by the latest **google-genai** SDK, leading to the successful integration of the 'gemini-flash-latest' alias.

## 🧩 Data Orchestration & Parsing
### From Text to Structured Data
To bridge the gap between the LLM's natural language output and the database's technical requirements, I implemented a robust **Data Parsing Layer**. This ensures that the intelligence logic provides structured inputs to the retrieval engine.

### High-Fidelity Gap Synthesis
- Structured Metadata Synthesis

    : Processes dictionary-based objects (title, year, limitations, future_work) for chronically aware analysis.

- Synergy Discovery

    : Proposes novel research directions by combining fragmented "Future Work" ideas from different sources.

### Key Technical Implementation
- **Output Sanitization**

    : Developed a cleaning logic to strip **Markdown Tags** (e.g., '```json") from the raw LLM responses, preventing parsing errors.

- **JSON Deserialization**

    : Leveraged Python's 'json' module to transform raw strings into functional **Python List** objects using 'json.loads()'.

- **Validation & Fallback**

    : Integrated error handling (try-except) to validate the data structure. If parsing fails, the system safely falls back to the original query to ensure continuous operation.

- **Strict Prompting**

    : Refined prompt templates to enforce **JSON-only** response, significantly improving the consistency of the data pipeline.

### Troubleshooting Conversational Noise in LLM Outputs
- **Challenge**

    : LLMs often include conversational prefixes or suffixes in their responses, which breaks standard 'json.loads()'.

- **Resolution**

    : Implemented **Regex-based extraction** using the pattern 're.search(r'\[.*\]', raw_result, re.DOTALL)' to surgically isolate the JSON array from raw strings.

## ⛓️ Full Orchestration Pipeline
### The Full Orchestration Pipeline
I designed and implemented a unified controller, 'run_full_pipeline', to automate the end-to-end reasoning flow from user input to final analysis:

1. **Query Expansion**

    : Transforms vague user queries into 3 precise technical search terms to maximize retrieval hit rates.

2. **Retrieval Interface**

    : Serves as a bridge for **Vector DB integration (Role B)**, passing expanded queries and receiving structured paper segments.

3. **Advanced Synthesis**

    : Orchestrates corss-paper reasoning to identify **Technical Contradictions** and **Research Silences** (unaddressed gaps) across multiple sources.

## 🛡️ Reliability & Hallucination Mitigation
To ensure academic rigor, the system employs a dual-layer defense:
- Strict Grounding & Citations

    : Prompts mandate that every claim must be backed by a specific source (e.g., [Title (Year)]). AI is instructed to output "information not available" rather than fabricating answers.

- Self-Correction Auditor

    : A secondary LLM pass acts as a "Fact-Checking Auditor", reviewing the initial report against the source context to remove unsupported claims.