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
    
    # CAMPO COPIA E INCOLLA (Sempre visibile)
    incollati = st.text_input("Incolla qui l'estrazione:", placeholder="es: 10 20 30 40 50 60")
    
    # Logica per estrarre i numeri
    lista_numeri = []
    if incollati:
        lista_numeri = re.findall(r'\d+', incollati)
        if len(lista_numeri) >= 6:
            st.success(f"✅ Rilevati: {', '.join(lista_numeri[:6])}")
        else:
            st.warning(f"Trovati solo {len(lista_numeri)} numeri.")

    # CASELLE MANUALI (Nascoste dentro un menu espandibile)
    with st.expander("Modifica o inserisci a mano"):
        st.write("Puoi correggere i numeri qui sotto:")
        c1, c2, c3 = st.columns(3)
        val1 = int(lista_numeri[0]) if len(lista_numeri) >= 1 else None
        val2 = int(lista_numeri[1]) if len(lista_numeri) >= 2 else None
        val3 = int(lista_numeri[2]) if len(lista_numeri) >= 3 else None
        
        n1 = c1.number_input("1°", 1, 90, value=val1, key="v1")
        n2 = c2.number_input("2°", 1, 90, value=val2, key="v2")
        n3 = c3.number_input("3°", 1, 90, value=val3, key="v3")
        
        c4, c5, c6 = st.columns(3)
        val4 = int(lista_numeri[3]) if len(lista_numeri) >= 4 else None
        val5 = int(lista_numeri[4]) if len(lista_numeri) >= 5 else None
        val6 = int(lista_numeri[5]) if len(lista_numeri) >= 6 else None
        
        n4 = c4.number_input("4°", 1, 90, value=val4, key="v4")
        n5 = c5.number_input("5°", 1, 90, value=val5, key="v5")
        n6 = c6.number_input("6°", 1, 90, value=val6, key="v6")

    st.markdown("---")

    # BOTTONE VERIFICA
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
            st.error("Inserisci tutti i 6 numeri (usa il campo incolla o il menu manuale).")

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
