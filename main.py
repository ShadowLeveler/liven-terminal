import streamlit as st
import os
from openai import OpenAI

# --- SETUP API KEY ---
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# --- PAGE SETUP ---
st.set_page_config(page_title="LIVEN Simulation Terminal", layout="wide")
st.title("🧠 LIVEN Simulation Terminal")
st.markdown("Enter world commands below. AI will generate world, characters, tabs, and systems.")

# --- COMMAND INPUT ---
user_input = st.text_area("📝 Command", placeholder="e.g. Create world: Solo Leveling, Beast Monarch, pre-Gate, born in Siberia")

# --- OUTPUT WINDOW ---
if st.button("Simulate"):
    with st.spinner("Simulating world..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a brutal simulation engine (LIVEN). Do not narrate. Accept the user's command as input and generate the simulation state. Load canon if possible. Create tabs, characters, factions, powers, locations, timelines, and tick logic. Respond as if the world is alive and reactive."},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.9,
                max_tokens=1200
            )
            result = response.choices[0].message.content
            st.markdown("### 🌍 Simulation Output")
            st.markdown(result)
        except Exception as e:
            st.error(f"⚠️ Error: {e}")
