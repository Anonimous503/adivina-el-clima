import streamlit as st
import requests
import random
import time

st.set_page_config(
    page_title="🌦️ Adivina el Clima",
    page_icon="☁️",
    layout="centered"
)

st.title("🎮 Juego: Adivina el Clima en El Salvador 🇸🇻")
st.markdown("Adivina correctamente el clima actual y mira la animación correspondiente!")

departamentos = [
    "Ahuachapán", "Cabañas", "Chalatenango", "Cuscatlán", "La Libertad",
    "La Paz", "La Unión", "Morazán", "San Miguel", "San Salvador",
    "San Vicente", "Santa Ana", "Sonsonate", "Usulután"
]

API_KEY = "3e43c04f02aeda8706ca4ad000bfb157"
TOTAL_RONDAS = 5

# --- Estado del juego ---
for key in ["ronda","puntaje","jugando","pregunta_mostrada",
            "clima_real","opciones","data_clima","respuesta_verificada"]:
    if key not in st.session_state:
        st.session_state[key] = 0 if key in ["ronda","puntaje"] else False if key in ["jugando","pregunta_mostrada","respuesta_verificada"] else ""

placeholder = st.empty()

# --- GIFs por tipo de clima ---
clima_gifs = {
    "lluvia": "https://media.giphy.com/media/l0HlBO7eyXzSZkJri/giphy.gif",
    "nublado": "https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif",
    "sol": "https://media.giphy.com/media/xT0xeJpnrWC4XWblEk/giphy.gif",
    "tormenta": "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif",
    "nieve": "https://media.giphy.com/media/3o6Zt6ML6BklcajjsA/giphy.gif"
}

# --- Iniciar juego ---
if not st.session_state.jugando:
    if st.button("🎯 Iniciar Juego", use_container_width=True):
        st.session_state.jugando = True
        st.session_state.ronda = 1
        st.session_state.puntaje = 0
        st.session_state.pregunta_mostrada = False
        st.session_state.respuesta_verificada = False
    st.stop()

st.subheader(f"🔎 Ronda {st.session_state.ronda} de {TOTAL_RONDAS}")
departamento = st.selectbox("📍 Selecciona el departamento:", departamentos)

def generar_pregunta():
    url = f"https://api.openweathermap.org/data/2.5/weather?q={departamento}&appid={API_KEY}&units=metric&lang=es"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        st.session_state.clima_real = data["weather"][0]["description"].capitalize()
        st.session_state.data_clima = data
        st.session_state.imagen_url = f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"

        posibles_climas = [
            "Soleado con pocas nubes", "Lluvia ligera", "Nublado total",
            "Tormentas eléctricas", "Cielo despejado", "Lluvia moderada",
            "Llovizna", "Viento fuerte", "Parcialmente nublado"
        ]
        st.session_state.opciones = random.sample(posibles_climas, 3)
        if st.session_state.clima_real not in st.session_state.opciones:
            st.session_state.opciones.append(st.session_state.clima_real)
        random.shuffle(st.session_state.opciones)
        st.session_state.pregunta_mostrada = True
    else:
        st.error("⚠️ No se pudo obtener el clima. Intenta de nuevo.")

# --- Mostrar pregunta ---
if st.button("🌤️ Ver pregunta", use_container_width=True) or st.session_state.pregunta_mostrada:
    if not st.session_state.pregunta_mostrada:
        generar_pregunta()

    eleccion = st.radio("🤔 ¿Cuál es el clima actual?", st.session_state.opciones, key=f"opcion_{st.session_state.ronda}")

    if not st.session_state.respuesta_verificada:
        if st.button("✅ Verificar respuesta", use_container_width=True):
            st.session_state.respuesta_verificada = True
            correcto = eleccion == st.session_state.clima_real
            if correcto:
                st.success("🎉 ¡Correcto!")
                st.session_state.puntaje += 1
                time.sleep(1)
                if st.session_state.ronda < TOTAL_RONDAS:
                    st.session_state.ronda += 1
                    st.session_state.pregunta_mostrada = False
                    st.session_state.respuesta_verificada = False
                    placeholder.empty()
                else:
                    st.balloons()
                    st.subheader("🏁 ¡Juego Terminado!")
                    st.write(f"⭐ Puntaje final: {st.session_state.puntaje}/{TOTAL_RONDAS}")
                    if st.session_state.puntaje == TOTAL_RONDAS:
                        st.success("🌟 ¡Perfecto! Eres un experto meteorólogo 🌦️")
                    elif st.session_state.puntaje >= 3:
                        st.info("💡 ¡Bien hecho! Conoces bastante del clima 🌤️")
                    else:
                        st.warning("🌧️ Necesitas practicar más... El clima es impredecible 😅")
                    if st.button("🔁 Jugar otra vez", use_container_width=True):
                        st.session_state.jugando = False
                        st.session_state.ronda = 1
                        st.session_state.puntaje = 0
                        st.session_state.pregunta_mostrada = False
                        st.session_state.respuesta_verificada = False
            else:
                st.error(f"❌ Incorrecto. El clima real es: **{st.session_state.clima_real}**")

            # --- Mostrar GIF según clima ---
            clima_lower = st.session_state.clima_real.lower()
            gif_url = clima_gifs.get("lluvia")  # default
            if "lluvia" in clima_lower or "llovizna" in clima_lower:
                gif_url = clima_gifs["lluvia"]
            elif "nublado" in clima_lower:
                gif_url = clima_gifs["nublado"]
            elif "soleado" in clima_lower or "despejado" in clima_lower:
                gif_url = clima_gifs["sol"]
            elif "tormenta" in clima_lower:
                gif_url = clima_gifs["tormenta"]
            elif "nieve" in clima_lower:
                gif_url = clima_gifs["nieve"]

            st.image(gif_url, width=250)

            st.info(
                f"🌡️ Temperatura: {st.session_state.data_clima['main']['temp']}°C  \n"
                f"💨 Viento: {st.session_state.data_clima['wind']['speed']} km/h  \n"
                f"💧 Humedad: {st.session_state.data_clima['main']['humidity']}%"
            )
