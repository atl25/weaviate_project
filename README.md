# weaviate_project

##Weaviate Step
Pali (Roman)

1. Chattha Sangayana Tipitaka 4.1 မှ စာများကို text ဖိုင်အဖြစ် ပြောင်းလဲခြင်း
2. Clear BOM and White Space (chatgpt မှ လုပ်ဆောင်
3. Pali စာများတွင် Chunk ID သတ်မှတ်
4. Pali စာများကို vector ပြောင်း
5. Local တွင် စမ်းရန် Docker installation လုပ်၊ Compose file down, >docker compose up -d ဖြင့် run ပါ။
6. localhost:8080 မှာ testလုပ်ပါ။
7. Creat Schema/Class
8. Insert Data
9. Qurey Search

1, 2, 3, 4 မှ ဖိုင်များကို အောက်တွင် down ပါ။
-chunk id ထည့်ပြီးသားဖိုင် text.csv,
-vector ပြောင်းပြီးဖိုင် test_with_vectors.csv 4. Pali စာများကို vector ပြောင်း

**Colab - sentence-transformers/all-MiniLM-L6-v2**

**https://colab.research.google.com/drive/1n3HWSJh9OsR29v58_CKrdPf9nOyfqBDh#scrollTo=jWlYOq8iLsYR**

vector.txt ဖိုင်တွင် အသုံးပြုသော ကုဒ်ကို ထည့်ထားသည်။

5. Local တွင် စမ်းရန် Docker installation လုပ်၊ Compose file down, >docker compose up -d ဖြင့် run ပါ။ 9.localhost:8080 မှာ testလုပ်ပါ။

→ 250720 မှ စတင်သည်။ 250721 တွင် ပြီးဆုံးသည်။

Docker install လုပ်ပါ
Version check

> docker --version
> PowerShell (Admin) ဖြင့် wsl --update run လုပ်ပါ။

ပြီးရင် computer ကို restart လုပ်ပါ။

Docker Desktop ကို ပြန်ဖွင့်ပါ။

docker-compose.yml ဖိုင် download လုပ်ပါ

> curl -o docker-compose.yml https://weaviate.io/developers/weaviate/installation/docker-compose/docker-compose.yml

Terminal မှာ docker compose up -d ဖြင့် Weaviate run ပါ
ဖိုင်ထဲရှိ (docker-compose.yml သွားထည့်ထားတဲ့) folder ထဲမှာပဲ ဖွင့်ပါ။
စစ်ချင်ရင် >docker ps
browser မှာ http://localhost:8080 ကို ဝင်ကြည့်ပါ

ရပ်ချင်ရင် docker compose down

docker-compose.yml ဖိုင်ထည့်ပေးထားသည်။ 7. Creat Schema/Class

250722 မှ စတင်သည်။ 250723 တွင် ပြီးဆုံးသည်။

-create_schema.py ဖိုင်ထည့်ပေးထားပါသည်။

8. Insert Data
   250722 မှ စတင်သည်။ 250723 တွင် ပြီးဆုံးသည်။

-insert_data.py data သွင်းတဲ့ code ဖိုင်ပါ။

9. Qurey Search

-search.py code ဖိုင်ထည့်ပေးထားပါတယ်. Query နေရာမှာ စာသားပြောင်းလဲ ရှာဖွေနိုင်။

---

Data များထပ်ထည့်ခြင်း

250725 ဖိုင်များ ထပ်ထည့်သည်။

-နောက်ထပ် vectory ပြောင်းပြီးသား 15 ဖိုင်ကို ထပ်ထည့်လိုက်ပါတယ်။ ဖိုင်တွေ့ထည့်ပေးလိုက်ပါတယ်။
-create_all_collections.py
-insert_multiple_csvs.py
ဒီကုဒ်ဖိုင်နဲ့ပါ။

-multi_collection_search_auto.py
ဒီကုဒ်ဖိုင်နဲ့ search လုပ်ကြည့်တယ် result မထွက်ဘူး။

search.py ဖိုင်နဲ့ ရှာရင် ဖိုင်အကုန်လုံးမှာ ရှာပေးပါတယ်။ ရှာထားတဲ့ နမူထား txt ဖိုင်ထည့်ပေးလိုက်ပါတယ်။
-စမ်းသပ်ရှာဖွေခြင်း.txt ဖိုင်ပါ

Drive link ထည့်ပေးထားပါတယ်။ ဒီမှာ ဖိုင်တွေရှိပါတယ်။

**https://drive.google.com/drive/folders/17e4KRF4Drb3Fk7uu0ZbXQjHTqVIeed5L**

- အကုန်လုံး chatGPT အကူအညီနဲ့ လုပ်ထားပါတယ်
