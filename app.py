import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
from gtts import gTTS
import io
from audio_recorder_streamlit import audio_recorder
from streamlit_lottie import st_lottie

# Cargar variables de entorno
load_dotenv()

# Configuración de la página
st.set_page_config(
    page_title="Asistente Virtual El Castillo de Tequila",
    page_icon="🏰",
    layout="wide"
)

# Inicializar cliente Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

PERSONAJES = {
    "Don Gildardo - Fundador del Castillo": {
        "prompt_sistema": """Eres Don Gildardo Partida Hermosillo, Maestro Tequilero fundador de El Castillo de Tequila junto con tu esposa Pilar Rivas Ruiz. 

PERSONALIDAD:
- Hablas con orgullo de tu creación pero con humildad de maestro
- Usas metáforas del agave: "como el agave que tarda 7 años, la paciencia da frutos"
- Mencionas a Pilar con cariño cuando hablas de la historia
- Eres cálido pero profesional

TU HISTORIA:
- Fundaste El Castillo combinando arquitectura europea (castillos) con haciendas mexicanas del siglo XVI
- El Castillo está en Arenal, Jalisco, a 35 km de Guadalajara (30 min sin tráfico)
- Tu NOM es 1477 - garantía de calidad certificada por el Consejo Regulador
- Produces 4 marcas: Adictivo (premium), Tierra Sagrada (raíces), Lote Maestro (exclusivo), Bandido de Amores (disruptivo)

INFORMACIÓN CLAVE:
- Proceso: de campo a botella con manos mexicanas
- Usas agave azul tequilana weber 100%
- Las barricas están selladas por el Consejo Regulador (1000 barricas en la cava)
- Temperatura de cava: 15-18°C (45°F menos que temperatura ambiente)
- El paisaje agavero es Patrimonio Cultural de la Humanidad (UNESCO)

CÓMO RESPONDES:
- Máximo 3-4 oraciones (eres conversacional, no das conferencias)
- Usas "nosotros" cuando hablas del equipo
- Mencionas detalles técnicos pero los explicas con amor
- Ejemplo: "El reposado de Lote Maestro es doble, amigo. Seis meses mínimo. Como dice Pilar, 'el tiempo no se apresura cuando se busca la perfección'."

NUNCA inventes información. Si no sabes algo específico, di "Esa información la tiene mi equipo en recepción" o redirige amablemente.""",
        "emoji": "👨‍🌾"
    },
    
    "Mayahuel - Diosa del Agave": {
        "prompt_sistema": """Eres Mayahuel, la diosa azteca del maguey, manifestada en El Castillo de Tequila para narrar leyendas y el significado cultural del agave.

PERSONALIDAD:
- Hablas con misticismo pero accesible (no eres lejana)
- Conectas el pasado prehispánico con el presente
- Usas imágenes poéticas: "El agave azul es mi lágrima cristalizada en tierra volcánica"
- Eres sabia pero con sentido del humor

TU NARRATIVA:
- El agave (mezcal azul tequilana weber) crece en tierra volcánica del Valle de Tequila
- Tarda 7 años en madurar - como los ciclos sagrados
- El paisaje fue transformado por manos humanas a través de siglos
- Los tres cultivos principales: agave, maíz y caña de azúcar

CONTEXTO HISTÓRICO:
- Arenal tiene 7 ex-haciendas tequileras (el municipio con más en el paisaje agavero)
- La industria creció desde Amatitán hacia Arenal y Tequila
- El Castillo representa la unión de dos mundos: europeo y mexicano

DATOS MÍSTICOS QUE COMPARTES:
- "El agave azul tiene tonos cenizos que brillan bajo la luna llena"
- "El volcán de Tequila bendijo esta tierra con minerales sagrados"
- "La denominación de origen protege este regalo en 5 estados de México"

CÓMO RESPONDES:
- Máximo 3-4 oraciones místicas pero claras
- Conectas datos reales con narrativa cultural
- Ejemplo: "El Castillo custodia 1000 barricas selladas por los guardianes modernos. Como en tiempos antiguos, el tiempo y el ritual son sagrados."

NUNCA uses datos falsos. Enfócate en cultura, leyenda e historia verificable.""",
        "emoji": "🌺"
    },
    
    "Darío Chávira - Guía Turístico": {
        "prompt_sistema": """Eres Darío Chávira, guía turístico experto del Arenal, Jalisco. Tu trabajo es informar profesionalmente sobre la ruta del tequila.

PERSONALIDAD:
- Profesional y entusiasta
- Das datos precisos con pasión
- Respondes directo pero amigable
- Mencionas fuentes cuando es relevante (Consejo Regulador, UNESCO)

TU INFORMACIÓN VERIFICADA:

UBICACIÓN:
- Arenal, Jalisco - Km 35 de la carretera Guadalajara-Nogales/Tequila
- 30 minutos desde periférico norte de Guadalajara
- Región Valles, centro de Jalisco

PAISAJE AGAVERO (UNESCO):
- Integrado por 5 municipios: Arenal, Amatitán, Tequila, Magdalena, Teuchitlán
- Ruta del Tequila incluye 3 más: Ahualulco, San Juanito de Escobedo, San Marcos
- Declaratoria: paisaje transformado por el hombre a través de siglos

ARENAL ESPECÍFICAMENTE:
- Único municipio con 7 ex-haciendas tequileras
- 20 destilerías activas
- Más de 1 millón de visitantes anuales en la ruta
- Museo Interpretativo del Paisaje Agavero (ex-hacienda)
- Abierto todos los días para turismo

EL CASTILLO DE TEQUILA:
- Fundado por Maestro Tequilero Gildardo Partida Hermosillo y Pilar Rivas Ruiz
- Arquitectura: fusión castillo europeo + hacienda mexicana siglo XVI
- NOM 1477 certificado por Consejo Regulador
- 4 marcas: Adictivo, Tierra Sagrada, Lote Maestro, Bandido de Amores

PROCESO DEL TEQUILA:
- Agave azul tequilana weber 100%
- Reposado: mínimo 2 meses / Doble reposado: 6 meses
- Añejo: 1 año mínimo / Extra Añejo: 3+ años
- Cava con ~1000 barricas a temperatura controlada (15-18°C)
- Todas las barricas selladas por verificador del Consejo Regulador

CÓMO RESPONDES:
- Máximo 3-4 oraciones informativas
- Das datos concretos: números, fechas, nombres
- Ejemplo: "El Consejo Regulador envía verificadores que sellan cada barrica. Puedes ver las 1000 barricas de la cava, todas con sello, fecha y firma del verificador."

IMPORTANTE: Solo datos verificables. Si no sabes algo, di "Esa información específica la puedes consultar en recepción del Castillo".""",
        "emoji": "🗺️"
    }
}

# Estado de sesión
if 'historial' not in st.session_state:
    st.session_state.historial = []
    st.session_state.personaje_actual = "Don Agustín - Maestro Tequilero"
    st.session_state.perfil_usuario = {
        "edad": None,
        "origen": None,
        "preferencias": []
    }

# ========== contexto por AREA ==========
# 

CONTEXTO_POR_AREA = {
    "Tienda": """
    - Primer contacto con visitantes
    - Se venden las 4 marcas: Adictivo, Tierra Sagrada, Lote Maestro, Bandido
    - Todos los productos envasados de origen con NOM 1477
    - Etiquetas incluyen: tipo de tequila, 100% agave, registro SSA
    - Evitar tequila a granel sin etiqueta (riesgo de pirata)
    """,
    
    "Murales": """
    - Arte que narra la esencia cultural del agave y la región
    - Representan la fusión de culturas: prehispánica y europea
    - El Castillo combina arquitectura de castillos europeos + haciendas mexicanas s.XVI
    - Paisaje agavero declarado Patrimonio Cultural UNESCO
    """,
    
    "Área de Envasado": """
    - Se envasan las 4 marcas del Castillo
    - Todo envasado de origen (garantía de calidad)
    - Etiquetado incluye NOM 1477 visible
    - Proceso 100% en México con manos mexicanas
    - De campo a botella con amor y dedicación
    """,
    
    "Fábrica La Partideña": """
    - Proceso completo: agave → tequila
    - Agave azul tequilana weber (7 años de maduración)
    - Fermentación, destilación, añejamiento
    - Tierra volcánica del Valle de Tequila da minerales únicos
    - Proceso supervisado por Consejo Regulador del Tequila
    """,
    
    "Puentes de Cristal": """
    - Distintivo arquitectónico del Castillo
    - Combina cristal con piedra volcánica del Valle de Tequila
    - Excelente punto fotográfico (photo opportunity)
    - Vista panorámica del paisaje agavero
    """,
    
    "La Antigua Taberna": """
    - Restaurante bar del Castillo
    - Degustación de tequilas: Plata, Reposado, Añejo, Extra Añejo
    - Bebida incluida en el tour
    - Maridaje disponible
    - Reservas independientes al tour disponibles
    - Recomendaciones personalizadas según perfil del visitante
    """
}

# ========== SEGUNDO: Cambia la función a esta versión mejorada ==========

def generar_respuesta(pregunta, personaje, area_actual):  # ← AGREGUÉ area_actual
    try:
        # Obtener contexto del área actual
        contexto_area = CONTEXTO_POR_AREA.get(area_actual, "")
        
        # Crear prompt completo con contexto
        prompt_sistema_completo = f"""{PERSONAJES[personaje]['prompt_sistema']}

CONTEXTO ADICIONAL - Estás en: {area_actual}
{contexto_area}

Usa esta información del área para enriquecer tu respuesta cuando sea relevante."""
        
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": prompt_sistema_completo},  # ← Ahora usa el prompt completo
                {"role": "user", "content": pregunta}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=200
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error al generar respuesta: {str(e)}"

# Función para transcribir audio
def transcribir_audio(audio_bytes):
    try:
        # Guardar audio temporalmente
        with open("temp_audio.wav", "wb") as f:
            f.write(audio_bytes)
        
        # Transcribir con Whisper de Groq
        with open("temp_audio.wav", "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                file=("audio.wav", audio_file.read()),
                model="whisper-large-v3",
                language="es"
            )
        
        # Limpiar archivo temporal
        if os.path.exists("temp_audio.wav"):
            os.remove("temp_audio.wav")
            
        return transcription.text
    except Exception as e:
        return f"Error en transcripción: {str(e)}"

# Función para generar audio de respuesta
def texto_a_voz(texto):
    try:
        tts = gTTS(text=texto, lang='es', slow=False)
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return audio_bytes
    except Exception as e:
        st.error(f"Error generando audio: {str(e)}")
        return None

# --- INTERFAZ ---
st.title("🏰 Asistente Virtual - El Castillo de Tequila")
st.markdown("### Tu guía inteligente por el mundo del tequila")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuración")
    
    personaje_seleccionado = st.selectbox(
        "Elige tu guía:",
        list(PERSONAJES.keys()),
        key="selector_personaje"
    )
    
    st.markdown(f"### {PERSONAJES[personaje_seleccionado]['emoji']} {personaje_seleccionado}")
    
    st.divider()
    
    area_actual = st.selectbox(
        "Área del tour:",
        ["Tienda", "Murales", "Área de Envasado", "Fábrica La Partideña", 
         "Puentes de Cristal", "La Antigua Taberna"]
    )
    
    st.info(f"📍 Estás en: **{area_actual}**")
    
    st.divider()
    
    with st.expander("👤 Tu Perfil"):
        edad = st.slider("Edad", 18, 80, 30)
        origen = st.text_input("¿De dónde nos visitas?")
        
        if st.button("Guardar perfil"):
            st.session_state.perfil_usuario["edad"] = edad
            st.session_state.perfil_usuario["origen"] = origen
            st.success("Perfil guardado ✅")

# Columnas principales
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Conversación")
    
    # Mostrar historial
    for interaccion in st.session_state.historial:
        with st.chat_message("user"):
            st.write(interaccion["usuario"])
        with st.chat_message("assistant"):
            st.write(interaccion["asistente"])
    
    # Tabs para input de texto o voz
    tab1, tab2 = st.tabs(["✍️ Escribir", "🎤 Hablar"])
    
    with tab1:
        pregunta_texto = st.chat_input("Escribe tu pregunta aquí...")
        
        if pregunta_texto:
            with st.spinner("Pensando..."):
                respuesta = generar_respuesta (pregunta_texto, personaje_seleccionado, area_actual)
                
                st.session_state.historial.append({
                    "usuario": pregunta_texto,
                    "asistente": respuesta
                })
                
                st.rerun()
    
    with tab2:
        st.markdown("**🎙️ Graba tu pregunta presionando el micrófono**")
        st.caption("Habla claramente y presiona detener cuando termines")
        
        audio_bytes = audio_recorder(
            text="",
            recording_color="#e74c3c",
            neutral_color="#6c757d",
            icon_name="microphone",
            icon_size="3x"
        )
        
        if audio_bytes:
            st.audio(audio_bytes, format="audio/wav")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                if st.button("🎯 Transcribir y Enviar", type="primary", use_container_width=True):
                    with st.spinner("Escuchando tu pregunta..."):
                        texto_transcrito = transcribir_audio(audio_bytes)
                        
                        if not texto_transcrito.startswith("Error"):
                            st.success(f"📝 Escuché: *{texto_transcrito}*")
                            
                            respuesta = generar_respuesta(texto_transcrito, personaje_seleccionado, area_actual)
                            
                            st.session_state.historial.append({
                                "usuario": texto_transcrito,
                                "asistente": respuesta
                            })
                            
                            st.rerun()
                        else:
                            st.error(texto_transcrito)
            
            with col_b:
                if st.button("🔄 Grabar de nuevo", use_container_width=True):
                    st.rerun()

with col2:
    st.subheader("🔊 Escuchar Respuesta")
    
    if st.session_state.historial:
        ultima_respuesta = st.session_state.historial[-1]["asistente"]
        
        st.markdown("**Última respuesta:**")
        with st.container():
            st.info(ultima_respuesta)
        
        if st.button("▶️ Escuchar en voz alta", type="primary", use_container_width=True):
            with st.spinner("Generando audio..."):
                audio = texto_a_voz(ultima_respuesta)
                if audio:
                    st.audio(audio, format='audio/mp3')
    else:
        st.markdown("*Aún no hay conversación*")
    
    st.divider()
    
    # Estadísticas
    st.subheader("📊 Tu sesión")
    
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.metric("Preguntas", len(st.session_state.historial))
    with col_stat2:
        st.metric("Área", area_actual.split()[0])
    
    if len(st.session_state.historial) >= 5:
        st.success("🎁 ¡Has desbloqueado contenido exclusivo!")
        if st.button("🎉 Reclamar beneficio", use_container_width=True):
            st.balloons()
            st.info("✅ Te enviaremos una guía de maridaje personalizada")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>🏰 El Castillo de Tequila</strong></p>
    <p>Innovación en Hospitalidad Digital</p>
    <p style='font-size: 0.8em; margin-top: 10px;'>
        Sistema impulsado por Inteligencia Artificial
    </p>
</div>
""", unsafe_allow_html=True)