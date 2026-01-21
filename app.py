import streamlit as st

# 1. Impostazioni della pagina
st.set_page_config(page_title="Regalati un Sogno", page_icon="🏆")

# 2. Definizione dei sistemi (le tue 6 colonne)
SCHEDINE = [
    {3, 10, 17, 40, 85, 86},  # Colonna 1
    {10, 17, 19, 40, 85, 86}, # Colonna 2
    {17, 19, 40, 75, 85, 86}, # Colonna 3
    {3, 19, 40, 75, 85, 86},  # Colonna 4
    {3, 10, 19, 75, 85, 86},  # Colonna 5
    {3, 10, 17, 75, 85, 86}   # Colonna 6
]

# 3. Creazione del Menu Laterale (Sidebar)
st.sidebar.title("Menu")
scelta = st.sidebar.radio("Vai a:", ["🍀 Verifica Vincite", "💰 Cassa Soci", "🏛️ Il Bottino"])

# --- SEZIONE 1: VERIFICA VINCITE ---
if scelta == "🍀 Verifica Vincite":
    st.title("🏆 Il Sogno - SuperEnalotto")
    st.write("Inserisci i 6 numeri estratti:")

    # Inserimento numeri
    cols = st.columns(6)
    n1 = cols[0].number_input("1°", 1, 90, 1)
    n2 = cols[1].number_input("2°", 1, 90, 1)
    n3 = cols[2].number_input("3°", 1, 90, 1)
    n4 = cols[3].number_input("4°", 1, 90, 1)
    n5 = cols[4].number_input("5°", 1, 90, 1)
    n6 = cols[5].number_input("6°", 1, 90, 1)

    if st.button("VERIFICA VINCITA"):
        estratti = {n1, n2, n3, n4, n5, n6}
        trovato = False
        
        for i, schedina in enumerate(SCHEDINE, 1):
            indovinati = schedina.intersection(estratti)
            punti = len(indovinati)
            
            if punti >= 2:
                st.success(f"🎯 COLONNA {i}: HAI FATTO {punti} PUNTI! ({indovinati})")
                st.balloons()
                trovato = True
                
        if not trovato:
            st.error("Nessuna vincita stasera. Avanti la prossima!")

# --- SEZIONE 2: CASSA (In Standby) ---
elif scelta == "💰 Cassa Soci":
    st.title("💰 Gestione Cassa")
    st.info("Questa sezione è in manutenzione. Qui vedrai entrate e uscite del gruppo.")
    st.warning("Parte Cassa e Grafici momentaneamente in standby.")

# --- SEZIONE 3: IL BOTTINO (In Standby) ---
elif scelta == "🏛️ Il Bottino":
    st.title("🏛️ Archivio Vincite")
    st.write("Qui verranno salvate le vincite storiche del gruppo.")
    st.info("Archivio vuoto o in fase di configurazione.")
