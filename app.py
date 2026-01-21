import streamlit as st

# Configurazione della pagina
st.set_page_config(page_title="Controllo Schedine", page_icon="🏆")

st.title("🏆 Il Sogno - SuperEnalotto")
st.write("Inserisci i numeri estratti e scopri se abbiamo vinto!")

# I vostri 6 sistemi (sestine)
SCHEDINE = [
    {3, 10, 17, 40, 85, 86},  # Colonna 1
    {10, 17, 19, 40, 85, 86}, # Colonna 2
    {17, 19, 40, 75, 85, 86}, # Colonna 3
    {3, 19, 40, 75, 85, 86},  # Colonna 4
    {3, 10, 19, 75, 85, 86},  # Colonna 5
    {3, 10, 17, 75, 85, 86}   # Colonna 6
]

# Creazione delle caselle per inserire i numeri
st.subheader("Numeri Estratti")
cols = st.columns(6)
n1 = cols[0].number_input("1°", 1, 90, 1)
n2 = cols[1].number_input("2°", 1, 90, 1)
n3 = cols[2].number_input("3°", 1, 90, 1)
n4 = cols[3].number_input("4°", 1, 90, 1)
n5 = cols[4].number_input("5°", 1, 90, 1)
n6 = cols[5].number_input("6°", 1, 90, 1)

# Bottone per il controllo
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
        st.error("Nessuna vincita. Continua a SOGNARE!")