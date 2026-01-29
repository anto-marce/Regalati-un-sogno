import streamlit as st
import re
import pandas as pd
from datetime import datetime, timedelta
import urllib.parse
from num2words import num2words
import random

# 1. IMPOSTAZIONI PAGINA
st.set_page_config(page_title="Regalati un Sogno", page_icon="🍀", layout="centered")

# 2. STILE CSS
st.markdown("""
    <style>
    .stSelectbox div[data-baseweb="select"] { border: 2px solid #003366 !important; border-radius: 10px; }
    .quota-box { text-align: center; background-color: #e8f5e9; padding: 20px; border-radius: 12px; border: 2px solid #c8e6c9; margin-top: 15px; }
    .quota-valore { font-size: 32px; font-weight: 800; color: #1b5e20; display: block; }
    .quota-testo { font-size: 18px; font-style: italic; color: #2e7d32; display: block; text-transform: capitalize; }
    .ams-button { display: block; padding: 12px; background-color: #003366; color: white !important; text-decoration: none; border-radius: 8px; font-weight: bold; text-align: center; margin-bottom: 20px; }
    .wa-button { display: block; padding: 12px; background-color: #25D366; color: white !important; text-decoration: none; border-radius: 8px; font-weight: bold; text-align: center; margin-top: 10px; }
    .wa-fail { background-color: #6c757d !important; }
    .status-red { background-color: #f8d7da; color: #721c24; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; }
    .status-green { background-color: #d4edda; color: #155724; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; }
    .countdown-text { font-size: 18px; font-weight: bold; color: #d32f2f; text-align: center; background: #fff3e0; padding: 10px; border-radius: 10px; border: 1px solid #ffe0b2; }
    .lotto-ball { background-color: #FFD700; color: black; border-radius: 50%; padding: 5px 8px; margin: 2px; font-weight: bold; border: 1px solid #b8860b; display: inline-block; min-width: 32px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 3. LOGICA CALENDARIO UFFICIALE (Ore 19:00)
def calcola_prossima_estrazione():
    adesso = datetime.now()
    giorni_estrazione = [1, 3, 4, 5] # Mar, Gio, Ven, Sab
    prossima = adesso.replace(hour=19, minute=0, second=0, microsecond=0)
    
    if adesso.weekday() not in giorni_estrazione or adesso >= prossima:
        for i in range(1, 8):
            test_data = adesso + timedelta(days=i)
            if test_data.weekday() in giorni_estrazione:
                return test_data.replace(hour=19, minute=0, second=0, microsecond=0)
    return prossima

now = datetime.now()
target = calcola_prossima_estrazione()
diff = target - now
giorni = diff.days
ore, resto = divmod(diff.seconds, 3600)
minuti, _ = divmod(resto, 60)

testo_timer = f"{ore}h {minuti}m"
if giorni > 0:
    testo_timer = f"{giorni}g " + testo_timer

# 4. FUNZIONI SUPPORTO
def salva_vincita(punti, importo_netto):
    nuovo_dato = {'Data': datetime.now().strftime("%d/%m/%Y %H:%M"), 'Punti': punti, 'Euro_Netto': importo_netto}
    try:
        df = pd.read_csv('archivio_vincite.csv')
        df = pd.concat([df, pd.DataFrame([nuovo_dato])], ignore_index=True)
    except:
        df = pd.DataFrame([nuovo_dato])
    df.to_csv('archivio_vincite.csv', index=False)

def carica_archivio():
    try: return pd.read_csv('archivio_vincite.csv')
    except: return pd.DataFrame(columns=['Data', 'Punti', 'Euro_Netto'])

# --- INTERFACCIA ---
st.title("🍀 Regalati un Sogno")
st.markdown(f'<div class="countdown-text">⏳ Prossima estrazione (ore 19:00): {testo_timer}</div>', unsafe_allow_html=True)

scelta = st.selectbox("🧭 COSA VUOI FARE?", ["🔍 Verifica Vincita", "📅 Stato Abbonamento", "💰 Calcolo Quote", "🏛️ Il Bottino"])
st.divider()

if scelta == "🔍 Verifica Vincita":
    st.subheader("📋 Verifica Estrazione")
    st.markdown('<a href="https://www.adm.gov.it/portale/monopoli/giochi/giochi_num_total/superenalotto" target="_blank" class="ams-button">➡️ PASSO 1: Sito Ufficiale AMS</a>', unsafe_allow_html=True)

    if 'n0' not in st.session_state:
        for i in range(6): st.session_state[f'n{i}'] = 1

    def distribuisci_numeri():
        if st.session_state.incolla_qui:
            numeri = re.findall(r'\d+', st.session_state.incolla_qui)
            if len(numeri) >= 6:
                for i in range(6): st.session_state[f"n{i}"] = int(numeri[i])

    st.text_input("PASSO 2: Incolla numeri e premi INVIO:", key="incolla_qui", on_change=distribuisci_numeri)
    
    with st.expander("👁️ Modifica Numeri"):
        cols = st.columns(3)
        final_nums = []
        for i in range(6):
            with cols[i % 3]:
                final_nums.append(st.number_input(f"{i+1}°", 1, 90, key=f"n{i}"))

    if st.button("VERIFICA ORA 🚀", type="primary", use_container_width=True):
        set_estratti = set(final_nums)
        SCHEDINE = [{3,10,17,40,85,86}, {10,17,19,40,85,86}, {17,19,40,75,85,86}, {3,19,40,75,85,86}, {3,10,19,75,85,86}, {3,10,17,75,85,86}]
        vincite = []
        for i, sch in enumerate(SCHEDINE, 1):
            indovinati = sorted(list(sch.intersection(set_estratti)))
            if len(indovinati) >= 2: vincite.append((i, len(indovinati), indovinati))
        
        if vincite:
            st.balloons()
            st.components.v1.html('<audio autoplay><source src="https://www.myinstants.com/media/sounds/ta-da.mp3" type="audio/mpeg"></audio>', height=0)
            
            # --- MESSAGGIO VITTORIA ---
            testo_wa = "❌ *ESITO ESTRAZIONE*\n\n🥳 *ABBIAMO VINTO!*\n\n"
            for v in vincite:
                st.success(f"🔥 **SCHEDINA {v[0]}:** {v[1]} PUNTI! ({v[2]})")
                testo_wa += f"✅ Schedina {v[0]}: *{v[1]} Punti* ({', '.join(map(str, v[2]))})\n"
            
            link_vittoria = f"https://wa.me/?text={urllib.parse.quote(testo_wa)}"
            st.markdown(f'<a href="{link_vittoria}" target="_blank" class="wa-button">📲 PASSO 3: Invia Vincita</a>', unsafe_allow_html=True)
        else:
            st.components.v1.html('<audio autoplay><source src="https://www.myinstants.com/media/sounds/sad-trombone.mp3" type="audio/mpeg"></audio>', height=0)
            st.warning("Nessuna vincita rilevata. 💸")
            
            # --- MESSAGGI SCONFITTA (Random + Intestazione Fissa) ---
            INTESTAZIONE_FISSA = "❌ *ESITO ESTRAZIONE*\n\n"
            
            FRASI_RANDOM = [
                "Niente da fare ragazzi. Anche stasera il jet privato lo compriamo domani. Si torna a lavorare!",
                "🐢 *CALMA*: Il successo è un viaggio, non una meta. Il nostro viaggio è solo molto, molto lento.",
                "🍝 *DIETA*: Stasera niente caviale, si torna a pane e cipolla. Ma con dignità!",
                "🏗️ *LAVORI IN CORSO*: La fortuna ci sta cercando, ma ha trovato traffico in tangenziale.",
                "🤏 *QUASI*: Ci siamo andati vicini... come io sono vicino a diventare astronauta.",
                "📉 *STRATEGIA*: Non abbiamo perso, abbiamo solo posticipato la gloria a data da destinarsi.",
                "🧘 *ZEN*: I soldi non danno la felicità. (Soprattutto quelli che non abbiamo vinto stasera).",
                "🛶 *NAUFRAGHI*: Siamo sulla stessa barca. Ed è una barca a remi. Molto piccoli.",
                "📵 *OFFLINE*: La Dea Bendata ci ha appena bloccato su WhatsApp. Riproveremo.",
                "🕯️ *SPERANZA*: Ragazzi, accendiamo un cero in gruppo, che la statistica da sola non basta più!",
                "🤔 Ho come il sospetto che i numeri estratti siano esattamente quelli che NON abbiamo giocato. Coincidenze? Io non credo.",
                "😅 Guardate il lato positivo: anche stasera abbiamo risparmiato lo stress di dover gestire milioni di euro. È un sollievo, vero?",
                "⛲ Ragazzi, disdite i voli per Honolulu. Per questa settimana il massimo che possiamo permetterci è un tuffo nella fontana del centro.",
                "🛌 La Dea Bendata ci deve ormai così tanti favori che la prossima volta dovrebbe venirci a rimboccare le coperte.",
                "🤖 Ho chiesto all'intelligenza artificiale quando vinceremo. Mi ha risposto con l'emoji che ride. Non è un buon segno.",
                "🤡 I numeri erano giusti, è l'ordine di estrazione che era completamente sbagliato. Tecnicamente è un successo morale.",
                "🐟 Aragosta rimandata a data da destinarsi. Stasera si festeggia con una scatoletta di tonno... di sottomarca.",
                "🏔️ Vado a vivere in un monastero in Tibet. Se la fortuna non mi trova qui, magari mi trova lì. Ci sentiamo alla prossima!",
                "🃏 Stiamo collezionando così tante sconfitte che tra poco potremo scambiarle come le figurine dei calciatori.",
                "💸 Il mio avvocato mi aveva sconsigliato di mandarvi questo messaggio, ma purtroppo siamo ancora poveri. A martedì!"
            ]
            
            messaggio_scelto = random.choice(FRASI_RANDOM)
            testo_finale = INTESTAZIONE_FISSA + messaggio_scelto
            
            # Creazione Link Sicuro
            link_sconfitta = f"https://wa.me/?text={urllib.parse.quote(testo_finale)}"
            
            st.markdown(f'<a href="{link_sconfitta}" target="_blank" class="wa-button wa-fail">📲 Avvisa i soci</a>', unsafe_allow_html=True)

elif scelta == "📅 Stato Abbonamento":
    st.subheader("📅 Gestione Abbonamento")
    fatti = st.slider("Concorsi giocati", 0, 15, value=0)
    rimanenti = 15 - fatti
    m1, m2 = st.columns(2)
    m1.metric("Rimanenti", f"{rimanenti}/15")
    st.progress(fatti / 15)
    st.divider()
    st.subheader("👥 Cassa Soci")
    soci = ["VS", "MM", "ED", "AP", "GGC", "AM"]
    pagati = 0
    c1, c2 = st.columns(2)
    for i, s in enumerate(soci):
        with c1 if i < 3 else c2:
            if st.checkbox(f"Quota {s}", key=f"paga_{s}"): pagati += 1
    m2.metric("Soci Pagati", f"{pagati}/6")
    status_class = "status-green" if pagati == 6 else "status-red"
    st.markdown(f'<div class="{status_class}">CASSA: {pagati}/6 SOCI PAGATI</div>', unsafe_allow_html=True)

elif scelta == "💰 Calcolo Quote":
    st.subheader("💰 Calcolo Netto")
    premio = st.number_input("Lordo Totale (€)", min_value=0.0, step=10.0, format="%.2f")
    if premio > 0:
        netto = premio - ((premio - 500) * 0.20 if premio > 500 else 0)
        quota = round(netto/6, 2)
        euro = int(quota)
        centesimi = int(round((quota - euro) * 100))
        testo_lettere = num2words(euro, lang='it') + " euro"
        if centesimi > 0:
            testo_lettere += f" e {num2words(centesimi, lang='it')} centesimi"
        st.markdown(f'<div class="quota-box"><span class="quota-valore">{quota:.2f} € a testa</span><span class="quota-testo">{testo_lettere}</span></div>', unsafe_allow_html=True)
        if st.button("💾 Salva nel Bottino"):
            salva_vincita("Vincita", netto)
            st.toast("Salvato!")

elif scelta == "🏛️ Il Bottino":
    st.subheader("🏛️ Archivio Storico")
    df = carica_archivio()
    if not df.empty:
        st.dataframe(df, use_container_width=True)
        st.metric("Totale Netto Accumulato", f"{df['Euro_Netto'].sum():.2f} €")
    else: st.info("Archivio vuoto.")
    st.divider()
    st.write("**Le nostre sestine:**")
    sestine = ["03-10-17-40-85-86", "10-17-19-40-85-86", "17-19-40-75-85-86", "03-19-40-75-85-86", "03-10-19-75-85-86", "03-10-17-75-85-86"]
    for i, s in enumerate(sestine, 1):
        num_list = s.split('-')
        balls_html = "".join([f'<span class="lotto-ball">{n}</span>' for n in num_list])
        st.markdown(f"**Schedina {i}:** {balls_html}", unsafe_allow_html=True)
        
