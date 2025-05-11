from flask import Flask, request, render_template
from gtts import gTTS
from moviepy.editor import *
from nltk.tokenize import sent_tokenize
import nltk
import os
import uuid

# Descarcă datele necesare pentru nltk
nltk.download('punkt')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_video():
    text = request.form['script']
    filename = str(uuid.uuid4())
    video_path = f'static/{filename}.mp4'

    sentences = sent_tokenize(text)

    clips = []
    image_folder = 'static/images'
    image_files = sorted([f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.png'))])
    total_images = len(image_files)

    for i, sentence in enumerate(sentences):
        # Generează audio
        audio_path = f'static/{filename}_audio_{i}.mp3'
        gTTS(sentence).save(audio_path)

        # Creează clip video pentru propoziție
        audioclip = AudioFileClip(audio_path)
        image_path = os.path.join(image_folder, image_files[i % total_images])
        imageclip = ImageClip(image_path).set_duration(audioclip.duration).set_audio(audioclip)
        imageclip = imageclip.resize(height=720)
        clips.append(imageclip)

    final_video = concatenate_videoclips(clips, method="compose")
    final_video.write_videofile(video_path, fps=24)

    return render_template('index.html', video_url=video_path)

if __name__ == '__main__':
    app.run(debug=True)
