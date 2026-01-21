import streamlit as st
import re
import pandas as pd
from datetime import datetime
import plotly.express as px

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Regalati un Sogno", page_icon="🍀", layout="centered")

# ------------------ CSS ------------------
st.markdown("""
<style>
div[data-testid="stNumberInput"] input {
    font-size: 20px !important;
    font-weight: bold !important;
}
.stButton button {
    width: 100%;
    height: 3em;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ------------------ INIT STATE ------------------
for i in range(6):
    if f"n{i}" not in st.session_state:
        st.session_state[f"n{i}"] = 1

# ------------------ FUNZIONI ------------------
def importa_numeri():
    testo = st.session_state.get("incolla_qui", "")
    nums = re.findall(r'\d+', testo)

    if len(nums) < 6:
        st.warning("Inserisci almeno 6 numeri")
        return

    for i in range(6):
        st.session_state[f"n{i}"] = int(nums[i])

# ------------------ UI ------------------
st.title("🍀 Regalati un Sogno")
st.subheader("📋 Verifica Estrazione")

st.text_input(
    "Incolla i numeri estratti:",
    key="incolla_qui",
    placeholder="Esempio: 10 22 35 44 51 68"
)

st.button("📥 IMPORTA NUMERI", on_click=importa_numeri)

# ------------------ NUMERI ------------------
st.divider()
st.markdown("### ✍️ Conferma o modifica")

cols = st.columns(6)
estratti = []

for i in range(6):
    val = cols[i].number_input(
        f"{i+1}°",
        min_value=1,
        max_value=90,
        value=st.session_state[f"n{i}"],
        key=f"input_{i}"
    )
    estratti.append(val)

# ------------------ VERIFICA ------------------
if st.button("🚀 VERIFICA ORA"):
    SCHEDINE = [
        {3,10,17,40,85,86},
        {10,17,19,40,85,86},
        {17,19,40,75,85,86},
        {3,19,40,75,85,86},
        {3,10,19,75,85,86},
        {3,10,17,75,85,86}
    ]

    set_estratti = set(estratti)
    vincite = []

    for i, sch in enumerate(SCHEDINE, 1):
        presi = sorted(sch.intersection(set_estratti))
        if len(presi) >= 2:
            vincite.append((i, len(presi), presi))

    if vincite:
        st.success("🎉 VINCITA!")
        for v in vincite:
            st.write(f"Schedina {v[0]} → {v[1]} punti {v[2]}")
    else:
        st.error("😢 Nessuna vincita")
