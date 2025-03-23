import os

output_filename = "Project listing.txt"
excluded_dirs = [".venv", ".idea", ".git", "__pycache__"]  # Список исключаемых директорий

try:
    os.remove(output_filename)
except FileNotFoundError:
    pass

with open(output_filename, 'a', encoding='utf-8') as outfile:
    for dirpath, dirnames, filenames in os.walk('.'):  # Используем os.walk для обхода всех поддиректорий

        # Исключаем директории из обхода.  Работаем с dirnames "in-place".
        dirnames[:] = [d for d in dirnames if d not in excluded_dirs]


        for filename in filenames:
            filepath = os.path.join(dirpath, filename) # Полный путь к файлу
            if filename.endswith((".md", ".py", "Dockerfile", ".yml")):
                try:
                    with open(filepath, 'r', encoding='utf-8') as infile: # Читаем с utf-8
                        outfile.write(f"File: {filepath}\n") # Пишем полный путь файла
                        for line in infile:
                            outfile.write(line)
                        outfile.write("\n")
                except UnicodeDecodeError:
                    print(f"Ошибка декодирования при чтении файла: {filepath}. Файл пропущен.") # Пишем полный путь в ошибке
                    continue
            else:
                outfile.write(f"File: {filepath}\n") # Пишем полный путь файла

print(f"Готово! Файл '{output_filename}' создан в кодировке UTF-8.")
