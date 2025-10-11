def cyper_encode(text,shift):
    texts = [text]
    for i in range(1, shift+1):
        encoded_text = ''
        
        for ch in text:
            if ch.isalpha():
                base = ord('A') if ch.isupper() else ord('a')
                encoded_text += chr((ord(ch) - base + 1) % 26 + base )
            else:
                encoded_text += ch
        texts.append(encoded_text)
        text = encoded_text
    return texts


def cyper_decode(text):
    texts = [text]
    for i in range(1,27):
        decoded=''
        for ch in text:
            if ch.isalpha():
                base = ord('A') if ch.isupper() else ord('a')
                decoded+=chr( (ord(ch)-base-1)%26+base)
            else:
                decoded+=ch
        texts.append(decoded)
        text = decoded
    return texts


def main():
    texts = cyper_encode('I love mars',26)
    for idx, text in enumerate(texts):
        print(f'{idx:02d}: {text}')

    
    print('='*50)
    print(texts[10])
    decoded = cyper_decode(texts[10])
    for idx, text in enumerate(decoded):
        print(f'{idx:02d}: {text}')
def test_alpha():
    text = "I love marts1"
    print("I will Test",text)
    for ch in text:
        print(f'{ch} is {ch.isalpha()}, {ch.isupper()}, {ch.islower()}, {ch.isalnum()}')
if __name__ == "__main__":
    main()
    #test_alpha()