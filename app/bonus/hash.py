import hashlib

def hash_password(password):
    # Create a sha256 hash object
    hash_object = hashlib.sha256()
    
    # Convert the password to bytes and hash it
    hash_object.update(password.encode('utf-8'))
    
    # Convert the hash to a hexadecimal string for easier handling
    hex_dig = hash_object.hexdigest()
    
    return hex_dig

# Example usage
password = 'example_password'
hashed_password = hash_password(password)
print('Hashed Password:', hashed_password)
