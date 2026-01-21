import streamlit as st
import re

# 1. Impostazioni Pagina
st.set_page_config(page_title="Regalati un Sogno", page_icon="🍀", layout="centered")

# 2. Stile CSS
st.markdown("""
    <style>
    .stNumberInput input { font-size: 22px !important; text-align: center !important; font-weight: bold; }
    .main { background-color: #f8f9fa; }
    div[data-testid="stExpander"] { background-color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍀 Regalati un Sogno")

# --- FUNZIONE LOGICA DI SMISTAMENTO ---
def distribuisci_numeri():
    if st.session_state.incolla_qui:
        numeri = re.findall(r'\d+', st.session_state.incolla_qui)
        if len(numeri) >= 6:
            for i in range(6):
                st.session_state[f"n{i}"] = int(numeri[i])

# 3. Creazione Schede
tab1, tab2, tab3 = st.tabs(["🔍 Verifica Vincita", "📜 Il Nostro Sistema", "💰 Calcolo Quote"])

with tab1:
    st.info("🎯 **Passaggio 1:** Prendi i numeri dal sito ufficiale")
    st.link_button("Apri Sito Ufficiale ADM 🏛️", 
                   "https://www.adm.gov.it/portale/monopoli/giochi/giochi_num_total/superenalotto", 
                   use_container_width=True)
    
    st.write("---")
    
    st.subheader("2. Incolla i numeri estratti")
    st.text_input(
        "Incolla qui la stringa e premi INVIO:", 
        placeholder="Esempio: 3 15 22 48 60 81",
        key="incolla_qui",
        on_change=distribuisci_numeri
    )
    
    with st.expander("Numeri rilevati (modifica se necessario)", expanded=True):
        c1, c2, c3 = st.columns(3)
        c4, c5, c6 = st.columns(3)
        
        n0 = c1.number_input("1°", 1, 90, key="n0")
        n1 = c2.number_input("2°", 1, 90, key="n1")
        n2 = c3.number_input("3°", 1, 90, key="n2")
        n3 = c4.number_input("4°", 1, 90, key="n3")
        n4 = c5.number_input("5°", 1, 90, key="n4")
        n5 = c6.number_input("6°", 1, 90, key="n5")

    final_nums = [n0, n1, n2, n3, n4, n5]

    if st.button("CONTROLLA SCHEDINE 🚀", use_container_width=True):
        if all(final_nums):
            set_estratti = set(final_nums)
            SCHEDINE = [
                {3, 10, 17, 40, 85, 86}, {10, 17, 19, 40, 85, 86},
                {17, 19, 40, 75, 85, 86}, {3, 19, 40, 75, 85, 86},
                {3, 10, 19, 75, 85, 86}, {3, 10, 17, 75, 85, 86}
            ]
            
            vincite_trovate = False
            for i, schedina in enumerate(SCHEDINE, 1):
                indovinati = sorted(list(schedina.intersection(set_estratti)))
                punti = len(indovinati)
                if punti >= 2:
                    st.balloons()
                    st.success(f"🔥 SCHEDINA {i}: {punti} PUNTI!")
                    st.write(f"Numeri centrati: {indovinati}")
                    vincite_trovate = True
            
            if not vincite_trovate:
                st.info("Nessuna vincita (minimo 2 punti).")
        else:
            st.error("Inserisci tutti i 6 numeri.")

with tab2:
    st.subheader("Le Sestine del Gruppo")
    sestine = [
        "03 - 10 - 17 - 40 - 85 - 86", "10 - 17 - 19 - 40 - 85 - 86",
        "17 - 19 - 40 - 75 - 85 - 86", "03 - 19 - 40 - 75 - 85 - 86",
        "03 - 10 - 19 - 75 - 85 - 86", "03 - 10 - 17 - 75 - 85 - 86"
    ]
    for i, s in enumerate(sestine, 1):
        st.code(f"Schedina {i}: {s}", language="text")

with tab3:
    st.subheader("💰 Divisione Premio")
    st.write("Inserisci il totale vinto per calcolare le quote:")
    
    # Input del premio
    premio = st.number_input("Totale vinto (€)", min_value=0.0, step=10.0, format="%.2f")
    
    if premio > 0:
        quota = premio / 6
        
        # Formattazione con punto per le migliaia e virgola per i decimali
        premio_f = f"{premio:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        quota_f = f"{quota:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        
        st.markdown(f"""
        ### 📊 Riepilogo Conti
        * **Premio Totale:** {premio_f} €
        * **Numero Soci:** 6
        ---
        ## 💎 Quota individuale: **{quota_f} €**
        """)
