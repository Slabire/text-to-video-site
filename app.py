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

@app.route('/generate-video', methods=['POST'])
def generate_video():
    text = request.form['text']
    audio_path = 'static/temp.mp3'
    video_path = 'static/result.mp4'

    # Generate audio from text
    tts = gTTS(text=text, lang='en')
    tts.save(audio_path)

    # Set headers for the Pexels API request
    headers = {
        "Authorization": api_key
    }

    # Search query for Pexels (you can modify this)
    search_query = "video generation"

    # Set the parameters for the search
    params = {
        "query": search_query,
        "per_page": 5,  # Number of results per page
        "page": 1       # Page number to retrieve
    }

    # Make a GET request to the Pexels API
    response = requests.get(url, headers=headers, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        photos = data.get('photos', [])

        # Create folder for images if it doesn't exist
        if not os.path.exists("images"):
            os.makedirs("images")

        # Download images from Pexels and save locally
        for photo in photos:
            image_url = photo['src']['original']
            image_name = f"{photo['id']}.jpg"
            img_data = requests.get(image_url).content
            with open(f"images/{image_name}", 'wb') as handler:
                handler.write(img_data)

        # Create video using images and audio
        audioclip = AudioFileClip(audio_path)
        clips = []

        # Add a text clip
        text_clip = TextClip(text, fontsize=30, color='white', bg_color='black', size=(1280, 720))
        text_clip = text_clip.set_duration(3)  # Duration of the text
        clips.append(text_clip)

        # Add images as clips
        for image_name in os.listdir("images"):
            img_path = f"images/{image_name}"
            clip = ImageClip(img_path)
            clip = clip.set_duration(3)  # Duration of each image
            clips.append(clip)

        # Create a base white video clip with audio
        videoclip = ColorClip(size=(1280, 720), color=(255, 255, 255), duration=audioclip.duration)
        videoclip = videoclip.set_audio(audioclip)

        # Combine the video clips (text + images) with the white background video
        final_clip = concatenate_videoclips(clips + [videoclip], method="compose")

        # Save the final video
        final_clip.write_videofile(video_path, fps=24)

        # Return the video to the user
        return render_template('video.html', video_path=video_path)
    else:
        return "Error fetching images from Pexels", 500

if __name__ == '__main__':
    app.run(debug=True)

