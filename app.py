import os
import nltk
from flask import Flask, render_template, request
from gtts import gTTS

# Setează locația de descărcare pentru fișierele NLTK
nltk_data_path = os.path.join(os.getcwd(), 'nltk_data')
if not os.path.exists(nltk_data_path):
    os.makedirs(nltk_data_path)

# Adaugă calea la fișierele NLTK
nltk.data.path.append(nltk_data_path)

# Descarcă 'punkt' dacă nu este deja disponibil
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', download_dir=nltk_data_path)

# Inițializează aplicația Flask
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_text_to_audio():
    if request.method == 'POST':
        text = request.form['text']  # Obține textul din formular
        language = request.form.get('language', 'en')  # Implicit engleză

        # Creează audio cu gTTS
        tts = gTTS(text=text, lang=language, slow=False)

        # Salvează fișierul audio
        audio_path = os.path.join('static', 'audio.mp3')
        tts.save(audio_path)

        # Returnează pagina cu player audio
        return render_template('index.html', audio_path=audio_path)

# ✅ ATENȚIE: indentarea corectă
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

@app.route('/video')
def video_page():
    return render_template('video.html')

@app.route('/generate-video', methods=['POST'])
def generate_video():
    text = request.form['text']
    audio_path = 'static/temp.mp3'
    video_path = 'static/result.mp4'

    from gtts import gTTS
    from moviepy.editor import ColorClip, AudioFileClip

    # Generează audio din text
    tts = gTTS(text=text, lang='en')
    tts.save(audio_path)

    # Creează video simplu alb cu audio
    audioclip = AudioFileClip(audio_path)
    videoclip = ColorClip(size=(1280, 720), color=(255, 255, 255), duration=audioclip.duration)
    videoclip = videoclip.set_audio(audioclip)
    videoclip.write_videofile(video_path, fps=24)
    # verifici dacă fișierul există fizic
    print("Există result.mp4?", os.path.exists(video_path))

    return render_template('video.html', video_path=video_path)





        
       




