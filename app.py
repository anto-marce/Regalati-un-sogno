import streamlit as st
import re
import pandas as pd
from datetime import datetime
import plotly.express as px

# 1. IMPOSTAZIONI PAGINA
st.set_page_config(page_title="Regalati un Sogno", page_icon="🍀", layout="centered")

# 2. STILE CSS PERSONALIZZATO
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .quota-box {
        text-align: center; background-color: #e8f5e9; padding: 25px;
        border-radius: 12px; border: 2px solid #c8e6c9; margin-top: 15px;
    }
    .quota-valore { font-size: 34px; font-weight: 800; color: #1b5e20; }
    /* Colori invertiti per lo stato cassa */
    .cassa-alert { background-color: #f8d7da; color: #721c24; padding: 15px; border-radius: 10px; border: 1px solid #f5c6cb; text-align: center; font-weight: bold; }
    .cassa-ok { background-color: #d4edda; color: #155724; padding: 15px; border-radius: 10px; border: 1px solid #c3e6cb; text-align: center; font-weight: bold; }
    
    div[data-testid="stNumberInput"] input { 
        font-size: 20px !important; font-weight: bold !important; color: #000000 !important; background-color: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNZIONI DI SERVIZIO ---
def play_audio(url):
    st.components.v1.html(f'<audio autoplay="true" style="display:none;"><source src="{url}" type="audio/mpeg"></audio>', height=0)

def carica_archivio():
    try:
        df = pd.read_csv('archivio_vincite.csv')
        df['Data'] = pd.to_datetime(df['Data'], dayfirst=True)
        return df
    except:
        return pd.DataFrame(columns=['Data', 'Punti', 'Euro_Netto'])

# --- INTERFACCIA ---
st.title("🍀 Regalati un Sogno")
tab1, tab2, tab3, tab4 = st.tabs(["🔍 Verifica", "📅 Abbonamento & Cassa", "💰 Calcolo Netto", "🏛️ Dashboard"])

# --- TAB 1: VERIFICA ---
with tab1:
    st.subheader("📋 Verifica Estrazione")
    def distribuisci_numeri():
        if st.session_state.incolla_qui:
            numeri = re.findall(r'\d+', st.session_state.incolla_qui)
            if len(numeri) >= 6:
                for i in range(6): st.session_state[f"n{i}"] = int(numeri[i])

    st.text_input("Incolla estratti:", key="incolla_qui", on_change=distribuisci_numeri)
    
    if st.button("VERIFICA ORA 🚀", type="primary", use_container_width=True):
        # Utilizziamo i numeri correnti in session_state
        estratti = [st.session_state.get(f"n{i}", 1) for i in range(6)]
        SCHEDINE = [{3,10,17,40,85,86}, {10,17,19,40,85,86}, {17,19,40,75,85,86}, {3,19,40,75,85,86}, {3,10,19,75,85,86}, {3,10,17,75,85,86}]
        vincite = []
        for i, sch in enumerate(SCHEDINE, 1):
            presi = sorted(list(sch.intersection(set(estratti))))
            if len(presi) >= 2: vincite.append((i, len(presi), presi))
        
        if vincite:
            st.balloons()
            play_audio("https://www.myinstants.com/media/sounds/ta-da.mp3")
            for v in vincite: st.success(f"🔥 Schedina {v[0]}: {v[1]} Punti!")
        else:
            play_audio("https://www.myinstants.com/media/sounds/sad-trombone.mp3")
            st.warning("Nessuna vincita.")

# --- TAB 2: CASSA & ABBONAMENTO (MODIFICATA) ---
with tab2:
    st.subheader("👥 Gestione Abbonamento (15 Concorsi)")
    
    # Sezione Conteggio Concorsi
    col_a, col_b = st.columns([2, 1])
    concorsi_fatti = col_a.slider("Concorsi effettuati", 0, 15, key="concorsi_fatti")
    rimanenti = 15 - concorsi_fatti
    col_b.metric("Rimanenti", rimanenti)
    
    st.progress(concorsi_fatti / 15)
    if rimanenti <= 2:
        st.error(f"⚠️ Attenzione! Mancano solo {rimanenti} concorsi alla scadenza!")

    st.divider()
    st.subheader("💰 Stato Pagamenti Rinnovo")
    soci = ["Socio 1", "Socio 2", "Socio 3", "Socio 4", "Socio 5", "Socio 6"]
    
    c1, c2 = st.columns(2)
    for i, s in enumerate(soci):
        with c1 if i < 3 else c2:
            st.checkbox(s, key=f"paga_{i}")
    
    pagati = sum([st.session_state.get(f"paga_{i}", False) for i in range(6)])
    
    # Inversione Colori richiesta
    if pagati < 6:
        st.markdown(f'<div class="cassa-alert">🔴 CASSA INCOMPLETA: {pagati} / 6 paganti<br><small>Mancano {6-pagati} quote per il prossimo abbonamento</small></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="cassa-ok">✅ CASSA COMPLETA: 6 / 6 paganti<br><small>Tutte le quote sono state raccolte!</small></div>', unsafe_allow_html=True)

# --- TAB 3: CALCOLO ---
with tab3:
    st.subheader("💰 Calcolo Netto")
    lordo = st.number_input("Vincita Lorda (€)", min_value=0.0)
    if lordo > 0:
        netto = lordo - ((lordo-500)*0.2 if lordo > 500 else 0)
        st.markdown(f'<div class="quota-box"><span class="quota-valore">{round(netto/6, 2)} €</span><br>Quota netta a testa</div>', unsafe_allow_html=True)

# --- TAB 4: DASHBOARD ---
with tab4:
    df = carica_archivio()
    if not df.empty:
        st.metric("Totale Bottino", f"{df['Euro_Netto'].sum():,.2f} €")
        fig = px.bar(df, x='Data', y='Euro_Netto', color='Punti', title="Storico Vincite")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Ancora nessuna vincita registrata.")
