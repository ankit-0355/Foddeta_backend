import supabase
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

class Database:
    def __init__(self):
        self.client = supabase.supabase_url
    
    def execute_query(self):
        response = (
            supabase.from_("foodeta")
            .select("*")
            .execute()
        )
        data_received = response.data
        return data_received
