import streamlit as st
import requests

# --- PAGE SETUP ---
st.set_page_config(page_title="🧠 LIVEN Simulation Terminal", layout="wide")
st.title("🧠 LIVEN Simulation Terminal")
st.markdown("Type your simulation command. AI will simulate canon, powers, factions, trauma, etc.")

# --- USER INPUT ---
user_input = st.text_area("📝 Command", placeholder="e.g. Create world: One Piece, Marine Deserter, Logia Fruit, East Blue")

# --- AI HANDLER ---
def ask_ai(prompt):
    url = "https://api.chatanywhere.tech/v1/chat/completions"
    headers = {
        "Authorization": "Bearer free",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are LIVEN, a brutal, uncensored, autonomous simulation engine. You simulate world logic, character memory, factions, power systems, and trauma over time. No explanation. No fluff. Just reactive simulation."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.95,
        "max_tokens": 1500
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=15)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    exc
