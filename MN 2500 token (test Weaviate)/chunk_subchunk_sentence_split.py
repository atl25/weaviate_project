import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer

# Download sentence tokenizer
nltk.download("punkt")

# ✅ INPUT CSV
input_file = "MN5_chunk.csv"  # your CSV file with 'id' and 'text' columns
df = pd.read_csv(input_file)

chunks = df["pali_text"].dropna().tolist()
chunk_ids = df["chunk_id"].dropna().tolist()

# ✅ Load LaBSE model
model = SentenceTransformer("sentence-transformers/LaBSE")

# ✅ Count tokens using LaBSE tokenizer
def count_tokens(text):
    return len(model.tokenize([text])[0])

# ✅ Split logic
final_rows = []

for i, chunk in enumerate(chunks):
    main_chunk_id = chunk_ids[i]
    sentences = sent_tokenize(chunk)

    sub_chunk = ""
    sub_chunk_tokens = 0
    sub_chunk_index = 1

    for sentence in sentences:
        sentence = sentence.strip()
        token_count = count_tokens(sentence)
        if sub_chunk_tokens + token_count <= 200:
            sub_chunk += sentence + " "
            sub_chunk_tokens += token_count
        else:
            for sent in sent_tokenize(sub_chunk.strip()):
                final_rows.append({
                    "main_chunk_id": main_chunk_id,
                    "sub_chunk_id": f"{main_chunk_id}_{sub_chunk_index}",
                    "sentence": sent.strip()
                })
            sub_chunk_index += 1
            sub_chunk = sentence + " "
            sub_chunk_tokens = token_count

    if sub_chunk.strip():
        for sent in sent_tokenize(sub_chunk.strip()):
            final_rows.append({
                "main_chunk_id": main_chunk_id,
                "sub_chunk_id": f"{main_chunk_id}_{sub_chunk_index}",
                "sentence": sent.strip()
            })

# ✅ Save to output CSV
output_file = "MN5_chunk_subchunk_sentences.csv"
pd.DataFrame(final_rows).to_csv(output_file, index=False)
print(f"✅ Done! Output saved as: {output_file}")