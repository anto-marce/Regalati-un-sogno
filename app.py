import streamlit as st
import re
import pandas as pd
from datetime import datetime
import os

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
    
    /* Stile per i box stato nel menu */
    .status-red { background-color: #f8d7da; color: #721c24; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; margin-bottom: 10px; border: 1px solid #f5c6cb; }
    .status-green { background-color: #d4edda; color: #155724; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; margin-bottom: 10px; border: 1px solid #c3e6cb; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNZIONI AUDIO ---
def play_audio(url):
    audio_html = f'<audio autoplay="true" style="display:none;"><source src="{url}" type="audio/mpeg"></audio>'
    st.components.v1.html(audio_html, height=0)

# --- FUNZIONE ARCHIVIO ---
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

# --- SIDEBAR (MENU TOGGLE) & INFO ---
with st.sidebar:
    st.title("🍀 Menù")
    # Menu di navigazione a pulsanti radio (Toggle)
    scelta = st.radio(
        "Seleziona sezione:",
        ["🔍 Verifica Vincita", "📅 Stato Abbonamento", "💰 Calcolo Quote", "🏛️ Il Bottino"],
        index=0
    )
    
    st.divider()
    
    # LINK UFFICIALE AMS
    st.markdown("### 🔗 Link Estrazioni")
    st.markdown("[🌐 Sito Ufficiale AMS](https://www.adm.gov.it/portale/giochi/lotto-e-lotterie/superenalotto)", unsafe_allow_html=True)
    
    st.divider()
    
    # GESTIONE CASSA SOCI (Versione compatta nella sidebar)
    st.subheader("👥 Cassa Rinnovo")
    soci = ["VS", "MM", "ED", "AP", "GGC", "AM"]
    pagati = 0
    for s in soci:
        if st.checkbox(f"Pagato da {s}", key=f"paga_{s}"):
            pagati += 1
    
    if pagati < 6:
        st.markdown(f'<div class="status-red">🔴 CASSA: {pagati}/6</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-green">✅ CASSA COMPLETA</div>', unsafe_allow_html=True)

# --- CONTENUTO PRINCIPALE ---
st.title("🍀 Regalati un Sogno")

if scelta == "🔍 Verifica Vincita":
    st.subheader("📋 Incolla e Verifica")
    
    def distribuisci_numeri():
        if st.session_state.incolla_qui:
            numeri = re.findall(r'\d+', st.session_state.incolla_qui)
            if len(numeri) >= 6:
                for i in range(6): st.session_state[f"n{i}"] = int(numeri[i])

    st.text_input("Sequenza (spazio o trattino):", key="incolla_qui", on_change=distribuisci_numeri, placeholder="Incolla e premi INVIO")
    
    with st.expander("👁️ Numeri rilevati", expanded=True):
        c1, c2, c3 = st.columns(3); c4, c5, c6 = st.columns(3)
        n0 = c1.number_input("1°", 1, 90, key="n0")
        n1 = c2.number_input("2°", 1, 90, key="n1")
        n2 = c3.number_input("3°", 1, 90, key="n2")
        n3 = c4.number_input("4°", 1, 90, key="n3")
        n4 = c5.number_input("5°", 1, 90, key="n4")
        n5 = c6.number_input("6°", 1, 90, key="n5")

    if st.button("VERIFICA ORA 🚀", type="primary", use_container_width=True):
        final_nums = [n0, n1, n2, n3, n4, n5]
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
            st.markdown(f'''<a href="https://wa.me/?text={msg_wa}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer; font-weight:bold;">📲 Avvisa il gruppo su WhatsApp</button></a>''', unsafe_allow_html=True)
        else:
            play_audio("https://www.myinstants.com/media/sounds/sad-trombone.mp3")
            st.warning("Nessuna vincita. Ritenta!")

elif scelta == "📅 Stato Abbonamento":
    st.subheader("📅 Abbonamento (15 Concorsi)")
    fatti = st.slider("Concorsi già passati", 0, 15, value=0)
    rimanenti = 15 - fatti
    
    if fatti == 0:
        st.info("🚀 L'abbonamento parte dal concorso di domani 22 Gennaio!")
    
    if rimanenti <= 3:
        st.markdown(f'<div class="status-red">⚠️ CONCORSI RIMANENTI: {rimanenti} / 15</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="status-green">📅 CONCORSI RIMANENTI: {rimanenti} / 15</div>', unsafe_allow_html=True)
    st.progress(fatti / 15)
    
    st.divider()
    st.write("**Schedine registrate:**")
    for i, s in enumerate(["03-10-17-40-85-86", "10-17-19-40-85-86", "17-19-40-75-85-86", "03-19-40-75-85-86", "03-10-19-75-85-86", "03-10-17-75-85-86"], 1):
        st.text(f"Schedina {i}: {s}")

elif scelta == "💰 Calcolo Quote":
    st.subheader("💰 Calcolo Netto e Archiviazione")
    premio_lordo = st.number_input("Importo vinto lordo (€)", min_value=0.0, step=10.0)
    if premio_lordo > 0:
        netto_tot = premio_lordo - ((premio_lordo - 500) * 0.20 if premio_lordo > 500 else 0)
        quota = round(netto_tot / 6, 2)
        st.markdown(f'<div class="quota-box"><span class="quota-valore">{quota} € a testa</span></div>', unsafe_allow_html=True)
        if st.button("💾 Salva nel Bottino"):
            salva_vincita("Vincita", netto_tot)
            st.toast("Vincita salvata nell'archivio!", icon="✅")

elif scelta == "🏛️ Il Bottino":
    st.subheader("🏛️ Il Bottino Storico")
    df_storico = carica_archivio()
    if not df_storico.empty:
        st.dataframe(df_storico, use_container_width=True)
        totale_vinto = df_storico['Euro_Netto'].sum()
        st.metric("Totale Netto Accumulato", f"{totale_vinto:,.2f} €".replace(",", "."))
        if st.button("Svuota Archivio (⚠️ Azione Irreversibile)"):
            if os.path.exists("archivio_vincite.csv"):
                os.remove("archivio_vincite.csv")
                st.rerun()
    else:
        st.info("L'archivio è ancora vuoto. Inizia a vincere!")
