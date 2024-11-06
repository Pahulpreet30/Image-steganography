from Crypto import Random
from Crypto.Cipher import AES
from cryptography.fernet import Fernet
from Crypto.Protocol.KDF import PBKDF2

class Encryptor:
    def __init__(self, key): 
        self.key = key

    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)
    
    def decrypt(self, ciphertext):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")
    

key=Fernet.generate_key()
f=Fernet(key)
aes_key = PBKDF2(key, b'salt', 32, count=1000000)
encryptor = Encryptor(aes_key)
# decryptor = Encryptor(aes_key)
print(aes_key)
encrypted_message=None
# while True:

#     choice = int(input("1.Press '1' to encrypt Message .\n""2.Press '2' to decrypt Message \n""3.To exit\n"))

#     if choice == 1:
#         message=input("enter text to be encrypted : " )
#         encrypted_message=encryptor.encrypt(message.encode())
#         print("the message encrypted is : ", encrypted_message)
#     elif choice == 2:
#       if encrypted_message is None:
#         print("No message encrypted yet")
#       else:
        
#         #  encrypted_message=encryptor.encrypt(message.encode())
#         decrypted_message=encryptor.decrypt(encrypted_message)
#         print("the message encrypted is : ", decrypted_message)

#     elif choice==3:
#         exit()

#     else:
#         print("Enter a valid option")

