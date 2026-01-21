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
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .tasse-box {
        text-align: center; background-color: #fff3cd; padding: 10px;
        border-radius: 8px; border: 1px solid #ffeeba; margin-bottom: 15px;
        font-size: 14px; color: #856404;
    }
    .quota-valore { font-size: 36px; font-weight: 800; color: #1b5e20; display: block; }
    .quota-lettere { font-size: 15px; color: #388e3c; font-style: italic; display: block; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍀 Regalati un Sogno")

# --- FUNZIONI ---
def play_audio(url):
    audio_html = f'<audio autoplay="true" style="display:none;"><source src="{url}" type="audio/mpeg"></audio>'
    st.components.v1.html(audio_html, height=0)

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

def format_euro(valore):
    return f"{valore:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def distribuisci_numeri():
    if st.session_state.incolla_qui:
        numeri = re.findall(r'\d+', st.session_state.incolla_qui)
        if len(numeri) >= 6:
            for i in range(6): st.session_state[f"n{i}"] = int(numeri[i])

# --- INTERFACCIA ---
tab1, tab2, tab3 = st.tabs(["🔍 Verifica", "📜 Schedine", "💰 Calcolo Netto"])

with tab1:
    st.info("🔗 **Passo 1:** Copia i numeri dal sito ufficiale")
    st.link_button("Vai al sito ADM 🏛️", "https://www.adm.gov.it/portale/monopoli/giochi/giochi_num_total/superenalotto", use_container_width=True)
    st.divider()
    st.subheader("📋 Passo 2: Incolla e Verifica")
    st.text_input("Incolla la sequenza (spazio o trattino) e premi INVIO:", key="incolla_qui", on_change=distribuisci_numeri)
    
    with st.expander("👁️ Vedi/Modifica i numeri rilevati", expanded=False):
        c1, c2, c3 = st.columns(3); c4, c5, c6 = st.columns(3)
        n0 = c1.number_input("1°", 1, 90, key="n0"); n1 = c2.number_input("2°", 1, 90, key="n1")
        n2 = c3.number_input("3°", 1, 90, key="n2"); n3 = c4.number_input("4°", 1, 90, key="n3")
        n4 = c5.number_input("5°", 1, 90, key="n4"); n5 = c6.number_input("6°", 1, 90, key="n5")

    if st.button("VERIFICA ORA 🚀", type="primary", use_container_width=True):
        final_nums = [n0, n1, n2, n3, n4, n5]
        if all(final_nums):
            set_estratti = set(final_nums)
            SCHEDINE = [{3, 10, 17, 40, 85, 86}, {10, 17, 19, 40, 85, 86}, {17, 19, 40, 75, 85, 86}, {3, 19, 40, 75, 85, 86}, {3, 10, 19, 75, 85, 86}, {3, 10, 17, 75, 85, 86}]
            vincite = []
            for i, schedina in enumerate(SCHEDINE, 1):
                indovinati = sorted(list(schedina.intersection(set_estratti)))
                if len(indovinati) >= 2: vincite.append((i, len(indovinati), indovinati))
            
            if vincite:
                st.balloons()
                play_audio("https://www.myinstants.com/media/sounds/ta-da.mp3")
                for v in vincite: st.success(f"🔥 **SCHEDINA {v[0]}:** {v[1]} PUNTI! ({v[2]})")
            else:
                play_audio("https://www.myinstants.com/media/sounds/sad-trombone.mp3")
                st.warning("Nessuna vincita. Ritenta!")

with tab2:
    st.subheader("Le Sestine del Gruppo")
    for i, s in enumerate(["03-10-17-40-85-86", "10-17-19-40-85-86", "17-19-40-75-85-86", "03-19-40-75-85-86", "03-10-19-75-85-86", "03-10-17-75-85-86"], 1):
        st.text(f"Schedina {i}: {s}")

with tab3:
    st.subheader("💰 Calcolo Netto in Tasca")
    premio_lordo = st.number_input("Inserisci la vincita totale lorda (€)", min_value=0.0, step=10.0)
    
    if premio_lordo > 0:
        # Calcolo Tassazione (20% sulla parte eccedente i 500€)
        if premio_lordo > 500:
            tasse = (premio_lordo - 500) * 0.20
            premio_netto = premio_lordo - tasse
        else:
            tasse = 0.0
            premio_netto = premio_lordo
        
        quota_netta = round(premio_netto / 6, 2)
        
        # UI Tasse
        if tasse > 0:
            st.markdown(f"""<div class="tasse-box">
                Sulla quota eccedente i 500€ è stata applicata la ritenuta del 20% (-{format_euro(tasse)} €).<br>
                <b>Totale Netto per il gruppo: {format_euro(premio_netto)} €</b>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="tasse-box" style="color:#155724; background-color:#d4edda; border-color:#c3e6cb;">Vincita inferiore a 500€: esente da tasse!</div>', unsafe_allow_html=True)

        # UI Quota Finale
        lettere = f"{numero_in_lettere(int(quota_netta))}/{int(round((quota_netta - int(quota_netta)) * 100)):02d}"
        st.markdown(f"""
        <div class="quota-box">
            <span style="color:#2e7d32; font-size:14px; text-transform:uppercase; font-weight:600;">Quota netta per ogni socio (6)</span>
            <span class="quota-valore">{format_euro(quota_netta)} €</span>
            <span class="quota-lettere">({lettere})</span>
        </div>
        """, unsafe_allow_html=True)
