import pandas as pd
import textwrap

# CSV ဖိုင်ဖွင့်ပါ
df = pd.read_csv("MN5_chunk.csv")  # ဖိုင်နာမည်ကိုသင့်အတိုင်းပြောင်း

# NaN များကို ဖယ်ရှားခြင်း (သို့) မပါဘဲသုံးချင်ရင် fillna("") လုပ်လို့ရ
df = df[df['pali_text'].notna()]  # NaN တန်ဖိုးပါတဲ့ row များဖယ်ရှား

# Chunk ပြန်ခွဲ
all_chunks = []

for index, row in df.iterrows():
    text = str(row['pali_text'])  # string ပြောင်းမယ်
    chunks = textwrap.wrap(text, width=500, break_long_words=False)
    for i, chunk in enumerate(chunks):
        all_chunks.append({
            "original_index": index,
            "chunk_index": i,
            "chunk_text": chunk
        })

# ပြန်ထုတ်ရန် DataFrame
chunk_df = pd.DataFrame(all_chunks)
chunk_df.to_csv("rechunked_output.csv", index=False)
