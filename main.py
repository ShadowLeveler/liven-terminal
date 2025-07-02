import streamlit as st
import json
import googleapiclient.discovery
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="LIVEN Memory Connector", layout="wide")
st.title("🧠 LIVEN Memory Connector")
st.markdown("Paste your simulation output below. This will be saved to your LIVEN memory files.")

# Load credentials from secrets
SERVICE_KEY = json.loads(st.secrets["GOOGLE_SERVICE_KEY"])

SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/spreadsheets"
]
credentials = Credentials.from_service_account_info(SERVICE_KEY, scopes=SCOPES)

# Get document IDs
doc_id = st.secrets["DOC_ID"]
sheet_id = st.secrets["SHEET_ID"]

# User input
sim_output = st.text_area("📜 Simulation Output", height=300)

# Save button
if st.button("💾 Save to Memory"):
    try:
        # Save to Docs
        docs_service = googleapiclient.discovery.build('docs', 'v1', credentials=credentials)
        docs_service.documents().batchUpdate(documentId=doc_id, body={
            "requests": [
                {
                    "insertText": {
                        "location": {"index": 1},
                        "text": f"\n{sim_output}\n"
                    }
                }
            ]
        }).execute()

        # Save to Sheets
        sheets_service = googleapiclient.discovery.build('sheets', 'v4', credentials=credentials)
        sheets_service.spreadsheets().values().append(
            spreadsheetId=sheet_id,
            range="Sheet1!A1",
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body={"values": [[sim_output]]}
        ).execute()

        st.success("✅ Simulation saved to Google Docs and Sheets.")

    except Exception as e:
        st.error(f"⚠️ Error saving: {e}")
