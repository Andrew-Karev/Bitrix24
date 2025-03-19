import re
from collections import Counter

def remove_html_tags(text):
    """Удаляет HTML-теги из текста"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def extract_words(text):
    """Извлекает слова из текста, состоящие из букв и длиной не менее 3 символов"""
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text)
    return [word.lower() for word in words]

def main():
    # Запрос пути к HTML-файлу
    file_path = input("Введите путь к HTML-файлу: ")
    
    try:
        # Чтение содержимого файла
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        # Удаление HTML-тегов
        text_without_tags = remove_html_tags(html_content)
        
        # Извлечение слов
        words = extract_words(text_without_tags)
        
        # Подсчёт частоты слов
        word_counts = Counter(words)
        
        # Получение топ-10 слов
        top_10_words = word_counts.most_common(10)
        
        # Вывод результата
        print("Топ-10 наиболее часто встречающихся слов:")
        for word, count in top_10_words:
            print(f"{word}: {count}")
    
    except FileNotFoundError:
        print("Файл не найден. Пожалуйста, проверьте путь к файлу.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()