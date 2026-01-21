import streamlit as st
import re
import pandas as pd
from datetime import datetime
import plotly.express as px # Per i grafici

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
    div[data-testid="stNumberInput"] input { font-size: 20px !important; font-weight: bold !important; }
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
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return pd.DataFrame(columns=['Data', 'Punti', 'Euro_Netto'])

def salva_vincita(punti, netto):
    nuovo = pd.DataFrame([{'Data': datetime.now().strftime("%d/%m/%Y"), 'Punti': punti, 'Euro_Netto': netto}])
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

    st.text_input("Inserisci sequenza estratti:", key="incolla_qui", on_change=distribuisci_numeri, placeholder="Es: 3-10-17-40-85-86")
    
    with st.expander("Modifica numeri manualmente"):
        c = st.columns(6)
        for i in range(6): 
            st.session_state[f"n{i}"] = c[i].number_input(f"{i+1}°", 1, 90, key=f"input_n{i}", value=st.session_state.get(f"n{i}", 1))

    if st.button("VERIFICA ORA 🚀", type="primary", use_container_width=True):
        estratti = [st.session_state[f"n{i}"] for i in range(6)]
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
            st.markdown(f'<a href="https://wa.me/?text={msg_wa}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:12px; border-radius:8px; cursor:pointer; font-weight:bold;">📲 Avvisa il gruppo</button></a>', unsafe_allow_html=True)
        else:
            play_audio("https://www.myinstants.com/media/sounds/sad-trombone.mp3")
            st.warning("Nessuna vincita questa volta.")

# --- TAB 2: CASSA SOCI (NOVITÀ) ---
with tab2:
    st.subheader("👥 Stato Pagamenti Giocata")
    st.info("Segna chi ha già versato la quota per la prossima estrazione.")
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
    st.subheader("💰 Calcolo e Risparmio")
    lordo = st.number_input("Vincita Lorda Totale (€)", min_value=0.0, step=10.0)
    if lordo > 0:
        netto = lordo - ((lordo-500)*0.2 if lordo > 500 else 0)
        quota = round(netto/6, 2)
        st.markdown(f'<div class="quota-box"><span class="quota-valore">{quota:,.2f} €</span><br>Netto a testa</div>', unsafe_allow_html=True)
        
        punti_vinti = st.selectbox("Quanti punti sono stati fatti?", [2, 3, 4, 5, "5+1", 6])
        if st.button("💾 Registra nel Bottino"):
            salva_vincita(str(punti_vinti), netto)
            st.toast("Vincita registrata!")

# --- TAB 4: DASHBOARD (NOVITÀ) ---
with tab4:
    st.subheader("🏛️ Analisi del Bottino")
    df = carica_archivio()
    
    if not df.empty:
        # Metriche principali
        tot_netto = df['Euro_Netto'].sum()
        c1, c2 = st.columns(2)
        c1.metric("Totale Vinto (Netto)", f"{tot_netto:,.2f} €")
        c2.metric("Numero Vincite", len(df))
        
        # Grafico delle vincite nel tempo
        st.write("📈 Andamento Vincite")
        fig = px.bar(df, x='Data', y='Euro_Netto', color='Punti', title="Vincite nel Tempo",
                     labels={'Euro_Netto': 'Euro (€)', 'Data': 'Giorno'})
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabella Storica
        with st.expander("Vedi i dettagli storici"):
            st.dataframe(df.sort_values(by='Data', ascending=False), use_container_width=True)
            
        if st.button("🗑️ Reset Storico"):
            import os
            if os.path.exists('archivio_vincite.csv'): os.remove('archivio_vincite.csv')
            st.rerun()
    else:
        st.info("Nessun dato presente nel bottino. Cominciamo a vincere!")import streamlit as st
import re
import pandas as pd
from datetime import datetime
import urllib.parse

# 1. IMPOSTAZIONI PAGINA
st.set_page_config(page_title="Regalati un Sogno", page_icon="🍀", layout="centered")

# 2. STILE CSS
st.markdown("""
    <style>
    div[data-testid="stNumberInput"] input { 
        font-size: 22px !important; text-align: center !important; font-weight: 900 !important; 
        color: #000000 !important; background-color: #ffffff !important; 
        border: 2px solid #cccccc !important; border-radius: 5px;
    }
    .main { background-color: #f9fafb; }
    .quota-box {
        text-align: center; background-color: #e8f5e9; padding: 25px;
        border-radius: 12px; border: 2px solid #c8e6c9; margin-top: 15px;
    }
    .quota-valore { font-size: 36px; font-weight: 800; color: #1b5e20; display: block; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNZIONI AUDIO ---
def play_audio(url):
    audio_html = f'<audio autoplay="true" style="display:none;"><source src="{url}" type="audio/mpeg"></audio>'
    st.components.v1.html(audio_html, height=0)

# --- FUNZIONE ARCHIVIO (CSV locale) ---
def salva_vincita(punti, importo_netto):
    nuovo_dato = {
        'Data': datetime.now().strftime("%d/%m/%Y %H:%M"),
        'Punti': punti,
        'Euro_Netto': importo_netto
    }
    try:
        df = pd.read_csv('archivio_vincite.csv')
        df = pd.concat([df, pd.DataFrame([nuovo_dato])], ignore_index=True)
    except FileNotFoundError:
        df = pd.DataFrame([nuovo_dato])
    df.to_csv('archivio_vincite.csv', index=False)

def carica_archivio():
    try:
        return pd.read_csv('archivio_vincite.csv')
    except FileNotFoundError:
        return pd.DataFrame(columns=['Data', 'Punti', 'Euro_Netto'])

# --- INTERFACCIA ---
st.title("🍀 Regalati un Sogno")
tab1, tab2, tab3, tab4 = st.tabs(["🔍 Verifica", "📜 Schedine", "💰 Calcolo", "🏛️ Il Bottino"])

with tab1:
    st.subheader("📋 Incolla e Verifica")
    # Logica di distribuzione numeri (già esistente)
    def distribuisci_numeri():
        if st.session_state.incolla_qui:
            numeri = re.findall(r'\d+', st.session_state.incolla_qui)
            if len(numeri) >= 6:
                for i in range(6): st.session_state[f"n{i}"] = int(numeri[i])

    st.text_input("Sequenza (spazio o trattino):", key="incolla_qui", on_change=distribuisci_numeri)
    
    with st.expander("👁️ Numeri rilevati", expanded=False):
        c1, c2, c3 = st.columns(3); c4, c5, c6 = st.columns(3)
        n0 = c1.number_input("1°", 1, 90, key="n0"); n1 = c2.number_input("2°", 1, 90, key="n1")
        n2 = c3.number_input("3°", 1, 90, key="n2"); n3 = c4.number_input("4°", 1, 90, key="n3")
        n4 = c5.number_input("5°", 1, 90, key="n4"); n5 = c6.number_input("6°", 1, 90, key="n5")

    if st.button("VERIFICA ORA 🚀", type="primary", use_container_width=True):
        final_nums = [n0, n1, n2, n3, n4, n5]
        if all(final_nums):
            set_estratti = set(final_nums)
            SCHEDINE = [{3, 10, 17, 40, 85, 86}, {10, 17, 19, 40, 85, 86}, {17, 19, 40, 75, 85, 86}, {3, 19, 40, 75, 85, 86}, {3, 10, 19, 75, 85, 86}, {3, 10, 17, 75, 85, 86}]
            vincite = []
            for i, sch in enumerate(SCHEDINE, 1):
                indovinati = sorted(list(sch.intersection(set_estratti)))
                if len(indovinati) >= 2: vincite.append((i, len(indovinati), indovinati))
            
            if vincite:
                st.balloons()
                play_audio("https://www.myinstants.com/media/sounds/ta-da.mp3")
                msg_wa = "🥳 *VINCITA SUPERENALOTTO!*%0A"
                for v in vincite:
                    st.success(f"🔥 **SCHEDINA {v[0]}:** {v[1]} PUNTI! ({v[2]})")
                    msg_wa += f"• Schedina {v[0]}: {v[1]} Punti ({v[2]})%0A"
                
                # Tasto rapido WhatsApp
                st.markdown(f'''<a href="https://wa.me/?text={msg_wa}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer; font-weight:bold;">📲 Avvisa il gruppo su WhatsApp</button></a>''', unsafe_allow_html=True)
            else:
                play_audio("https://www.myinstants.com/media/sounds/sad-trombone.mp3")
                st.warning("Nessuna vincita. Ritenta!")

with tab3:
    st.subheader("💰 Calcolo Netto e Archiviazione")
    premio_lordo = st.number_input("Importo vinto lordo (€)", min_value=0.0, step=10.0)
    if premio_lordo > 0:
        netto_tot = premio_lordo - ((premio_lordo - 500) * 0.20 if premio_lordo > 500 else 0)
        quota = round(netto_tot / 6, 2)
        
        st.markdown(f'<div class="quota-box"><span class="quota-valore">{quota} € a testa</span></div>', unsafe_allow_html=True)
        
        if st.button("💾 Salva nel Bottino"):
            salva_vincita("Vedi Dettaglio", netto_tot)
            st.toast("Vincita salvata nell'archivio!", icon="✅")

with tab4:
    st.subheader("🏛️ Il Bottino Storico")
    df_storico = carica_archivio()
    if not df_storico.empty:
        st.dataframe(df_storico, use_container_width=True)
        totale_vinto = df_storico['Euro_Netto'].sum()
        st.metric("Totale Netto Accumulato", f"{totale_vinto:,.2f} €".replace(",", "."))
        if st.button("Svuota Archivio (⚠️ Azione Irreversibile)"):
            import os
            if os.path.exists("archivio_vincite.csv"):
                os.remove("archivio_vincite.csv")
                st.rerun()
    else:
        st.info("L'archivio è ancora vuoto. Inizia a vincere!")

with tab2:
    # (Visualizzazione schedine fisse)
    st.write("Sestine registrate...")
    for i, s in enumerate(["03-10-17-40-85-86", "10-17-19-40-85-86", "17-19-40-75-85-86", "03-19-40-75-85-86", "03-10-19-75-85-86", "03-10-17-75-85-86"], 1):
        st.text(f"Schedina {i}: {s}")
