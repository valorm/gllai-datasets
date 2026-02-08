GLLAI Datasets is a collection of frozen, versioned, curriculum-grounded linguistic datasets for Ghanaian local languages.

The repository currently includes Asante/Akuapem Twi, Eʋegbe (Ewe), and Ga, each maintained in strict language isolation and versioned independently.

The datasets are designed for:

Retrieval-Augmented Generation (RAG)

Instruction tuning

Linguistic research and language preservation

All data is:

PDF-grounded (no web or inferred knowledge)

Append-only and regression-safe

Built with refusal-first behavior (UNKNOWN responses expected)

Free of cross-language or cross-dialect contamination

This repository contains data only.
Runtime logic, models, and applications live in separate repositories.

## RAG runtime wiring (critical)

RAG retrievers **must** load only `knowledge_chunks.jsonl` for a given language and version. Do not point the runtime at a directory or at `training_pairs.jsonl`, and do not hardcode a version that doesn't match the query. Use the `text` field on each chunk (not `content`). Example path:

```
gllai-datasets/<language>/<version>/knowledge_chunks.jsonl
```

Quick verification logs:

```
console.log("DATA FILE:", datasetPath);
console.log("RAW CHUNKS:", chunks.length);
console.log("SAMPLE CHUNK:", chunks[0]);
```

Expected signal:

- `RAW CHUNKS` is non-zero.
- `SAMPLE CHUNK` includes `chunk_id`, `language`, `topic`, `text`, and `confidence`.
