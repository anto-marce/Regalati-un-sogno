import streamlit as st
import re
import pandas as pd
from datetime import datetime
import urllib.parse

# -------------------------------------------------
# IMPOSTAZIONI PAGINA
# -------------------------------------------------
st.set_page_config(
    page_title="Regalati un Sogno",
    page_icon="🍀",
    layout="centered"
)

# -------------------------------------------------
# STILE CSS
# -------------------------------------------------
st.markdown("""
<style>
.ams-button, .wa-button {
    display:block;
    padding:12px;
    margin-bottom:12px;
    text-align:center;
    border-radius:8px;
    font-weight:bold;
    color:white!important;
    text-decoration:none;
}
.ams-button { background:#003366; }
.wa-button { background:#25D366; }

.status-red {
    background:#f8d7da;
    padding:10px;
    border-radius:8px;
    text-align:center;
    font-weight:bold;
}
.status-green {
    background:#d4edda;
    padding:10px;
    border-radius:8px;
    text-align:center;
    font-weight:bold;
}

.quota-box {
    background:#e8f5e9;
    padding:20px;
    border-radius:12px;
    text-align:center;
}
.quota-valore {
    font-size:32px;
    font-weight:800;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# FUNZIONI AUDIO
# -------------------------------------------------
def play_audio(url):
    st.components.v1.html(
        f'<audio autoplay style="display:none"><source src="{url}"></audio>',
        height=0
    )

# -------------------------------------------------
# FUNZIONI BOTTINO
# -------------------------------------------------
def registra_movimento(tipo, descrizione, importo):
    nuovo = {
        "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "Tipo": tipo,
        "Descrizione": descrizione,
        "Importo": importo
    }
    try:
        df = pd.read_csv("bottino.csv")
        df = pd.concat([df, pd.DataFrame([nuovo])], ignore_index=True)
    except FileNotFoundError:
        df = pd.DataFrame([nuovo])
    df.to_csv("bottino.csv", index=False)

def carica_bottino():
    try:
        return pd.read_csv("bottino.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Data", "Tipo", "Descrizione", "Importo"])

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
with st.sidebar:
    st.title("🍀 Menù")
    scelta = st.radio(
        "Seleziona sezione:",
        ["🔍 Verifica Vincita", "📜 Stato Abbonamento", "💰 Calcolo Quote", "🏛️ Il Bottino"]
    )
    st.divider()
    st.info("Inizio Abbonamento: 22 Gen 2026")

# -------------------------------------------------
# SESSION STATE INIT
# -------------------------------------------------
if "estrazioni" not in st.session_state:
    st.session_state.estrazioni = 0
if "ultima_estrazione_registrata" not in st.session_state:
    st.session_state.ultima_estrazione_registrata = 0

soci = ["VS", "MM", "ED", "AP", "GGC", "AM"]
for s in soci:
    st.session_state.setdefault(f"paga_{s}", False)

# -------------------------------------------------
# TITOLO
# -------------------------------------------------
st.title("🍀 Regalati un Sogno")

# =================================================
# 🔍 VERIFICA VINCITA
# =================================================
if scelta == "🔍 Verifica Vincita":

    st.subheader("📋 Verifica Estrazione")

    # PASSO 1 AMS
    st.markdown(
        """
        <a href="https://www.adm.gov.it/portale/monopoli/giochi/giochi_num_total/superenalotto"
           target="_blank"
           class="ams-button">
           ➡️ PASSO 1: Controlla Estrazione su Sito AMS
        </a>
        """,
        unsafe_allow_html=True
    )

    # inizializza numeri
    if "n0" not in st.session_state:
        for i in range(6):
            st.session_state[f"n{i}"] = 1

    # PASSO 2 incolla numeri
    def distribuisci():
        nums = re.findall(r"\d+", st.session_state.incolla)
        if len(nums) >= 6:
            for i in range(6):
                st.session_state[f"n{i}"] = int(nums[i])

    st.text_input(
        "PASSO 2: Incolla i numeri estratti e premi INVIO",
        key="incolla",
        on_change=distribuisci
    )

    cols = st.columns(6)
    estratti = [
        cols[i].number_input(f"{i+1}°", 1, 90, key=f"n{i}")
        for i in range(6)
    ]

    # PASSO 3 verifica
