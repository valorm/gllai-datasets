import json
import os

def validate(path, ftype):
    if not os.path.exists(path): return
    errs = 0
    with open(path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            try:
                data = json.loads(line)
                req = ["chunk_id", "text", "confidence"] if ftype=="kc" else ["instruction", "input", "output"]
                for r in req:
                    if r not in data: 
                        print(f"Error in {path} L{i+1}: Missing {r}")
                        errs += 1
            except Exception as e:
                print(f"JSON Error in {path} L{i+1}: {e}")
                errs += 1
    if errs == 0: print(f"[PASS] {path}")

if __name__ == "__main__":
    for l in ['twi', 'ewe', 'ga']:
        validate(f"{l}/v3_rag_ready/knowledge_chunks.jsonl", "kc")
        validate(f"{l}/v3_rag_ready/training_pairs.jsonl", "tp")
