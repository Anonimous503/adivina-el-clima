import streamlit as st
import requests
import random

# --- Configuración de la página ---
st.set_page_config(
    page_title="🌦️ Adivina el Clima",
    page_icon="☁️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Título y descripción ---
st.title("🎮 Juego Interactivo: Adivina el Clima en El Salvador 🇸🇻")
st.markdown(
    """
Bienvenido al juego meteorológico más divertido ☁️🌤️.  
Tu objetivo: adivinar correctamente el clima actual de los departamentos de El Salvador.  
Cada acierto suma puntos. ¡Vamos a jugar! 🎯
"""
)

# --- Lista de departamentos ---
departamentos = [
    "Ahuachapán", "Cabañas", "Chalatenango", "Cuscatlán", "La Libertad",
    "La Paz", "La Unión", "Morazán", "San Miguel", "San Salvador",
    "San Vicente", "Santa Ana", "Sonsonate", "Usulután"
]

API_KEY = "3e43c04f02aeda8706ca4ad000bfb157"
TOTAL_RONDAS = 5

# --- Estado del juego ---
if "ronda" not in st.session_state:
    st.session_state.ronda = 1
if "puntaje" not in st.session_state:
    st.session_state.puntaje = 0
if "jugando" not in st.session_state:
    st.session_state.jugando = False
if "pregunta_mostrada" not in st.session_state:
    st.session_state.pregunta_mostrada = False
if "clima_real" not in st.session_state:
    st.session_state.clima_real = ""
if "opciones" not in st.session_state:
    st.session_state.opciones = []

# --- Iniciar juego ---
if not st.session_state.jugando:
    if st.button("🎯 Iniciar Juego", use_container_width=True):
        st.session_state.jugando = True
        st.session_state.ronda = 1
        st.session_state.puntaje = 0
        st.session_state.pregunta_mostrada = False
    st.stop()

st.subheader(f"🔎 Ronda {st.session_state.ronda} de {TOTAL_RONDAS}")

# --- Selección de departamento ---
departamento = st.selectbox("📍 Selecciona el departamento:", departamentos)

# --- Botón Ver Pregunta ---
if st.button("🌤️ Ver pregunta", use_container_width=True) or st.session_state.pregunta_mostrada:
    # Obtener clima solo si no se ha mostrado
    if not st.session_state.pregunta_mostrada:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={departamento}&appid={API_KEY}&units=metric&lang=es"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            st.session_state.clima_real = data["weather"][0]["description"].capitalize()
            icono = data["weather"][0]["icon"]
            st.session_state.imagen_url = f"http://openweathermap.org/img/wn/{icono}@2x.png"

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
            st.stop()

    # Mostrar opciones
    eleccion = st.radio(
        "🤔 ¿Cuál es el clima actual?",
        st.session_state.opciones,
        key=f"opcion_{st.session_state.ronda}"
    )

    # Botón Verificar Respuesta
    if st.button("✅ Verificar respuesta", use_container_width=True):
        if eleccion == st.session_state.clima_real:
            st.success("🎉 ¡Correcto!")
            st.session_state.puntaje += 1
        else:
            st.error(f"❌ Incorrecto. El clima real es: **{st.session_state.clima_real}**")

        # Mostrar detalles del clima
        st.image(st.session_state.imagen_url, caption=f"Clima actual en {departamento}", width=150)
        st.info(
            f"🌡️ Temperatura: {data['main']['temp']}°C  \n"
            f"💨 Viento: {data['wind']['speed']} km/h  \n"
            f"💧 Humedad: {data['main']['humidity']}%"
        )

        # Pasar a siguiente ronda
        if st.session_state.ronda < TOTAL_RONDAS:
            if st.button("➡️ Siguiente Ronda", use_container_width=True):
                st.session_state.ronda += 1
                st.session_state.pregunta_mostrada = False
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

            if st.button("🔁 Jugar otra vez", use_container_width=True):
                st.session_state.jugando = False
                st.session_state.pregunta_mostrada = False
                st.experimental_rerun()

