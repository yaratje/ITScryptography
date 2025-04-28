
def caesar_decrypt(text, shift):
    decrypted = ''
    for char in text:
        shifted = (ord(char.upper()) - ord('A') - shift) % 26
        decrypted += chr(shifted + ord('A'))
    return decrypted

#shifts 0–25 to generate all the possibilities
def gen_shift_list(text):
    options = [caesar_decrypt(text, shift) for shift in range(0, 26)]
    #print(options[1])
    return(options)