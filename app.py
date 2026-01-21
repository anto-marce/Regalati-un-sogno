import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Cassa Soci Sogno", page_icon="💰")

# --- LOGICA COSTI ---
COSTO_ESTRAZIONE_TOTALE = 6  # 1€ x 6 persone
QUOTA_SOCIO = 15             # 15€ coprono 15 estrazioni
# --------------------

st.title("💰 Gestione Cassa e Schedine")

# TAB 1: Controllo Vincite (Quello che abbiamo fatto prima)
tab1, tab2 = st.tabs(["Check Schedine", "Cassa Soci"])

with tab1:
    st.subheader("Hai vinto stasera?")
    # ... (qui rimane il codice delle schedine che hai già) ...
    st.info("Inserisci i numeri per verificare la vincita.")

with tab2:
    st.subheader("Situazione Cassa Soci")
    
    # In un'app reale qui collegheremmo il Foglio Google. 
    # Per ora simuliamo la memoria con un inserimento manuale veloce.
    
    soci = ["Tu", "Socio 2", "Socio 3", "Socio 4", "Socio 5", "Socio 6"]
    pagati = []
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Chi ha pagato gli ultimi 15€?")
        for s in soci:
            p = st.checkbox(f"{s} ha pagato", key=s)
            if p: pagati.append(s)
            
    with col2:
        estrazioni_fatte = st.number_input("Quante estrazioni abbiamo giocato in totale?", min_value=0, value=1)

    # CALCOLI FINANZIARI
    entrate = len(pagati) * QUOTA_SOCIO
    uscite = estrazioni_fatte * COSTO_ESTRAZIONE_TOTALE
    bilancio = entrate - uscite

    # METRICHE
    c1, c2, c3 = st.columns(3)
    c1.metric("Entrate Totali", f"{entrate}€")
    c2.metric("Uscite Totali", f"{uscite}€")
    c3.metric("Fondo Cassa", f"{bilancio}€", delta=bilancio)

    # GRAFICO
    st.subheader("Andamento Cassa")
    dati_grafico = pd.DataFrame({
        'Categoria': ['Entrate', 'Uscite', 'Residuo'],
        'Euro': [entrate, uscite, bilancio]
    })
    
    fig, ax = plt.subplots()
    colors = ['#2ecc71', '#e74c3c', '#f1c40f']
    ax.bar(dati_grafico['Categoria'], dati_grafico['Euro'], color=colors)
    st.pyplot(fig)

    if bilancio < 0:
        st.error("⚠️ ATTENZIONE: La cassa è in rosso! Qualcuno deve pagare.")
    else:
        st.success(f"Siamo coperti per altre {int(bilancio/COSTO_ESTRAZIONE_TOTALE)} estrazioni.")
        netto = premio - ((premio - 500) * 0.20 if premio > 500 else 0)
        st.markdown(f'<div class="quota-box"><span class="quota-valore">{round(netto/6, 2)} € a testa</span></div>', unsafe_allow_html=True)
        if st.button("💾 Salva"):
            salva_vincita("Vincita", netto)
            st.toast("Salvato!")

elif scelta == "🏛️ Il Bottino":
    st.subheader("🏛️ Archivio")
    df = carica_archivio()
    if not df.empty:
        st.dataframe(df, use_container_width=True)
        st.metric("Totale Netto", f"{df['Euro_Netto'].sum():,.2f} €".replace(",", "."))
    else: st.info("Archivio vuoto.")
