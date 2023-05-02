from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup
import openai
import os

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Load OpenAI API key from environment variables
openai.api_key = os.environ.get('OPENAI_API_KEY')

def scrape_painting():
    url = "https://www.harvardartmuseums.org/collections/object/299843"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    image_url = soup.find("img", class_="primary-image")["src"]
    title = soup.find("h1", class_="title").text.strip()
    artist = soup.find("div", class_="people-list__person").text.strip()
    date = soup.find("span", class_="date-display-single").text.strip()

    return {
        "image_url": image_url,
        "title": title,
        "artist": artist,
        "date": date
    }

def generate_artwork_info(artist, title):
    prompt = f"Please provide a beautiful interpretation of '{title}' by {artist}. Make it short, fun, and interesting."

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].text.strip()

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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
