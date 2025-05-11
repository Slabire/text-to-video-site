from flask import Flask, request, render_template, url_for
from gtts import gTTS
from moviepy.editor import *
import os
import uuid

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_video():
    text = request.form['script']
    filename = str(uuid.uuid4())
    audio_path = os.path.join('static', f'{filename}.mp3')
    video_path = os.path.join('static', f'{filename}.mp4')
    image_path = 'static/background.jpg'

    # Generate audio
    tts = gTTS(text)
    tts.save(audio_path)

    # Create video
    audioclip = AudioFileClip(audio_path)
    imageclip = ImageClip(image_path).set_duration(audioclip.duration).set_audio(audioclip)
    video = imageclip.resize(height=720)
    video.write_videofile(video_path, fps=24)

    # Use url_for to get the correct URL for the video file
    video_url = url_for('static', filename=f'{filename}.mp4')

    return render_template('index.html', video_url=video_url)

if __name__ == '__main__':
    app.run(debug=True)
