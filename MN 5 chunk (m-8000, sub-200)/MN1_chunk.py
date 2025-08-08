import csv
import os
import re

# ====== CONFIGURATION ======
INPUT_FILE = "MN text.txt"   # Input text file name
MAIN_CHUNK_TOKEN_LIMIT = 8000
SUB_CHUNK_TOKEN_LIMIT = 200
OUTPUT_FILE = "output_chunks_main8k_sub200.csv"

# ====== FUNCTION TO SPLIT INTO SENTENCES ======
def split_into_sentences(text):
    text = text.replace('\n', ' ')
    sentences = []
    current = []
    paren_level = 0

    parts = re.split(r'(\.|\(|\))', text)

    i = 0
    while i < len(parts):
        part = parts[i]
        if part == '(':
            paren_level += 1
            if current:
                current[-1] += part
            else:
                current.append(part)
        elif part == ')':
            paren_level = max(paren_level - 1, 0)
            current.append(part)
        elif part == '.' and paren_level == 0:
            current.append(part)
            sentence = ''.join(current).strip()
            if sentence:
                sentences.append(sentence)
            current = []
        else:
            current.append(part)
        i += 1

    return sentences

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

    # Step 1: Create main chunks of ~8000 tokens
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

    # Step 2: Create subchunks of ~200 tokens per main chunk
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
                sub_chunk_id = f"{main_chunk_id}-{sub_index:03d}"
                rows.append([main_chunk_id, sub_chunk_id, sub_chunk.strip()])
                sub_chunk = sentence
                sub_tokens = sentence_tokens
                sub_index += 1
            else:
                sub_chunk += " " + sentence
                sub_tokens += sentence_tokens

        if sub_chunk:
            sub_chunk_id = f"{main_chunk_id}-{sub_index:03d}"
            rows.append([main_chunk_id, sub_chunk_id, sub_chunk.strip()])

    # Step 3: Write to CSV file
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["main_chunk_id", "sub_chunk_id", "text"])
        writer.writerows(rows)

# ====== EXECUTE SCRIPT ======
if __name__ == "__main__":
    process_file()
