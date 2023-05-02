from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup
import openai
import random
import os

app = Flask(__name__)

# Load OpenAI API key from environment variables
openai.api_key = os.environ.get("OPENAI_API_KEY")

def scrape_painting():
    api_key = os.environ.get("HARVARD_API_KEY")
    url = f"https://api.harvardartmuseums.org/object?apikey={api_key}&size=100&sort=random&classification=Paintings&hasimage=1&sortorder=asc"
    response = requests.get(url)
    data = response.json()

    if "records" not in data or not data["records"]:
        return {
            "image_url": None,
            "title": None,
            "artist": None,
            "date": None
        }

    painting = random.choice(data["records"])

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

def generate_artwork_info(artist, title):
    prompt1 = f"You are an art critique and poet. Please provide a beautiful interpretation of '{title}' by {artist}. Make it short if possible in bullet points. Make it fun and interesting. Include a short section that explains how it could resonate with our current society."
    prompt2 = f"Using the interpretation above as inspiration, write a short poem (4 lines) about '{title}' by {artist}. Make it fun and creative!"
    prompt3 = f"You are now writing an article about '{title}' by {artist}. Use the interpretation and poem above to write a 100 word article about this artwork and why it's significant."

    response1 = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt1,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
    )

    response2 = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt2,
        max_tokens=25,
        n=1,
        stop=None,
        temperature=0.7,
    )

    response3 = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt3,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return {
        "interpretation": response1.choices[0].text.strip(),
        "poem": response2.choices[0].text.strip(),
        "article": response3.choices[0].text.strip()
    }

@app.route('/')
def index():
    painting = scrape_painting()
    painting_info = generate_artwork_info(painting["artist"], painting["title"])
    painting["info"] = painting_info
    return render_template('index.html', painting=painting)

@app.route('/next_artwork')
def next_artwork():
    painting = scrape_painting()
    painting_info = generate_artwork_info(painting["artist"], painting["title"])
    painting["info"] = painting_info
    return jsonify(painting)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

