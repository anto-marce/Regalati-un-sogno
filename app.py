import streamlit as st
import re
import pandas as pd
from datetime import datetime
import plotly.express as px

# 1. IMPOSTAZIONI PAGINA
st.set_page_config(page_title="Regalati un Sogno", page_icon="🍀", layout="centered")

# 2. STILE CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton button { width: 100%; border-radius: 8px; height: 3em; font-weight: bold; }
    .quota-box {
        text-align: center; background-color: #e8f5e9; padding: 25px;
        border-radius: 12px; border: 2px solid #c8e6c9; margin-top: 15px;
    }
    .quota-valore { font-size: 34px; font-weight: 800; color: #1b5e20; }
    .status-red { background-color: #f8d7da; color: #721c24; padding: 15px; border-radius: 10px; border: 1px solid #f5c6cb; text-align: center; font-weight: bold; margin-bottom: 10px; }
    .status-green { background-color: #d4edda; color: #155724; padding: 15px; border-radius: 10px; border: 1px solid #c3e6cb; text-align: center; font-weight: bold; margin-bottom: 10px; }
    .status-blue { background-color: #cce5ff; color: #004085; padding: 15px; border-radius: 10px; border: 1px solid #b8daff; text-align: center; font-weight: bold; margin-bottom: 10px; }
    div[data-testid="stNumberInput"] input { font-size: 20px !important; font-weight: bold !important; color: #000000 !important; background-color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- INIZIALIZZAZIONE STATO ---
if 'n0' not in st.session_state:
    for i in range(6): st.session_state[f'n{i}'] = 1

# --- FUNZIONI ---
def play_audio(url):
    st.components.v1.html(f'<audio autoplay="true" style="display:none;"><source src="{url}" type="audio/mpeg"></audio>', height=0)

def carica_archivio():
    try: return pd.read_csv('archivio_vincite.csv')
    except: return pd.DataFrame(columns=['Data', 'Punti', 'Euro_Netto'])

# --- SIDEBAR MENU ---
with st.sidebar:
    st.title("🍀 Menù")
    scelta = st.radio("Naviga:", ["🔍 Verifica Vincite", "📅 Stato Abbonamento", "💰 Calcolo Netto", "🏛️ Dashboard Bottino"])
    st.divider()
    st.info("Inizio: 22 Gen 2026")

st.title("🍀 Regalati un Sogno")

# --- LOGICA NAVIGAZIONE ---
if scelta == "🔍 Verifica Vincite":
    st.subheader("📋 Verifica Estrazione")
    
    # Campo di input per incollare
    incolla = st.text_input("Incolla gli estratti qui (separati da spazio o trattino) e premi INVIO:", key="txt_incolla")
    
    # Se l'utente incolla qualcosa, aggiorniamo lo stato
    if incolla:
        numeri_trovati = re.findall(r'\d+', incolla)
        if len(numeri_trovati) >= 6:
            for i in range(6):
                st.session_state[f'n{i}'] = int(numeri_trovati[i])
            st.success("✅ Numeri aggiornati nelle celle!")

    # Celle di verifica
    st.write("Numeri nelle celle per la verifica:")
    cols = st.columns(6)
    numeri_finali = []
    for i in range(6):
        # Il valore del number_input è legato alla chiave n0, n1, ecc. nello state
        val = cols[i].number_input(f"{i+1}°", 1, 90, key=f"n{i}")
        numeri_finali.append(val)

    if st.button("VERIFICA ORA 🚀", type="primary", use_container_width=True):
        SCHEDINE = [{3,10,17,40,85,86}, {10,17,19,40,85,86}, {17,19,40,75,85,86}, {3,19,40,75,85,86}, {3,10,19,75,85,86}, {3,10,17,75,85,86}]
        vincite = []
        set_estratti = set(numeri_finali)
        
        for idx, sch in enumerate(SCHEDINE, 1):
            presi = sorted(list(sch.intersection(set_estratti)))
            if len(presi) >= 2: vincite.append((idx, len(presi), presi))
        
        if vincite:
            st.balloons(); play_audio("https://www.myinstants.com/media/sounds/ta-da.mp3")
            for v in vincite: st.success(f"🔥 Schedina {v[0]}: {v[1]} Punti! ({v[2]})")
            msg_wa = f"🥳 Abbiamo vinto! Punti: " + ", ".join([str(v[1]) for v in vincite])
            st.markdown(f'<a href="https://wa.me/?text={msg_wa}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:12px; border-radius:8px; cursor:pointer; font-weight:bold;">📲 Avvisa il gruppo su WhatsApp</button></a>', unsafe_allow_html=True)
        else:
            play_audio("https://www.myinstants.com/media/sounds/sad-trombone.mp3")
            st.warning("Nessuna vincita. Ritenta!")

elif scelta == "📅 Stato Abbonamento":
    st.subheader("📅 Gestione Abbonamento (15 Concorsi)")
    fatti = st.slider("Concorsi passati", 0, 15, value=0)
    rim = 15 - fatti
    if fatti == 0: st.markdown('<div class="status-blue">🚀 PRONTI AL VIA!</div>', unsafe_allow_html=True)
    elif rim <= 3: st.markdown(f'<div class="status-red">⚠️ RIMANENTI: {rim} / 15</div>', unsafe_allow_html=True)
    else: st.markdown(f'<div class="status-green">📅 RIMANENTI: {rim} / 15</div>', unsafe_allow_html=True)
    st.progress(fatti / 15)
    st.divider()
    st.subheader("💰 Cassa Soci")
    soci = ["VS", "MM", "ED", "AP", "GGC", "AM"]
    c1, c2 = st.columns(2)
    for i, s in enumerate(soci):
        with c1 if i < 3 else c2: st.checkbox(f"Pagato da {s}", key=f"p_{s}")
    p = sum([st.session_state.get(f"p_{s}", False) for s in soci])
    if p < 6: st.markdown(f'<div class="status-red">🔴 CASSA: {p}/6</div>', unsafe_allow_html=True)
    else: st.markdown('<div class="status-green">✅ CASSA COMPLETA!</div>', unsafe_allow_html=True)

elif scelta == "💰 Calcolo Netto":
    st.subheader("💰 Calcolo Vincita")
    l = st.number_input("Lordo Totale (€)", min_value=0.0)
    if l > 0:
        n = l - ((l-500)*0.2 if l > 500 else 0)
        st.markdown(f'<div class="quota-box"><span class="quota-valore">{round(n/6, 2):,.2f} €</span><br>A testa</div>', unsafe_allow_html=True)
        if st.button("💾 Registra"):
            nuovo = pd.DataFrame([{'Data': datetime.now().strftime("%d/%m/%Y"), 'Punti': 'Vincita', 'Euro_Netto': n}])
            try:
                df = carica_archivio()
                df = pd.concat([df, nuovo], ignore_index=True)
            except: df = nuovo
            df.to_csv('archivio_vincite.csv', index=False)
            st.success("Salvato!")

elif scelta == "🏛️ Dashboard Bottino":
    st.subheader("🏛️ Bottino Storico")
    df = carica_archivio()
    if not df.empty:
        st.metric("Totale Netto", f"{df['Euro_Netto'].sum():,.2f} €")
        st.plotly_chart(px.bar(df, x='Data', y='Euro_Netto'), use_container_width=True)
    else: st.info("Archivio vuoto.")
