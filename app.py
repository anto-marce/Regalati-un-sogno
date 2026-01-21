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
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
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

# --- INTERFACCIA ---
st.title("🍀 Regalati un Sogno")
st.subheader("Inizio Abbonamento: 22 Gennaio 2026")

tab1, tab2, tab3, tab4 = st.tabs(["🔍 Verifica", "📅 Abbonamento & Cassa", "💰 Calcolo Netto", "🏛️ Dashboard"])

# --- TAB 1: VERIFICA ---
with tab1:
    st.info("🎯 Prossima estrazione: Giovedì 22 Gennaio")
    def distribuisci_numeri():
        if st.session_state.incolla_qui:
            nums = re.findall(r'\d+', st.session_state.incolla_qui)
            if len(nums) >= 6:
                for i in range(6): st.session_state[f"n{i}"] = int(nums[i])
    st.text_input("Incolla estratti:", key="incolla_qui", on_change=distribuisci_numeri)
    
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

# --- TAB 2: CASSA & ABBONAMENTO ---
with tab2:
    st.subheader("📅 Stato Abbonamento (15 Concorsi)")
    conc_fatti = st.slider("Concorsi già passati", 0, 15, key="conc_fatti", value=0)
    rimanenti = 15 - conc_fatti
    
    if conc_fatti == 0:
        st.markdown(f'<div class="status-blue">🚀 PRONTI AL VIA!<br><small>Tutti i 15 concorsi sono ancora disponibili</small></div>', unsafe_allow_html=True)
    elif rimanenti <= 3:
        st.markdown(f'<div class="status-red">⚠️ RIMANENTI: {rimanenti} / 15<br><small>Abbonamento quasi terminato!</small></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="status-green">📅 RIMANENTI: {rimanenti} / 15<br><small>Abbonamento in corso</small></div>', unsafe_allow_html=True)
    
    st.progress(conc_fatti / 15)

    st.divider()
    st.subheader("💰 Cassa Rinnovo (VS, MM, ED, AP, GGC, AM)")
    soci = ["VS", "MM", "ED", "AP", "GGC", "AM"]
    c1, c2 = st.columns(2)
    for i, s in enumerate(soci):
        with c1 if i < 3 else c2: st.checkbox(f"Pagato da {s}", key=f"paga_{i}")
    
    pagati = sum([st.session_state.get(f"paga_{i}", False) for i in range(6)])
    if pagati < 6:
        st.markdown(f'<div class="status-red">🔴 CASSA: {pagati}/6 SOCI<br><small>Mancano {6-pagati} quote</small></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="status-green">✅ CASSA COMPLETA!<br><small>Tutto pronto per il prossimo rinnovo</small></div>', unsafe_allow_html=True)

# --- TAB 3 & 4 (Calcolo e Dashboard rimangono invariati) ---
with tab3:
    st.subheader("💰 Calcolo Netto")
    lordo = st.number_input("Vincita Lorda (€)", min_value=0.0)
    if lordo > 0:
        netto = lordo - ((lordo-500)*0.2 if lordo > 500 else 0)
        st.markdown(f'<div class="quota-box"><span class="quota-valore">{round(netto/6, 2):,.2f} €</span><br>Netto a testa</div>', unsafe_allow_html=True)
        if st.button("💾 Registra nel Bottino"):
            # Funzione salva_vincita semplificata qui per brevità
            nuovo = pd.DataFrame([{'Data': datetime.now().strftime("%d/%m/%Y"), 'Punti': 'Vincita', 'Euro_Netto': netto}])
            try:
                df = pd.read_csv('archivio_vincite.csv')
                df = pd.concat([df, nuovo], ignore_index=True)
            except: df = nuovo
            df.to_csv('archivio_vincite.csv', index=False)
            st.toast("Registrato!")

with tab4:
    df = carica_archivio()
    if not df.empty:
        st.metric("Totale Bottino", f"{df['Euro_Netto'].sum():,.2f} €")
        st.plotly_chart(px.bar(df, x='Data', y='Euro_Netto', title="Storico"), use_container_width=True)
    else: st.info("Ancora nessuna vincita.")
