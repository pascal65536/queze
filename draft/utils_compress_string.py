def compress_string(s):
    compressed = []
    count = 1

    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            compressed.append(s[i - 1])
            if count > 1:
                compressed.append(str(count))
            count = 1

    # Добавляем последний символ и его количество
    compressed.append(s[-1])
    if count > 1:
        compressed.append(str(count))

    compressed_string = ''.join(compressed)

    # Если сжатая строка все еще длиннее 100 символов, возвращаем оригинал
    return compressed_string if len(compressed_string) <= 100 else s

# Пример использования
original_string = "aaabbbccddeeefffffggghhhiiijjjjjjkkkkk"
original_string = "# Если сжатая строка все еще длиннее 100 символов, возвращаем оригинал"
compressed_string = compress_string(original_string)
print("Оригинальная строка:", original_string)
print("Сжатая строка:", compressed_string)
