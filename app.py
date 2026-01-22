import streamlit as st
import re
import pandas as pd
from datetime import datetime
import urllib.parse
from streamlit_extras.let_it_rain import rain 

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="Regalati un Sogno v3.0", page_icon="🍀", layout="centered")

# --- STILE CSS UNIVERSALE (Light & Dark) ---
st.markdown("""
    <style>
    .stSelectbox div[data-baseweb="select"] { border: 2px solid #4CAF50 !important; border-radius: 10px; }
    .quota-box { 
        text-align: center; background-color: rgba(76, 175, 80, 0.15); 
        padding: 30px; border-radius: 15px; border: 3px solid #4CAF50; margin-top: 20px;
    }
    .quota-titolo { font-size: 20px; font-weight: 800; color: #4CAF50; display: block; margin-bottom: 10px; }
    .quota-valore { font-size: 38px; font-weight: 900; color: #FFD700; display: block; text-shadow: 2px 2px 4px #000; }
    .wa-button { 
        display: inline-block; padding: 14px 20px; background-color: #25D366 !important; color: white !important; 
        text-decoration: none; border-radius: 10px; width: 100%; text-align: center; font-weight: 800; font-size: 18px;
    }
    .ams-button { 
        display: inline-block; padding: 12px 20px; background-color: #2196F3 !important; color: white !important; 
        text-decoration: none; border-radius: 10px; width: 100%; text-align: center; font-weight: bold;
    }
    .status-red { background-color: rgba(255, 82, 82, 0.2); color: #FF5252; padding: 12px; border-radius: 10px; text-align: center; font-weight: 900; border: 2px solid #FF5252; }
    .status-green { background-color: rgba(76, 175, 80, 0.2); color: #4CAF50; padding: 12px; border-radius: 10px; text-align: center; font-weight: 900; border: 2px solid #4CAF50; }
    </style>
    """, unsafe_allow_html=True)

# --- INIZIALIZZAZIONE ---
if 'n' not in st.session_state:
    st.session_state.n = [1, 1, 1, 1, 1, 1]

# --- FUNZIONI ---
def format_it(val):
    return f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def db_save(punti, netto):
    row = {'Data': datetime.now().strftime("%d/%m/%Y %H:%M"), 'Punti': punti, 'Euro_Netto': netto}
    try:
        df = pd.read_csv('archivio_vincite.csv')
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    except:
        df = pd.DataFrame([row])
    df.to_csv('archivio_vincite.csv', index=False)

def carica_numeri_callback():
    testo = st.session_state.txt_input
    if testo:
        numeri = [int(n) for n in re.findall(r'\d+', testo) if 1 <= int(n) <= 90]
        if len(numeri) >= 6:
            st.session_state.n = numeri[:6]
            st.toast("✅ Numeri caricati correttamente!")

# --- INTERFACCIA ---
st.title("🍀 Regalati un Sogno")
menu = ["🔍 Verifica Vincita", "📅 Abbonamento", "💰 Calcolo Quote", "🏛️ Il Bottino"]
scelta = st.selectbox("🧭 NAVIGAZIONE", menu)
st.divider()

if scelta == "🔍 Verifica Vincita":
    st.markdown('<a href="https://www.adm.gov.it/portale/monopoli/giochi/giochi_num_total/superenalotto" target="_blank" class="ams-button">➡️ APRI SITO UFFICIALE AMS</a>', unsafe_allow_html=True)
    
    # Input con callback immediato
    st.text_input("1. Incolla numeri qui:", key="txt_input", on_change=carica_numeri_callback, placeholder="Es. 3 10 17 40 85 86")
    
    st.info("💡 Dopo aver incollato, premi INVIO o clicca fuori dal campo per aggiornare le celle.")

    with st.expander("👁️ Controllo e Modifica Manuale", expanded=False):
        c = st.columns(6)
        # Aggiorniamo i singoli valori basandoci sullo stato centrale
        for i in range(6):
            st.session_state.n[i] = c[i].number_input(f"{i+1}°", 1, 90, value=st.session_state.n[i], key=f"cell_{i}")

    if st.button("VERIFICA ORA 🚀", type="primary", use_container_width=True):
        estratti = st.session_state.n
        SCHEDINE = [{3,10,17,40,85,86}, {10,17,19,40,85,86}, {17,19,40,75,85,86}, {3,19,40,75,85,86}, {3,10,19,75,85,86}, {3,10,17,75,85,86}]
        results = []
        for idx, s in enumerate(SCHEDINE, 1):
            match = sorted(list(s.intersection(set(estratti))))
            if len(match) >= 2: results.append((idx, len(match), match))
        
        if results:
            rain(emoji="💶", font_size=54, falling_speed=5, animation_length="3")
            msg = "🥳 *VINCITA SUPERENALOTTO!*\n\n"
            for r in results:
                st.success(f"🔥 Schedina {r[0]}: {r[1]} Punti! ({r[2]})")
                msg += f"✅ Sch {r[0]}: {r[1]} Pt ({r[2]})\n"
            st.markdown(f'<a href="https://wa.me/?text={urllib.parse.quote(msg)}" target="_blank" class="wa-button">📲 CONDIVIDI SU WHATSAPP</a>', unsafe_allow
            
