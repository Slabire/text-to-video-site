from flask import Flask, request, render_template
from gtts import gTTS
from moviepy.editor import *
import os
import uuid
from PIL import Image
Image.ANTIALIAS = Image.Resampling.LANCZOS

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_video():
    try:
        # Preia textul din formular
        text = request.form['script']
        
        # Creează un nume unic pentru fișierele generate
        filename = str(uuid.uuid4())
        audio_path = f'static/{filename}.mp3'
        video_path = f'static/{filename}.mp4'
        image_path = 'static/background.jpg'

        # Verifică dacă imaginea există
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file {image_path} not found.")
        
        # Generează audio din text
        tts = gTTS(text)
        tts.save(audio_path)

        # Creează videoclipul din imagine și audio
        audioclip = AudioFileClip(audio_path)
        imageclip = ImageClip(image_path).set_duration(audioclip.duration).set_audio(audioclip)
        video = imageclip.resize(height=720)
        video.write_videofile(video_path, fps=24)

        # Returnează video-ul generat în pagina HTML
        return render_template('index.html', video_url=video_path)
    
    except Exception as e:
        # Afișează eroarea în loguri și returnează un mesaj de eroare
        print(f"Error: {e}")
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)

        
       

