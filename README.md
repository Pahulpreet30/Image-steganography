# Image-steganography
<br>
This Image Steganography project is a Python-based web application that allows users to hide and retrieve secret messages within digital images. Using the Least Significant Bit (LSB) method for encoding data, this application provides a secure way to embed encrypted text into images without visibly altering them. The encryption is handled using AES (Advanced Encryption Standard) to ensure that the hidden messages are secure and can only be accessed by authorized users.
<br>
# Features
<br>
- Encryption and Decryption: Encrypts messages using AES before encoding them into images, ensuring an additional layer of security.
- Data Hiding Using LSB: Implements the LSB technique to embed data within images, altering only the least significant bits to keep the image appearance nearly identical.
- Simple User Interface: Provides an easy-to-use interface built with Flask, allowing users to upload an image, enter a message, and retrieve the message from an encoded image.
- Secure Message Extraction: Only authorized users with the correct decryption key can retrieve the hidden message from an image.
- Supports Various Image Formats: Compatible with common image formats like PNG and BMP, which support lossless data embedding.

## Technologies Used

- Python: For backend processing, encryption, and image manipulation.
- Flask: As the web framework to serve the application and handle requests.
- Cryptography Library: For AES encryption and decryption of messages.
- Pillow (PIL): For image processing and manipulation.
- HTML, CSS, JavaScript: For the frontend interface of the application.

## How It Works

1. Message Encryption: Users enter a message to hide within an image, which is then encrypted using AES encryption.
2. Encoding the Message: The encrypted message is embedded into the least significant bits of the image's pixels.
3. Decoding the Message: To retrieve the message, the application extracts and decrypts the hidden data, returning the original message to the user.

# Getting Started
<br>
1. Clone the repository:<br>
   ```bash
   git clone https://github.com/yourusername/Image-steganography.git
   cd Image-steganography
   ```
<br>
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
<br>
3. Run the Flask application:
   ```bash
   python app.py
   ```
<br>
4. Open the app in your browser at `http://127.0.0.1:5000`.
<br>
 Use Cases
 <br>
- Confidential Communication: Safely transmit sensitive messages embedded within images.
- Digital Watermarking: Embed ownership or authentication data into images for intellectual property protection.
- Data Privacy in Public Platforms: Hide private information within images shared on public platforms.

## Future Improvements

- Support for more complex steganography algorithms.
- Enhanced user authentication and encryption techniques.
- Adding support for additional image formats.
