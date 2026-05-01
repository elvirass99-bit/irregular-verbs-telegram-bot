# 📚 Telegram Bot для изучения неправильных глаголов

Бот помогает изучать английские неправильные глаголы через тренировку, словарь и систему повторения.

---

## 🇷🇺 Описание

Это Telegram-бот для изучения неправильных глаголов английского языка.

Проект создан не просто как учебная практика, а как полноценный мини-продукт:
бот умеет хранить прогресс, работать со списком слов "на изучение", проверять ответы и помогать повторять ошибки.

---

## 🚀 Возможности

- 📖 Словарь неправильных глаголов
- ✅ Отметка слов как "знаю"
- ❓ Отметка слов как "не знаю"
- 🧠 Список "На изучение"
- 🎯 Тренировка с 5 уровнями сложности
- 🔁 Повтор ошибок
- 📊 Статистика пользователя
- 🔐 Защита доступа паролем
- 💾 Сохранение прогресса в JSON

---

## 🧠 Как это работает

1. Пользователь открывает словарь.
2. Отмечает слова как "знаю" или "не знаю".
3. Слова "не знаю" попадают в список "На изучение".
4. Пользователь проходит тренировку.
5. Бот проверяет ответы и сохраняет ошибки.
6. Выученные слова можно убрать из списка.

---

## 🛠 Запуск

    pip install -r requirements.txt
    python bot.py

---

## 🔑 Настройка

В файле `bot.py` нужно указать:

    TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
    ACCESS_PASSWORD = "YOUR_PASSWORD"

---

## ⚠️ Важно

Файл `user_progress.json` создаётся автоматически.

Он хранит прогресс пользователя и не должен загружаться в GitHub.

---

# 🇺🇸 English Version

## 📚 Telegram Bot for Learning Irregular Verbs

This is a Telegram bot for learning English irregular verbs through practice, repetition, and progress tracking.

The project was created not just as a simple beginner exercise, but as a small real product with user progress, study list, training levels, and mistake repetition.

---

## 🚀 Features

- 📖 Irregular verbs dictionary
- ✅ Mark verbs as known
- ❓ Mark verbs as unknown
- 🧠 Study list
- 🎯 Training with 5 difficulty levels
- 🔁 Mistake repetition
- 📊 User statistics
- 🔐 Password protection
- 💾 Progress saving with JSON

---

## 🧠 How it works

1. The user opens the dictionary.
2. The user marks verbs as known or unknown.
3. Unknown verbs are added to the study list.
4. The user starts training.
5. The bot checks answers and saves mistakes.
6. Learned verbs can be removed from the study list.

---

## 🛠 Run

    pip install -r requirements.txt
    python bot.py

---

## 🔑 Setup

In `bot.py`, set:

    TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
    ACCESS_PASSWORD = "YOUR_PASSWORD"

---

## 📌 Tech Stack

- Python
- python-telegram-bot
- JSON

---

## 🎯 Project Goal

The goal of this project is to practice Python, Telegram Bot API, user progress tracking, and building a real portfolio project.

This project is part of my learning path toward AI automation and practical software development.
