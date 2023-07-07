import pyttsx3
from datetime import datetime

class TextToSpeech:
    engine: pyttsx3.Engine

    def __init__(self, voice, rate, volume):
        self.engine = pyttsx3.init()
        if voice:
            self.engine.setProperty("voice", voice)
        
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)
    
    def list_available_voices(self):
        voices: list = [self.engine.getProperty('voices')]

        for i,voice in enumerate(voices[0]):
            print(f'{i+1} {voice.name}: {voice.languages} ({voice.id})')

    def text_to_speech(self, text, filename="reporte.mp3"):
        self.engine.save_to_file(text, filename)
        self.engine.runAndWait()

def reporte_cita_mp3(cita):
    filename = f"reportes/mp3/REPORTE_MP3_CITA_{cita.pk}.mp3"
    text =  f"INMUEBLES INCAIBO. {fecha_a_texto(str(datetime.now().date()))}. COMPROBANTE EN FORMATO MP3 DE CITA DE VISITA. " 
    text += f"DEBE LLEVAR ESTE COMPROBANTE EL DÍA DE LA CITA PARA SER ADMITIDO EN LA VISITA AL INMUEBLE. "
    text += f"INMUEBLE A VISITAR: {cita.inmueble.nombre}. "
    text += f"SECTOR DEL INMUEBLE: {cita.inmueble.sector.nombre}. "
    text += f"DIRECCIÓN DEL INMUEBLE: {cita.inmueble.ubicacion_detallada}. "
    text += f"FECHA Y HORA: {fecha_a_texto(str(cita.fecha_asignada.date()))} a las {cita.fecha_asignada.hour} horas. "
    text += f"NOMBRE DEL VISITANTE: {cita.persona}. "
    text += f"CÉDULA DEL VISITANTE: {cita.persona.cedula()}. "
    text += f"NOMBRE DEL AGENTE: {cita.inmueble.agente}. "
    text += f"TELÉFONO DEL AGENTE: {cita.inmueble.agente.numero_telefono}. "
    text += f"CORREO DEL AGENTE: {cita.inmueble.agente.usuario_persona.email}. "

    text += f"NÚMERO DE CITA: {cita.pk}. "

    text += f"FIN DEL REPORTE. LA MODIFICACIÓN DE ESTE DOCUMENTO DIGITAL ESTÁ PROHIBIDA."

    TextToSpeech(None, 200, 100).text_to_speech(text, filename)
    return filename

def fecha_a_texto(fecha):
    print(fecha)
    texto = f"{fecha.split('-')[2]} de "
    
    mes = int(fecha.split('-')[1])
    if(mes == 1):
        texto += "enero"
    elif(mes == 2):
        texto += "febrero"
    elif(mes == 3):
        texto += "marzo"
    elif(mes == 4):
        texto += "abril"
    elif(mes == 5):
        texto += "mayo"
    elif(mes == 6):
        texto += "junio"
    elif(mes == 7):
        texto += "julio"
    elif(mes == 8):
        texto += "agosto"
    elif(mes == 9):
        texto += "septiembre"
    elif(mes == 10):
        texto += "octubre"
    elif(mes == 11):
        texto += "noviembre"
    elif(mes == 12):
        texto += "diciembre"
    
    texto += f" del {fecha.split('-')[0]}"

    return texto
