from flask import Flask, render_template, request
import os
import yt_dlp

app = Flask(__name__)

DOWNLOAD_PATH = "downloads"
os.makedirs(DOWNLOAD_PATH, exist_ok=True)


def is_youtube_url(url):
    return "youtube.com" in url or "youtu.be" in url


def download_video(url):
    ydl_opts = {
        "outtmpl": os.path.join(
            DOWNLOAD_PATH,
            "%(title)s.%(ext)s"
        ),

        # Default format = WEBM
        "format": "bestvideo[ext=webm]+bestaudio[ext=webm]/best[ext=webm]/best",
        "merge_output_format": "webm",

        "noplaylist": False,
        "quiet": False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


@app.route("/", methods=["GET", "POST"])
def home():
    message = ""

    if request.method == "POST":
        url = request.form.get("url", "").strip()

        if not url:
            message = "Please enter a URL."

        elif not is_youtube_url(url):
            message = "That is not a valid YouTube URL."

        else:
            try:
                download_video(url)
                message = "Download completed successfully (WEBM)."

            except Exception as e:
                message = f"Error: {str(e)}"

    return render_template(
        "index.html",
        message=message
    )


# Instant route:
# /https://youtube.com/watch?v=xxxx
# /https://youtube.com/shorts/xxxx
@app.route("/<path:youtubelink>")
def instant_download(youtubelink):
    if not youtubelink.startswith("http"):
        youtubelink = "https://" + youtubelink

    if not is_youtube_url(youtubelink):
        return "Invalid YouTube URL."

    try:
        download_video(youtubelink)
        return "Download started successfully (WEBM)."

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port
    )