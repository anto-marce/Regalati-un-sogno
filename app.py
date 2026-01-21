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
    if st.button("VERIFICA ORA 🚀", use_container_width=True):

        SCHEDINE = [
            {3,10,17,40,85,86},
            {10,17,19,40,85,86},
            {17,19,40,75,85,86},
            {3,19,40,75,85,86},
            {3,10,19,75,85,86},
            {3,10,17,75,85,86},
        ]

        vincite = []
        for i, sch in enumerate(SCHEDINE, 1):
            presi = sorted(sch.intersection(set(estratti)))
            if len(presi) >= 2:
                vincite.append((i, len(presi), presi))

        if vincite:
            play_audio("https://www.myinstants.com/media/sounds/ta-da.mp3")
            st.balloons()

            for v in vincite:
                st.success(f"🔥 Schedina {v[0]}: {v[1]} punti ({', '.join(map(str, v[2]))})")

            # testo WhatsApp dinamico + bottino
            df = carica_bottino()
            entrate = df[df.Tipo=="Entrata"].Importo.sum()
            uscite = df[df.Tipo=="Uscita"].Importo.sum()
            vincite_tot = df[df.Tipo=="Vincita"].Importo.sum()
            fondo = entrate + uscite + vincite_tot

            testo = "🥳 *VINCITA SUPERENALOTTO!*\n\n"
            for v in vincite:
                testo += f"✅ Schedina {v[0]} → {v[1]} punti ({', '.join(map(str,v[2]))})\n"
            testo += f"\n💰 Fondo cassa attuale: {fondo:.2f} €"

            wa = urllib.parse.quote(testo)
            st.markdown(
                f'<a href="https://wa.me/?text={wa}" target="_blank" class="wa-button">📲 PASSO 4: Invia su WhatsApp</a>',
                unsafe_allow_html=True
            )
        else:
            play_audio("https://www.myinstants.com/media/sounds/sad-trombone.mp3")
            st.warning("Nessuna vincita rilevata.")

# =================================================
# 📜 STATO ABBONAMENTO
# =================================================
elif scelta == "📜 Stato Abbonamento":

    st.subheader("📜 Abbonamento (15 estrazioni)")

    fatti = st.slider(
        "Concorsi effettuati",
        0, 15,
        st.session_state.estrazioni
    )

    # anti doppia estrazione
    if fatti > st.session_state.ultima_estrazione_registrata:
        registra_movimento("Uscita", "Costo estrazione", -6)
        st.session_state.ultima_estrazione_registrata = fatti
        st.session_state.estrazioni = fatti

    st.progress(fatti / 15)

    # reset ciclo
    if fatti == 15:
        registra_movimento("Entrata", "Rinnovo abbonamento (Flavio)", 15)
        for s in soci:
            st.session_state[f"paga_{s}"] = False
        st.session_state.estrazioni = 0
        st.session_state.ultima_estrazione_registrata = 0
        st.experimental_rerun()

    st.divider()
    st.subheader("👥 Cassa Soci")

    pagati = 0
    c1, c2 = st.columns(2)
    for i, s in enumerate(soci):
        with c1 if i < 3 else c2:
            if st.checkbox(f"Pagato da {s}", key=f"paga_{s}"):
                pagati += 1

    if pagati < 6:
        st.markdown(
            f'<div class="status-red">🔴 CASSA: {pagati}/6 soci hanno pagato</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="status-green">✅ CASSA COMPLETA! RINNOVO PRONTO</div>',
            unsafe_allow_html=True
        )

# =================================================
# 💰 CALCOLO QUOTE
# =================================================
elif scelta == "💰 Calcolo Quote":

    st.subheader("💰 Calcolo Netto")
    premio = st.number_input("Premio lordo (€)", min_value=0.0, step=10.0)

    if premio > 0:
        netto = premio - ((premio - 500) * 0.20 if premio > 500 else 0)
        st.markdown(
            f'<div class="quota-box"><span class="quota-valore">{netto/6:.2f} € a testa</span></div>',
            unsafe_allow_html=True
        )

        if st.button("💾 Salva Vincita"):
            registra_movimento("Vincita", "Vincita SuperEnalotto", netto)
            st.toast("Vincita salvata nel Bottino")

# =================================================
# 🏛️ IL BOTTINO
# =================================================
elif scelta == "🏛️ Il Bottino":

    st.subheader("🏛️ Archivio Bottino")
    df = carica_bottino()

    if not df.empty:
        st.dataframe(df, use_container_width=True)

        entrate = df[df.Tipo=="Entrata"].Importo.sum()
        uscite = df[df.Tipo=="Uscita"].Importo.sum()
        vincite = df[df.Tipo=="Vincita"].Importo.sum()
        fondo = entrate + uscite + vincite

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Entrate", f"{entrate:.2f} €")
        c2.metric("Uscite", f"{uscite:.2f} €")
        c3.metric("Vincite", f"{vincite:.2f} €")
        c4.metric("Fondo Cassa", f"{fondo:.2f} €")
    else:
        st.info("Archivio vuoto.")
