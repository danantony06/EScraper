import os
from dotenv import load_dotenv
from datetime import datetime
from supabase import create_client, Client

load_dotenv()
supaUrl = os.getenv("SUPABASE_URL")
supaKey = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(supaUrl, supaKey)

def fetch_all_data(table, start_page=15):
    """Fetch all records from a given table, starting from a specified page."""
    page = start_page
    all_data = []
    
    while True:
        response = supabase.table(table).select("*").range((page-1)*1000, page*1000-1).execute()
        
        if not response.data:
            break
        
        all_data.extend(response.data)
        page += 1  
    
    return all_data


def reformat_date(date_str):
    """Convert any date format into 'Year, Month Name day, time EST'"""
    correct_format = "%Y, %B %d, %H:%M EST"

    
    try:
        datetime.strptime(date_str, correct_format)
        return None  
    except ValueError:
        pass

    try:
        date_str_no_tz = date_str.replace(" EST", "")  # Remove ' EST'
        date_obj = datetime.strptime(date_str_no_tz, "%Y-%m-%d %H:%M:%S")
        return date_obj.strftime(correct_format)
    except ValueError:
        pass

    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return date_obj.strftime(correct_format)
    except ValueError:
        pass

    try:
        date_str_no_tz = date_str.replace(" EST", "")
        date_obj = datetime.strptime(date_str_no_tz, "%B %d, %H:%M")
        date_obj = date_obj.replace(year=2025) 
        return date_obj.strftime(correct_format)
    except ValueError:
        pass

    try:
        date_str_no_tz = date_str.replace(" EST", "")
        date_obj = datetime.strptime(date_str_no_tz, "%B %d, %Y, %H:%M")
        return date_obj.strftime(correct_format)
    except ValueError:
        pass

    print(f" Failed to parse date: '{date_str}'")
    return None  


def update_database(table, record_id, new_date):
    """Update a record in the database with the corrected date."""
    response = supabase.table(table).update({"Date": new_date}).eq("id", record_id).execute()
    return response

hit_rate_data = fetch_all_data("HitRates")

for record in hit_rate_data:
    old_date = record.get('Date')
    
    if not old_date:
        continue
    
    new_date = reformat_date(old_date)
    
    if new_date:
        record_id = record.get('id') 
        update_database("HitRates", record_id, new_date)
        print(f"Updated record {record_id}: '{old_date}' → '{new_date}'")
    else:
        print(f" Date '{old_date}' is already in the correct format or could not be parsed.")
