import streamlit as st
import requests

# --- PAGE SETUP ---
st.set_page_config(page_title="🧠 LIVEN Simulation Terminal", layout="wide")
st.title("🧠 LIVEN Simulation Terminal")
st.markdown("Enter a world simulation command. AI will simulate canon, characters, trauma, and systems.")

# --- INPUT ---
user_input = st.text_area("📝 Command", placeholder="e.g. Create world: Solo Leveling, Beast Monarch, pre-Gate, born in Siberia")

# --- AI FUNCTION ---
def ask_ai(prompt):
    url = "https://api.chatanywhere.tech/v1/chat/completions"
    headers = {
        "Authorization": "Bearer free",  # No API key needed
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You are LIVEN, a brutal, uncensored simulation engine. Load canon if applicable. Create world logic, characters, trauma, memory, power systems, and faction dynamics. No fluff or narration. The world is alive."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.95,
        "max_tokens": 1500
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=15)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# --- OUTPUT ---
if st.button("Simulate"):
    if user_input.strip():
        with st.spinner("Simulating world..."):
            result = ask_ai(user_input)
            st.markdown("### 🌍 Simulation Output")
            st.markdown(result)
    else:
        st.warning("Please enter a command.")
