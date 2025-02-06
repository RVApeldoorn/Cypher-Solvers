from english_quadgrams import quadgram_score
import random

# Lookup dictionaries for letter indexing
alphabet = 'abcdefghijklmnopqrstuvwxyz'
letter_to_index = {char: i for i, char in enumerate(alphabet)}
index_to_letter = {i: char for i, char in enumerate(alphabet)}

def validate_input(key, text):
    if not key:
        print("Key cannot be empty.")
        return False
    if not key.isalpha():
        print("Key must contain only alphabetic characters.")
        return False
    if not text:
        print("Ciphertext cannot be empty.")
        return False
    return True

def vigenere_transform(text, key, encrypt=True):
    if not validate_input(key, text):
        return None
    key = key.lower()
    transformed_text = ''
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = letter_to_index[key[key_index]]
            is_upper = char.isupper()
            base_char = char.lower()
            
            transformed_char = index_to_letter[(letter_to_index[base_char] + (shift if encrypt else -shift)) % 26]
            transformed_text += transformed_char.upper() if is_upper else transformed_char
            
            key_index = (key_index + 1) % len(key)
        else:
            transformed_text += char

    return transformed_text

def encrypt_vigenere(plaintext, key):
    return vigenere_transform(plaintext, key, encrypt=True)

def decrypt_vigenere(ciphertext, key):
    return vigenere_transform(ciphertext, key, encrypt=False)

# Cleans text, extracts quadgrams, and calculates fitness score
def quadgram_fitness(text):
    if not text:
        return None
    clean_text = ''.join([char.lower() for char in text if char.isalpha()])
    quadgrams = [clean_text[idx:idx + 4] for idx in range(len(clean_text) - 3)]
    return sum(quadgram_score.get(quad, 23) for quad in quadgrams)

# Mutate character at random index
def mutate_key(current_key):
    key_list = list(current_key)
    random_index = random.randint(0, len(current_key) - 1)
    key_list[random_index] = random.choice(alphabet)
    return ''.join(key_list)

# Decypher with only length of cyperkey
def solve_vigenere(ciphertext, key_length, runs=2, iterations=3000):
    best_overall_score = float('inf')
    best_overall_text, best_overall_key = '', ''
    
    for _ in range(runs):
        current_key = ''.join(random.choice(alphabet) for _ in range(key_length))
        no_improve_count = 0
        best_score, current_best_score = 5000, 5000
        best_text, best_key = '', current_key
        
        for _ in range(iterations * (key_length ** 2)):
            decrypted_text = decrypt_vigenere(ciphertext, current_key)
            if decrypted_text is None:
                print("Terminating early due to input validation error.")
                return None
            
            current_score = quadgram_fitness(decrypted_text)
            
            if current_score < current_best_score:
                if current_score < best_score:
                    best_score, best_text, best_key = current_score, decrypted_text, current_key 
                current_best_score = current_score
                test_key = current_key
            else:
                no_improve_count += 1
                if no_improve_count % (key_length * 100) == 0:
                    no_improve_count = 0
                    current_key = best_key
                if random.randint(1, 100) == 99:
                    current_best_score = current_score
                else:
                    current_key = test_key
            
            current_key = mutate_key(current_key)
        
        if best_score < best_overall_score:
            best_overall_score, best_overall_key, best_overall_text = best_score, best_key, best_text

    return best_overall_key, best_overall_text

plaintext = """Peter Piper picked a peck of pickled peppers.
A peck of pickled peppers Peter Piper picked."""

key = "secret"
encrypted_text = encrypt_vigenere(plaintext, key)
print(f"Encrypted Text: {encrypted_text}")

decrypted_text = decrypt_vigenere(encrypted_text, key)
print(f"Decrypted Text: {decrypted_text}")

recovered_key, recovered_text = solve_vigenere(encrypted_text, len(key))

print(f"Recovered Key: {recovered_key}")
print(f"Recovered Text: {recovered_text}")