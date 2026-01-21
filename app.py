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
    div[data-testid="stNumberInput"] input { 
        font-size: 20px !important; 
        font-weight: bold !important; 
        color: #000000 !important; 
        background-color: #ffffff !important;
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
    except (FileNotFoundError, pd.errors.EmptyDataError, Exception):
        return pd.DataFrame(columns=['Data', 'Punti', 'Euro_Netto'])

def salva_vincita(punti, netto):
    nuovo = pd.DataFrame([{'Data': datetime.now().strftime("%d/%m/%Y"), 'Punti': str(punti), 'Euro_Netto': netto}])
    df = carica_archivio()
    df = pd.concat([df, nuovo], ignore_index=True)
    df.to_csv('archivio_vincite.csv', index=False)

# --- INTERFACCIA PRINCIPALE ---
st.title("🍀 Regalati un Sogno")
tab1, tab2, tab3, tab4 = st.tabs(["🔍 Verifica", "👥 Cassa Soci", "💰 Calcolo Netto", "🏛️ Dashboard Bottino"])

# --- TAB 1: VERIFICA ---
with tab1:
    st.subheader("📋 Incolla Risultati")
    def distribuisci_numeri():
        if st.session_state.incolla_qui:
            numeri = re.findall(r'\d+', st.session_state.incolla_qui)
            if len(numeri) >= 6:
                for i in range(6): st.session_state[f"n{i}"] = int(numeri[i])

    st.text_input("Inserisci sequenza estratti (spazio o trattino):", key="incolla_qui", on_change=distribuisci_numeri, placeholder="Es: 3-10-17-40-85-86")
    
    with st.expander("Modifica numeri manualmente", expanded=False):
        c = st.columns(6)
        n_inputs = []
        for i in range(6): 
            val_default = st.session_state.get(f"n{i}", 1)
            n_inputs.append(c[i].number_input(f"{i+1}°", 1, 90, key=f"input_n{i}", value=val_default))

    if st.button("VERIFICA ORA 🚀", type="primary", use_container_width=True):
        estratti = [st.session_state.get(f"input_n{i}", 1) for i in range(6)]
        SCHEDINE = [{3,10,17,40,85,86}, {10,17,19,40,85,86}, {17,19,40,75,85,86}, {3,19,40,75,85,86}, {3,10,19,75,85,86}, {3,10,17,75,85,86}]
        vincite = []
        for i, sch in enumerate(SCHEDINE, 1):
            presi = sorted(list(sch.intersection(set(estratti))))
            if len(presi) >= 2: vincite.append((i, len(presi), presi))
        
        if vincite:
            st.balloons()
            play_audio("https://www.myinstants.com/media/sounds/ta-da.mp3")
            for v in vincite: st.success(f"🔥 Schedina {v[0]}: **{v[1]} Punti** ({v[2]})")
            msg_wa = f"🥳 Abbiamo vinto! Punti fatti: " + ", ".join([str(v[1]) for v in vincite])
            st.markdown(f'<a href="https://wa.me/?text={msg_wa}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:12px; border-radius:8px; cursor:pointer; font-weight:bold;">📲 Avvisa il gruppo su WhatsApp</button></a>', unsafe_allow_html=True)
        else:
            play_audio("https://www.myinstants.com/media/sounds/sad-trombone.mp3")
            st.warning("Nessuna vincita questa volta.")

# --- TAB 2: CASSA SOCI ---
with tab2:
    st.subheader("👥 Stato Pagamenti Giocata")
    st.info("Segna chi ha già versato la quota per la prossima estrazione.")
    # Sostituisci questi nomi con quelli reali del tuo gruppo
    soci = ["Socio 1", "Socio 2", "Socio 3", "Socio 4", "Socio 5", "Socio 6"]
    
    col1, col2 = st.columns(2)
    for i, s in enumerate(soci):
        with col1 if i < 3 else col2:
            st.checkbox(s, key=f"paga_{i}")
    
    pagati = sum([st.session_state.get(f"paga_{i}", False) for i in range(6)])
    st.divider()
    st.metric("Soci che hanno pagato", f"{pagati} / 6")
    if pagati == 6:
        st.success("✅ Cassa completa! La giocata è coperta.")
    else:
        st.warning(f"⏳ Mancano ancora {6-pagati} quote.")

# --- TAB 3: CALCOLO ---
with tab3:
    st.subheader("💰 Calcolo Netto")
    lordo = st.number_input("Vincita Lorda Totale (€)", min_value=0.0, step=10.0)
    if lordo > 0:
        netto = lordo - ((lordo-500)*0.2 if lordo > 500 else 0)
        quota = round(netto/6, 2)
        st.markdown(f'<div class="quota-box"><span class="quota-valore">{quota:,.2f} €</span><br>Netto a testa</div>', unsafe_allow_html=True)
        
        punti_vinti = st.selectbox("Quanti punti sono stati fatti?", [2, 3, 4, 5, "5+1", 6])
        if st.button("💾 Registra nel Bottino"):
            salva_vincita(punti_vinti, netto)
            st.toast("Vincita registrata correttamente!")

# --- TAB 4: DASHBOARD ---
with tab4:
    st.subheader("🏛️ Analisi del Bottino")
    df_data = carica_archivio()
    
    if not df_data.empty:
        tot_netto = df_data['Euro_Netto'].sum()
        c1, c2 = st.columns(2)
        c1.metric("Totale Vinto (Netto)", f"{tot_netto:,.2f} €")
        c2.metric("Numero Vincite", len(df_data))
        
        st.write("📈 Andamento Vincite")
        fig = px.bar(df_data, x='Data', y='Euro_Netto', color='Punti', 
                     title="Storico Vincite",
                     labels={'Euro_Netto': 'Euro (€)', 'Data': 'Data Estrazione'})
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("Vedi tabella dettagliata"):
            st.dataframe(df_data.sort_values(by='Data', ascending=False), use_container_width=True)
            
        if st.button("🗑️ Reset Storico"):
            import os
            if os.path.exists('archivio_vincite.csv'): 
                os.remove('archivio_vincite.csv')
                st.rerun()
    else:
        st.info("Nessun dato presente nel bottino. Cominciamo a vincere!")
