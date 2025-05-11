import os
import requests
from gtts import gTTS
from moviepy.editor import AudioFileClip, ImageClip, TextClip, concatenate_videoclips, ColorClip
from flask import Flask, render_template, request

# Your Pexels API Key
api_key = 'x5CFAga01HCx7vWoy8URSRy8qucwHAoFFFv7JgTS2d6Kh2XPhS4PIIoG'

# Set the Pexels API URL
url = "https://api.pexels.com/v1/search"

# Initialize Flask app
app = Flask(__name__)

# 🔧 ADĂUGAT: ruta pentru afișarea paginii video.html
@app.route('/video', methods=['GET'])
def video_page():
    return render_template('video.html')

@app.route('/generate-video', methods=['POST'])
def generate_video():
    text = request.form['text']
    audio_path = 'static/temp.mp3'
    video_path = 'static/result.mp4'

    # Generate audio from text
    tts = gTTS(text=text, lang='en')
    tts.save(audio_path)

    headers = { "Authorization": api_key }
    search_query = "video generation"
    params = { "query": search_query, "per_page": 5, "page": 1 }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        photos = data.get('photos', [])

        if not os.path.exists("images"):
            os.makedirs("images")

        for photo in photos:
            image_url = photo['src']['original']
            image_name = f"{photo['id']}.jpg"
            img_data = requests.get(image_url).content
            with open(f"images/{image_name}", 'wb') as handler:
                handler.write(img_data)

        audioclip = AudioFileClip(audio_path)
        clips = []

        text_clip = TextClip(text, fontsize=30, color='white', bg_color='black', size=(1280, 720)).set_duration(3)
        clips.append(text_clip)

        for image_name in os.listdir("images"):
            img_path = f"images/{image_name}"
            clip = ImageClip(img_path).set_duration(3)
            clips.append(clip)

        videoclip = ColorClip(size=(1280, 720), color=(255, 255, 255), duration=audioclip.duration).set_audio(audioclip)
        final_clip = concatenate_videoclips(clips + [videoclip], method="compose")

        final_clip.write_videofile(video_path, fps=24)

        return render_template('video.html', video_path=video_path)
    else:
        return "Error fetching images from Pexels", 500

if __name__ == '__main__':
    app.run(debug=True)


