import streamlit as st
import requests
from datetime import datetime

# Set up API credentials (replace with your actual credentials)
API_KEY = st.secrets["API_KEY"]
BASE_URL = "https://kurier.api-us1.com/api/3/"

def fetch_campaigns():
    url = f"{BASE_URL}campaigns"
    params = {
        "status": "scheduled",
        "sort": "send_date",
        "direction": "ASC",
        "per_page": 50
    }
    headers = {"Api-Token": API_KEY}
    
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()

def toggle_campaign(campaign_id, status):
    url = f"{BASE_URL}campaigns/{campaign_id}/toggle"
    headers = {"Api-Token": API_KEY}
    data = {"status": status}
    
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()

st.title("ActiveCampaign Scheduled Campaigns")

if 'campaigns' not in st.session_state:
    st.session_state.campaigns = fetch_campaigns()

with st.container():
    for campaign in st.session_state.campaigns['campaigns']:
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.write(f"**{campaign['name']}**")
            st.write(f"Send Date: {datetime.fromtimestamp(campaign['senddate']).strftime('%Y-%m-%d %H:%M:%S')}")
        
        with col2:
            if campaign['status'] == 1:
                if st.button(f"Disable {campaign['id']}", key=f"disable_{campaign['id']}"):
                    try:
                        result = toggle_campaign(campaign['id'], 0)
                        st.success(f"Campaign {campaign['name']} disabled successfully.")
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
            st.write(f"Status: {'Enabled' if campaign['status'] == 1 else 'Disabled'}")

if st.button("Refresh Campaign List"):
    st.session_state.campaigns = fetch_campaigns()

st.write(f"Total scheduled campaigns: {len(st.session_state.campaigns['campaigns'])}")