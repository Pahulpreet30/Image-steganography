from PIL import Image

def encode(image_path, message):
    img = Image.open(image_path)
    
   


    # Check and convert to RGB mode if necessary
    if img.mode != 'RGB':
        img = img.convert('RGB')
    pixels = img.load()
    # Continue with encoding logic


    binary_message = ''.join(format(ord(char), '08b') for char in message) + '11111111'  # Terminating signal
    message_index = 0

    width, height = img.size
    pixels = img.load()

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]

            if message_index < len(binary_message):
                r &= 0b11111110  # Clear the least significant bit
                r |= int(binary_message[message_index])
                message_index += 1

            pixels[x, y] = (r, g, b)

            if message_index >= len(binary_message):
                 print("Encoding successful!")
                 return img.save('static/'+'encoded_image.png')
                
               

    print("Message too long for the image!")

def decode(image_path):
    img = Image.open(image_path)
    width, height = img.size
    pixels = img.load()

    binary_message = ''
    message = ''

    for y in range(height):
        for x in range(width):
            r, _, _ = pixels[x, y]
            binary_message += str(r & 1)

            if binary_message[-8:] == '11111111':
                message = ''.join(chr(int(binary_message[i:i + 8], 2)) for i in range(0, len(binary_message) - 8, 8))
                return message
                

    print("No message found in the image!")

def main():
    choice = int(input(":: Welcome to Steganography ::\n"
                       "1. Encode\n2. Decode\n"))

    if choice == 1:
        image_path = input("Enter image name(with extension) : ")
        message = input("Enter data to be encoded : ")
        encode(image_path, message)
    elif choice == 2:
        image_path = input("Enter image name(with extension) : ")
        decode(image_path)
    else:
        print("Invalid choice!")

if __name__ == '__main__':
    main()
