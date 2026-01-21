import streamlit as st
import re
import pandas as pd
from datetime import datetime
import os
import urllib.parse
# Importiamo la funzione per la pioggia (Assicurati di avere streamlit-extras nel requirements.txt)
from streamlit_extras.let_it_rain import rain 

# 1. IMPOSTAZIONI PAGINA
st.set_page_config(page_title="Regalati un Sogno", page_icon="🍀", layout="centered")

# 2. STILE CSS
st.markdown("""
    <style>
    .stSelectbox div[data-baseweb="select"] {
        border: 2px solid #003366 !important;
        border-radius: 10px;
    }
    div[data-testid="stNumberInput"] input { 
        font-size: 22px !important; text-align: center !important; font-weight: 900 !important; 
        color: #000000 !important; background-color: #ffffff !important; 
        border: 2px solid #cccccc !important; border-radius: 5px;
    }
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
    .status-red { background-color: #f8d7da; color: #721c24; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; margin-bottom: 10px; }
    .status-green { background-color: #d4edda; color: #155724; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNZIONI AUDIO / ARCHIVIO ---
def play_audio(url):
    audio_html = f'<audio autoplay="true" style="display:none;"><source src="{url}" type="audio/mpeg"></audio>'
    st.components.v1.html(audio_html, height=0)

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

# --- MENU DI NAVIGAZIONE SUPERIORE ---
st.title("🍀 Regalati un Sogno")
scelta = st.selectbox("🧭 COSA VUOI FARE?", 
                     ["🔍 Verifica Vincita", "📅 Stato Abbonamento", "💰 Calcolo Quote", "🏛️ Il Bottino"])

st.divider()

# --- LOGICA DELLE SEZIONI ---

if scelta == "🔍 Verifica Vincita":
    st.subheader("📋 Verifica Estrazione")
    st.markdown('<a href="https://www.adm.gov.it/portale/monopoli/giochi/giochi_num_total/superenalotto" target="_blank" class="ams-button">➡️ PASSO 1: Controlla Estrazione su Sito AMS</a>', unsafe_allow_html=True)

    if 'n0' not in st.session_state:
        for i in range(6): st.session_state[f'n{i}'] = 1

    def distribuisci_numeri():
        testo = st.session_state.incolla_qui
        if testo:
            numeri_grezzi = re.findall(r'\d+', testo)
            numeri_validi = [int(n) for n in numeri_grezzi if 1 <= int(n) <= 90]
            if len(numeri_validi) >= 6:
                for i in range(6): 
                    st.session_state[f"n{i}"] = numeri_validi[i]
            else:
                st.toast(f"⚠️ Trovati solo {len(numeri_validi)} numeri validi", icon="⚠️")

    c_input, c_btn = st.columns([4, 1])
    with c_input:
        st.text_input("PASSO 2: Incolla qui la sequenza:", key="incolla_qui", on_change=distribuisci_numeri)
    with c_btn:
        st.write("")
        st.write("") 
        if st.button("⤵️"):
            distribuisci_numeri()
            st.rerun()
    
    st.write("👁️ **Numeri rilevati:**")
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
            rain(emoji="💶", font_size=54, falling_speed=5, animation_length="3")
            play_audio("https://www.myinstants.com/media/sounds/ta-da.mp3")
            testo_wa = "🥳 *VINCITA SUPERENALOTTO!*\n\n"
            for v in vincite:
                st.success(f"🔥 **SCHEDINA {v[0]}:** {v[1]} PUNTI! ({v[2]})")
                testo_wa += f"✅ Schedina {v[0]}: *{v[1]} Punti* ({', '.join(map(str, v[2]))})\n"
            testo_encoded = urllib.parse.quote(testo_wa)
            st.markdown(f'<a href="https://wa.me/?text={testo_encoded}" target="_blank" class="wa-button">📲 PASSO 3: Invia Esito su WhatsApp</a>', unsafe_allow_html=True)
        else:
            play_audio("https://www.myinstants.com/media/sounds/sad-trombone.mp3")
            st.warning("Nessuna vincita rilevata.")

elif scelta == "📅 Stato Abbonamento":
    st.subheader("📅 Gestione Abbonamento (15 Concorsi)")
    fatti = st.slider("Concorsi già giocati", 0, 15, value=0)
    rimanenti = 15 - fatti
    
    if rimanenti > 5:
        st.info(f"✅ Concorsi rimanenti: {rimanenti} su 15")
    elif 1 <= rimanenti <= 5:
        st.warning(f"⚠️ Attenzione: mancano solo {rimanenti} estrazioni al rinnovo!")
    else:
        st.error("🆘 ABBONAMENTO SCADUTO! Raccogliere le quote.")
    
    st.progress(fatti / 15)
    st.divider()
    
    st.subheader("👥 Cassa Soci (Prossimo Rinnovo)")
    soci = ["VS", "MM", "ED", "AP", "GGC", "AM"]
    c1, c2 = st.columns(2)
    pagati = 0
    for i, s in enumerate(soci):
        # Selezione colonna (c1 per i primi 3, c2 per gli altri)
        target_col = c1 if i < 3 else c2
        with target_col:
            if st.checkbox(f"Ricevuta da {s}", key=f"paga_{s}"):
                pagati += 1
    
    if pagati < 6:
        st.markdown(f'<div class="status-red">🔴 CASSA: {pagati}/6 SOCI HANNO PAGATO</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-green">✅ CASSA COMPLETA! RINNOVO PRONTO</div>', unsafe_allow_html=True)

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
        totale = df['Euro_Netto'].sum()
        st.metric("Totale Netto Accumulato", f"{totale:,.2f} €".replace(",", "X").replace(".", ",").replace("X", "."))
    else:
        st.info("Archivio vuoto.")
            st.warning("Nessuna vincita rilevata.")

elif scelta == "📅 Stato Abbonamento":
    st.subheader("📅 Gestione Abbonamento (15 Concorsi)")
        with c1 if i < 3 else c2:
            if st.checkbox(f"Quota ricevuta da {s}", key=f"paga_{s}"):
                pagati += 1
    
    if pagati < 6:
        st.markdown(f'<div class="status-red">🔴 CASSA: {pagati}/6 SOCI HANNO PAGATO</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-green">✅ CASSA COMPLETA! RINNOVO PRONTO</div>', unsafe_allow_html=True)

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
        totale = df['Euro_Netto'].sum()
        st.metric("Totale Netto Accumulato", f"{totale:,.2f} €".replace(",", "X").replace(".", ",").replace("X", "."))
    else:
        st.info("Archivio vuoto.")
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
        totale = df['Euro_Netto'].sum()
        st.metric("Totale Netto Accumulato", f"{totale:,.2f} €".replace(",", "X").replace(".", ",").replace("X", "."))
    else:
        st.info("Archivio vuoto.")
    st.subheader("📅 Gestione Abbonamento (15 Concorsi)")
    fatti = st.slider("Concorsi passati", 0, 15, value=0)
    st.info(f"Concorsi rimanenti: {15 - fatti} su 15")
    st.progress(fatti / 15)
    
    st.divider()
    st.subheader("👥 Cassa Soci")
    soci = ["VS", "MM", "ED", "AP", "GGC", "AM"]
    c1, c2 = st.columns(2)
    pagati = 0
    for i, s in enumerate(soci):
        with c1 if i < 3 else c2:
            if st.checkbox(f"Pagato da {s}", key=f"paga_{s}"):
                pagati += 1
    
    if pagati < 6:
        st.markdown(f'<div class="status-red">🔴 CASSA: {pagati}/6 SOCI HANNO PAGATO</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-green">✅ CASSA COMPLETA! RINNOVO PRONTO</div>', unsafe_allow_html=True)

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
        totale = df['Euro_Netto'].sum()
        st.metric("Totale Netto", f"{totale:,.2f} €".replace(",", "X").replace(".", ",").replace("X", "."))
    else:
        st.info("Archivio vuoto.")
    fatti = st.slider("Concorsi passati", 0, 15, value=0)
    st.info(f"Concorsi rimanenti: {15 - fatti} su 15")
    st.progress(fatti / 15)
    
    st.divider()
    st.subheader("👥 Cassa Soci")
    soci = ["VS", "MM", "ED", "AP", "GGC", "AM"]
    c1, c2 = st.columns(2)
    pagati = 0
    for i, s in enumerate(soci):
        with c1 if i < 3 else c2:
            if st.checkbox(f"Pagato da {s}", key=f"paga_{s}"):
                pagati += 1
    
    if pagati < 6:
        st.markdown(f'<div class="status-red">🔴 CASSA: {pagati}/6 SOCI HANNO PAGATO</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-green">✅ CASSA COMPLETA! RINNOVO PRONTO</div>', unsafe_allow_html=True)
    
    st.divider()
    st.write("**Le nostre sestine:**")
    for i, s in enumerate(["03-10-17-40-85-86", "10-17-19-40-85-86", "17-19-40-75-85-86", "03-19-40-75-85-86", "03-10-19-75-85-86", "03-10-17-75-85-86"], 1):
        st.text(f"Schedina {i}: {s}")

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
        totale = df['Euro_Netto'].sum()
        st.metric("Totale Netto", f"{totale:,.2f} €".replace(",", "X").replace(".", ",").replace("X", "."))
    else:
        st.info("Archivio vuoto.")
