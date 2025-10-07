import streamlit as st
import requests
import random

st.set_page_config(page_title="🌦️ Adivina el Clima", page_icon="☁️", layout="centered")

st.title("🎮 Juego: Adivina el Clima en El Salvador 🇸🇻")
st.write("Selecciona el departamento y trata de adivinar el clima actual 🌤️")

# --- Configuración inicial ---
departamentos_el_salvador = [
    "Ahuachapán", "Cabañas", "Chalatenango", "Cuscatlán", "La Libertad",
    "La Paz", "La Unión", "Morazán", "San Miguel", "San Salvador",
    "San Vicente", "Santa Ana", "Sonsonate", "Usulután"
]

API_KEY = "3e43c04f02aeda8706ca4ad000bfb157"
TOTAL_RONDAS = 5

# --- Estado de sesión ---
if "ronda" not in st.session_state:
    st.session_state.ronda = 1
if "puntaje" not in st.session_state:
    st.session_state.puntaje = 0
if "jugando" not in st.session_state:
    st.session_state.jugando = False

# --- Iniciar juego ---
if not st.session_state.jugando:
    if st.button("🎯 Iniciar Juego"):
        st.session_state.jugando = True
        st.session_state.ronda = 1
        st.session_state.puntaje = 0
    st.stop()

st.subheader(f"🔎 Ronda {st.session_state.ronda} de {TOTAL_RONDAS}")

departamento = st.selectbox("📍 Selecciona el departamento:", options=departamentos_el_salvador, key=f"dep_{st.session_state.ronda}")

if st.button("🌤️ Ver pregunta"):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={departamento}&appid={API_KEY}&units=metric&lang=es"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        clima_real = data["weather"][0]["description"].capitalize()
        icono = data["weather"][0]["icon"]
        imagen_url = f"http://openweathermap.org/img/wn/{icono}@2x.png"

        # Crear opciones falsas
        posibles_climas = [
            "Soleado con pocas nubes", "Lluvia ligera", "Nublado total",
            "Tormentas eléctricas", "Cielo despejado", "Lluvia moderada",
            "Llovizna", "Viento fuerte", "Parcialmente nublado"
        ]

        opciones = random.sample(posibles_climas, 3)
        if clima_real not in opciones:
            opciones.append(clima_real)
        random.shuffle(opciones)

        eleccion = st.radio("🤔 ¿Cuál es el clima actual?", opciones, key=f"opcion_{st.session_state.ronda}")

        if st.button("✅ Comprobar respuesta"):
            if eleccion == clima_real:
                st.success("🎉 ¡Correcto!")
                st.session_state.puntaje += 1
            else:
                st.error(f"❌ Incorrecto. El clima real es: **{clima_real}**")

            st.image(imagen_url, caption=f"Clima actual en {departamento}")
            st.info(
                f"🌡️ Temperatura: {data['main']['temp']}°C  \n"
                f"💨 Viento: {data['wind']['speed']} km/h  \n"
                f"💧 Humedad: {data['main']['humidity']}%"
            )

            # Pasar a siguiente ronda
            if st.session_state.ronda < TOTAL_RONDAS:
                if st.button("➡️ Siguiente Ronda"):
                    st.session_state.ronda += 1
                    st.experimental_rerun()
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

                if st.button("🔁 Jugar otra vez"):
                    st.session_state.jugando = False
                    st.experimental_rerun()
    else:
        st.error("⚠️ No se pudo obtener el clima. Intenta de nuevo.")
