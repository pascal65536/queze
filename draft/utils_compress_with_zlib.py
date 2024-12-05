import zlib

def compress_with_zlib(s):
    # Сжимаем строку и кодируем в base64 для удобного представления
    compressed = zlib.compress(s.encode('utf-8'))
    return compressed

def decompress_with_zlib(s):
    decompress = zlib.decompress(s) 
    return decompress

# Пример использования
original_string = "ваш текст здесь Пример длинной строки" * 25  # Пример длинной строки
compressed_data = compress_with_zlib(original_string)
decompress_data = decompress_with_zlib(compressed_data)
print("Оригинальная строка:\n", original_string.encode(), len(original_string.encode()))
print("Сжатая строка (в формате base64):\n", compressed_data, len(compressed_data))
print("Оригинальная строка:\n", decompress_data.decode(), len(decompress_data.decode()))
