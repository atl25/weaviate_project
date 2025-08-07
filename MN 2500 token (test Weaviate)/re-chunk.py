import pandas as pd
import textwrap

# Load CSV
df = pd.read_csv('MN5_chunk.csv')

# Store new chunks here
new_rows = []

for idx, row in df.iterrows():
    chunks = textwrap.wrap(row['pali_text'], width=200, break_long_words=False)
    for i, chunk in enumerate(chunks):
        new_rows.append({
            'chunk_id': f"{row['chunk_id']}",
            'sub_chunk_id':f"{row['chunk_id']}_{i}", 
            'pali_text': chunk
        })

# Create new DataFrame
chunked_df = pd.DataFrame(new_rows)
chunked_df.to_csv('MN5_re-chunked.csv', index=False)