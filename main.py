import streamlit as st
import requests

# --- PAGE SETUP ---
st.set_page_config(page_title="🧠 LIVEN Simulation Terminal", layout="wide")
st.title("🧠 LIVEN Simulation Terminal")
st.markdown("Enter world commands below. AI will generate world, characters, tabs, and systems.")

# --- INPUT ---
user_input = st.text_area("📝 Command", placeholder="e.g. Create world: One Piece, Marine Deserter, Loguetown, Logia fruit")

# --- AI FUNCTION ---
def ask_ai(prompt):
    url = "https://api.llmfree.tech/v1/chat/completions"  # ✅ Claude-compatible free proxy
    headers = {
        "Authorization": "Bearer free",  # No key needed
        "Content-Type": "application/json"
    }
    data = {
        "model": "claude-3-haiku-20240307",
        "messages": [
            {"role": "system", "content": "You are LIVEN, a brutal simulation engine. Load canon if applicable. Simulate world, character, trauma, power systems, factions, events, and evolving logic. No meta commentary."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.9,
        "max_tokens": 1200
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ Error: {e}"

# --- RUN SIMULATION ---
if st.button("Simulate"):
    if user_input.strip():
        with st.spinner("Simulating world..."):
            result = ask_ai(user_input)
            st.markdown("### 🌍 Simulation Output")
            st.markdown(result)
    else:
        st.warning("Please enter a command.")
