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

    if not files:
        return "No files uploaded"

    songs = []

    for f in files:

        if f.filename == "":
            continue

        # tránh trùng tên file
        filename = str(uuid.uuid4()) + ".mp3"
        path = os.path.join(UPLOAD_FOLDER, filename)

        f.save(path)

        try:
            audio = AudioSegment.from_file(path)
            songs.append(audio)
        except Exception as e:
            return f"Error processing file: {str(e)}"

    if len(songs) == 0:
        return "No valid audio files"

    # ghép tất cả bài trước
    final = songs[0]

    for s in songs[1:]:
        final += s

    # nhân 3 lần sau khi ghép
    final = final * 3

    # tạo file output
    output_name = str(uuid.uuid4()) + ".mp3"
    output_path = os.path.join(OUTPUT_FOLDER, output_name)

    try:
        final.export(output_path, format="mp3")
    except Exception as e:
        return f"Export error: {str(e)}"

    return send_file(output_path, as_attachment=True)


if __name__ == "__main__":
    app.run()
