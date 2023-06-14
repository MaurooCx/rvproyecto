import pyttsx3
from pydub import AudioSegment
from pydub.playback import play

def modificar_tono_voz(archivo_entrada, archivo_salida, factor_tono):
    # Cargar el archivo de audio
    audio = AudioSegment.from_file(archivo_entrada)

    # Aumentar o disminuir el tono
    audio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * factor_tono)
    })

    # Exportar el archivo modificado
    audio.export(archivo_salida, format="wav")

def texto_a_voz(texto, archivo_salida):
    engine = pyttsx3.init()
    engine.save_to_file(texto, archivo_salida)
    engine.runAndWait()

# Modificar el tono de un archivo de audio
modificar_tono_voz("tacoo.wav", "salida.wav", 1.5)  # Aumentar el tono en un 50%

# Convertir texto a voz y guardar como archivo de audio
texto_a_voz("Hola, esto es una prueba", "salida.wav")

# Reproducir el archivo de audio resultante
audio = AudioSegment.from_file("salida.wav")
play(audio)
