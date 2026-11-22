import re

ENCODE_MAP = {
    '11111111': 'H', '1111111': 'G', '111111': 'F', '11111': 'E',
    '1111': 'D', '111': 'C', '11': 'B', '1': 'A',
    '00000000': '8', '0000000': '7', '000000': '6', '00000': '5',
    '0000': '4', '000': '3', '00': '2', '0': '1'
}
DECODE_MAP = {v: k for k, v in ENCODE_MAP.items()}
VALID_CHARS = set(DECODE_MAP.keys())
ENCODE_REGEX = re.compile('|'.join(sorted(ENCODE_MAP, key=len, reverse=True)))


def text_to_utf8_binary(text: str) -> str:
    return ''.join(format(byte, '08b') for byte in text.encode('utf-8'))


def decode_from_utf8_binary(binary_text: str) -> str:
    try:
        byte_chunks = [binary_text[i:i + 8] for i in range(0, len(binary_text), 8)]
        byte_array = bytearray(int(chunk, 2) for chunk in byte_chunks)
        return byte_array.decode('utf-8')
    except (UnicodeDecodeError, ValueError) as e:
        raise ValueError(f'Ошибка декодирования UTF-8: {e}')


def encrypt(text: str) -> str:
    if not text:
        return ''
    binary_text = text_to_utf8_binary(text)
    encrypted_chars = ENCODE_REGEX.sub(lambda m: ENCODE_MAP[m.group(0)], binary_text)
    return ' '.join(encrypted_chars[i:i + 2] for i in range(0, len(encrypted_chars), 2))


def decrypt(encrypted_text: str) -> str:
    if not encrypted_text.strip():
        return ''

    condensed = encrypted_text.replace(' ', '')

    invalid = set(condensed) - VALID_CHARS
    if invalid:
        raise ValueError(f'Неизвестные символы: {invalid}')

    binary_text = ''.join(DECODE_MAP[char] for char in condensed)

    if len(binary_text) % 8 != 0:
        raise ValueError(
            f'Длина бинарных данных ({len(binary_text)}) не кратна 8. '
            f'Данные повреждены.'
        )

    return decode_from_utf8_binary(binary_text)


def main() -> None:
    while True:
        choice = input("Выберите действие (encrypt / decrypt) или exit: ").strip().lower()
        if choice == 'exit':
            break
        if choice not in ('encrypt', 'decrypt'):
            print("Неверный ввод. Введите 'encrypt', 'decrypt' или 'exit'.")
            continue

        input_text = input("Введите текст: ")
        try:
            if choice == 'encrypt':
                print("Результат:", encrypt(input_text))
            else:
                print("Результат:", decrypt(input_text))
        except ValueError as e:
            print(f"Ошибка: {e}")


if __name__ == '__main__':
    main()
