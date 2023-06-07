from cryptography.fernet import Fernet

# Generate a secret key
key = Fernet.generate_key()

print("key: ", key)

# Save the key to a file named 'secret.key'
with open('secret.key', 'wb') as f:
    f.write(key)

message = b'Blue Straight'
print("message: ", message)
encrypted_message = Fernet(key).encrypt(message)
print("encrypted_message: ", encrypted_message)
decrypted_message = Fernet(key).decrypt(encrypted_message)
print("decrypted_message: ", decrypted_message)


# Load the secret key from the file
with open('secret.key', 'rb') as f:
    key = f.read()
print("key read: ", key)
decrypted_message = Fernet(key).decrypt(encrypted_message)
print("decrypted_message: loaded", decrypted_message)

#print the bit length of the encrypted message
print("encrypted_message bit length: ", len(encrypted_message)*8)
#print the bit length of the original message
print("message bit length: ", len(message)*8)