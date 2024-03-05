import hashlib

def hash_blocks_individually(file_path, block_size=65536):
    """
    Hashes each block of a file individually and returns a list of hash outputs for each block.

    :param file_path: Path to the file to be hashed
    :param block_size: Size of each block read from the file (in bytes)
    :return: A list of hexadecimal hash strings, one for each block of the file content
    """
    block_hashes = []
    with open(file_path, 'rb') as f:  # Open the file in binary mode
        block = f.read(block_size)  # Read the first block of the file
        while block:  # Keep reading blocks until the end of the file
            hash_object = hashlib.sha256()  # Create a new sha256 hash object for each block
            hash_object.update(block)  # Update the hash object with the block
            block_hashes.append(hash_object.hexdigest())  # Append the block's hash to the list
            block = f.read(block_size)  # Read the next block of the file
    return block_hashes

# Example usage
# Make sure to replace 'path_to_your_file' with the actual file path
file_path = 'path_to_your_file'
block_hashes = hash_blocks_individually(file_path)
for i, block_hash in enumerate(block_hashes):
    print(f'Block {i+1} hash: {block_hash}')
