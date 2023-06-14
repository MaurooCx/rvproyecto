import pyaudio
import sounddevice as sd
import numpy as np
from pydub import AudioSegment
from pydub.playback import play


def modificar_tono_voz(input_data, factor_tono):
    # Convertir los datos de entrada a un objeto AudioSegment
    audio = AudioSegment(
        input_data.tobytes(),
        frame_rate=44100,
        sample_width=input_data.dtype.itemsize,
        channels=1
    )

    # Aumentar o disminuir el tono
    audio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * factor_tono)
    })

    # Convertir el objeto AudioSegment modificado a un array NumPy
    output_data = np.frombuffer(audio.raw_data, dtype=np.int16)

    return output_data

def capturar_audio():
    # Configuración de la captura de audio
    sample_rate = 44100
    frames_per_buffer = 1024

    # Inicializar el objeto PyAudio
    p = pyaudio.PyAudio()

    # Abrir el stream de audio desde el micrófono
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=frames_per_buffer)

    print("Capturando audio. Presiona Ctrl+C para detener.")

    try:
        while True:
            # Leer los datos de audio desde el stream
            input_data = stream.read(frames_per_buffer)

            # Convertir los datos de audio a un array NumPy
            input_data = np.frombuffer(input_data, dtype=np.int16)

            # Modificar el tono de voz
            output_data = modificar_tono_voz(input_data, 1.5)  # Aumentar el tono en un 50%

            # Reproducir el audio modificado
            sd.play(output_data, sample_rate)

    except KeyboardInterrupt:
        print("Captura de audio detenida.")

    # Detener la reproducción y cerrar el stream de audio
    sd.stop()
    stream.stop_stream()
    stream.close()
    p.terminate()


capturar_audio()
