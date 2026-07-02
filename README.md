# EviRank-X
## Intelligent Candidate Discovery System for AI-Powered Talent Ranking

## Overview

EviRank-X is an explainable AI-powered candidate discovery and ranking system designed to identify the most relevant candidates for a given job description. Rather than relying on simple keyword matching, the system combines semantic understanding, hybrid retrieval, evidence-based reasoning, and behavioral intelligence to produce a transparent and defensible ranked shortlist.

The platform is built as an end-to-end offline pipeline capable of processing large candidate datasets, generating recruiter-ready explanations, and exporting validator-compliant submission files.

The system is designed for CPU-only execution and produces deterministic, reproducible rankings.

---

# Problem Statement

Recruiters often review thousands of candidate profiles where traditional keyword-based search fails to capture semantic relevance, transferable experience, or behavioral quality.

The objective of EviRank-X is to:

- Understand complex hiring requirements
- Retrieve the most relevant candidates efficiently
- Fuse multiple evidence sources into a unified ranking
- Explain every recommendation with traceable evidence
- Produce submission-ready ranked outputs for evaluation

---

# Key Features

### Semantic Job Understanding

- Structured job intent extraction
- Required and preferred skill identification
- Experience and constraint extraction
- Hiring signal interpretation

---

### Hybrid Candidate Retrieval

Combines multiple retrieval strategies to maximize recall.

- BM25 lexical retrieval
- Dense semantic retrieval
- FAISS vector search
- Automatic fallback to Scikit-Learn Nearest Neighbors
- Hybrid score fusion

---

### Evidence-Based Ranking

Candidate ranking is based on multiple evidence sources rather than embeddings alone.

Evidence includes:

- Semantic similarity
- Skill overlap
- Career relevance
- Technical experience
- Profile summary
- Career history
- Certifications
- Education
- Industry alignment
- Behavioral signals (when applicable)

Each evidence source contributes independently to the final recommendation.

---

### Behavioral Intelligence

When behavioral signals materially contribute to ranking, they are incorporated into both the ranking model and explanations.

Examples include:

- Recruiter responsiveness
- Assessment performance
- Profile completeness
- Interview completion
- Open-to-work status
- Notice period
- Platform activity
- Verification status

Behavioral evidence is never referenced unless it contributes to the final score.

---

### Explainable Recommendations

Each recommendation is generated from structured evidence rather than predefined templates or generative text.

The reasoning engine:

- References only verified candidate evidence
- Never hallucinates skills or experience
- Produces deterministic explanations
- Supports sentence-level evidence attribution
- Generates recruiter-friendly summaries

---

### Submission Automation

The export pipeline automatically produces:

- Official submission CSV
- Official submission XLSX
- Recruiter workbook with expanded evidence
- Validation reports
- Performance reports
- Dataset audit

The official submission schema is derived dynamically from the organizer's sample submission template.

---

# System Architecture

```
Job Description
        │
        ▼
Intent Extraction
        │
        ▼
Hybrid Retrieval
(BM25 + Dense Retrieval)
        │
        ▼
Top Candidate Retrieval
        │
        ▼
Evidence Builder
        │
        ▼
Evidence Fusion
        │
        ▼
Ranking Engine
        │
        ▼
Evidence-Based Reasoning
        │
        ▼
Submission Generation
```

---

# Ranking Methodology

Candidate ranking combines multiple complementary evidence sources.

Examples include:

- Semantic relevance
- Lexical relevance
- Skill alignment
- Technical expertise
- Career progression
- Certifications
- Education
- Domain relevance
- Behavioral signals
- Hiring constraints

The ranking engine is configurable through external configuration files rather than hardcoded weights.

---

# Explainability Pipeline

Every recommendation is generated using structured evidence.

The reasoning engine follows this hierarchy:

1. Current role
2. Relevant experience
3. Matched technical skills
4. Career highlights
5. Certifications
6. Education
7. Industry relevance
8. Behavioral signals (only when used)
9. Missing or weaker evidence (when applicable)

Every statement is traceable to the candidate profile and evidence vector.

---

# Robustness

The system is designed with graceful degradation.

| Preferred | Fallback |
|-----------|----------|
| FAISS | Scikit-Learn Nearest Neighbors |
| BGE Embeddings | Existing embedding implementation |
| Cross Encoder | Skip reranking |
| SHAP | Feature importance fallback |

The ranking pipeline continues operating even when optional components are unavailable.

---

# Project Structure

```
backend/

app/
├── api/
├── ml/
│   ├── embeddings/
│   ├── retrieval/
│   ├── evidence/
│   ├── reasoning/
│   ├── ranking/
│   ├── export/
│   └── pipeline/

config/

results/

tests/

run_pipeline.py
```

---

# Results Directory

Pipeline execution generates:

```
results/

submission.csv
submission.xlsx
ranked_candidates.xlsx

backend_audit.md
methodology.md
prototype_summary.md

dataset_report.json
retrieval_report.json
behavior_report.json
ranking.json
ranking_report.json
reasoning_report.json
performance_report.json
submission_validation.json
export_report.json

logs/
```

---

# Running the Project

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Execute the Complete Pipeline

```bash
python run_pipeline.py
```

The pipeline automatically:

- Loads the candidate dataset
- Parses the job description
- Reuses cached embeddings
- Loads retrieval indices
- Performs hybrid retrieval
- Builds evidence vectors
- Generates ranked candidates
- Produces evidence-based reasoning
- Exports submission files
- Validates the submission
- Generates reports

---

## Execute Tests

```bash
pytest
```

---

# Reproducibility

The pipeline is deterministic.

It uses:

- Fixed random seeds
- Cached embeddings
- Stable ranking
- Deterministic template selection
- Configurable parameters
- Validator-backed export

Running the same pipeline on the same inputs produces identical outputs.

---

# Design Principles

The project was designed around five core principles.

### Explainability

Every recommendation must be supported by verifiable evidence.

### Robustness

Graceful fallbacks prevent optional dependencies from breaking the pipeline.

### Reproducibility

Results remain deterministic across executions.

### Efficiency

The pipeline is optimized for CPU-only execution.

### Practicality

Engineering decisions prioritize ranking quality, transparency, and recruiter usability.

---

# Limitations

Current prototype limitations include:

- Ranking quality depends on available structured candidate information.
- Optional reranking requires locally available models.
- Behavioral evidence is used only when available and configured.
- The system does not fabricate missing candidate information.

---

# Future Improvements

Potential future enhancements include:

- Learning-to-Rank with supervised relevance labels
- Cross-encoder reranking for larger candidate pools
- Adaptive evidence weighting
- Personalized recruiter preferences
- Active feedback learning
- Interactive ranking refinement
- Real-time embedding updates

---

# Technology Stack

### Backend

- Python
- Flask

### Machine Learning

- Sentence Transformers
- FAISS
- Scikit-Learn
- BM25
- LightGBM (optional)

### Data Processing

- Pandas
- NumPy

### Explainability

- SHAP (optional)
- Evidence Attribution Engine

### Export

- OpenPyXL
- CSV
- JSON

---

# Conclusion

EviRank-X demonstrates an evidence-driven approach to intelligent candidate discovery by combining semantic retrieval, structured evidence fusion, behavioral intelligence, and explainable ranking.

The system emphasizes transparency, reproducibility, and practical recruiter usability while remaining fully offline, CPU-efficient, and compliant with the competition submission requirements.
