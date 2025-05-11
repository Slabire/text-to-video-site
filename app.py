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






        
       

