import streamlit as st
import re
import pandas as pd
from datetime import datetime
import urllib.parse
from streamlit_extras.let_it_rain import rain 

# 1. IMPOSTAZIONI PAGINA
st.set_page_config(page_title="Regalati un Sogno", page_icon="🍀", layout="centered")

# 2. STILE CSS
st.markdown("""
    <style>
    .stSelectbox div[data-baseweb="select"] { border: 2px solid #003366 !important; border-radius: 10px; }
    div[data-testid="stNumberInput"] input { 
        font-size: 24px !important; text-align: center !important; font-weight: 900 !important; 
        color: #000000 !important; border: 2px solid #cccccc !important;
    }
    .quota-box { 
        text-align: center; background-color: #e8f5e9; padding: 30px; 
        border-radius: 15px; border: 3px solid #1b5e20; margin-top: 20px;
    }
    .quota-titolo { font-size: 18px; color: #1b5e20; font-weight: bold; display: block; }
    .quota-valore { font-size: 32px; font-weight: 900; color: #1b5e20; display: block; }
    .ams-button { display: inline-block; padding: 12px 20px; background-color: #003366; color: white !important; text-decoration: none; border-radius: 8px; width: 100%; text-align: center; }
    .wa-button { display: inline-block; padding: 12px 20px; background-color: #25D366; color: white !important; text-decoration: none; border-radius: 8px; width: 100%; text-align: center; }
    .status-red { background-color: #f8d7da; color: #721c24; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; }
    .status-green { background-color: #d4edda; color: #155724; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNZIONI ---
def format_euro(val):
    return f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def salva_vincita(punti, netto):
    d = {'Data': datetime.now().strftime("%d/%m/%Y %H:%M"), 'Punti': punti, 'Euro_Netto': netto}
    try:
        df = pd.read_csv('archivio_vincite.csv')
        df = pd.concat([df, pd.DataFrame([d])], ignore_index=True)
    except:
        df = pd.DataFrame([d])
    df.to_csv('archivio_vincite.csv', index=False)

def carica_archivio():
    try: return pd.read_csv('archivio_vincite.csv')
    except: return pd.DataFrame(columns=['Data', 'Punti', 'Euro_Netto'])

# --- APP ---
st.title("🍀 Regalati un Sogno")
scelta = st.selectbox("🧭 MENU", ["Verifica Vincita", "Abbonamento", "Calcolo Quote", "Bottino"])
st.divider()

if scelta == "Verifica Vincita":
    st.subheader("📋 Verifica Estrazione")
    st.markdown('<a href="https://www.adm.gov.it/portale/monopoli/giochi/giochi_num_total/superenalotto" target="_blank" class="ams-button">➡️ SITO UFFICIALE AMS</a>', unsafe_allow_html=True)
    
    if 'n0' not in st.session_state:
        for i in range(6): st.session_state[f'n{i}'] = 1

    txt = st.text_input("Incolla qui i numeri estratti:")
    if st.button("Carica Numeri ⤵️"):
        nums = [int(n) for n in re.findall(r'\d+', txt) if 1 <= int(n) <= 90]
        if len(nums) >= 6:
            for i in range(6): st.session_state[f"n{i}"] = nums[i]
            st.rerun()

    with st.expander("👁️ Modifica manuale", expanded=False):
        c = st.columns(6)
        for i in range(6):
            st.session_state[f"n{i}"] = c[i].number_input(f"{i+1}°", 1, 90, key=f"key_n{i}", value=st.session_state[f"n{i}"])

    if st.button("VERIFICA ORA 🚀", type="primary", use_container_width=True):
        estratti = [st.session_state[f"n{i}"] for i in range(6)]
        SCHEDINE = [{3,10,17,40,85,86}, {10,17,19,40,85,86}, {17,19,40,75,85,86}, {3,19,40,75,85,86}, {3,10,19,75,85,86}, {3,10,17,75,85,86}]
        vincite = []
        for i, sch in enumerate(SCHEDINE, 1):
            presi = sorted(list(sch.intersection(set(estratti))))
            if len(presi) >= 2: vincite.append((i, len(presi), presi))
        
        if vincite:
            rain(emoji="💶", font_size=54, falling_speed=5, animation_length="3")
            msg = "🥳 *VINCITA SUPERENALOTTO!*\n\n"
            for v in vincite:
                st.success(f"🔥 Schedina {v[0]}: {v[1]} Punti! ({v[2]})")
                msg += f"✅ Sch {v[0]}: {v[1]} Pt ({v[2]})\n"
            st.markdown(f'<a href="https://wa.me/?text={urllib.parse.quote(msg)}" target="_blank" class="wa-button">📲 WhatsApp</a>', unsafe_allow_html=True)
        else:
            st.info("Nessuna vincita.")

elif scelta == "Abbonamento":
    st.subheader("📅 Stato Abbonamento")
    fatti = st.slider("Concorsi fatti", 0, 15, 0)
    st.progress(fatti / 15)
    st.write(f"Rimanenti: {15-fatti}")
    st.divider()
    st.subheader("👥 Cassa Soci")
    soci = ["VS", "MM", "ED", "AP", "GGC", "AM"]
    pagati = 0
    c1, c2 = st.columns(2)
    for i, s in enumerate(soci):
        t = c1 if i < 3 else c2
        if t.checkbox(f"Socio {s}", key=f"p_{s}"): pagati += 1
    if pagati == 6: st.markdown('<div class="status-green">COMPLETA</div>', unsafe_allow_html=True)
    else: st.markdown(f'<div class="status-red">MANCANO {6-pagati} QUOTE</div>', unsafe_allow_html=True)

elif scelta == "Calcolo Quote":
    st.subheader("💰 Calcolo Netto")
    lordo = st.number_input("Premio Lordo (€)", min_value=0.0, format="%.2f")
    if lordo > 0:
        netto = lordo - ((lordo-500)*0.20 if lordo > 500 else 0)
        st.markdown(f'<div class="quota-box"><span class="quota-titolo">PER SOCIO:</span><br><span class="quota-valore">{format_euro(netto/6)} €</span><br><small>Totale Netto: {format_euro(netto)} €</small></div>', unsafe_allow_html=True)
        if st.button("💾 Salva"):
            salva_vincita("Vincita", netto)
            st.toast("Salvato!")

elif scelta == "Bottino":
    st.subheader("🏛️ Archivio Storico")
    df = carica_archivio()
    if not df.empty:
        df_vis = df.copy()
        df_vis['Euro_Netto'] = df_vis['Euro_Netto'].apply(format_euro)
        st.table(df_vis)
        st.metric("TOTALE", f"{format_euro(df['Euro_Netto'].sum())} €")
    else:
        st.info("Vuoto.")
