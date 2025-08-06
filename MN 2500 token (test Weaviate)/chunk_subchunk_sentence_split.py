import pandas as pd
from sentence_transformers import SentenceTransformer

# Input CSV file name
input_file = "MN5_chunk.csv"

# Read the CSV
df = pd.read_csv(input_file)
chunks = df["pali_text"].dropna().tolist()
chunk_ids = df["chunk_id"].dropna().tolist()

# Load LaBSE model
model = SentenceTransformer("sentence-transformers/LaBSE")

# Token counter using LaBSE
def count_tokens(text):
    return len(model.tokenize([text])[0])

# Final list of dictionaries
final_rows = []

for i, chunk in enumerate(chunks):
    main_chunk_id = chunk_ids[i]
    
    # 👇 Use dot to split sentence
    sentences = [s.strip() + "." for s in chunk.split(".") if s.strip()]
    
    sub_chunk = ""
    sub_chunk_tokens = 0
    sub_chunk_index = 1

    for sentence in sentences:
        token_count = count_tokens(sentence)
        if sub_chunk_tokens + token_count <= 200:
            sub_chunk += sentence + " "
            sub_chunk_tokens += token_count
        else:
            for sent in sub_chunk.strip().split("."):
                sent = sent.strip()
                if sent:
                    final_rows.append({
                        "main_chunk_id": main_chunk_id,
                        "sub_chunk_id": f"{main_chunk_id}_{sub_chunk_index}",
                        "sentence": sent + "."
                    })
            sub_chunk_index += 1
            sub_chunk = sentence + " "
            sub_chunk_tokens = token_count

    if sub_chunk.strip():
        for sent in sub_chunk.strip().split("."):
            sent = sent.strip()
            if sent:
                final_rows.append({
                    "main_chunk_id": main_chunk_id,
                    "sub_chunk_id": f"{main_chunk_id}_{sub_chunk_index}",
                    "sentence": sent + "."
                })

# Save output
output_file = "MN5_chunk_subchunk_sentences.csv"
pd.DataFrame(final_rows).to_csv(output_file, index=False)
print(f"✅ Done! Output saved to {output_file}")
