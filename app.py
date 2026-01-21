import streamlit as st

# 1. Impostazioni Pagina (Titolo che appare sul browser)
st.set_page_config(
    page_title="Regalati un Sogno",
    page_icon="🍀",
    layout="centered" # Mantiene tutto al centro, perfetto per il cellulare
)

# 2. Stile CSS per far somigliare i numeri a dei "pallini" della lotteria
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
    """, unsafe_allow_status=True)

st.title("🍀 Regalati un Sogno")
st.write("Benvenuti nel sistema del gruppo. Buona fortuna!")

# Creazione delle schede per risparmiare spazio su mobile
tab1, tab2 = st.tabs(["🔍 Verifica Vincita", "📜 Le Nostre Schedine"])

with tab1:
    st.subheader("Inserisci l'estrazione")
    
    # Griglia 3x2 per i numeri (più ordinata su smartphone)
    c1, c2, c3 = st.columns(3)
    n1 = c1.number_input("1°", 1, 90, 1, key="v1")
    n2 = c2.number_input("2°", 1, 90, 1, key="v2")
    n3 = c3.number_input("3°", 1, 90, 1, key="v3")
    
    c4, c5, c6 = st.columns(3)
    n4 = c4.number_input("4°", 1, 90, 1, key="v4")
    n5 = c5.number_input("5°", 1, 90, 1, key="v5")
    n6 = c6.number_input("6°", 1, 90, 1, key="v6")

    st.markdown("---") # Linea di separazione

    if st.button("VERIFICA ORA 🚀", use_container_width=True):
        estratti = {n1, n2, n3, n4, n5, n6}
        
        # Le vostre sestine ufficiali
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
                st.success(f"✅ COLONNA {i}: HAI FATTO {punti} PUNTI!")
                st.write(f"Numeri indovinati: {sorted(list(indovinati))}")
                vincite_trovate = True
        
        if not vincite_trovate:
            st.warning("Nessuna vincita per questa estrazione. Ritenta!")

with tab2:
    st.subheader("Sistema in gioco")
    st.info("Ogni partecipante ha una rotazione equa dei numeri variabili.")
    
    # Mostra le schedine in modo elegante
    schedine_lista = [
        "3 - 10 - 17 - 40 - 85 - 86",
        "10 - 17 - 19 - 40 - 85 - 86",
        "17 - 19 - 40 - 75 - 85 - 86",
        "3 - 19 - 40 - 75 - 85 - 86",
        "3 - 10 - 19 - 75 - 85 - 86",
        "3 - 10 - 17 - 75 - 85 - 86"
    ]
    
    for i, s in enumerate(schedine_lista, 1):
        st.code(f"Colonna {i}: {s}", language="text")