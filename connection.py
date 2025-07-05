from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

# Get URI from environment
mongo_uri = os.getenv("MONGO_URI")
if not mongo_uri:
    print("❌ MONGO_URI not found in environment")
    exit(1)

# Connect to MongoDB
client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)

try:
    client.admin.command('ping')
    print("✅ Connected to MongoDB Atlas successfully!")
except Exception as e:
    print("❌ Connection to MongoDB Atlas failed:")
    print(e)
