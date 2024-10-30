import streamlit as st
import requests
from datetime import datetime

API_KEY = st.secrets["API_TOKEN"]
BASE_URL = "https://kurier.api-us1.com/api/3/"

def make_api_request(endpoint, params=None):
    headers = {"Api-Token": API_KEY}
    response = requests.get(BASE_URL + endpoint, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def get_scheduled_campaigns():
    campaigns_data = make_api_request("campaigns", {"filters[status]": "1", "filters[type]": "recurring", "orders[sdate]": "ASC"})
    
    scheduled_campaigns = []
    for campaign in campaigns_data["campaigns"]:
        if campaign["status"] == "scheduled" and campaign["type"] in ["activersss", "recurring"]:
            campaign_lists = ", ".join([list["list"]["name"] for list in campaign["campaignLists"]])
            send_date = datetime.strptime(campaign["sdate"], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M")
            
            scheduled_campaigns.append({
                "id": campaign["id"],
                "name": campaign["name"],
                "type": campaign["type"],
                "lists": campaign_lists,
                "send_date": send_date
            })
    
    return scheduled_campaigns

def main():
    st.title("Scheduled Campaigns from ActiveCampaign")

    if st.button("Fetch Scheduled Campaigns"):
        try:
            campaigns = get_scheduled_campaigns()
            
            if campaigns:
                st.write(f"Found {len(campaigns)} scheduled campaigns:")
                
                for campaign in campaigns:
                    st.markdown(f"""
                        ### Campaign: {campaign['name']}
                        - Type: {campaign['type'].capitalize()}
                        - Associated Lists: {campaign['lists']}
                        - Scheduled Send Date: {campaign['send_date']}
                        """)
            else:
                st.info("No scheduled campaigns found matching the criteria.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()