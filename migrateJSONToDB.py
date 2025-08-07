import json
from firebase_config import auth, db

with open("dataMSJ.json", "r", encoding="utf-8") as f:
    data = json.load(f)




for entry in data:
    ref = db.child("users").child("buvana_sriram@gmail_com")
    ref.push(entry)