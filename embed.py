import requests
import json
import math

def embed_text(text):
    resp = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": text},
    )
    return resp.json()["embedding"]



def normalize(vector):
    total = sum(x * x for x in vector)
    length = math.sqrt(total)
    result = [round(x / length, 6) for x in vector]
    return result

if __name__ == "__main__":
    for date in ("2017-01-01", "2021-04-21"):
        with open(f"data/sections-{date}.json", encoding="utf-8") as f:
            sections = json.load(f)

        vectors = []
        for i, s in enumerate(sections):
            text = f"search_document: {s['heading']} {s['body']}"
            vectors.append({
                "identifier":    s["identifier"],
                "revision_date": s["revision_date"],
                "vector":        normalize(embed_text(text)),
            })
            print(f"{i+1}/{len(sections)} {s['identifier']}")

        with open(f"data/vectors-{date}.json", "w", encoding="utf-8") as f:
            json.dump(vectors, f)

        print(f"{date}: {len(vectors)} vektorer")