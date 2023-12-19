import re

# Укажите путь к исходному файлу и целевому файлу
source_file_path = '/parser/old_item'
target_file_path = '/parser/item_python'


def process_content(content):
    # Заменяем пробелы на "_____"
    modified_content = re.sub(r'(?<=\S) (?!\S* )', '__________', content.strip())
    # Добавляем "_____" в конец каждой строки
    return '\n'.join([line + '__________' for line in modified_content.split('\n')])


try:
    # Открываем исходный файл для чтения
    with open(source_file_path, 'r', encoding='utf-8') as source_file:
        # Читаем содержимое исходного файла
        file_content = source_file.read()
        modified_file_content = process_content(file_content)

    # Открываем целевой файл для записи (это перезапишет его существующее содержимое)
    with open(target_file_path, 'w', encoding='utf-8') as target_file:
        # Записываем обновленное содержимое обратно в целевой файл
        target_file.write(modified_file_content)

    print(f"Содержимое файла {source_file_path} успешно скопировано с добавленными '__________' в {target_file_path}")
except FileNotFoundError:
    print("Указанный файл не найден.")
except Exception as e:
    print(f"Произошла ошибка: {e}")



