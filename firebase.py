import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from pathlib import Path
import pandas as pd
cred = credentials.Certificate('test-sdk.json')
firebase_admin.initialize_app(cred,{'databaseURL':'https://test-6b8ec-default-rtdb.firebaseio.com/'})
csv_file_path = 'hand_landmarks.csv'
df = pd.read_csv('hand_landmarks.csv')
db_ref = db.reference('/users')
user_list = df.to_dict(orient='records')
for user_data in user_list:
    db_ref.push(user_data)