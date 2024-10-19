def encrypt_rail_fence(message, depth):
    # Create a rail of empty strings
    rail = ['' for _ in range(depth)]
    
    # The message is traversed in a zigzag manner
    down = False
    row = 0
    
    for char in message:
        rail[row] += char
        
        if row == 0 or row == depth - 1:
            down = not down
        row += 1 if down else -1
    
    # Concatenate all rows to get the encrypted message
    return ''.join(rail)

def decrypt_rail_fence(encrypted_message, depth):
    # Create a list of empty strings for the rail pattern
    rail = [['\n' for _ in range(len(encrypted_message))] for _ in range(depth)]
    
    # Mark the places in the zigzag pattern where characters were placed
    down = None
    row, col = 0, 0
    for i in range(len(encrypted_message)):
        if row == 0:
            down = True
        if row == depth - 1:
            down = False
        
        rail[row][col] = '*'
        col += 1
        
        row = row + 1 if down else row - 1
    
    # Now, place the characters in the marked positions
    index = 0
    for i in range(depth):
        for j in range(len(encrypted_message)):
            if rail[i][j] == '*' and index < len(encrypted_message):
                rail[i][j] = encrypted_message[index]
                index += 1
    
    # Read the message following the zigzag pattern
    result = []
    row, col = 0, 0
    for i in range(len(encrypted_message)):
        if row == 0:
            down = True
        if row == depth - 1:
            down = False
        
        if rail[row][col] != '\n':
            result.append(rail[row][col])
            col += 1
        
        row = row + 1 if down else row - 1
    
    return ''.join(result)

def repeated_rail_fence_cipher(message, key):
    depth, repeat = key
    
    # Convert message to lowercase and keep spaces
    message = message.lower()
    
    # Repeat the encryption process 'r' times
    for _ in range(repeat):
        message = encrypt_rail_fence(message, depth)
    
    return message

def repeated_rail_fence_decipher(encrypted_message, key):
    depth, repeat = key
    
    # Repeat the decryption process 'r' times
    for _ in range(repeat):
        encrypted_message = decrypt_rail_fence(encrypted_message, depth)
    
    return encrypted_message

# Example usage:
if __name__ == "__main__":
    # Input message and key for encryption
    n = input("Enter the message: ")
    k = tuple(map(int, input("Enter the key (depth, repeats): ").split(',')))
    
    # Encrypt message
    encrypted_message = repeated_rail_fence_cipher(n, k)
    print("Encrypted message:", encrypted_message)
    
    # Decrypt message
    decrypted_message = repeated_rail_fence_decipher(encrypted_message, k)
    print("Decrypted message:", decrypted_message)
