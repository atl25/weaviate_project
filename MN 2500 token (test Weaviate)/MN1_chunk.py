import csv
import os

# ====== CONFIGURATION ======
INPUT_FILE = "MN1_chunk.txt"   # replace with your file name
MAIN_CHUNK_TOKEN_LIMIT = 8000
SUB_CHUNK_TOKEN_LIMIT = 200
OUTPUT_FILE = "output_chunks.csv"

# ====== FUNCTION TO SPLIT INTO SENTENCES ======
def split_into_sentences(text):
    sentences = text.replace('\n', ' ').split('.')
    clean_sentences = [s.strip() + '.' for s in sentences if s.strip()]
    return clean_sentences

# ====== FUNCTION TO COUNT TOKENS (WORDS) ======
def count_tokens(text):
    return len(text.split())

# ====== MAIN PROCESS ======
def process_file():
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        full_text = f.read()

    sentences = split_into_sentences(full_text)

    main_chunks = []
    current_chunk = ""
    current_tokens = 0

    # Step 1: Make main chunks of ~8000 tokens
    for sentence in sentences:
        sentence_tokens = count_tokens(sentence)
        if current_tokens + sentence_tokens > MAIN_CHUNK_TOKEN_LIMIT:
            main_chunks.append(current_chunk.strip())
            current_chunk = sentence
            current_tokens = sentence_tokens
        else:
            current_chunk += " " + sentence
            current_tokens += sentence_tokens
    if current_chunk:
        main_chunks.append(current_chunk.strip())

    # Step 2: For each main chunk, make subchunks ~200 tokens
    rows = []
    for main_index, main_chunk in enumerate(main_chunks, start=1):
        main_chunk_id = f"chunk{main_index:03d}"
        sub_sentences = split_into_sentences(main_chunk)

        sub_chunk = ""
        sub_tokens = 0
        sub_index = 1

        for sentence in sub_sentences:
            sentence_tokens = count_tokens(sentence)
            if sub_tokens + sentence_tokens > SUB_CHUNK_TOKEN_LIMIT:
                sub_chunk_id = f"{main_chunk_id}_{sub_index}"
                rows.append([main_chunk_id, sub_chunk_id, sub_chunk.strip()])
                sub_chunk = sentence
                sub_tokens = sentence_tokens
                sub_index += 1
            else:
                sub_chunk += " " + sentence
                sub_tokens += sentence_tokens
        if sub_chunk:
            sub_chunk_id = f"{main_chunk_id}_{sub_index}"
            rows.append([main_chunk_id, sub_chunk_id, sub_chunk.strip()])

    # Step 3: Write to CSV
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['main_chunk_id', 'sub_chunk_id', 'text'])
        writer.writerows(rows)

    print(f"✅ Done! Total main chunks: {len(main_chunks)}, CSV saved to: {OUTPUT_FILE}")

# ====== RUN ======
if __name__ == "__main__":
    process_file()
