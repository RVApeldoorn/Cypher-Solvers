from english_quadgrams import quadgram_score

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def caesar_cipher(text, shift, mode='encrypt'):
    shift = shift if mode == 'encrypt' else -shift
    result = []

    for char in text:
        if char.isalpha():
            shifted = alphabet[(alphabet.index(char.lower()) + shift) % 26]
            result.append(shifted.upper() if char.isupper() else shifted)
        else:
            result.append(char)
    
    return ''.join(result)

def quadgram_fitness(text):
    score = 0
    clean_text = ''.join(filter(str.isalpha, text)).lower()
    quadgrams = [clean_text[i:i+4] for i in range(len(text) - 3)]
    for quad in quadgrams:
        score += quadgram_score.get(quad, 23)
    return score

def solve_caesar_cipher(ciphertext):
    best_score, best_decryption = float('inf'), ''
    
    for shift in range(26):
        decrypted_text = caesar_cipher(ciphertext, shift, mode='decrypt')
        score = quadgram_fitness(decrypted_text)
        
        if score < best_score:
            best_score, best_decryption = score, decrypted_text
    
    return best_decryption

plaintext = """Peter Piper picked a peck of pickled peppers.
A peck of pickled peppers Peter Piper picked."""
shift = 3

encrypted_text = caesar_cipher(plaintext, shift, mode='encrypt')
print(f"Encrypted: {encrypted_text}")

decrypted_text = caesar_cipher(encrypted_text, shift, mode='decrypt')
print(f"Decrypted: {decrypted_text}")