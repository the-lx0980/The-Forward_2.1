import os
class Config:   
    APP_ID = int(os.environ.get("APP_ID", "21288218"))
    API_HASH = os.environ.get("API_HASH", "dd47d5c4fbc31534aa764ef9918b3acd")
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "6658841062:AAFDWIgbflwa0sedHXoXqycHL_Mnz85h7TU") 
    OWNER_ID = os.environ.get("OWNER_ID", "")
    DATABASE_URI = os.environ.get("DATABASE_URI", "")
    DATABASE_NAME = os.environ.get("DATABASE_NAME","Cluster0")
    COLLECTION_NAME = os.environ.get('COLLECTION_NAME', 'Forward_data')
    TO_CHANNEL = -1001592628992
