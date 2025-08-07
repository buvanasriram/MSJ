import pyrebase
# import firebase_admin
# from firebase_admin import credentials, firestore


#--- Pyrebase config for client-side auth ---
firebase_config = {
  "apiKey": "AIzaSyBLwEod9BBKhnkYc8BWW60KIBhJQ3S_gIs",
  "authDomain": "msjproject-64a65.firebaseapp.com",
  "projectId": "msjproject-64a65",
  "storageBucket": "msjproject-64a65.firebasestorage.app",
  "messagingSenderId": "724042457421",
  "appId": "1:724042457421:web:c810813e2427399df51704",
  "databaseURL":"https://msjproject-64a65-default-rtdb.firebaseio.com"
}

# --- Initialize Pyrebase ---
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()

# --- Firebase Admin SDK for Firestore ---
# cred = credentials.Certificate("firebase_admin_config.json")  # Downloaded service account key
# firebase_admin.initialize_app(cred)
# db = firestore.client()
