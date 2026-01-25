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
    
    def fetch_data(self,table_name, columns,filter=None):

        query = supabase.table(table_name).select(columns)
        if filter:
            query = query.eq(filter["column"], filter["value"])
        try:    
            response = query.execute()
        except Exception as e:
            print("Error executing query:", e)
            return []
        data_received = response.data
        return data_received
    
    def insert_data(self,data,table_name):
        # print("Inserting data:", data)
        response = (
            supabase.table(table_name)
            .insert(data)
            .execute()
        )
        return response.data
    
    def update_data(self,table_name, data, filter=None):
        query = supabase.table(table_name).update(data)

        if(filter):
            query.eq(filter["column"],filter["value"])
        try:
            res = query.execute()
        except Exception as e:
            print("Error executing query:", e)
        
        return res

    def upsert_data(self,table_name, data, filter=None):
        query = supabase.table(table_name).upsert(data)

        if(filter):
            query.eq(filter["column"],filter["value"])
        try:
            res = query.execute()
        except Exception as e:
            print("Error executing query:", e)
        
        return res