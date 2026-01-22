import streamlit as st
import re
import pandas as pd
from datetime import datetime
import urllib.parse
from streamlit_extras.let_it_rain import rain 

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="Regalati un Sogno v2.2", page_icon="🍀", layout="centered")

# --- STILE CSS UNIVERSALE (Light & Dark Mode) ---
st.markdown("""
    <style>
    /* Input e Selectbox con bordi neutri ma visibili */
    .stSelectbox div[data-baseweb="select"] { border: 2px solid #4CAF50 !important; border-radius: 10px; }
    
    /* Box Risultato Vincita - Sfondo adattivo con bordo luminoso */
    .quota-box { 
        text-align: center; 
        background-color: rgba(76, 175, 80, 0.1); 
        padding: 30px; 
        border-radius: 15px; 
        border: 3px solid #4CAF50; 
        margin-top: 20px;
    }
    
    /* Colore Oro/Verde per i valori, leggibile su bianco e nero */
    .quota-titolo { font-size: 20px; font-weight: 800; color: #4CAF50; display: block; margin-bottom: 10px; }
    .quota-valore { font-size: 38px; font-weight: 900; color: #FFD700; display: block; text-shadow: 1px 1px 2px #000; }
    
    /* Bottoni ad alto contrasto */
    .wa-button { 
        display: inline-block; padding: 14px 20px; background-color: #25D366; color: white !important; 
        text-decoration: none; border-radius: 10px; width: 100%; text-align: center; font-weight: 800; font-size: 18px;
    }
    .ams-button { 
        display: inline-block; padding: 12px 20px; background-color: #2196F3; color: white !important; 
        text-decoration: none; border-radius: 10px; width: 100%; text-align: center; font-weight: bold;
    }
    
    /* Stati Cassa Adattivi */
    .status-red { 
        background-color: rgba(255, 82, 82, 0.2); color: #FF5252; 
        padding: 12px; border-radius: 10px; text-align: center; font-weight: 900; border: 2px solid #FF5252; 
    }
    .status-green { 
        background-color: rgba(76, 175, 80, 0.2); color: #4CAF50; 
        padding: 12px; border-radius: 10px; text-align: center; font-weight: 900; border: 2px solid #4CAF50; 
    }
    
    /* Forza visibilità etichette slider e checkbox */
    label p { font-size: 18px !important; font-weight: 700 !important; }
    </style>
    """, unsafe_allow_html=True)

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

def db_load():
    try: return pd.read_csv('archivio_vincite.csv')
    except: return pd.DataFrame(columns=['Data', 'Punti', 'Euro_Netto'])

# --- GESTIONE STATO ---
if 'n0' not in st.session_state:
    for i in range(6): st.session_state[f'n{i}'] = 1

# --- INTERFACCIA ---
st.title("🍀 Regalati un Sogno")
menu = ["🔍 Verifica Vincita", "📅 Abbonamento", "💰 Calcolo Quote", "🏛️ Il Bottino"]
scelta = st.selectbox("🧭 NAVIGAZIONE", menu)
st.divider()

if scelta == "🔍 Verifica Vincita":
    st.markdown('<a href="https://www.adm.gov.it/portale/monopoli/giochi/giochi_num_total/superenalotto" target="_blank" class="ams-button">➡️ APRI SITO UFFICIALE AMS</a>', unsafe_allow_html=True)
    
    txt = st.text_input("1. Incolla numeri:", placeholder="Es. 3 10 17 40 85 86")
    if st.button("Carica Numeri ⤵️"):
        nums = [int(n) for n in re.findall(r'\d+', txt) if 1 <= int(n) <= 90]
        if len(nums) >= 6:
            for i in range(6): st.session_state[f"n{i}"] = nums[i]
            st.rerun()
        else: st.error("Inserisci almeno 6 numeri validi.")

    with st.expander("👁️ Modifica Manuale", expanded=False):
        c = st.columns(6)
        for i in range(6):
            st.session_state[f"n{i}"] = c[i].number_input(f"{i+1}°", 1, 90, key=f"f{i}", value=st.session_state[f"n{i}"])

    if st.button("VERIFICA ORA 🚀", type="primary", use_container_width=True):
        estratti = [st.session_state[f"n{i}"] for i in range(6)]
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
            st.markdown(f'<a href="https://wa.me/?text={urllib.parse.quote(msg)}" target="_blank" class="wa-button">📲 CONDIVIDI SU WHATSAPP</a>', unsafe_allow_html=True)
        else:
            st.info("Nessuna vincita rilevata.")

elif scelta == "📅 Abbonamento":
    st.subheader("📊 Stato Giocate")
    fatti = st.slider("Concorsi completati", 0, 15, 0)
    rimanenti = 15 - fatti
    st.progress(fatti / 15)
    if rimanenti <= 5: st.warning(f"⚠️ Mancano {rimanenti} estrazioni!")
    else: st.success(f"Tutto regolare: -{rimanenti}")
    
    st.divider()
    st.subheader("👥 Cassa Rinnovo")
    soci = ["VS", "MM", "ED", "AP", "GGC", "AM"]
    pagati = 0
    c1, c2 = st.columns(2)
    for i, s in enumerate(soci):
        col = c1 if i < 3 else c2
        if col.checkbox(f"Quota {s}", key=f"p_{s}"): pagati += 1
    
    if pagati == 6: st.markdown('<div class="status-green">✅ CASSA COMPLETA</div>', unsafe_allow_html=True)
    else: st.markdown(f'<div class="status-red">⏳ MANCANO {6-pagati} QUOTE</div>', unsafe_allow_html=True)

elif scelta == "💰 Calcolo Quote":
    st.subheader("💰 Calcolo Ripartizione")
    lordo = st.number_input("Premio Lordo (€)", min_value=0.0, format="%.2f", step=100.0)
    if lordo > 0:
        netto = lordo - ((lordo-500)*0.20 if lordo > 500 else 0)
        st.markdown(f"""
            <div class="quota-box">
                <span class="quota-titolo">VINCITA PER SOCIO (NETTA):</span>
                <span class="quota-valore">{format_it(netto/6)} €</span>
                <hr style="border: 1px solid #4CAF50;">
                <span style="font-weight: bold;">Totale Netto Gruppo: {format_it(netto)} €</span>
            </div>
        """, unsafe_allow_html=True)
        if st.button("💾 REGISTRA NEL BOTTINO"):
            db_save("Vincita", netto)
            st.toast("Salvato!")

elif scelta == "🏛️ Il Bottino":
    st.subheader("📜 Storico Vincite")
    df = db_load()
    if not df.empty:
        df_view = df.copy()
        df_view['Euro_Netto'] = df_view['Euro_Netto'].apply(format_it)
        st.table(df_view)
        st.metric("TOTALE ACCUMULATO", f"{format_it(df['Euro_Netto'].sum())} €")
    else:
        st.info("L'archivio è vuoto.")
