import streamlit as st
import re
import pandas as pd
from datetime import datetime
import urllib.parse
from num2words import num2words

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="Regalati un Sogno", page_icon="🍀")

# CSS Ottimizzato per Mobile
st.markdown("""
    <style>
    .quota-box {
        text-align: center; background-color: #f0f4f8; padding: 20px;
        border-radius: 15px; border: 2px solid #003366; margin: 10px 0;
    }
    .quota-valore { font-size: 32px; font-weight: 800; color: #003366; display: block; }
    .quota-testo { font-size: 16px; color: #555; font-style: italic; text-transform: capitalize; }
    .wa-button {
        display: block; text-align: center; padding: 12px; background-color: #25D366; 
        color: white !important; border-radius: 10px; text-decoration: none; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGICA CALCOLO TESTUALE ---
def euro_in_lettere(cifra):
    intera = int(cifra)
    decimali = int(round((cifra - intera) * 100))
    testo = num2words(intera, lang='it') + " euro"
    if decimali > 0:
        testo += f" e {num2words(decimali, lang='it')} centesimi"
    return testo

# --- FUNZIONI DATI ---
def carica_archivio():
    try: return pd.read_csv('archivio_vincite.csv')
    except: return pd.DataFrame(columns=['Data', 'Punti', 'Euro_Netto'])

# --- MENU ---
scelta = st.selectbox("🧭 MENU", ["🔍 Verifica", "📅 Abbonamento", "💰 Calcolo", "🏛️ Archivio"])

if scelta == "🔍 Verifica":
    st.subheader("🔍 Verifica Vincita")
    # Qui inserisci la logica re.findall che avevi già (funziona bene)
    incolla = st.text_input("Incolla qui l'estrazione:")
    if incolla:
        numeri = re.findall(r'\d+', incolla)
        if len(numeri) >= 6:
            st.success(f"Rilevati: {', '.join(numeri[:6])}")
            # ... logica confronto sestine ...

elif scelta == "💰 Calcolo":
    st.subheader("💰 Calcolo Quote")
    lordo = st.number_input("Inserisci Lordo Totale (€)", min_value=0.0, step=10.0, format="%.2f")
    
    if lordo > 0:
        # Calcolo tasse (20% sopra i 500€)
        netto_totale = lordo - ((lordo - 500) * 0.20 if lordo > 500 else 0)
        quota_testa = round(netto_totale / 6, 2)
        
        testo_lettere = euro_in_lettere(quota_testa)
        
        st.markdown(f"""
            <div class="quota-box">
                <span class="quota-valore">{quota_testa:.2f} €</span>
                <span class="quota-testo">{testo_lettere}</span>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("💾 Salva nel Bottino"):
            # Funzione salva_vincita...
            st.success("Salvato correttamente!")

elif scelta == "📅 Abbonamento":
    st.subheader("📅 Stato Abbonamento")
    fatti = st.slider("Concorsi fatti", 0, 15, 0)
    st.metric("Rimanenti", 15 - fatti)
    st.progress(fatti / 15)

elif scelta == "🏛️ Archivio":
    st.subheader("🏛️ Il Bottino")
    df = carica_archivio()
    if not df.empty:
        st.dataframe(df)
        st.metric("Totale Accumulato", f"{df['Euro_Netto'].sum():.2f} €")
    else:
        st.info("Nessuna vincita salvata.")
