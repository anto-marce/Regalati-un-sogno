import streamlit as st
import re

# 1. IMPOSTAZIONI PAGINA
st.set_page_config(page_title="Regalati un Sogno", page_icon="🍀", layout="centered")

# 2. STILE CSS
st.markdown("""
    <style>
    div[data-testid="stNumberInput"] input { 
        font-size: 22px !important; text-align: center !important; font-weight: 900 !important; 
        color: #000000 !important; background-color: #ffffff !important; 
        border: 2px solid #cccccc !important; border-radius: 5px;
    }
    .main { background-color: #f9fafb; }
    .quota-box {
        text-align: center; background-color: #e8f5e9; padding: 25px;
        border-radius: 12px; border: 2px solid #c8e6c9; margin-top: 15px;
    }
    .quota-valore { font-size: 36px; font-weight: 800; color: #1b5e20; display: block; }
    .quota-lettere { font-size: 15px; color: #388e3c; font-style: italic; display: block; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍀 Regalati un Sogno")

# --- FUNZIONE AUDIO ---
def play_audio(url):
    audio_html = f"""
        <audio autoplay="true" style="display:none;">
            <source src="{url}" type="audio/mpeg">
        </audio>
    """
    st.components.v1.html(audio_html, height=0)

# --- FUNZIONI DI SUPPORTO ---
def numero_in_lettere(n):
    if n == 0: return "zero"
    units = ["", "uno", "due", "tre", "quattro", "cinque", "sei", "sette", "otto", "nove"]
    teens = ["dieci", "undici", "dodici", "tredici", "quattordici", "quindici", "sedici", "diciassette", "diciotto", "diciannove"]
    tens = ["", "", "venti", "trenta", "quaranta", "cinquanta", "sessanta", "settanta", "ottanta", "novanta"]
    def convert_999(num):
        res = ""
        h, t, u = num // 100, (num % 100) // 10, num % 10
        if h > 0: res += "cento" if h == 1 else units[h] + "cento"
        if t == 1: res += teens[u]
        else:
            res += tens[t]
            if u > 0:
                if res and res[-1] in "ai" and units[u][0] in "ua": res = res[:-1]
                res += units[u]
        return res
    def convert_recursive(num):
        if num < 1000: return convert_999(num)
        if num < 1000000:
            m, r = num // 1000, num % 1000
            return ("mille" if m == 1 else convert_999(m) + "mila") + convert_999(r)
        m, r = num // 1000000, num % 1000000
        return ("unmilione" if m == 1 else convert_999(m) + "milioni") + convert_recursive(r)
    return convert_recursive(int(n))

def distribuisci_numeri():
    if st.session_state.incolla_qui:
        # Estrae i numeri indipendentemente dal separatore (spazio, trattino, virgola, ecc.)
        numeri = re.findall(r'\d+', st.session_state.incolla_qui)
        if len(numeri) >= 6:
            for i in range(6): st.session_state[f"n{i}"] = int(numeri[i])

# --- INTERFACCIA ---
tab1, tab2, tab3 = st.tabs(["🔍 Verifica", "📜 Schedine", "💰 Calcolo"])

with tab1:
    st.info("🔗 **Passo 1:** Copia i numeri dal sito ufficiale")
    st.link_button("Vai al sito ADM 🏛️", "https://www.adm.gov.it/portale/monopoli/giochi/giochi_num_total/superenalotto", use_container_width=True)
    st.divider()
    
    st.subheader("📋 Passo 2: Incolla e Verifica")
    
    # MODIFICA: Istruzioni più specifiche
    st.text_input(
        "Incolla la sequenza (numeri separati da uno spazio o un trattino) e premi INVIO:", 
        key="incolla_qui", 
        on_change=distribuisci_numeri,
        placeholder="Es: 10 20 30 40 50 60 oppure 10-20-30-40-50-60"
    )
    
    with st.expander("👁️ Vedi/Modifica i numeri rilevati", expanded=False):
        c1, c2, c3 = st.columns(3); c4, c5, c6 = st.columns(3)
        n0 = c1.number_input("1°", 1, 90, key="n0"); n1 = c2.number_input("2°", 1, 90, key="n1")
        n2 = c3.number_input("3°", 1, 90, key="n2"); n3 = c4.number_input("4°", 1, 90, key="n3")
        n4 = c5.number_input("5°", 1, 90, key="n4"); n5 = c6.number_input("6°", 1, 90, key="n5")

    st.write("") 
    
    if st.button("VERIFICA ORA 🚀", type="primary", use_container_width=True):
        final_nums = [n0, n1, n2, n3, n4, n5]
        if all(final_nums):
            set_estratti = set(final_nums)
            SCHEDINE = [{3, 10, 17, 40, 85, 86}, {10, 17, 19, 40, 85, 86}, {17, 19, 40, 75, 85, 86}, {3, 19, 40, 75, 85, 86}, {3, 10, 19, 75, 85, 86}, {3, 10, 17, 75, 85, 86}]
            
            vincite = []
            for i, schedina in enumerate(SCHEDINE, 1):
                indovinati = sorted(list(schedina.intersection(set_estratti)))
                if len(indovinati) >= 2:
                    vincite.append((i, len(indovinati), indovinati))
            
            if vincite:
                st.balloons()
                play_audio("https://www.myinstants.com/media/sounds/ta-da.mp3")
                for v in vincite:
                    st.success(f"🔥 **SCHEDINA {v[0]}:** {v[1]} PUNTI! ({v[2]})")
            else:
                play_audio("https://www.myinstants.com/media/sounds/sad-trombone.mp3")
                st.warning("Nessuna vincita. Ritenta!")
        else:
            st.error("⚠️ Inserisci tutti i numeri.")

with tab2:
    st.subheader("Le Sestine del Gruppo")
    for i, s in enumerate(["03-10-17-40-85-86", "10-17-19-40-85-86", "17-19-40-75-85-86", "03-19-40-75-85-86", "03-10-19-75-85-86", "03-10-17-75-85-86"], 1):
        st.text(f"Schedina {i}: {s}")

with tab3:
    st.subheader("💰 Divisione Vincita")
    premio = st.number_input("Totale (€)", min_value=0.0, step=10.0)
    if premio > 0:
        quota = round(premio / 6, 2)
        quota_f = f"{quota:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        lettere = f"{numero_in_lettere(int(quota))}/{int(round((quota - int(quota)) * 100)):02d}"
        st.markdown(f'<div class="quota-box"><span style="color:#2e7d32; font-size:14px;">Quota individuale</span><span class="quota-valore">{quota_f} €</span><span class="quota-lettere">({lettere})</span></div>', unsafe_allow_html=True)
