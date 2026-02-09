import json
import os
import sys

def validate_rag_file(filepath, file_type):
    print(f"Validating {filepath}...")
    if not os.path.exists(filepath):
        print(f"[FAIL] File not found: {filepath}")
        return False
    
    errors = 0
    with open(filepath, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            try:
                data = json.loads(line)
                
                if file_type == "knowledge":
                    # Check for legacy RAG fields
                    required = ["chunk_id", "text", "confidence", "topic"]
                    for field in required:
                        if field not in data:
                            print(f"  Line {i+1}: Missing '{field}'")
                            errors += 1
                    if data.get("confidence") != 1.0:
                         print(f"  Line {i+1}: Confidence is {data.get('confidence')}, expected 1.0 for Authority layer")
                         errors += 1

                elif file_type == "pairs":
                    # Check for instruction tuning fields
                    required = ["instruction", "input", "output"]
                    for field in required:
                        if field not in data:
                            print(f"  Line {i+1}: Missing '{field}'")
                            errors += 1
            except:
                print(f"  Line {i+1}: Invalid JSON")
                errors += 1
                
    if errors == 0:
        print(f"[PASS] {filepath} is RAG-ready.")
        return True
    else:
        print(f"[FAIL] {filepath} has {errors} errors.")
        return False

if __name__ == "__main__":
    # Validate all generated files
    languages = ['twi', 'ewe', 'ga']
    for lang in languages:
        validate_rag_file(f"{lang}/v3_rag_ready/knowledge_chunks.jsonl", "knowledge")
        validate_rag_file(f"{lang}/v3_rag_ready/training_pairs.jsonl", "pairs")
