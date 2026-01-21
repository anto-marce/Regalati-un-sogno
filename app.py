import streamlit as st
import re

# 1. Impostazioni Pagina
st.set_page_config(page_title="Regalati un Sogno", page_icon="🍀", layout="centered")

# 2. Stile CSS
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
    
    # Inizializziamo i numeri nella memoria del browser (Session State)
    if 'numeri_fissi' not in st.session_state:
        st.session_state.numeri_fissi = [None] * 6

    # CAMPO COPIA E INCOLLA
    incollati = st.text_input("1. Incolla qui l'estrazione:", placeholder="es: 10 20 30 40 50 60")
    
    if st.button("Carica Numeri Incollati 📥", use_container_width=True):
        if incollati:
            trovati = re.findall(r'\d+', incollati)
            if len(trovati) >= 6:
                # Trasformiamo i primi 6 numeri trovati in numeri interi e li salviamo
                st.session_state.numeri_fissi = [int(x) for x in trovati[:6]]
                st.success(f"✅ Numeri caricati: {st.session_state.numeri_fissi}")
            else:
                st.error(f"Ho trovato solo {len(trovati)} numeri. Ne servono 6!")
        else:
            st.warning("Il campo è vuoto. Incolla prima i numeri.")

    # CASELLE MANUALI (Nascoste)
    with st.expander("2. Modifica o inserisci a mano"):
        st.write("Puoi correggere i numeri qui:")
        c1, c2, c3 = st.columns(3)
        c4, c5, c6 = st.columns(3)
        col_list = [c1, c2, c3, c4, c5, c6]
        
        final_nums = []
        for i in range(6):
            valore_iniziale = st.session_state.numeri_fissi[i]
            # Creiamo la casella
            n = col_list[i].number_input(f"{i+1}°", 1, 90, value=valore_iniziale, key=f"casella_{i}")
            final_nums.append(n)

    st.markdown("---")

    # BOTTONE VERIFICA FINALE
    if st.button("VERIFICA VINCITA 🚀", use_container_width=True):
        # Usiamo i numeri delle caselle (che sono stati aggiornati dal tasto carica)
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
            st.error("Mancano dei numeri. Incolla i numeri e clicca 'Carica' oppure inseriscili a mano.")

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
