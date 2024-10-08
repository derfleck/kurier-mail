import streamlit as st
import requests
from datetime import datetime

API_KEY = st.secrets["API_TOKEN"]
BASE_URL = "https://kurier.api-us1.com/admin/api.php"

def fetch_campaigns(page=1):
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    url = f"{BASE_URL}"
    params = {
        "api_action": "campaign_list",
        "api_output": "json",
        "sort": "sdate",
        "sort_direction": "DESC",
        "filters[name]": "KURIER",
        "full": "0",
        "filters[sdate_since_datetime]": current_timestamp,
        "page": page
    }
    headers = {"API-TOKEN": API_KEY}
    
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()

#https://www.activecampaign.com/api/example.php?call=campaign_status - Example
def toggle_campaign(campaign_id, status):
    url = f"{BASE_URL}"
    headers = {"API-TOKEN": API_KEY}
    params = {
        "api_action": "campaign_status",
        "api_output": "json",
        "id": campaign_id,
        "status": status
    }
    
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()

st.title("Newsletter Tool")

st.session_state.campaigns = []

page = 1
while True:
    campaigns = fetch_campaigns(page)
    if not campaigns["result_code"] == 1:
        break
    campaigns = {k: v for k, v in campaigns.items() if k.isdigit()}
    for k, v in campaigns.items():
        if k.isdigit():
            st.session_state.campaigns.append(v)
    page += 1

with st.container():
    for campaign in st.session_state.campaigns:
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.write(campaign.get('name'))
            #if send_date:
            #    st.write(f"Send Date: {datetime.fromtimestamp(send_date).strftime('%Y-%m-%d %H:%M:%S')}")
            #else:
            #    st.write("Send Date: N/A")
            #st.write(f"**{campaign['name']}**")
            #st.write(f"Send Date: {datetime.fromtimestamp(campaign['senddate']).strftime('%Y-%m-%d %H:%M:%S')}")
        
        with col2:
            if campaign['status'] == "Geplant":
                if st.button(f"Disable {campaign['id']}", key=f"disable_{campaign['id']}"):
                    try:
                        result = toggle_campaign(campaign['id'], 3)
                        st.success(f"Campaign {campaign['name']} paused successfully.")
                        st.session_state.campaigns = fetch_campaigns()  # Refresh the list
                    except Exception as e:
                        st.error(f"Error disabling campaign: {str(e)}")
            else:
                if st.button(f"Enable {campaign['id']}", key=f"enable_{campaign['id']}"):
                    try:
                        result = toggle_campaign(campaign['id'], 1)
                        st.success(f"Campaign {campaign['name']} enabled successfully.")
                        st.session_state.campaigns = fetch_campaigns()  # Refresh the list
                    except Exception as e:
                        st.error(f"Error enabling campaign: {str(e)}")

        with col3:
            st.write(f"Status: {campaign['status']}")

if st.button("Refresh Campaign List"):
    st.session_state.campaigns = fetch_campaigns()

st.write(f"Total scheduled campaigns: {len(st.session_state.campaigns)}")