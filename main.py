import streamlit as st
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
import googleapiclient.discovery
import urllib.parse
import json

# --- STREAMLIT SETUP ---
st.set_page_config(page_title="LIVEN Memory Connector", layout="wide")
st.title("🧠 LIVEN Memory Connector")
st.markdown("Paste your simulation output below. This will be saved to your LIVEN memory files.")

# --- STATE INIT ---
if "credentials" not in st.session_state:
    st.session_state["credentials"] = None

# --- USER INPUT ---
sim_output = st.text_area("📜 Simulation Output", height=300)

# --- GOOGLE AUTH FLOW ---
client_id = st.secrets["GOOGLE_CLIENT_ID"]
client_secret = st.secrets["GOOGLE_CLIENT_SECRET"]
REDIRECT_URI = "https://liven-terminal-yjkmpuuqdzfq3lep9h4c7d.streamlit.app"

flow = Flow.from_client_config(
    {
        "web": {
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uris": [REDIRECT_URI],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    },
    scopes=[
        "https://www.googleapis.com/auth/documents",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
    ],
    redirect_uri=REDIRECT_URI
)

# --- GET TOKEN FROM REDIRECT ---
query_params = st.experimental_get_query_params()
if "code" in query_params and st.session_state["credentials"] is None:
    code = query_params["code"][0]
    flow.fetch_token(code=code)
    creds = flow.credentials
    st.session_state["credentials"] = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": creds.scopes
    }
    st.success("✅ Google authorization complete. You can now save to memory!")

# --- IF NOT AUTHED YET ---
if st.session_state["credentials"] is None:
    auth_url, _ = flow.authorization_url(prompt='consent')
    st.markdown(f"[🔗 Click here to authorize Google]({auth_url})")

# --- AUTHED: Save Output ---
else:
    creds = Credentials(**st.session_state["credentials"])
    doc_id = st.secrets["DOC_ID"]
    sheet_id = st.secrets["SHEET_ID"]

    if st.button("💾 Save to Memory"):
        try:
            # Save to Google Docs
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

            # Save to Google Sheets
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
