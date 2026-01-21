import streamlit as st
import matplotlib.pyplot as plt

# 1. Configurazione della pagina
st.set_page_config(page_title="Controllo Schedine", page_icon="🏆")

st.title("🏆 Il Sogno - SuperEnalotto")
st.write("Inserisci i numeri estratti e scopri se abbiamo vinto!")

# --- SEZIONE SUPERENALOTTO ---

# I vostri 6 sistemi (sestine)
SCHEDINE = [
    {3, 10, 17, 40, 85, 86},  # Colonna 1
    {10, 17, 19, 40, 85, 86}, # Colonna 2
    {17, 19, 40, 75, 85, 86}, # Colonna 3
    {3, 19, 40, 75, 85, 86},  # Colonna 4
    {3, 10, 19, 75, 85, 86},  # Colonna 5
    {3, 10, 17, 75, 85, 86}   # Colonna 6
]

st.subheader("Numeri Estratti")
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
        st.error("Nessuna vincita. Ritenta la prossima volta!")

# --- SEZIONE CASSA SOCI ---
st.markdown("---") # Linea di separazione
st.header("📊 Gestione Cassa Soci")

st.info("Ogni quota da 15€ versata da un socio copre 15 estrazioni (1€ a colonna).")

# Input per la "Memoria" dell'app
# Nota: Cambia i numeri 'value' qui sotto su GitHub per salvare i dati definitivamente
col_a, col_b = st.columns(2)
with col_a:
    soci_paganti = st.number_input("Quanti soci hanno pagato 15€?", 0, 6, value=6)
with col_b:
    estrazioni_fatte = st.number_input("Quante estrazioni abbiamo giocato?", 0, 100, value=0)

# Calcoli
entrate = soci_paganti * 15
uscite = estrazioni_fatte * 6  # 6€ totali a estrazione per il gruppo
residuo = entrate - uscite

# Visualizzazione dei soldi
c1, c2, c3 = st.columns(3)
c1.metric("Totale Raccolto", f"{entrate}€")
c2.metric("Totale Speso", f"{uscite}€")
c3.metric("Fondo Cassa", f"{residuo}€")

# --- GRAFICO ---
st.subheader("Grafico Entrate vs Uscite")
fig, ax = plt.subplots(figsize=(8, 4))
categorie = ['Soldi Raccolti', 'Soldi Spesi', 'Fondo Rimanente']
valori = [entrate, uscite, max(0, residuo)]
colori = ['#2ecc71', '#e74c3c', '#3498db']

ax.bar(categorie, valori, color=colori)
ax.set_ylabel('Euro (€)')
st.pyplot(fig)

# Messaggio di stato
if residuo > 0:
    estrazioni_rimanenti = residuo // 6
    st.success(f"✅ La cassa è in attivo! Siamo coperti per altre {estrazioni_rimanenti} estrazioni.")
elif residuo == 0:
    st.warning("⚠️ La cassa è vuota. È ora di raccogliere le nuove quote!")
else:
    st.error(f"🆘 Siamo in debito di {abs(residuo)}€! Bisogna ricaricare subito.")
