from flask import Flask, request, send_file, render_template
from pydub import AudioSegment
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_files():
    files = request.files.getlist("files")

    songs = []

    for f in files:
        path = os.path.join(UPLOAD_FOLDER, f.filename)
        f.save(path)

        audio = AudioSegment.from_mp3(path)

        # lặp 3 lần
        audio = audio * 3

        songs.append(audio)

    # ghép tất cả
    final = songs[0]

    for s in songs[1:]:
        final += s

    output_name = str(uuid.uuid4()) + ".mp3"
    output_path = os.path.join(OUTPUT_FOLDER, output_name)

    final.export(output_path, format="mp3")

    return send_file(output_path, as_attachment=True)


if __name__ == "__main__":
    app.run()
