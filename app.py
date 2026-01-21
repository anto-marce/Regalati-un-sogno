import streamlit as st
import re

# 1. Impostazioni Pagina
st.set_page_config(page_title="Regalati un Sogno", page_icon="🍀", layout="centered")

# 2. Stile CSS
st.markdown("<style>.stNumberInput input { font-size: 20px !important; text-align: center !important; }</style>", unsafe_allow_html=True)

st.title("🍀 Regalati un Sogno")

# --- FUNZIONE LOGICA PER SMISTARE I NUMERI ---
def carica_numeri():
    if st.session_state.testo_incollato:
        trovati = re.findall(r'\d+', st.session_state.testo_incollato)
        if len(trovati) >= 6:
            for i in range(6):
                # Aggiorniamo direttamente le chiavi delle caselle numeriche
                st.session_state[f"n{i}"] = int(trovati[i])

# 3. Schede
tab1, tab2, tab3 = st.tabs(["🔍 Verifica", "📜 Schedine", "📊 Archivio e Quote"])

with tab1:
    st.subheader("Inserimento Numeri")
    
    # Campo per incollare con funzione "on_change" (si attiva da sola)
    st.text_input(
        "Incolla qui l'estrazione e premi Invio:", 
        placeholder="es: 10 20 30 40 50 60",
        key="testo_incollato",
        on_change=carica_numeri
    )
    
    st.write("---")
    
    # Caselle numeriche (Sempre visibili o dentro expander, ma ora collegate)
    with st.expander("Controlla o inserisci a mano i 6 numeri", expanded=True):
        c1, c2, c3 = st.columns(3)
        c4, c5, c6 = st.columns(3)
        
        n0 = c1.number_input("1°", 1, 90, key="n0")
        n1 = c2.number_input("2°", 1, 90, key="n1")
        n2 = c3.number_input("3°", 1, 90, key="n2")
        n3 = c4.number_input("4°", 1, 90, key="n3")
        n4 = c5.number_input("5°", 1, 90, key="n4")
        n5 = c6.number_input("6°", 1, 90, key="n5")

    final_nums = [n0, n1, n2, n3, n4, n5]

    if st.button("VERIFICA VINCITA 🚀", use_container_width=True):
        # Filtriamo i numeri (escludiamo quelli a 0 o 1 di default se non inseriti)
        if all(final_nums):
            set_estratti = set(final_nums)
            SCHEDINE = [
                {3, 10, 17, 40, 85, 86}, {10, 17, 19, 40, 85, 86},
                {17, 19, 40, 75, 85, 86}, {3, 19, 40, 75, 85, 86},
                {3, 10, 19, 75, 85, 86}, {3, 10, 17, 75, 85, 86}
            ]
            
            vincite_trovate = False
            for i, schedina in enumerate(SCHEDINE, 1):
                indovinati = schedina.intersection(set_estratti)
                punti = len(indovinati)
                if punti >= 2:
                    st.balloons()
                    st.success(f"✅ SCHEDINA {i}: HAI FATTO {punti} PUNTI!")
                    st.write(f"Numeri indovinati: {sorted(list(indovinati))}")
                    vincite_trovate = True
            
            if not vincite_trovate:
                st.warning("Nessuna vincita per questa estrazione.")
        else:
            st.error("Inserisci tutti i 6 numeri prima di verificare.")

with tab2:
    st.subheader("Il nostro sistema")
    schedine_lista = [
        "3 - 10 - 17 - 40 - 85 - 86", "10 - 17 - 19 - 40 - 85 - 86",
        "17 - 19 - 40 - 75 - 85 - 86", "3 - 19 - 40 - 75 - 85 - 86",
        "3 - 10 - 19 - 75 - 85 - 86", "3 - 10 - 17 - 75 - 85 - 86"
    ]
    for i, s in enumerate(schedine_lista, 1):
        st.code(f"Schedina {i}: {s}", language="text")

with tab3:
    st.subheader("📊 Risultati e Divisione")
    st.link_button("📜 Apri Archivio Storico Ufficiale", "https://www.superenalotto.it/archivio-estrazioni", use_container_width=True)
    st.divider()
    st.write("💰 **Calcolatore Divisione Vincita**")
    premio = st.number_input("Importo totale vinto (€)", min_value=0.0, step=0.50)
    if premio > 0:
        st.success(f"💎 Quota per ogni socio: **{premio / 6:.2f} €**")
