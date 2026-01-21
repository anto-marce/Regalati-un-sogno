import streamlit as st
import re

# 1. Impostazioni Pagina
st.set_page_config(page_title="Regalati un Sogno", page_icon="🍀", layout="centered")

# 2. Stile CSS
st.markdown("""
    <style>
    .stNumberInput input { font-size: 22px !important; text-align: center !important; font-weight: bold; }
    .main { background-color: #f8f9fa; }
    div[data-testid="stExpander"] { background-color: white; border-radius: 10px; }
    .quota-box {
        text-align: center;
        background-color: #d4edda;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #c3e6cb;
        margin-top: 10px;
    }
    .quota-valore {
        font-size: 32px;
        font-weight: bold;
        color: #155724;
        display: block;
    }
    .quota-lettere {
        font-size: 16px;
        color: #155724;
        font-style: italic;
        display: block;
        margin-top: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🍀 Regalati un Sogno")

# --- FUNZIONE PER NUMERI IN LETTERE ---
def numero_in_lettere(n):
    units = ["", "uno", "due", "tre", "quattro", "cinque", "sei", "sette", "otto", "nove"]
    teens = ["dieci", "undici", "dodici", "tredici", "quattordici", "quindici", "sedici", "diciassette", "diciotto", "diciannove"]
    tens = ["", "", "venti", "trenta", "quaranta", "cinquanta", "sessanta", "settanta", "ottanta", "novanta"]
    
    def convert_chunk(num):
        res = ""
        h = num // 100
        t = (num % 100) // 10
        u = num % 10
        if h > 0:
            res += "cento" if h == 1 else units[h] + "cento"
        if t == 1:
            res += teens[u]
        else:
            res += tens[t]
            if u > 0:
                if res and res[-1] in "ai" and units[u][0] in "ua":
                    res = res[:-1]
                res += units[u]
        return res

    n = int(n)
    if n == 0: return "zero"
    if n < 1000:
        return convert_chunk(n)
    if n < 1000000:
        m = n // 1000
        r = n % 1000
        prefix = "mille" if m == 1 else convert_chunk(m) + "mila"
        return prefix + convert_chunk(r)
    return "cifra oltre un milione"

# --- FUNZIONE LOGICA DI SMISTAMENTO ---
def distribuisci_numeri():
    if st.session_state.incolla_qui:
        numeri = re.findall(r'\d+', st.session_state.incolla_qui)
        if len(numeri) >= 6:
            for i in range(6):
                st.session_state[f"n{i}"] = int(numeri[i])

# 3. Schede
tab1, tab2, tab3 = st.tabs(["🔍 Verifica Vincita", "📜 Il Nostro Sistema", "💰 Calcolo Quote"])

with tab1:
    st.info("🎯 **Passaggio 1:** Prendi i numeri dal sito ufficiale")
    st.link_button("Apri Sito Ufficiale ADM 🏛️", "https://www.adm.gov.it/portale/monopoli/giochi/giochi_num_total/superenalotto", use_container_width=True)
    st.write("---")
    st.subheader("2. Incolla i numeri estratti")
    st.text_input("Incolla qui la stringa e premi INVIO:", key="incolla_qui", on_change=distribuisci_numeri)
    
    with st.expander("Numeri rilevati", expanded=True):
        c1, c2, c3 = st.columns(3); c4, c5, c6 = st.columns(3)
        n0 = c1.number_input("1°", 1, 90, key="n0"); n1 = c2.number_input("2°", 1, 90, key="n1")
        n2 = c3.number_input("3°", 1, 90, key="n2"); n3 = c4.number_input("4°", 1, 90, key="n3")
        n4 = c5.number_input("5°", 1, 90, key="n4"); n5 = c6.number_input("6°", 1, 90, key="n5")

    if st.button("CONTROLLA SCHEDINE 🚀", use_container_width=True):
        final_nums = [n0, n1, n2, n3, n4, n5]
        if all(final_nums):
            set_estratti = set(final_nums)
            SCHEDINE = [{3, 10, 17, 40, 85, 86}, {10, 17, 19, 40, 85, 86}, {17, 19, 40, 75, 85, 86}, {3, 19, 40, 75, 85, 86}, {3, 10, 19, 75, 85, 86}, {3, 10, 17, 75, 85, 86}]
            vincite_trovate = False
            for i, schedina in enumerate(SCHEDINE, 1):
                indovinati = sorted(list(schedina.intersection(set_estratti)))
                if len(indovinati) >= 2:
                    st.balloons()
                    st.success(f"🔥 SCHEDINA {i}: {len(indovinati)} PUNTI!")
                    st.write(f"Numeri centrati: {indovinati}")
                    vincite_trovate = True
            if not vincite_trovate: st.info("Nessuna vincita.")

with tab2:
    st.subheader("Le Sestine del Gruppo")
    sestine = ["03-10-17-40-85-86", "10-17-19-40-85-86", "17-19-40-75-85-86", "03-19-40-75-85-86", "03-10-19-75-85-86", "03-10-17-75-85-86"]
    for i, s in enumerate(sestine, 1): st.code(f"Schedina {i}: {s}", language="text")

with tab3:
    st.subheader("💰 Divisione Premio")
    premio = st.number_input("Totale vinto (€)", min_value=0.0, step=10.0, format="%.2f")
    
    if premio > 0:
        quota = premio / 6
        quota_f = f"{quota:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        centesimi = int(round((quota - int(quota)) * 100))
        lettere = f"{numero_in_lettere(int(quota))}/{centesimi:02d}"
        
        # BOX RISULTATO CENTRATO
        st.markdown(f"""
        <div class="quota-box">
            <span style="color: #155724; font-size: 14px; text-transform: uppercase;">Quota individuale (6 persone)</span>
            <span class="quota-valore">{quota_f} €</span>
            <span class="quota-lettere">({lettere})</span>
        </div>
        """, unsafe_allow_html=True)
