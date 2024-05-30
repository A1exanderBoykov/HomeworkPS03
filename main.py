import requests
from bs4 import BeautifulSoup
from googletrans import Translator


# Создаём функцию, которая будет получать информацию
def get_english_words():
    url = "https://randomword.com/"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на успешность запроса

        # Создаём объект Soup
        soup = BeautifulSoup(response.content, "html.parser")
        # Получаем слово. text.strip удаляет все пробелы из результата
        english_word = soup.find("div", id="random_word").text.strip()
        # Получаем описание слова
        word_definition = soup.find("div", id="random_word_definition").text.strip()

        # Чтобы программа возвращала словарь
        return {
            "english_word": english_word,
            "word_definition": word_definition
        }
    # Функция, которая сообщит об ошибке, но не остановит программу
    except requests.RequestException as e:
        print(f"Произошла ошибка: {e}")
        return None


# Создаём функцию, которая будет переводить на русский язык
def translate_to_russian(word, definition):
    translator = Translator()
    translated_word = translator.translate(word, src='en', dest='ru').text
    translated_definition = translator.translate(definition, src='en', dest='ru').text
    return translated_word, translated_definition


# Создаём функцию, которая будет делать саму игру
def word_game():
    print("Добро пожаловать в игру")

    while True:
        # Получаем случайное слово и его определение
        word_dict = get_english_words()
        if word_dict is None:
            continue  # Если произошла ошибка, попробуем снова

        word = word_dict.get("english_word")
        word_definition = word_dict.get("word_definition")

        # Переводим слово и его определение на русский
        translated_word, translated_definition = translate_to_russian(word, word_definition)

        # Начинаем игру
        print(f"Значение слова - {translated_definition}")
        user = input("Что это за слово? ")
        if user.lower() == translated_word.lower():
            print("Все верно!")
        else:
            print(f"Ответ неверный, было загадано это слово - {translated_word}")

        # Создаём возможность закончить игру
        play_again = input("Хотите сыграть еще раз? да/нет: ")
        if play_again.lower() != "да":
            print("Спасибо за игру!")
            break

if __name__ == "__main__":
    word_game()