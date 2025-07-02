import streamlit as st
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import datetime
import re

# --- CONFIGURATION ---
GOOGLE_SERVICE_KEY = {
  "type": "service_account",
  "project_id": "livenconnector",
  "private_key_id": "75df95a234e792022109215e4427554142b8960c",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEuwIBADAN...\n-----END PRIVATE KEY-----\n",
  "client_email": "livenservice@livenconnector.iam.gserviceaccount.com",
  "client_id": "110223949084267592579",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/livenservice@livenconnector.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/spreadsheets"
]

# --- WORLD SETUP ---
worlds = {
    "one_piece": {
        "doc_id": "1PzMZ17V01fIZuf1hfP2xwS7xbjUYL-f-ekVyhWTKluM",
        "sheet_id": "1BUyZmZE0_zbm-hhcN2R6_wpK9oIOBESpK17o4jSsptI"
    },
    # Add more worlds here
}

# --- INIT ---
credentials = Credentials.from_service_account_info(GOOGLE_SERVICE_KEY, scopes=SCOPES)
docs_service = build("docs", "v1", credentials=credentials)
sheets_service = build("sheets", "v4", credentials=credentials)

# --- UI ---
st.title("🧠 LIVEN Memory Connector")
selected_world = st.selectbox("🌍 Select World", list(worlds.keys()))
text_input = st.text_area("📜 Simulation Output")

# --- MEMORY FILTER ---
def is_valid_simulation(text):
    if not text.strip():
        return False
    if len(text.strip()) < 10:
        return False
    return any(keyword in text.lower() for keyword in ["character", "world", "location", "faction", "status", "skill", "time", "act", "weather"])

if st.button("💾 Save to Docs & Sheets"):
    if not is_valid_simulation(text_input):
        st.warning("⚠️ Ignored: Does not match in-world simulation format.")
    else:
        try:
            doc_id = worlds[selected_world]["doc_id"]
            sheet_id = worlds[selected_world]["sheet_id"]
            now = datetime.datetime.now().isoformat()

            # Save to Google Doc
            docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={
                    "requests": [
                        {
                            "insertText": {
                                "location": {"index": 1},
                                "text": f"\n[{now}]\n{text_input}\n"
                            }
                        }
                    ]
                },
            ).execute()

            # Save to Google Sheet
            sheets_service.spreadsheets().values().append(
                spreadsheetId=sheet_id,
                range="Sheet1!A:B",
                valueInputOption="RAW",
                body={"values": [[now, text_input]]},
            ).execute()

            st.success("✅ Simulation saved to Docs and Sheets.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
