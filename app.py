from flask import Flask, render_template, request, redirect, url_for, session,flash
from flask_sqlalchemy import SQLAlchemy
from Crypto.Protocol.KDF import PBKDF2
from aes import Encryptor  
import base64
from lsb import *
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)

app.config['SECRET_KEY'] = 'jhdjdkjdlajflj'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///encrypt.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Upload_Folder = "C:\\Users\\Asus\\Desktop\\My Project\\static"
Allowed_Extensions = {'png', 'jpg', 'jpeg', 'gif'}
app.config["Upload_Folder"] = Upload_Folder

app.app_context().push()
db = SQLAlchemy(app)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Allowed_Extensions


class Encrypt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String, nullable=False)

@app.route("/", methods=['GET','POST'])
def hello_world1():
    return render_template("index.html")

@app.route("/hello", methods=['GET', 'POST'])
def hello_world():
    if request.method == "POST":
        message = request.form.get("message")
        aes_key = PBKDF2(b'some password', b'salt', 32, count=1000000)
        encryptor = Encryptor(aes_key)
        encrypted_message = encryptor.encrypt(message.encode())
        encrypted_message_base64 = base64.b64encode(encrypted_message).decode('utf-8')

        new_message = Encrypt(message=encrypted_message_base64)
        db.session.add(new_message)
        db.session.commit()

        # Fetch the recently added encrypted message from the database
        encrypted_message_from_db = Encrypt.query.order_by(Encrypt.id.desc()).first().message

        # Store the encrypted message in the session
        session['encrypted_message'] = encrypted_message_from_db
        
        # Redirect to the /upload route
        
        # return redirect(url_for('upload'))
       
        return render_template("upload.html")

    return render_template("encrypt.html")

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'image' not in request.files:
            return "No image part in the form!"

        file = request.files['image']
        if file.filename == '':
            return "No selected file!"
       
        # Get the encrypted message from the session
        encrypted_message1= session.pop('encrypted_message', None)

        if encrypted_message1 is None:
            return "Error: Encrypted message not found in session!"

        # Here you can process the image file as needed.
        file_path = 'static/' + secure_filename(file.filename)
        file.save(file_path)

        # Decode the encrypted message from base64
        # encrypted_message = base64.b64decode(encrypted_message_base64)

        # Pass the encrypted message to the encode_lsb method
        encode(file_path, encrypted_message1)
        
        return render_template("index.html")

    return render_template("upload.html")



@app.route('/decrypt', methods=['GET', 'POST'])
def image_decode():
    print("Inside image_decode function")
    if request.method == 'POST':
        print("POST method detected")
        if 'image' not in request.files:
            return "No image part in the form!"

        file = request.files['image']
        if file.filename == '':
            return "No selected file!"

        # Check if the file is an allowed image format
        if file and allowed_file(file.filename):
            image_path = 'static/' + secure_filename(file.filename)
            print("Image path:", image_path)

            # Save the uploaded image to check if it's received correctly
            file.save(image_path)

            # Check if the file is saved correctly
            if not os.path.exists(image_path):
                return "Error: Uploaded file not saved correctly!"

            try:
                # Attempt to decode the message
                decoded_message = decode(image_path)
                print("Decoded message:", decoded_message)
                session["decrypted_message"]=decoded_message
                print("Decrypted message stored in session:", session["decrypted_message"])
                # Redirect to the 'show' route with the decoded message
                return redirect(url_for('decrypted_message'))
                
            except Exception as e:
                print("Error decoding message:", e)
                return "Error decoding message"
        else:
            return "Invalid file format. Allowed formats are: png, jpg, jpeg, gif"
        

    return render_template("decrypt.html")

@app.route("/decrypted_message",methods=['GET','POST'])
def decrypted_message():
    decrypted_message2=session.pop("decrypted_message",None)
    if decrypted_message2 is None:
        return "Error: Decrypted message not found in session!"
    # decrypted_message2=session.get("decrypted_message",None)
    print(decrypted_message2)
    decrypted_message_binary = base64.b64decode(decrypted_message2)
    aes_key = PBKDF2(b'some password', b'salt', 32, count=1000000)
    decryptor = Encryptor(aes_key)
    decrypted_message1 = decryptor.decrypt(decrypted_message_binary)


    return render_template("display.html",decrypted_message1=decrypted_message1)

if __name__ == '__main__':

    app.run(debug=True)



