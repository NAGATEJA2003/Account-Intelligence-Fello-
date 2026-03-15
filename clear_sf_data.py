import os
from dotenv import load_dotenv
from simple_salesforce import Salesforce

load_dotenv()

def wipe_data():
    sf = Salesforce(
        username=os.getenv('SF_USERNAME'), 
        password=os.getenv('SF_PASSWORD'), 
        security_token=os.getenv('SF_TOKEN')
    )
    
    # Query all records
    records = sf.query_all("SELECT Id FROM Visitor_Intelligence__c")
    
    if records['totalSize'] == 0:
        print("Inventory already empty!")
        return

    print(f"Deleting {records['totalSize']} records...")
    for r in records['records']:
        sf.Visitor_Intelligence__c.delete(r['Id'])
    
    print("✨ Salesforce Object is now 100% empty.")

if __name__ == "__main__":
    wipe_data()