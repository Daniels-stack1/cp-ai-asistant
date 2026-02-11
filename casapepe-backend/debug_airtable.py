import os
from pyairtable import Api
from dotenv import load_dotenv
import json

load_dotenv()

api_key = os.environ.get("AIRTABLE_API_KEY")
base_id = os.environ.get("AIRTABLE_BASE_ID")
table_name = "Visitas" # Using the name provided by the user

print(f"DEBUGGING AIRTABLE CONNECTION")
print(f"Base ID: {base_id}")
print(f"Table: {table_name}")

if not api_key:
    print("ERROR: AIRTABLE_API_KEY is missing in .env")
    exit()

api = Api(api_key)
table = api.table(base_id, table_name)

try:
    print(f"\nFetching first 5 records from '{table_name}'...")
    records = table.all(max_records=5)
    
    if not records:
        print("SUCCESS: Connection worked, but the table is EMPTY found []")
    else:
        print(f"SUCCESS: Found {len(records)} records.")
        print("First record structure (CHECK FIELD NAMES):")
        print(json.dumps(records[0]['fields'], indent=2))
        
        print("\nList of Names found:")
        for r in records:
            # Try to guess the name field
            fields = r['fields']
            name = fields.get('Nombre') or fields.get('Name') or fields.get('Restaurant') or "UNKNOWN FIELD"
            print(f"- ID: {r['id']} | Name: {name}")

except Exception as e:
    print(f"\nERROR FETCHING DATA: {e}")
    if "404" in str(e):
        print("HINT: Check if 'AIRTABLE_TABLE_NAME' in .env matches the actual table name in Airtable.")
