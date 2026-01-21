import streamlit as st
import re
import pandas as pd
from datetime import datetime
import plotly.express as px

# 1. IMPOSTAZIONI PAGINA
st.set_page_config(page_title="Regalati un Sogno", page_icon="🍀", layout="centered")

# 2. STILE CSS PER IL MENU TOGGLE E BOX
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    /* Stile per i pulsanti del menu */
    .stButton button { width: 100%; border-radius: 8px; height: 3em; font-weight: bold; }
    .quota-box {
        text-align: center; background-color: #e8f5e9; padding: 25px;
        border-radius: 12px; border: 2px solid #c8e6c9; margin-top: 15px;
    }
    .quota-valore { font-size: 34px; font-weight: 800; color: #1b5e20; }
    .status-red { background-color: #f8d7da; color: #721c24; padding: 15px; border-radius: 10px; border: 1px solid #f5c6cb; text-align: center; font-weight: bold; margin-bottom: 10px; }
    .status-green { background-color: #d4edda; color: #155724; padding: 15px; border-radius: 10px; border: 1px solid #c3e6cb; text-align: center; font-weight: bold; margin-bottom: 10px; }
    .status-blue { background-color: #cce5ff; color: #004085; padding: 15px; border-radius: 10px; border: 1px solid #b8daff; text-align: center; font-weight: bold; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNZIONI ---
def play_audio(url):
    st.components.v1.html(f'<audio autoplay="true" style="display:none;"><source src="{url}" type="audio/mpeg"></audio>', height=0)

def carica_archivio():
    try:
        df = pd.read_csv('archivio_vincite.csv')
        df['Data'] = pd.to_datetime(df['Data'], dayfirst=True)
        return df
    except: return pd.DataFrame(columns=['Data', 'Punti', 'Euro_Netto'])

# --- SIDEBAR MENU (TOGGLE) ---
with st.sidebar:
    st.title("🍀 Menù")
    # Utilizziamo un radio button con stile a pulsante (disponibile in alcune versioni) 
    # o un semplice selectbox/radio per la navigazione
    scelta = st.radio(
        "Naviga tra le sezioni:",
        ["🔍 Verifica Vincite", "📅 Stato Abbonamento", "💰 Calcolo Netto", "🏛️ Dashboard Bottino"],
        index=0
    )
    st.divider()
    st.info("Inizio: 22 Gen 2026")

# --- TITOLO PRINCIPALE ---
st.title("🍀 Regalati un Sogno")

# --- LOGICA NAVIGAZIONE (Invece dei Tab) ---

if scelta == "🔍 Verifica Vincite":
    st.subheader("📋 Verifica Estrazione")
    st.info("🎯 Prossima estrazione: Giovedì 22 Gennaio")
    
    def distribuisci_numeri():
        if st.session_state.incolla_qui:
            nums = re.findall(r'\d+', st.session_state.incolla_qui)
            if len(nums) >= 6:
                for i in range(6): st.session_state[f"n{i}"] = int(nums[i])
                
    st.text_input("Incolla gli estratti qui:", key="incolla_qui", on_change=distribuisci_numeri)
    
    if st.button("VERIFICA ORA 🚀", type="primary", use_container_width=True):
        estratti = [st.session_state.get(f"n{i}", 1) for i in range(6)]
        SCHEDINE = [{3,10,17,40,85,86}, {10,17,19,40,85,86}, {17,19,40,75,85,86}, {3,19,40,75,85,86}, {3,10,19,75,85,86}, {3,10,17,75,85,86}]
        vincite = []
        for i, sch in enumerate(SCHEDINE, 1):
            presi = sorted(list(sch.intersection(set(estratti))))
            if len(presi) >= 2: vincite.append((i, len(presi), presi))
        
        if vincite:
            st.balloons(); play_audio("https://www.myinstants.com/media/sounds/ta-da.mp3")
            for v in vincite: st.success(f"🔥 Schedina {v[0]}: {v[1]} Punti!")
        else:
            play_audio("https://www.myinstants.com/media/sounds/sad-trombone.mp3")
            st.warning("Nessuna vincita.")

elif scelta == "📅 Stato Abbonamento":
    st.subheader("📅 Gestione Abbonamento (15 Concorsi)")
    
    conc_fatti = st.slider("Concorsi già passati", 0, 15, key="conc_fatti", value=0)
    rimanenti = 15 - conc_fatti
    
    if conc_fatti == 0:
        st.markdown(f'<div class="status-blue">🚀 PRONTI AL VIA!<br>L\'abbonamento inizia domani 22 Gennaio</div>', unsafe_allow_html=True)
    elif rimanenti <= 3:
        st.markdown(f'<div class="status-red">⚠️ RIMANENTI: {rimanenti} / 15<br>PREPARARE RINNOVO</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="status-green">📅 RIMANENTI: {rimanenti} / 15<br>ABBONAMENTO REGOLARE</div>', unsafe_allow_html=True)
    
    st.progress(conc_fatti / 15)

    st.divider()
    st.subheader("💰 Cassa Soci (VS, MM, ED, AP, GGC, AM)")
    soci = ["VS", "MM", "ED", "AP", "GGC", "AM"]
    c1, c2 = st.columns(2)
    for i, s in enumerate(soci):
        with c1 if i < 3 else c2: st.checkbox(f"Pagato da {s}", key=f"paga_{i}")
    
    pagati = sum([st.session_state.get(f"paga_{i}", False) for i in range(6)])
    if pagati < 6:
        st.markdown(f'<div class="status-red">🔴 CASSA: {pagati}/6 SOCI</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="status-green">✅ CASSA COMPLETA!</div>', unsafe_allow_html=True)

elif scelta == "💰 Calcolo Netto":
    st.subheader("💰 Calcolo Vincita")
    lordo = st.number_input("Vincita Lorda Totale (€)", min_value=0.0)
    if lordo > 0:
        netto = lordo - ((lordo-500)*0.2 if lordo > 500 else 0)
        st.markdown(f'<div class="quota-box"><span class="quota-valore">{round(netto/6, 2):,.2f} €</span><br>Netto a testa</div>', unsafe_allow_html=True)
        
        if st.button("💾 Registra nel Bottino"):
            nuovo = pd.DataFrame([{'Data': datetime.now().strftime("%d/%m/%Y"), 'Punti': 'Vincita', 'Euro_Netto': netto}])
            try:
                df = pd.read_csv('archivio_vincite.csv')
                df = pd.concat([df, nuovo], ignore_index=True)
            except: df = nuovo
            df.to_csv('archivio_vincite.csv', index=False)
            st.success("Dati salvati in Dashboard!")

elif scelta == "🏛️ Dashboard Bottino":
    st.subheader("🏛️ Il Bottino Storico")
    df = carica_archivio()
    if not df.empty:
        st.metric("Totale Bottino Netto", f"{df['Euro_Netto'].sum():,.2f} €")
        st.plotly_chart(px.bar(df, x='Data', y='Euro_Netto', title="Vincite nel tempo"), use_container_width=True)
        with st.expander("Vedi dettagli"):
            st.write(df)
    else:
        st.info("L'archivio è vuoto. Registra le vincite nella sezione 'Calcolo Netto'.")
