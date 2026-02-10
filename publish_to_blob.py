from vercel_blob import put
import os

# Set BLOB_READ_WRITE_TOKEN from Vercel dashboard
for lang in ["twi", "ewe", "ga"]:
    file_path = f"{lang}/v3_rag_ready/knowledge_chunks.jsonl"
    with open(file_path, 'rb') as f:
        # Upload with language-specific path
        blob_url = put(f"datasets/{lang}/knowledge_chunks.jsonl", f, {
            "access": "public",
            "addRandomSuffix": False  # Keep stable URL for versioning
        })
        print(f"Uploaded {lang}: {blob_url}")
