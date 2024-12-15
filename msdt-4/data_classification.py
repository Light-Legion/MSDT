import json
import logging
from ruwordnet import RuWordNet

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("data_classification.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# === Шаг 1. Расширение словаря с помощью RuWordNet ===

# Базовый словарь
expressive_status_dict = {
    "mood": {
        "text": {
            "negative": ["грусть", "печаль", "разочарование", "злость", "усталость", "слёзы",
                         "ненужность", "обман", "поражение", "жестокость" ],
            "positive": ["радость", "вдохновение", "любовь", "оптимизм", "счастье", "дружба",
                         "смех", "целеустремленность", "удовлетворение", "искренность", "люблю", "любовь" ],
            "neutral": ["спокойствие", "тишина", "наблюдение", "размышление", "безмолвие",
                        "нейтралитет", "ожидание", "баланс", "равновесие" ]
        },
        "emoji": {
            "negative": ["😢", "😡", "😭", "😞", "😔", "😩", "🥵", "🤬", "🫤", "😶‍🌫️", "🥶"],
            "positive": ["😊", "😍", "😁", "😎", "🎉", "❤️", "🌞", "👍", "✨", "🥰", "🤗"],
            "neutral": ["😐", "🤔", "😶", "🙄", "😏", "🫢", "🤷‍♂️", "🤷‍♀️", "😑"]
        }
    },
    "worldview": {
        "text": {
            "optimistic": ["верю", "будущее светлое", "надежда", "лучшее впереди", "силы внутри",
                           "благоприятные изменения", "будущее без границ", "оптимизм в каждом шаге"],
            "pessimistic": ["всё плохо", "нет смысла", "ничего не изменится", "бесперспективность",
                            "сгущение туч", "жизнь не имеет смысла", "невозможные цели"],
            "skeptical": ["сомнения", "критика", "не верю", "ложь", "недостаток доказательств",
                          "сомнительные утверждения", "вопросы без ответов", "критический взгляд"]
        },
        "emoji": {
            "optimistic": ["😊", "🌟", "✨", "🌞", "👍", "🎯", "🌈", "💪"],
            "pessimistic": ["😢", "😔", "😭", "😩", "😟", "🫤", "😶‍🌫️"],
            "skeptical": ["🙄", "🤔", "😏", "🤷‍♂️", "🤷‍♀️"]
        }
    },
    "provocative": {
        "text": {
            "political": ["свобода", "правительство", "оппозиция", "митинг", "реформы",
                          "выборы", "оппозиционный лидер", "диктатура", "коррупция"],
            "discrimination": ["ненавижу", "нетерпимость", "разделение", "агрессия", "расизм",
                               "ксенофобия", "презрение", "стереотипы", "антисемитизм" ],
            "false_statements": ["всемирный заговор", "неверная информация", "фальшивые новости",
                                 "мнимые факты", "слухи", "псевдонаучные утверждения", "непроверенная информация"]
        },
        "emoji": {
            "political": ["🤬", "✊", "🇷🇺", "🇺🇦", "🔴", "⚖️"],
            "discrimination": ["🤬", "😡", "👎", "❌"],
            "false_statements": ["😏", "🙄", "🤥", "🧐"]
        }
    },
    "manipulative": {
        "text": {
            "sympathy_request": ["помогите", "мне плохо", "жаль", "тяжело", "нуждаюсь в поддержке",
                                 "мне так трудно", "у меня всё разваливается", "мне страшно", "мне так одиноко" ],
            "superiority": ["я лучше всех", "никто не понимает", "умнее других", "я всегда прав",
                            "мои идеи лучшие", "я никогда не ошибаюсь", "я единственный, кто понимает"],
            "indirect_aggression": ["плохие люди", "вред", "нападение", "обвинение", "вы виноваты",
                                    "это ваша ошибка", "это ваша вина", "это ваша проблема", "мне это не нравится"],
            "hidden_accusation": ["кто виноват", "почему вы", "всё из-за вас", "я бы никогда так не сделал",
                                  "вы как всегда", "вы опять допустили ошибку", "кто же так работает"]
        },
        "emoji": {
            "sympathy_request": ["😢", "😭", "😟", "🫤", "🥺", "💔"],
            "superiority": ["😎", "😏", "🤴", "👸", "👑", "💸", "🔥"],
            "indirect_aggression": ["🤬", "😡", "❌", "👎", "🖕"],
            "hidden_accusation": ["🙄", "😤", "🤷‍♂️", "🤷‍♀️"]
        }
    }
}

# Словарь стоп-слов
stopwords_dict = {
    "commercial": {
        "text": {
            "self_promotion": [
                "приглашаю", "заходите", "мой блог", "мой канал", "подписывайтесь",
                "делюсь опытом", "мои достижения", "узнайте больше", "inst", "insta",
                "инст", "инста", "ищу работу",
                "https://", "репост", "ищешь работу", "вакансия", "онлайн",
            ],
            "sales": [
                "распродажа", "скидка", "товар", "продаю", "купить", "предложение",
                "акция", "новинка", "доставка", "заказ", "лс"
            ]
        }
    },
    "situational": {
        "text": {
            "personal_events": [
                "день рождения", "свадьба", "юбилей", "встреча", "в отпуске",
                "в дороге", "поездка", "новый год", "праздник"
            ],
            "calendar_events": [
                "день защитника отечества", "8 марта", "новый год", "рождество",
                "праздник", "поздравляю", "каникулы", "выходные"
            ],
            "social_significant_events": [
                "митинг", "выборы", "катастрофа", "чрезвычайное происшествие",
                "проблема", "новости", "важная информация", "объявление", "доллар"
            ]
        }
    }
}

# Инициализация RuWordNet
wordnet = RuWordNet()

def expand_keywords_ruwordnet(keywords):
    expanded_keywords = set(keywords)
    for word in keywords:
        synsets = wordnet.get_synsets(word)
        for synset in synsets:
            for lemma in synset.senses:
                expanded_keywords.add(lemma.name.lower())  # Добавляем все леммы из синонимичных групп
    return list(expanded_keywords)

# Расширение словаря
logging.info("Расширение словарей с помощью RuWordNet")
for category, subcategories in expressive_status_dict.items():
    for modality, sentiments in subcategories.items():
        if modality == "text":  # Расширяем только текстовые токены
            for sentiment, keywords in sentiments.items():
                expressive_status_dict[category][modality][sentiment] = expand_keywords_ruwordnet(keywords)

# Расширение словаря стоп-слов
for category, subcategories in stopwords_dict.items():
    for modality, sentiments in subcategories.items():
        if modality == "text":  # Расширяем только текстовые токены
            for sentiment, keywords in sentiments.items():
                stopwords_dict[category][modality][sentiment] = expand_keywords_ruwordnet(keywords)

# === Шаг 2. Классификация статусов ===

# Загрузка данных пользователей
input_file = "cleared_data.json"
output_file = "second_expressive_statuses.json"


logging.info(f"Загрузка данных из файла {input_file}")
with open(input_file, "r", encoding="utf-8") as file:
    data = json.load(file)


# Функция для классификации статусов
logging.info("Классификация статусов")
def classify_status(status, dictionary):
    status_lower = status.lower()

    # Шаг 1: Проверяем текстовые токены
    for category, subcategories in dictionary.items():
        for modality, sentiments in subcategories.items():
            if modality == "text":
                for sentiment, keywords in sentiments.items():
                    if any(keyword in status_lower for keyword in keywords):
                        return {category: sentiment}  # Если нашли текстовое совпадение, возвращаем результат

    # Шаг 2: Проверяем эмодзи, только если текстовое совпадение не найдено
    for category, subcategories in dictionary.items():
        for modality, sentiments in subcategories.items():
            if modality == "emoji":
                for sentiment, keywords in sentiments.items():
                    if any(emoji in status for emoji in keywords):
                        return {category: sentiment}  # Если нашли совпадение по эмодзи, возвращаем результат

    # Если ничего не найдено, возвращаем None
    return None


# Анализ статусов
expressive_statuses = []

for user in data:
    status_text = user.get("status", "")
    classification = classify_status(status_text, expressive_status_dict)
    if classification:
        user["status"] = {
            "text": status_text,
            "classification": classification
        }
        expressive_statuses.append(user)

# Сохранение экспрессивных статусов
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(expressive_statuses, file, ensure_ascii=False, indent=4)

# === Шаг 3. Фильтрация стоп-словами ===

# Функция фильтрации
logging.info("Фильтрация статусов")
def filter_stopwords(status, stopwords):
    status_lower = status.lower()
    for category, subcategories in stopwords.items():
        for modality, sentiments in subcategories.items():
            for sentiment, keywords in sentiments.items():
                if any(keyword in status_lower for keyword in keywords):
                    return True  # Статус содержит стоп-слова
    return False

# Убираем статусы с использованием стоп-слов
filtered_statuses = []

for user in expressive_statuses:
    status_text = user["status"]["text"]
    if not filter_stopwords(status_text, stopwords_dict):
        filtered_statuses.append(user)

# Сохранение очищенных данных
filtered_output_file = "cleared_second_expressive_statuses.json"


logging.info(f"Обработано пользователей: {len(data)}")
logging.info(f"Экспрессивных статусов найдено: {len(expressive_statuses)}")
logging.info(f"Экспрессивных статусов после очистки от стоп-слов: {len(filtered_statuses)}")


logging.info(f"Сохранение данных в файл {output_file}")
with open(filtered_output_file, "w", encoding="utf-8") as file:
    json.dump(filtered_statuses, file, ensure_ascii=False, indent=4)
logging.info("Данные успешно сохранены.")