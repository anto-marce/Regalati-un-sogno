import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configurazione Pagina
st.set_page_config(page_title="Regalati un Sogno", page_icon="💰")

# --- DATI FISSI ---
SCHEDINE = [
    {3, 10, 17, 40, 85, 86}, {10, 17, 19, 40, 85, 86},
    {17, 19, 40, 75, 85, 86}, {3, 19, 40, 75, 85, 86},
    {3, 10, 19, 75, 85, 86}, {3, 10, 17, 75, 85, 86}
]
COSTO_ESTRAZIONE_GRUPPO = 6 # 1€ a testa x 6 persone

# --- MENU LATERALE ---
st.sidebar.title("Menu Principale")
scelta = st.sidebar.radio("Vai a:", ["🍀 Verifica Vincite", "📊 Cassa Soci"])

# --- SEZIONE 1: VERIFICA VINCITE ---
if scelta == "🍀 Verifica Vincite":
    st.title("🍀 Verifica le Schedine")
    st.write("Inserisci i numeri estratti stasera:")
    
    cols = st.columns(6)
    n1 = cols[0].number_input("N1", 1, 90, 1)
    n2 = cols[1].number_input("N2", 1, 90, 1)
    n3 = cols[2].number_input("N3", 1, 90, 1)
    n4 = cols[3].number_input("N4", 1, 90, 1)
    n5 = cols[4].number_input("N5", 1, 90, 1)
    n6 = cols[5].number_input("N6", 1, 90, 1)
    
    if st.button("CONTROLLA"):
        estratti = {n1, n2, n3, n4, n5, n6}
        vincite = []
        for i, s in enumerate(SCHEDINE, 1):
            punti = len(s.intersection(estratti))
            if punti >= 2:
                vincite.append(f"Colonna {i}: {punti} PUNTI!")
        
        if vincite:
            st.balloons()
            for v in vincite: st.success(v)
        else:
            st.error("Nessuna vincita stasera.")

# --- SEZIONE 2: CASSA SOCI ---
elif scelta == "📊 Cassa Soci":
    st.title("📊 Gestione Cassa Gruppo")
    
    st.info("""
    **Regola:** Ogni socio che paga 15€ copre 15 estrazioni.
    Il grafico mostra quanto fondo cassa rimane dopo le giocate effettuate.
    """)

    # Input per la memoria (da aggiornare manualmente quando qualcuno paga)
    soci_paganti = st.number_input("Quanti soci hanno versato i 15€?", 0, 6, value=6)
    estrazioni_giocate = st.number_input("Quante estrazioni abbiamo già fatto da inizio cassa?", 0, 100, value=0)

    # Calcoli
    entrate_totali = soci_paganti * 15
    uscite_totali = estrazioni_giocate * COSTO_ESTRAZIONE_GRUPPO
    fondo_residuo = entrate_totali - uscite_totali

    # Visualizzazione Metriche
    c1, c2, c3 = st.columns(3)
    c1.metric("Totale Raccolto", f"{entrate_totali}€")
    c2.metric("Spesa Giocate", f"{uscite_totali}€")
    c3.metric("Fondo Attuale", f"{fondo_residuo}€")

    # Grafico a barre
    st.subheader("Grafico Entrate vs Uscite")
    fig, ax = plt.subplots()
    categorie = ['Entrate', 'Uscite', 'Residuo']
    valori = [entrate_totali, uscite_totali, fondo_residuo]
    colori = ['#2ecc71', '#e74c3c', '#3498db']
    
    ax.bar(categorie, valori, color=colori)
    st.pyplot(fig)

    if fondo_residuo <= 0:
        st.error("⚠️ FONDO ESAURITO! I soci devono versare la nuova quota.")
    else:
        estrazioni_rimanenti = fondo_residuo // COSTO_ESTRAZIONE_GRUPPO
        st.success(f"✅ Siamo coperti per altre {estrazioni_rimanenti} estrazioni.")
