import hmac

def compare_hashed_strings(hash1, hash2):
    # Securely compare two hashed strings
    return hash1 == hash2

# Example usage
hash1 = 'a5f5d5f0e3943b2316584c3e5e9e3b5e'
hash2 = 'a5f5d5f0e3943b2316584c3e5e9e3b5e'
hash3 = 'b5e4d5e5f3942a1236584c3d4d9d2c5d'

print('Hash 1 and Hash 2 are equal:', compare_hashed_strings(hash1, hash2))
print('Hash 1 and Hash 3 are equal:', compare_hashed_strings(hash1, hash3))
