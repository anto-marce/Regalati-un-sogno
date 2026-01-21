import streamlit as st
import re

# 1. Impostazioni Pagina
st.set_page_config(page_title="Regalati un Sogno", page_icon="🍀", layout="centered")

# 2. Stile CSS per i numeri
st.markdown("""
    <style>
    .stNumberInput input { font-size: 20px !important; text-align: center !important; }
    .main { background-color: #f5f7f9; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍀 Regalati un Sogno")

# 3. Schede
tab1, tab2, tab3 = st.tabs(["🔍 Verifica", "📜 Schedine", "📊 Archivio e Quote"])

with tab1:
    st.subheader("Inserimento Numeri")
    
    # Campo per incollare
    incollati = st.text_input("Incolla qui l'estrazione:", placeholder="es: 10 20 30 40 50 60")
    
    # Estrazione automatica dei numeri dal testo incollato
    numeri_estratti_da_testo = re.findall(r'\d+', incollati) if incollati else []
    
    # Prepariamo i 6 numeri finali da usare per il calcolo
    final_nums = []

    # Expander per inserimento manuale o controllo
    with st.expander("Modifica o inserisci a mano"):
        st.write("I numeri sotto si aggiornano se incolli sopra:")
        cols = st.columns(3)
        cols2 = st.columns(3)
        
        for i in range(6):
            # Se abbiamo un numero incollato lo usiamo, altrimenti lasciamo vuoto (None)
            default_val = int(numeri_estratti_da_testo[i]) if len(numeri_estratti_da_testo) > i else None
            
            # Posizioniamo le caselle nelle colonne
            target_col = cols[i] if i < 3 else cols2[i-3]
            
            n = target_col.number_input(f"{i+1}°", 1, 90, value=default_val, key=f"n{i}")
            final_nums.append(n)

    st.markdown("---")

    # BOTTONE VERIFICA
    if st.button("VERIFICA ORA 🚀", use_container_width=True):
        # Controlliamo se abbiamo tutti e 6 i numeri (sia da incolla che manuali)
        if all(v is not None for v in final_nums):
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
            st.error("Mancano dei numeri. Incolla l'estrazione o compila le 6 caselle manuali.")

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
    premio = st.number_input("Importo totale vinto (€)", min_value=0.0, step=0.50, value=0.0)
    if premio > 0:
        quota = premio / 6
        st.success(f"💎 Quota per ogni socio: **{quota:.2f} €**")
