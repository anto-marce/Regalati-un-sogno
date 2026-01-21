import streamlit as st
import re
import pandas as pd
from datetime import datetime
import os
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
    .ams-button {
        display: inline-block; padding: 12px 20px; background-color: #003366; color: white !important;
        text-decoration: none; border-radius: 8px; font-weight: bold; margin-bottom: 20px; 
        text-align: center; width: 100%; border: 1px solid #002244;
    }
    .wa-button {
        display: inline-block; padding: 12px 20px; background-color: #25D366; color: white !important;
        text-decoration: none; border-radius: 8px; font-weight: bold; margin-top: 10px; 
        text-align: center; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNZIONI AUDIO ---
def play_audio(url):
    audio_html = f'<audio autoplay="true" style="display:none;"><source src="{url}" type="audio/mpeg"></audio>'
    st.components.v1.html(audio_html, height=0)

# --- FUNZIONI ARCHIVIO ---
def salva_vincita(punti, importo_netto):
    nuovo_dato = {'Data': datetime.now().strftime("%d/%m/%Y %H:%M"), 'Punti': punti, 'Euro_Netto': importo_netto}
    try:
        df = pd.read_csv('archivio_vincite.csv')
        df = pd.concat([df, pd.DataFrame([nuovo_dato])], ignore_index=True)
    except FileNotFoundError:
        df = pd.DataFrame([nuovo_dato])
    df.to_csv('archivio_vincite.csv', index=False)

def carica_archivio():
    try: return pd.read_csv('archivio_vincite.csv')
    except FileNotFoundError: return pd.DataFrame(columns=['Data', 'Punti', 'Euro_Netto'])

# --- SIDEBAR ---
with st.sidebar:
    st.title("🍀 Menù")
    scelta = st.radio("Seleziona sezione:", ["🔍 Verifica Vincita", "📅 Stato Abbonamento", "💰 Calcolo Quote", "🏛️ Il Bottino"], index=0)
    st.divider()
    st.subheader("👥 Cassa Soci")
    soci = ["VS", "MM", "ED", "AP", "GGC", "AM"]
    pagati = sum([st.checkbox(f"Pagato da {s}", key=f"paga_{s}") for s in soci])
    st.progress(pagati / 6)
    if pagati == 6: st.success("Cassa Completa!")

# --- CONTENUTO PRINCIPALE ---
st.title("🍀 Regalati un Sogno")

if scelta == "🔍 Verifica Vincita":
    st.subheader("📋 Verifica Estrazione")
    
    # PASSO 1: AMS
    st.markdown('<a href="https://www.adm.gov.it/portale/monopoli/giochi/giochi_num_total/superenalotto" target="_blank" class="ams-button">➡️ PASSO 1: Controlla Estrazione su Sito AMS</a>', unsafe_allow_html=True)

    # PASSO 2: Inserimento
    if 'n0' not in st.session_state:
        for i in range(6): st.session_state[f'n{i}'] = 1

    def distribuisci_numeri():
        if st.session_state.incolla_qui:
            numeri = re.findall(r'\d+', st.session_state.incolla_qui)
            if len(numeri) >= 6:
                for i in range(6): st.session_state[f"n{i}"] = int(numeri[i])

    st.text_input("PASSO 2: Incolla sequenza e premi INVIO:", key="incolla_qui", on_change=distribuisci_numeri, placeholder="Es: 5 12 24 38 70 81")
    
    with st.expander("👁️ Numeri rilevati (Modifica se necessario)", expanded=False):
        cols = st.columns(6)
        final_nums = [cols[i].number_input(f"{i+1}°", 1, 90, key=f"n{i}") for i in range(6)]

    if st.button("VERIFICA ORA 🚀", type="primary", use_container_width=True):
        set_estratti = set(final_nums)
        SCHEDINE = [{3,10,17,40,85,86}, {10,17,19,40,85,86}, {17,19,40,75,85,86}, {3,19,40,75,85,86}, {3,10,19,75,85,86}, {3,10,17,75,85,86}]
        vincite = []
        for i, sch in enumerate(SCHEDINE, 1):
            indovinati = sorted(list(sch.intersection(set_estratti)))
            if len(indovinati) >= 2: vincite.append((i, len(indovinati), indovinati))
        
        if vincite:
            st.balloons()
            play_audio("https://www.myinstants.com/media/sounds/ta-da.mp3")
            
            testo_wa = "🥳 *VINCITA SUPERENALOTTO!*\n\n"
            for v in vincite:
                st.success(f"🔥 **SCHEDINA {v[0]}:** {v[1]} PUNTI! ({v[2]})")
                testo_wa += f"✅ Schedina {v[0]}: *{v[1]} Punti* ({', '.join(map(str, v[2]))})\n"
            
            # LINK API WHATSAPP (I dati vengono codificati solo per il browser locale)
            testo_encoded = urllib.parse.quote(testo_wa)
            st.markdown(f'<a href="https://wa.me/?text={testo_encoded}" target="_blank" class="wa-button">📲 PASSO 3: Invia Esito su WhatsApp</a>', unsafe_allow_html=True)
        else:
            play_audio("https://www.myinstants.com/media/sounds/sad-trombone.mp3")
            st.warning("Nessuna vincita rilevata.")

elif scelta == "📅 Stato Abbonamento":
    st.subheader("📅 Abbonamento")
    fatti = st.slider("Concorsi passati", 0, 15, value=0)
    st.info(f"Concorsi rimanenti: {15 - fatti} su 15")
    st.progress(fatti / 15)

elif scelta == "💰 Calcolo Quote":
    st.subheader("💰 Calcolo Netto")
    premio = st.number_input("Lordo (€)", min_value=0.0, step=10.0)
    if premio > 0:
        netto = premio - ((premio - 500) * 0.20 if premio > 500 else 0)
        st.markdown(f'<div class="quota-box"><span class="quota-valore">{round(netto/6, 2)} € a testa</span></div>', unsafe_allow_html=True)
        if st.button("💾 Salva nel Bottino"):
            salva_vincita("Vincita", netto)
            st.toast("Salvato!")

elif scelta == "🏛️ Il Bottino":
    st.subheader("🏛️ Archivio Storico")
    df = carica_archivio()
    if not df.empty:
        st.dataframe(df, use_container_width=True)
        st.metric("Totale Netto", f"{df['Euro_Netto'].sum():,.2f} €".replace(",", "."))
    else: st.info("Archivio vuoto.")
