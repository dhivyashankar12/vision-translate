from application import app, dropzone
from flask import render_template, request, redirect, url_for, session
from .forms import QRCodeData
import secrets
import os

# OCR
import cv2
import pytesseract
from PIL import Image
import numpy as np
# pip install gTTS
from gtts import gTTS

# import utils
from . import utils


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == 'POST':

        # set a session value
        sentence = ""
        
        f = request.files.get('file')
        filename, extension = f.filename.split(".")
        generated_filename = secrets.token_hex(10) + f".{extension}"
       

        file_location = os.path.join(app.config['UPLOADED_PATH'], generated_filename)

        f.save(file_location)

        # print(file_location)

        # OCR here
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


        img = cv2.imread(file_location)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


        boxes = pytesseract.image_to_data(img)
        # print(boxes)
    
        for i, box in enumerate(boxes.splitlines()):
            if i == 0:
                continue

            box = box.split()
            # print(box)

            # only deal with boxes with word in it.
            if len(box) == 12:
                sentence += box[11] + " "
       
        # print(sentence)
        session["sentence"] = sentence

        # delete file after you are done working with it
        os.remove(file_location)

        return redirect("/decoded")

    else:
       return render_template("upload.html", title="Home")


@app.route("/decoded", methods=["GET", "POST"])
def decoded():

    form = QRCodeData()

    # Retrieve sentence from session (could be None)
    sentence = session.get("sentence", "")
    print(sentence)
    # Detect language for display (if sentence empty, lang will default)
    lang, _ = utils.detect_language(sentence if sentence else "")
    print(lang)
    if request.method == "POST":
        # On POST, get form data and generate audio from translated text
        text_data = form.data_field.data
        translate_to = form.language.data

        # Translate the text
        translated_text = utils.translate_text(text_data, translate_to)

        # Generate TTS audio
        tts = gTTS(translated_text, lang=translate_to)
        generated_audio_filename = secrets.token_hex(10) + ".mp3"  # Use .mp3 for gTTS output

        file_location = os.path.join(app.config['AUDIO_FILE_UPLOAD'], generated_audio_filename)
        tts.save(file_location)

        # Set the form field data to the translated text so it shows in the textarea
        form.data_field.data = translated_text

        # Render template with audio available
        return render_template(
            "decoded.html",
            title="Decoded",
            form=form,
            lang=utils.languages.get(lang, lang),
            audio=url_for('static', filename='audio_files/' + generated_audio_filename)
        )

    # GET request: prefill form textarea with extracted sentence
    form.data_field.data = sentence


    return render_template(
        "decoded.html",
        title="Decoded",
        form=form,
        lang=utils.languages.get(lang, lang),
        audio=None
    )
    session["sentence"] = ""
    return response


