import requests
from flask import Flask, render_template

app = Flask(__name__)

MEME_URL = "https://meme-api.com/gimme/wholesomememes"


@app.route("/")
def index():
    response = requests.request("GET", MEME_URL)
    data = response.json()
    return render_template(
        "meme.html",
        image_url=data.get("url"),
        title=data.get("title"),
        subreddit=data.get("subreddit"),
    )


if __name__ == "__main__":
    app.run(debug=True)
