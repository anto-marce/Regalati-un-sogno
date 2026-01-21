import streamlit as st

# 1. Impostazioni Pagina
st.set_page_config(
    page_title="Regalati un Sogno",
    page_icon="🍀",
    layout="centered"
)

# 2. Stile CSS
st.markdown("""
    <style>
    .stNumberInput input {
        font-size: 20px !important;
        text-align: center !important;
    }
    .main {
        background-color: #f5f7f9;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🍀 Regalati un Sogno")

# 3. Creazione di 3 Schede
tab1, tab2, tab3 = st.tabs(["🔍 Verifica", "📜 Schedine", "📊 Archivio e Quote"])

with tab1:
    st.subheader("Inserisci i numeri estratti")
    c1, c2, c3 = st.columns(3)
    n1 = c1.number_input("1°", 1, 90, value=None, placeholder="?", key="v1")
    n2 = c2.number_input("2°", 1, 90, value=None, placeholder="?", key="v2")
    n3 = c3.number_input("3°", 1, 90, value=None, placeholder="?", key="v3")
    
    c4, c5, c6 = st.columns(3)
    n4 = c4.number_input("4°", 1, 90, value=None, placeholder="?", key="v4")
    n5 = c5.number_input("5°", 1, 90, value=None, placeholder="?", key="v5")
    n6 = c6.number_input("6°", 1, 90, value=None, placeholder="?", key="v6")

    if st.button("VERIFICA ORA 🚀", use_container_width=True):
        if n1 and n2 and n3 and n4 and n5 and n6:
            estratti = {n1, n2, n3, n4, n5, n6}
            SCHEDINE = [
                {3, 10, 17, 40, 85, 86}, {10, 17, 19, 40, 85, 86},
                {17, 19, 40, 75, 85, 86}, {3, 19, 40, 75, 85, 86},
                {3, 10, 19, 75, 85, 86}, {3, 10, 17, 75, 85, 86}
            ]
            vincite_trovate = False
            for i, schedina in enumerate(SCHEDINE, 1):
                indovinati = schedina.intersection(estratti)
                punti = len(indovinati)
                if punti >= 2:
                    st.balloons()
                    st.success(f"✅ SCHEDINA {i}: HAI FATTO {punti} PUNTI!")
                    st.write(f"Numeri indovinati: {sorted(list(indovinati))}")
                    vincite_trovate = True
            if not vincite_trovate:
                st.warning("Nessuna vincita per questa estrazione.")
        else:
            st.error("Inserisci tutti i 6 numeri.")

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
    
    # Link rapido all'archivio ufficiale
    st.link_button("Vedi Estrazioni Ufficiali (Sisal)", "https://www.superenalotto.it/risultati", use_container_width=True)
    
    st.divider()
    
    # Calcolatore di Quote
    st.write("💰 **Calcolatore Divisione Vincita**")
    premio = st.number_input("Inserisci l'importo vinto (€)", min_value=0.0, step=0.50)
    if premio > 0:
        quota = premio / 6
        st.info(f"Ogni partecipante riceve: **{quota:.2f} €**")
