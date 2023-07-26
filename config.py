import os
class Config:   
    API_ID = int(os.environ.get("API_ID", "21288218"))
    API_HASH = os.environ.get("API_HASH", "dd47d5c4fbc31534aa764ef9918b3acd")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "6658841062:AAFDWIgbflwa0sedHXoXqycHL_Mnz85h7TU") 
    OWNER_ID = os.environ.get("OWNER_ID", "")
    DATABASE_URI = os.environ.get("DATABASE_URI", "")
    DATABASE_NAME = os.environ.get("DATABASE_NAME","Cluster0")
    COLLECTION_NAME = os.environ.get('COLLECTION_NAME', 'Forward_data')
    SESSION = os.environ.get("SESSION", "Forward_Session")


