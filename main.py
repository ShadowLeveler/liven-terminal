import streamlit as st
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import datetime

# Google API setup
GOOGLE_SERVICE_KEY = {
  "type": "service_account",
  "project_id": "livenconnector",
  "private_key_id": "75df95a234e792022109215e4427554142b8960c",
  "private_key": """-----BEGIN PRIVATE KEY-----\nMIIEuwIBADANBgkqhkiG9w0BAQEFAASCBKUwggShAgEAAoIBAQC1fdsP7owXGjCZ\nB63q/zWXHHUfIYhkHbWdsMMjYMy2r6cT82/sUNZCDFyc6hr9vQFwqhJH+79F1b18\nmJkQjF6wjvCd4SwbzrbBrskFbfSFLdC1nz5yPPJnxxuDbgdoarbWPpSOyzypXXVB\nwBvmFOwK09ZNE/8+NJZWDBTPvi/VEPTsIO/IZu53+tKpJa5o0LpV6dlvtvCssLKk\nUB7pkK9oi3942H4KmmBsN6fW+KNXs2265z4WpOU6BMVex+ZPOffRkq5DU5NjZrqs\nVRGSjPQQ4UQtJhSPsUk8Hlvef5kFPGnCxdoglrIPHdVN/AIHSBJ+5wTk2GlDGx/d\nNmgNWkYTAgMBAAECgf93dN87HUgX7KUQFH3krxYW4CQ22VtsiiGAKVhHcO9NT1Ap\nUZHZeVuNHZXXsj8Rw9Wu0kI2Hv1Geei+mbIlsj6g93Rodk0SAH1J/kFR0Y2gGwfE\ng4wWpQboR6VUXJeDorm1Snt9gUfsMhd7r3atehfjCIuFMCRQTUymVk1cb1IMan7U\nH4NPkxdgw15CqHGBBnrZSjQx4HfDk2V314VOxURg/xPEye32jpOcOjZh64joe/8L\nQUD01K3EDfh65GV0PGUctEXD6OOR4x/XQHRF3FGO97y9ICjJcedcBK1sOmDMxQcr\nXjZV2rhFVz1F2APVLzn7n0Hz6uwqBCMGhEU9t1UCgYEA9DN7ofnUZP/tVmbStAqO\n4oG+g6jwEJQZvE+3YOkrxJEv3Koyux5bhz2zLrEbDGwEPQV23JFp5apq8Wo3WhJH\nhtHx/1iDehocExfAaO/IZKeFg4TlYhZHyR6ip37Ck3l5m6vC5P3uQ4ZF3D5GYN2F\nQqs6BNPvmnzJ1EePF9MWTv8CgYEAvkK4iSjWS0APY+oqaEU8jNC4jH588Vqcy7lE\ncEplkDdusZjqlnsUP3rHl13gwPZKTYg9CFI0tz9717NxlxtSYsvSPEHlIm7asRv8\nSB+hekOzbAXlsdj4BhwVGLyO/GNGfCQVXmq5D2OHb2SpzDHQZTjwPj44wn8BE07G\nAlow3O0CgYBfV1ZWqAafpDgSerSa7GBa2NL77lJD9r6RggITiRW4egLYwW5rFfAg\nPhueCDGKSQXimSaN+QwCSeXU+WZA+VAJuCAmVHWIj3cUkTpi/fMcMTd0YMd54z8F\nq7tPb7MiBtROzeGaq/WBUYQm9/1cRkCIBffx+JjclQnrokCgyZ41GwKBgQCKWOvk\n2KwSpe9LARB7J7Vi07cOej+SJQiU3xAT8xUtLBGy1HXonHDZxAb0W1A+IBlhjWqL\n7XLluSTtcU9syHI84ubp6CScyCz/0lC9hTqfNDF4oEUo8JNRpgP1K89xWSL8zCQ5\ntrMArKfj6TfLAoH9yMxxBj+xtjZq+sHjHgAf9QKBgEyhfES8qIUiO4wrf4PNxkp8\nPp9Wwfe2jzWUpd0wDNQawAt5KtsibzG1L0oFF3Z09vfbZqAyPAv50xDOULaocgMu\nhV8ka0c0MAFPRj5HVvQhH6pmwJPLdFdmIBAI8SG91DTfUizkZnForr0/P+nue9xm\nIAmqq/yXHze9UZmK9wcM\n-----END PRIVATE KEY-----""",
  "client_email": "livenservice@livenconnector.iam.gserviceaccount.com",
  "client_id": "110223949084267592579",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/livenservice@livenconnector.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

DOC_ID = "1PzMZ17V01fIZuf1hfP2xwS7xbjUYL-f-ekVyhWTKluM"
SHEET_ID = "1BUyZmZE0_zbm-hhcN2R6_wpK9oIOBESpK17o4jSsptI"
SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/spreadsheets"
]

credentials = Credentials.from_service_account_info(GOOGLE_SERVICE_KEY, scopes=SCOPES)
docs_service = build("docs", "v1", credentials=credentials)
sheets_service = build("sheets", "v4", credentials=credentials)

st.title("🧠 LIVEN Memory Connector")
st.write("Paste your simulation output below. This will be saved to your LIVEN memory files.")

text_input = st.text_area("📜 Simulation Output")

if st.button("💾 Save to Docs & Sheets"):
    try:
        # Save to Google Doc
        docs_service.documents().batchUpdate(
            documentId=DOC_ID,
            body={
                "requests": [
                    {
                        "insertText": {
                            "location": {"index": 1},
                            "text": f"\n{datetime.datetime.now().isoformat()}\n{text_input}\n"
                        }
                    }
                ]
            },
        ).execute()

        # Save to Google Sheet
        sheets_service.spreadsheets().values().append(
            spreadsheetId=SHEET_ID,
            range="Sheet1!A:A",
            valueInputOption="RAW",
            body={"values": [[datetime.datetime.now().isoformat(), text_input]]},
        ).execute()

        st.success("✅ Simulation saved to Docs and Sheets.")
    except Exception as e:
        st.error(f"❌ Error: {e}")
