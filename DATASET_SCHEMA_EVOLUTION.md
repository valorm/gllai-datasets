# GLLAI Dataset Schema Evolution & Migration Guide

## Executive Summary
This document tracks the schema evolution of the GLLAI datasets from **v1/v2 (Probabilistic/Scraped)** to **v3 (Authoritative/Government-Backed)**.

**Critical Warning:** The GLLAI Runtime (RAG) was originally built for v1/v2 schemas. Consumers must use the files in `v3_rag_ready/` directories. The raw `v3/` files are strictly for linguistic auditing and do not contain RAG-required fields like `chunk_id`.

---

## 1. Schema Comparison

### Knowledge Chunks (`knowledge_chunks.jsonl`)

| Field | v1 / v2 (Legacy RAG) | v3 (Authority Layer) | v3_rag_ready (Runtime) |
| :--- | :--- | :--- | :--- |
| **Identity** | `chunk_id` (UUID) | *None* | Generated Deterministic ID |
| **Content** | `text` (Long prose) | `definition` (Concise) | Mapped from `definition` |
| **Trust** | `confidence` (Float) | *None* | Hardcoded `1.0` (Authority) |

### Training Pairs (`training_pairs.jsonl`)

| Field | v1 / v2 (Instruction Tuning) | v3 (Translation Authority) | v3_rag_ready (Runtime) |
| :--- | :--- | :--- | :--- |
| **Structure**| `instruction/input/output` | `english/local` | Synthesized Instruction |

## 2. Integration
Point your RAG indexers to:
- `gllai-datasets/{lang}/v3_rag_ready/knowledge_chunks.jsonl`
- `gllai-datasets/{lang}/v3_rag_ready/training_pairs.jsonl`
