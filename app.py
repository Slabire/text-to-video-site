from flask import Flask, request, render_template, send_from_directory
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip
import os
import requests
import uuid

app = Flask(__name__)

PEXELS_API_KEY = "x5CFAga01HCx7vWoy8URSRy8qucwHAoFFFv7JgTS2d6Kh2XPhS4PIIoG"
HEADERS = {"Authorization": PEXELS_API_KEY}

@app.route('/')
def home():
    return render_template('video.html')

@app.route('/generate-video', methods=['POST'])
def generate_video():
    text = request.form['text']
    unique_id = str(uuid.uuid4())
    audio_path = f"static/audio_{unique_id}.mp3"
    image_path = f"static/image_{unique_id}.jpg"
    video_path = f"static/video_{unique_id}.mp4"

    # 1. Generează audio cu gTTS
    tts = gTTS(text)
    tts.save(audio_path)

    # 2. Ia o imagine de pe Pexels
    r = requests.get("https://api.pexels.com/v1/search?query=nature&per_page=1", headers=HEADERS)
    img_url = r.json()['photos'][0]['src']['large']
    img_data = requests.get(img_url).content
    with open(image_path, 'wb') as f:
        f.write(img_data)

    # 3. Creează videoclipul
    audioclip = AudioFileClip(audio_path)
    imageclip = ImageClip(image_path, duration=audioclip.duration).set_audio(audioclip)
    imageclip.write_videofile(video_path, fps=24)

    return render_template("video.html", video_path=video_path)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)



