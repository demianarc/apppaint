from flask import Flask, render_template, jsonify
import requests
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Load API keys from environment variables
openai.api_key = os.environ.get('OPENAI_API_KEY')
HARVARD_API_KEY = os.environ.get('HARVARD_API_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_painting')
def get_painting():
    painting = get_random_painting()
    if painting:
        painting_info = generate_artwork_info(painting["artist"], painting["title"])
        painting["info"] = painting_info
        return jsonify({"success": True, "data": painting})
    else:
        return jsonify({"success": False})


def get_random_painting():
    url = "https://api.harvardartmuseums.org/object"
    params = {
        "apikey": HARVARD_API_KEY,
        "q": "classification:Paintings",
        "size": 1,
        "page": 1,
        "sort": "random",
        "sortorder": "asc",
        "hasimage": 1,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["info"]["totalrecords"] > 0:
            painting = data["records"][0]
            image_url = painting["primaryimageurl"]
            title = painting["title"]
            artist = painting["people"][0]["name"] if "people" in painting and painting["people"] else "Unknown artist"
            date = painting["dated"]

            return {
                "image_url": image_url,
                "title": title,
                "artist": artist,
                "date": date
            }
    return None


def generate_artwork_info(artist, title):
    prompt = f"Provide a brief and interesting interpretation of '{title}' by {artist}."
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].text.strip()


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
