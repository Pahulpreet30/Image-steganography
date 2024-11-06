
from PIL import Image
import os

def message_to_bin(message):
    """Converts a message to binary."""
    return ''.join(format(ord(char), '08b') for char in message)

def compress_message(message):
    """Compresses the message."""
    # Implement your message compression algorithm here
    # For demonstration purposes, let's assume a simple compression by removing spaces
    compressed_message = message.replace(" ", "")
    return compressed_message

def encode_lsb(image_path, message):
    """Encodes a message into an image using LSB steganography."""
    img = Image.open(image_path)
    width, height = img.size
    binary_message = message_to_bin(message)

    # Adding a delimiter at the end
    binary_message += '1111111111111110'

    if len(binary_message) > width * height * 3:
        raise ValueError("Message is too large for the image.")

    data_index = 0
    for y in range(height):
        for x in range(width):
            pixel = list(img.getpixel((x, y)))
            for i in range(3):
                if data_index < len(binary_message):
                    pixel[i] = pixel[i] & ~1 | int(binary_message[data_index])
                    data_index += 1
            img.putpixel((x, y), tuple(pixel))

    encoded_file_path = os.path.splitext(image_path)[0] + "_encoded.png"
    img.save(encoded_file_path)
    print(f"Encoded image saved as '{encoded_file_path}'")
    print(message)
def decode_lsb(image_path):
    """Decodes a message from an image using LSB steganography."""
    from PIL import Image
    import os

    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError("Image file not found.")
        
        img = Image.open(image_path)
        width, height = img.size

        binary_message = ""
        for y in range(height):
            for x in range(width):
                pixel = img.getpixel((x, y))
                for color in pixel:
                    binary_message += str(color & 1)

        delimiter = '1111111111111110'
        delimiter_index = binary_message.find(delimiter)
        if delimiter_index == -1:
            return "No message found in the image."
        else:
            binary_message = binary_message[:delimiter_index]

        message_chunks = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]

        message = ""
        for chunk in message_chunks:
            message += chr(int(chunk, 2))

        return message

    except Exception as e:
        # Log the error
        print(f"Error decoding message from image: {e}")
        return "Error decoding message from image."


# # Prompt user for input
# image_path = input("Enter the path to the image file: ").strip()
# if not os.path.exists(image_path):
#     print("File not found.")
#     exit()

# # Load the image to get its dimensions
# img = Image.open(image_path)
# width, height = img.size

# encode_or_decode = input("Do you want to encode (E) or decode (D) a message? ").upper()
# if encode_or_decode == "E":
#     message = input("Enter the message to encode: ")

#     # Convert message to binary
#     binary_message = message_to_bin(message)

#     # Calculate the maximum message size that can be encoded
#     max_message_size = width * height * 3

#     if len(binary_message) > max_message_size:
#         print("Message is too large for the image.")
#         option = input("Do you want to compress the message (C) or input another image with greater size (I)? ").upper()
#         if option == "C":
#             # Implement message compression here
#             compressed_message = compress_message(message)
#             binary_message = message_to_bin(compressed_message)
#             if len(binary_message) > max_message_size:
#                 print("Compressed message is still too large. Exiting.")
#                 exit()
#         elif option == "I":
#             new_image_path = input("Enter the path to another image file with greater size: ").strip()
#             if not os.path.exists(new_image_path):
#                 print("File not found.")
#                 exit()
#             img = Image.open(new_image_path)
#             width, height = img.size
#             max_message_size = width * height * 3
#         else:
#             print("Invalid option. Exiting.")
#             exit()

#     # Encode the message into the image
#     encode_lsb(image_path, message)
# elif encode_or_decode == "D":
#     decode_lsb(image_path)
# else:
#     print("Invalid option.")