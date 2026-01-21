import streamlit as st
import re

# 1. IMPOSTAZIONI PAGINA
st.set_page_config(
    page_title="Regalati un Sogno", 
    page_icon="🍀", 
    layout="centered"
)

# 2. STILE CSS AD ALTO CONTRASTO
st.markdown("""
    <style>
    /* FORZA I CAMPI NUMERICI AD ESSERE BIANCHI CON TESTO NERO */
    div[data-testid="stNumberInput"] input { 
        font-size: 22px !important; 
        text-align: center !important; 
        font-weight: 900 !important; 
        color: #000000 !important;       /* Testo Nero */
        background-color: #ffffff !important; /* Sfondo Bianco */
        border: 2px solid #cccccc !important; /* Bordo Grigio visibile */
        border-radius: 5px;
    }
    
    /* Sfondo generale pulito */
    .main { 
        background-color: #f9fafb; 
    }
    
    /* Stile Expander */
    div[data-testid="stExpander"] { 
        background-color: #ffffff; 
        border: 1px solid #e0e0e0; 
        border-radius: 8px; 
        color: #000000 !important;
    }
    
    /* Box Quota (Tab 3) */
    .quota-box {
        text-align: center;
        background-color: #e8f5e9;
        padding: 25px;
        border-radius: 12px;
        border: 2px solid #c8e6c9;
        margin-top: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .quota-titolo {
        color: #2e7d32;
        font-size: 14px; 
        text-transform: uppercase; 
        letter-spacing: 1px;
        font-weight: 600;
    }
    .quota-valore {
        font-size: 36px;
        font-weight: 800;
        color: #1b5e20;
        display: block;
        margin: 10px 0;
    }
    .quota-lettere {
        font-size: 15px;
        color: #388e3c;
        font-style: italic;
        display: block;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🍀 Regalati un Sogno")

# --- FUNZIONI ---

def numero_in_lettere(n):
    if n == 0: return "zero"
    units = ["", "uno", "due", "tre", "quattro", "cinque", "sei", "sette", "otto", "nove"]
    teens = ["dieci", "undici", "dodici", "tredici", "quattordici", "quindici", "sedici", "diciassette", "diciotto", "diciannove"]
    tens = ["", "", "venti", "trenta", "quaranta", "cinquanta", "sessanta", "settanta", "ottanta", "novanta"]

    def convert_999(num):
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

    def convert_recursive(num):
        if num < 1000: return convert_999(num)
        if num < 1000000:
            m = num // 1000
            r = num % 1000
            prefix = "mille" if m == 1 else convert_999(m) + "mila"
            return prefix + convert_999(r)
        if num < 1000000000:
            m = num // 1000000
            r = num % 1000000
            prefix = "unmilione" if m == 1 else convert_999(m) + "milioni"
            return prefix + convert_recursive(r)
        return "cifra astronomica"

    return convert_recursive(int(n))

def distribuisci_numeri():
    if st.session_state.incolla_qui:
        numeri = re.findall(r'\d+', st.session_state.incolla_qui)
        if len(numeri) >= 6:
            for i in range(6):
                st.session_state[f"n{i}"] = int(numeri[i])

# --- INTERFACCIA ---

tab1, tab2, tab3 = st.tabs(["🔍 Verifica", "📜 Schedine", "💰 Calcolo"])

# TAB 1
with tab1:
    st.info("🔗 **Passo 1:** Copia i numeri dal sito ufficiale")
    st.link_button("Vai al sito ADM 🏛️", "https://www.adm.gov.it/portale/monopoli/giochi/giochi_num_total/superenalotto", use_container_width=True)
    
    st.divider()
    
    st.subheader("📋 Passo 2: Incolla e Verifica")
    st.text_input("Incolla la sequenza e premi INVIO:", key="incolla_qui", on_change=distribuisci_numeri, placeholder="Es: 10 22 35 48 50 90")
    
    # Expander chiuso di default
    with st.expander("👁️ Vedi/Modifica i numeri rilevati", expanded=False):
        st.caption("Questi sono i numeri rilevati:")
        c1, c2, c3 = st.columns(3); c4, c5, c6 = st.columns(3)
        n0 = c1.number_input("1°", 1, 90, key="n0")
        n1 = c2.number_input("2°", 1, 90, key="n1")
        n2 = c3.number_input("3°", 1, 90, key="n2")
        n3 = c4.number_input("4°", 1, 90, key="n3")
        n4 = c5.number_input("5°", 1, 90, key="n4")
        n5 = c6.number_input("6°", 1, 90, key="n5")

    st.write("") 
    
    if st.button("VERIFICA ORA 🚀", type="primary", use_container_width=True):
        final_nums = [n0, n1, n2, n3, n4, n5]
        if all(final_nums):
            set_estratti = set(final_nums)
            SCHEDINE = [{3, 10, 17, 40, 85, 86}, {10, 17, 19, 40, 85, 86}, {17, 19, 40, 75, 85, 86}, {3, 19, 40, 75, 85, 86}, {3, 10, 19, 75, 85, 86}, {3, 10, 17, 75, 85, 86}]
            
            vincite_trovate = False
            for i, schedina in enumerate(SCHEDINE, 1):
                indovinati = sorted(list(schedina.intersection(set_estratti)))
                if len(indovinati) >= 2:
                    st.balloons()
                    st.success(f"🔥 **SCHEDINA {i}:** {len(indovinati)} PUNTI! (Centrati: {indovinati})")
                    vincite_trovate = True
            if not vincite_trovate: st.warning("Nessuna vincita (minimo 2 punti). Ritenta!")
        else: st.error("⚠️ Inserisci o incolla tutti i 6 numeri.")

# TAB 2
with tab2:
    st.subheader("Le Sestine del Gruppo")
    sestine = ["03 - 10 - 17 - 40 - 85 - 86", "10 - 17 - 19 - 40 - 85 - 86", "17 - 19 - 40 - 75 - 85 - 86", "03 - 19 - 40 - 75 - 85 - 86", "03 - 10 - 19 - 75 - 85 - 86", "03 - 10 - 17 - 75 - 85 - 86"]
    for i, s in enumerate(sestine, 1):
        st.text(f"Schedina {i}: {s}")

# TAB 3
with tab3:
    st.subheader("💰 Divisione Vincita")
    st.write("Inserisci l'importo totale vinto:")
    premio = st.number_input("Totale (€)", min_value=0.0, step=10.0)
    
    if premio > 0:
        quota = round(premio / 6, 2)
        def format_it(valore): return f"{valore:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        quota_f = format_it(quota)
        centesimi = int(round((quota - int(quota)) * 100))
        testo_intero = numero_in_lettere(int(quota))
        lettere = f"{testo_intero}/{centesimi:02d}"
        
        st.markdown(f"""
        <div class="quota-box">
            <span class="quota-titolo">Quota individuale (6 soci)</span>
            <span class="quota-valore">{quota_f} €</span>
            <span class="quota-lettere">({lettere})</span>
        </div>
        """, unsafe_allow_html=True)
