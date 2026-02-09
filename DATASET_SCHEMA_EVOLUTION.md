# GLLAI Dataset Schema Evolution & Migration Guide

## Executive Summary
This document tracks the shift from probabilistic data (v1/v2) to authoritative data (v3).

**Critical Rule:**
- `v3/` = Raw Authority (Linguistic Audit Source).
- `v3_rag_ready/` = Runtime Artifacts (System Compatible). 

Use `v3_rag_ready` for your RAG system to prevent field-missing errors (chunk_id, confidence).

## 1. Mappings
- **v3 (Raw):** term, definition, type, dialect, source
- **v3_rag_ready:** chunk_id, text, confidence (1.0), topic, source
