import streamlit as st
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
import googleapiclient.discovery
import os
import json

st.set_page_config(page_title="LIVEN Memory Connector", layout="wide")
st.title("🧠 LIVEN Memory Connector")
st.markdown("Paste your simulation output below. This will be saved to your LIVEN memory files.")

# --- SETUP ---
if "credentials" not in st.session_state:
    st.session_state["credentials"] = None

# --- INPUT ---
sim_output = st.text_area("📜 Simulation Output", height=300)

# --- GOOGLE AUTH ---
if not st.session_state["credentials"]:
    st.markdown("🔐 Please log into Google to enable saving.")
    client_id = st.secrets["GOOGLE_CLIENT_ID"]
    client_secret = st.secrets["GOOGLE_CLIENT_SECRET"]

    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uris": ["http://localhost:8501"],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=[
            "https://www.googleapis.com/auth/documents",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
        ],
        redirect_uri="http://localhost:8501"
    )

    auth_url, _ = flow.authorization_url(prompt='consent')
    st.markdown(f"[🔗 Click here to authorize Google]({auth_url})")

else:
    creds = Credentials(**st.session_state["credentials"])
    doc_id = st.secrets["DOC_ID"]
    sheet_id = st.secrets["SHEET_ID"]

    if st.button("💾 Save to Memory"):
        try:
            # --- Save to Google Doc ---
            docs_service = googleapiclient.discovery.build('docs', 'v1', credentials=creds)
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

            # --- Save to Google Sheet ---
            sheets_service = googleapiclient.discovery.build('sheets', 'v4', credentials=creds)
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
