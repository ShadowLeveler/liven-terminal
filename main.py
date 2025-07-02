import streamlit as st
import requests

# --- PAGE SETUP ---
st.set_page_config(page_title="🧠 LIVEN Simulation Terminal", layout="wide")
st.title("🧠 LIVEN Simulation Terminal")
st.markdown("Enter a simulation command. Claude will simulate canon, powers, trauma, and factions.")

# --- USER INPUT ---
user_input = st.text_area("📝 Command", placeholder="e.g. Play in: One Piece, ex-Warlord, Logia fruit, hiding in Skypiea")

# --- AI FUNCTION ---
def ask_ai(prompt):
    url = "https://banterai.xyz/api/chat"  # ✅ Claude-3 Haiku proxy
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "model": "claude-3-haiku",
        "messages": [
            {"role": "system", "content": "You are LIVEN, a brutal, uncensored simulation engine. Load canon if known. Simulate world logic, mutation, trauma, power systems, factions, memory, and consequences. No fluff. No guidance."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=15)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# --- SIMULATE ---
if st.button("Simulate"):
    if user_input.strip():
        with st.spinner("Simulating..."):
            result = ask_ai(user_input)
            st.markdown("### 🌍 Simulation Output")
            st.markdown(result)
    else:
        st.warning("Please enter a command.")
