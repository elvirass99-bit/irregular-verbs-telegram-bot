import json
import logging
import os
import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

TOKEN = ""
ACCESS_PASSWORD = "070699"
PROGRESS_FILE = "user_progress.json"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

(
    AUTH_PASSWORD,
    MAIN_MENU,
    DICTIONARY_MODE,
    CHOOSE_COUNT,
    CHOOSE_LEVEL,
    RESET_CONFIRM,
    LEVEL1,
    LEVEL2,
    LEVEL3,
    LEVEL4,
    LEVEL5,
) = range(11)

VERBS = [
    {"ru": "быть", "base": "be", "past": "was/were", "participle": "been"},
    {"ru": "становиться", "base": "become", "past": "became", "participle": "become"},
    {"ru": "начинать", "base": "begin", "past": "began", "participle": "begun"},
    {"ru": "ломать", "base": "break", "past": "broke", "participle": "broken"},
    {"ru": "приносить", "base": "bring", "past": "brought", "participle": "brought"},
    {"ru": "строить", "base": "build", "past": "built", "participle": "built"},
    {"ru": "покупать", "base": "buy", "past": "bought", "participle": "bought"},
    {"ru": "ловить", "base": "catch", "past": "caught", "participle": "caught"},
    {"ru": "выбирать", "base": "choose", "past": "chose", "participle": "chosen"},
    {"ru": "приходить", "base": "come", "past": "came", "participle": "come"},
    {"ru": "стоить", "base": "cost", "past": "cost", "participle": "cost"},
    {"ru": "резать", "base": "cut", "past": "cut", "participle": "cut"},
    {"ru": "делать", "base": "do", "past": "did", "participle": "done"},
    {"ru": "рисовать", "base": "draw", "past": "drew", "participle": "drawn"},
    {"ru": "пить", "base": "drink", "past": "drank", "participle": "drunk"},
    {"ru": "водить", "base": "drive", "past": "drove", "participle": "driven"},
    {"ru": "есть", "base": "eat", "past": "ate", "participle": "eaten"},
    {"ru": "падать", "base": "fall", "past": "fell", "participle": "fallen"},
    {"ru": "чувствовать", "base": "feel", "past": "felt", "participle": "felt"},
    {"ru": "драться", "base": "fight", "past": "fought", "participle": "fought"},
    {"ru": "находить", "base": "find", "past": "found", "participle": "found"},
    {"ru": "летать", "base": "fly", "past": "flew", "participle": "flown"},
    {"ru": "забывать", "base": "forget", "past": "forgot", "participle": "forgotten"},
    {"ru": "получать", "base": "get", "past": "got", "participle": "got"},
    {"ru": "давать", "base": "give", "past": "gave", "participle": "given"},
    {"ru": "идти", "base": "go", "past": "went", "participle": "gone"},
    {"ru": "расти", "base": "grow", "past": "grew", "participle": "grown"},
    {"ru": "иметь", "base": "have", "past": "had", "participle": "had"},
    {"ru": "слышать", "base": "hear", "past": "heard", "participle": "heard"},
    {"ru": "прятать", "base": "hide", "past": "hid", "participle": "hidden"},
    {"ru": "держать", "base": "hold", "past": "held", "participle": "held"},
    {"ru": "хранить", "base": "keep", "past": "kept", "participle": "kept"},
    {"ru": "знать", "base": "know", "past": "knew", "participle": "known"},
    {"ru": "оставлять / покидать", "base": "leave", "past": "left", "participle": "left"},
    {"ru": "позволять", "base": "let", "past": "let", "participle": "let"},
    {"ru": "терять", "base": "lose", "past": "lost", "participle": "lost"},
    {"ru": "делать / создавать", "base": "make", "past": "made", "participle": "made"},
    {"ru": "значить / иметь в виду", "base": "mean", "past": "meant", "participle": "meant"},
    {"ru": "встречать", "base": "meet", "past": "met", "participle": "met"},
    {"ru": "платить", "base": "pay", "past": "paid", "participle": "paid"},
    {"ru": "класть", "base": "put", "past": "put", "participle": "put"},
    {"ru": "читать", "base": "read", "past": "read", "participle": "read"},
    {"ru": "ездить верхом", "base": "ride", "past": "rode", "participle": "ridden"},
    {"ru": "звонить", "base": "ring", "past": "rang", "participle": "rung"},
    {"ru": "бежать", "base": "run", "past": "ran", "participle": "run"},
    {"ru": "говорить / сказать", "base": "say", "past": "said", "participle": "said"},
    {"ru": "видеть", "base": "see", "past": "saw", "participle": "seen"},
    {"ru": "продавать", "base": "sell", "past": "sold", "participle": "sold"},
    {"ru": "отправлять", "base": "send", "past": "sent", "participle": "sent"},
    {"ru": "показывать", "base": "show", "past": "showed", "participle": "shown"},
    {"ru": "закрывать", "base": "shut", "past": "shut", "participle": "shut"},
    {"ru": "петь", "base": "sing", "past": "sang", "participle": "sung"},
    {"ru": "сидеть", "base": "sit", "past": "sat", "participle": "sat"},
    {"ru": "спать", "base": "sleep", "past": "slept", "participle": "slept"},
    {"ru": "говорить", "base": "speak", "past": "spoke", "participle": "spoken"},
    {"ru": "тратить", "base": "spend", "past": "spent", "participle": "spent"},
    {"ru": "стоять", "base": "stand", "past": "stood", "participle": "stood"},
    {"ru": "красть", "base": "steal", "past": "stole", "participle": "stolen"},
    {"ru": "плавать", "base": "swim", "past": "swam", "participle": "swum"},
    {"ru": "брать", "base": "take", "past": "took", "participle": "taken"},
    {"ru": "учить", "base": "teach", "past": "taught", "participle": "taught"},
    {"ru": "рассказывать", "base": "tell", "past": "told", "participle": "told"},
    {"ru": "думать", "base": "think", "past": "thought", "participle": "thought"},
    {"ru": "бросать", "base": "throw", "past": "threw", "participle": "thrown"},
    {"ru": "понимать", "base": "understand", "past": "understood", "participle": "understood"},
    {"ru": "просыпаться", "base": "wake", "past": "woke", "participle": "woken"},
    {"ru": "носить", "base": "wear", "past": "wore", "participle": "worn"},
    {"ru": "выигрывать", "base": "win", "past": "won", "participle": "won"},
    {"ru": "писать", "base": "write", "past": "wrote", "participle": "written"},
    {"ru": "кусать", "base": "bite", "past": "bit", "participle": "bitten"},
    {"ru": "дуть", "base": "blow", "past": "blew", "participle": "blown"},
    {"ru": "иметь дело", "base": "deal", "past": "dealt", "participle": "dealt"},
    {"ru": "кормить", "base": "feed", "past": "fed", "participle": "fed"},
    {"ru": "висеть", "base": "hang", "past": "hung", "participle": "hung"},
    {"ru": "ударять", "base": "hit", "past": "hit", "participle": "hit"},
    {"ru": "причинять боль", "base": "hurt", "past": "hurt", "participle": "hurt"},
    {"ru": "вести", "base": "lead", "past": "led", "participle": "led"},
    {"ru": "одалживать", "base": "lend", "past": "lent", "participle": "lent"},
    {"ru": "лежать", "base": "lie", "past": "lay", "participle": "lain"},
    {"ru": "зажигать / освещать", "base": "light", "past": "lit", "participle": "lit"},
]

ALL_FORMS = []
for verb in VERBS:
    ALL_FORMS.extend([verb["base"], verb["past"], verb["participle"]])


def load_progress():
    if not os.path.exists(PROGRESS_FILE):
        return {}
    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return {}


def save_progress(data):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def get_user_record(user_id: int):
    data = load_progress()
    key = str(user_id)

    if key not in data:
        data[key] = {
            "known_verbs": [],
            "unknown_verbs": [],
            "total_answers": 0,
            "correct_answers": 0,
            "wrong_answers": 0,
            "mistake_forms": 0,
            "best_streak": 0,
            "shown_counts": {},
        }
        save_progress(data)

    data[key].setdefault("known_verbs", [])
    data[key].setdefault("unknown_verbs", [])
    data[key].setdefault("total_answers", 0)
    data[key].setdefault("correct_answers", 0)
    data[key].setdefault("wrong_answers", 0)
    data[key].setdefault("mistake_forms", 0)
    data[key].setdefault("best_streak", 0)
    data[key].setdefault("shown_counts", {})
    save_progress(data)

    return data[key]


def save_user_record(user_id: int, record: dict):
    data = load_progress()
    data[str(user_id)] = record
    save_progress(data)


def mark_verb_status(user_id: int, verb_base: str, known: bool):
    record = get_user_record(user_id)
    known_list = record["known_verbs"]
    unknown_list = record["unknown_verbs"]

    if known:
        if verb_base not in known_list:
            known_list.append(verb_base)
        if verb_base in unknown_list:
            unknown_list.remove(verb_base)
    else:
        if verb_base not in unknown_list:
            unknown_list.append(verb_base)
        if verb_base in known_list:
            known_list.remove(verb_base)

    save_user_record(user_id, record)


def get_unknown_verbs(user_id: int):
    record = get_user_record(user_id)
    unknown_bases = record["unknown_verbs"]
    return [verb for verb in VERBS if verb["base"] in unknown_bases]


def reset_user_progress(user_id: int):
    data = load_progress()
    key = str(user_id)
    if key in data:
        del data[key]
        save_progress(data)


def update_user_progress(user_id: int, correct: bool, mistake_forms: int, best_streak: int):
    record = get_user_record(user_id)

    record["total_answers"] += 1
    if correct:
        record["correct_answers"] += 1
    else:
        record["wrong_answers"] += 1

    record["mistake_forms"] += mistake_forms
    if best_streak > record["best_streak"]:
        record["best_streak"] = best_streak

    save_user_record(user_id, record)


def increment_shown_count(user_id: int, verb_base: str):
    record = get_user_record(user_id)
    counts = record["shown_counts"]
    counts[verb_base] = counts.get(verb_base, 0) + 1
    save_user_record(user_id, record)


def get_correct_forms(verb: dict) -> list[str]:
    return [verb["base"], verb["past"], verb["participle"]]


def count_errors(user_answer: list[str], correct_answer: list[str]) -> int:
    errors = 0
    for user_word, correct_word in zip(user_answer, correct_answer):
        if user_word.strip().lower() != correct_word.strip().lower():
            errors += 1
    return errors


def get_error_details(user_answer: list[str], correct_answer: list[str]) -> list[str]:
    names = ["I", "II", "III"]
    details = []
    for i, (user_word, correct_word) in enumerate(zip(user_answer, correct_answer)):
        if user_word.strip().lower() != correct_word.strip().lower():
            details.append(f"Ошибка в форме {names[i]}: правильно <b>{correct_word}</b>")
    return details


def mask_word(word: str) -> str:
    if len(word) <= 2:
        return word
    if len(word) == 3:
        return word[0] + "_" + word[-1]
    return word[0] + "_" * (len(word) - 2) + word[-1]


def start_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Словарь 📚", callback_data="dictionary")],
        [InlineKeyboardButton("На изучение ❓", callback_data="study_list")],
        [InlineKeyboardButton("Тренировка 🚀", callback_data="training")],
        [InlineKeyboardButton("Уровни 🔥", callback_data="levels")],
        [InlineKeyboardButton("Сброс прогресса 🗑", callback_data="reset_progress")],
    ])


def levels_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Уровень 1🧚🏼", callback_data="level_1")],
        [InlineKeyboardButton("Уровень 2🏋🏽‍♂️", callback_data="level_2")],
        [InlineKeyboardButton("Уровень 3🎉", callback_data="level_3")],
        [InlineKeyboardButton("Уровень 4💥", callback_data="level_4")],
        [InlineKeyboardButton("Уровень 5💣", callback_data="level_5")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="back_main")],
    ])


def count_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("5 слов", callback_data="count_5")],
        [InlineKeyboardButton("10 слов", callback_data="count_10")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="back_main")],
    ])


def dictionary_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Знаю ✅", callback_data="mark_known")],
        [InlineKeyboardButton("Не знаю ❓", callback_data="mark_unknown")],
        [InlineKeyboardButton("Следующее слово ➡️", callback_data="next_dictionary")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="back_main")],
    ])


def after_answer_keyboard(has_mistakes=False):
    keyboard = [[InlineKeyboardButton("Следующее слово ➡️", callback_data="next_word")]]
    if has_mistakes:
        keyboard.append([InlineKeyboardButton("Повторить ошибки 🔁", callback_data="repeat_mistakes")])
    keyboard.append([InlineKeyboardButton("⬅️ В меню", callback_data="back_main")])
    return InlineKeyboardMarkup(keyboard)


def reset_confirm_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Да, сбросить ❗", callback_data="confirm_reset")],
        [InlineKeyboardButton("Нет", callback_data="back_main")],
    ])


def get_state_by_level(level: int):
    if level == 1:
        return LEVEL1
    if level == 2:
        return LEVEL2
    if level == 3:
        return LEVEL3
    if level == 4:
        return LEVEL4
    return LEVEL5


def build_choice_options(correct_forms: list[str], total_options: int):
    options = []

    for i, word in enumerate(correct_forms):
        options.append({
            "id": f"correct_{i}",
            "word": word,
        })

    pool = list(set(word for word in ALL_FORMS if word not in set(correct_forms)))
    random.shuffle(pool)

    needed = max(0, total_options - len(options))
    distractors = pool[:needed]

    for i, word in enumerate(distractors):
        options.append({
            "id": f"distractor_{i}",
            "word": word,
        })

    random.shuffle(options)
    return options


def get_triplet_options(correct_verb: dict, total_options: int = 4):
    correct_triplet = get_correct_forms(correct_verb)
    other_verbs = [v for v in VERBS if v != correct_verb]
    random.shuffle(other_verbs)

    triplets = [correct_triplet]
    for verb in other_verbs[: total_options - 1]:
        triplets.append(get_correct_forms(verb))

    random.shuffle(triplets)
    return triplets


def reset_session(context: ContextTypes.DEFAULT_TYPE):
    auth_ok = context.user_data.get("auth_ok", False)
    current_level = context.user_data.get("current_level", 5)

    context.user_data.clear()
    context.user_data["auth_ok"] = auth_ok
    context.user_data["current_level"] = current_level
    context.user_data["round_correct"] = 0
    context.user_data["round_total"] = 0
    context.user_data["round_mistake_forms"] = 0
    context.user_data["streak"] = 0
    context.user_data["best_streak"] = 0
    context.user_data["mistake_verbs"] = []
    context.user_data["mistake_mode"] = False
    context.user_data["selected_answers"] = []
    context.user_data["selected_ids"] = []
    context.user_data["round_verbs"] = []
    context.user_data["choice_options"] = []


def build_round_verbs(context: ContextTypes.DEFAULT_TYPE, user_id: int):
    limit = context.user_data.get("round_limit", 5)

    if context.user_data.get("mistake_mode") and context.user_data.get("mistake_verbs"):
        pool = context.user_data["mistake_verbs"][:]
        random.shuffle(pool)
        context.user_data["round_verbs"] = pool[:limit]
        return

    record = get_user_record(user_id)
    counts = record["shown_counts"]

    pool = VERBS[:]
    pool.sort(key=lambda verb: counts.get(verb["base"], 0))

    grouped = {}
    for verb in pool:
        cnt = counts.get(verb["base"], 0)
        grouped.setdefault(cnt, []).append(verb)

    ordered_pool = []
    for cnt in sorted(grouped.keys()):
        chunk = grouped[cnt]
        random.shuffle(chunk)
        ordered_pool.extend(chunk)

    context.user_data["round_verbs"] = ordered_pool[:limit]


def get_next_round_verb(context: ContextTypes.DEFAULT_TYPE, user_id: int):
    round_verbs = context.user_data.get("round_verbs", [])

    if not round_verbs:
        build_round_verbs(context, user_id)
        round_verbs = context.user_data.get("round_verbs", [])

    if not round_verbs:
        return random.choice(VERBS)

    return round_verbs.pop(0)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("auth_ok"):
        await show_main_menu_message(update, update.effective_user.id)
        return MAIN_MENU

    await update.message.reply_text("Введите пароль 🔐")
    return AUTH_PASSWORD


async def check_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    password = update.message.text.strip()

    if password != ACCESS_PASSWORD:
        await update.message.reply_text("Неверный пароль ❌\nПопробуй ещё раз.")
        return AUTH_PASSWORD

    context.user_data["auth_ok"] = True
    reset_session(context)
    context.user_data["current_level"] = 5

    await show_main_menu_message(update, update.effective_user.id)
    return MAIN_MENU


async def show_main_menu_message(update: Update, user_id: int):
    record = get_user_record(user_id)
    text = (
        "Привет! Я бот для изучения неправильных глаголов 🇬🇧\n\n"
        "Что у меня есть:\n"
        "• Словарь 📚\n"
        "• На изучение ❓\n"
        "• Тренировка 🚀\n"
        "• Уровни 🔥\n"
        "• Повтор ошибок 🔁\n"
        "• Статистика и серии правильных ответов\n\n"
        f"Твоя общая статистика:\n"
        f"Ответов: <b>{record['total_answers']}</b>\n"
        f"Правильных: <b>{record['correct_answers']}</b>\n"
        f"Ошибок: <b>{record['wrong_answers']}</b>\n"
        f"Лучшая серия: <b>{record['best_streak']}</b>\n\n"
        "Выбери режим:"
    )
    await update.message.reply_text(text, reply_markup=start_keyboard(), parse_mode="HTML")


async def show_main_menu_query(query, user_id: int):
    record = get_user_record(user_id)
    text = (
        "Привет! Я бот для изучения неправильных глаголов 🇬🇧\n\n"
        "Что у меня есть:\n"
        "• Словарь 📚\n"
        "• На изучение ❓\n"
        "• Тренировка 🚀\n"
        "• Уровни 🔥\n"
        "• Повтор ошибок 🔁\n"
        "• Статистика и серии правильных ответов\n\n"
        f"Твоя общая статистика:\n"
        f"Ответов: <b>{record['total_answers']}</b>\n"
        f"Правильных: <b>{record['correct_answers']}</b>\n"
        f"Ошибок: <b>{record['wrong_answers']}</b>\n"
        f"Лучшая серия: <b>{record['best_streak']}</b>\n\n"
        "Выбери режим:"
    )
    await query.edit_message_text(text, reply_markup=start_keyboard(), parse_mode="HTML")


async def back_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not context.user_data.get("auth_ok"):
        await query.edit_message_text("Сначала введи пароль 🔐")
        return AUTH_PASSWORD

    await show_main_menu_query(query, query.from_user.id)
    return MAIN_MENU


async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "back_main":
        await show_main_menu_query(query, query.from_user.id)
        return MAIN_MENU

    if query.data == "dictionary":
        return await send_dictionary_card(query, context, query.from_user.id, edit=True)

    if query.data == "study_list":
        unknown = get_unknown_verbs(query.from_user.id)
        if not unknown:
            await query.answer(
                "На изучение 0 слов. Чтобы добавить — зайди в Словарь 📚 и нажми «Не знаю ❓».",
                show_alert=True,
            )
            return MAIN_MENU
        return await show_study_list(query)

    if query.data == "training":
        await query.edit_message_text(
            "Тренировка 🚀\n\nВыбери количество слов в раунде:",
            reply_markup=count_keyboard(),
        )
        return CHOOSE_COUNT

    if query.data == "levels":
        await query.edit_message_text(
            "Уровни 🔥\n\nВыбери уровень сложности:",
            reply_markup=levels_keyboard(),
        )
        return CHOOSE_LEVEL

    if query.data == "reset_progress":
        await query.edit_message_text(
            "Вы точно хотите сбросить прогресс?",
            reply_markup=reset_confirm_keyboard(),
        )
        return RESET_CONFIRM

    return MAIN_MENU


async def send_dictionary_card(query, context: ContextTypes.DEFAULT_TYPE, user_id: int, edit=True):
    verb = random.choice(VERBS)
    context.user_data["dictionary_verb"] = verb

    record = get_user_record(user_id)
    known_list = record["known_verbs"]
    unknown_list = record["unknown_verbs"]

    status = "Статус: без отметки"
    if verb["base"] in known_list:
        status = "Статус: знаю ✅"
    elif verb["base"] in unknown_list:
        status = "Статус: на изучение ❓"

    text = (
        f"Словарь 📚\n\n"
        f"Русский: <b>{verb['ru']}</b>\n"
        f"I : <b>{verb['base']}</b>\n"
        f"II : <b>{verb['past']}</b>\n"
        f"III : <b>{verb['participle']}</b>\n\n"
        f"{status}"
    )

    if edit:
        await query.edit_message_text(text, reply_markup=dictionary_keyboard(), parse_mode="HTML")
    else:
        await query.message.reply_text(text, reply_markup=dictionary_keyboard(), parse_mode="HTML")

    return DICTIONARY_MODE


async def next_dictionary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    return await send_dictionary_card(query, context, query.from_user.id, edit=True)


async def mark_known(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("Отмечено как знаю ✅")
    verb = context.user_data.get("dictionary_verb")
    if verb:
        mark_verb_status(query.from_user.id, verb["base"], known=True)
    return await send_dictionary_card(query, context, query.from_user.id, edit=True)


async def mark_unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("Добавлено в список на изучение ❓")
    verb = context.user_data.get("dictionary_verb")
    if verb:
        mark_verb_status(query.from_user.id, verb["base"], known=False)
    return await send_dictionary_card(query, context, query.from_user.id, edit=True)


async def mark_learned_from_study(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("Слово отмечено как выученное ✅")

    verb_base = query.data.split(":", 1)[1]
    mark_verb_status(query.from_user.id, verb_base, known=True)

    remaining = get_unknown_verbs(query.from_user.id)
    if not remaining:
        await query.edit_message_text(
            "На изучение ❓\n\n"
            "Сейчас 0 слов.\n\n"
            "Чтобы добавить слова — зайди в Словарь 📚 и нажми «Не знаю ❓».",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Назад", callback_data="back_main")]
            ]),
        )
        return MAIN_MENU

    return await show_study_list(query)


async def show_study_list(query):
    unknown_verbs = get_unknown_verbs(query.from_user.id)

    if not unknown_verbs:
        await query.edit_message_text(
            "На изучение ❓\n\n"
            "Сейчас 0 слов.\n\n"
            "Чтобы добавить слова — зайди в Словарь 📚 и нажми «Не знаю ❓».",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Назад", callback_data="back_main")]
            ]),
        )
        return MAIN_MENU

    text_lines = ["На изучение ❓\n"]
    keyboard = []

    for i, verb in enumerate(unknown_verbs, start=1):
        text_lines.append(f"{i}. {verb['ru']} — {verb['base']}, {verb['past']}, {verb['participle']}")
        keyboard.append([
            InlineKeyboardButton(
                f"Выучено ✅ ({verb['base']})",
                callback_data=f"learned:{verb['base']}"
            )
        ])

    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="back_main")])

    await query.edit_message_text(
        "\n".join(text_lines),
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return MAIN_MENU


async def reset_confirm_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "confirm_reset":
        reset_user_progress(query.from_user.id)
        await query.edit_message_text(
            "Прогресс сброшен ✅",
            reply_markup=start_keyboard(),
        )
        return MAIN_MENU

    await show_main_menu_query(query, query.from_user.id)
    return MAIN_MENU


async def choose_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "back_main":
        await show_main_menu_query(query, query.from_user.id)
        return MAIN_MENU

    count = int(query.data.split("_")[1])
    current_level = context.user_data.get("current_level", 5)

    reset_session(context)
    context.user_data["auth_ok"] = True
    context.user_data["current_level"] = current_level
    context.user_data["round_limit"] = count
    build_round_verbs(context, query.from_user.id)

    await query.edit_message_text(
        f"Тренировка 🚀\n\n"
        f"Количество слов: <b>{count}</b>\n"
        f"Текущий уровень: <b>{context.user_data.get('current_level', 5)}</b>\n\n"
        f"Начинаем!",
        parse_mode="HTML",
    )
    return await send_task(query, context, edit=True)


async def choose_level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "back_main":
        await show_main_menu_query(query, query.from_user.id)
        return MAIN_MENU

    level = int(query.data.split("_")[1])
    context.user_data["current_level"] = level

    await query.edit_message_text(
        f"Уровень <b>{level}</b> выбран ✅\n\n"
        f"Теперь можешь идти в Тренировка 🚀",
        reply_markup=start_keyboard(),
        parse_mode="HTML",
    )
    return MAIN_MENU


async def send_round_summary(query, context: ContextTypes.DEFAULT_TYPE):
    total = context.user_data.get("round_total", 0)
    correct = context.user_data.get("round_correct", 0)
    mistakes = context.user_data.get("round_mistake_forms", 0)
    best_streak = context.user_data.get("best_streak", 0)

    text = (
        f"🏁 Раунд завершён\n\n"
        f"Правильно: <b>{correct}/{total}</b>\n"
        f"Ошибок по формам: <b>{mistakes}</b>\n"
        f"Лучшая серия: <b>{best_streak}</b>\n"
    )

    if context.user_data.get("mistake_verbs"):
        keyboard = [
            [InlineKeyboardButton("Повторить ошибки 🔁", callback_data="repeat_mistakes")],
            [InlineKeyboardButton("⬅️ В меню", callback_data="back_main")],
        ]
    else:
        keyboard = [[InlineKeyboardButton("⬅️ В меню", callback_data="back_main")]]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML",
    )


def build_choice_keyboard(choice_options, selected_ids):
    keyboard = []
    row = []

    for item in choice_options:
        label = f"✅ {item['word']}" if item["id"] in selected_ids else item["word"]
        row.append(
            InlineKeyboardButton(label, callback_data=f"pick:{item['id']}:{item['word']}")
        )
        if len(row) == 2:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton("Сбросить выбор 🔄", callback_data="reset_choice")])
    return InlineKeyboardMarkup(keyboard)


async def send_task(query, context: ContextTypes.DEFAULT_TYPE, edit=True):
    level = context.user_data["current_level"]
    verb = get_next_round_verb(context, query.from_user.id)
    increment_shown_count(query.from_user.id, verb["base"])

    context.user_data["current_verb"] = verb
    context.user_data["selected_answers"] = []
    context.user_data["selected_ids"] = []

    ru = verb["ru"]
    correct_forms = get_correct_forms(verb)

    if level == 1:
        choice_options = build_choice_options(correct_forms, total_options=6)
        context.user_data["choice_options"] = choice_options

        text = (
            f"📘 Уровень 1\n\n"
            f"Русский глагол: <b>{ru}</b>\n"
            f"Выбери 3 правильные формы по порядку.\n\n"
            f"Твой выбор: —"
        )
        markup = build_choice_keyboard(choice_options, [])

    elif level == 2:
        choice_options = build_choice_options(correct_forms, total_options=9)
        context.user_data["choice_options"] = choice_options

        text = (
            f"📗 Уровень 2\n\n"
            f"Русский глагол: <b>{ru}</b>\n"
            f"Выбери 3 правильные формы по порядку.\n\n"
            f"Твой выбор: —"
        )
        markup = build_choice_keyboard(choice_options, [])

    elif level == 3:
        triplet_options = get_triplet_options(verb, total_options=4)
        context.user_data["triplet_options"] = triplet_options
        masked = " – ".join(mask_word(word) for word in correct_forms)

        text = (
            f"📙 Уровень 3\n\n"
            f"Русский глагол: <b>{ru}</b>\n"
            f"Формы с пропусками:\n<b>{masked}</b>\n\n"
            f"Выбери правильный полный набор форм:"
        )

        keyboard = []
        for triplet in triplet_options:
            keyboard.append([
                InlineKeyboardButton(
                    " – ".join(triplet),
                    callback_data=f"triplet:{'|'.join(triplet)}"
                )
            ])
        markup = InlineKeyboardMarkup(keyboard)

    elif level == 4:
        text = (
            f"📕 Уровень 4\n\n"
            f"Русский глагол: <b>{ru}</b>\n"
            f"I : <b>{verb['base']}</b>\n\n"
            f"Напиши II и III форму через запятую.\n"
            f"Пример: <code>went, gone</code>"
        )
        markup = None

    else:
        text = (
            f"📒 Уровень 5\n\n"
            f"Русский глагол: <b>{ru}</b>\n\n"
            f"Напиши I, II, III форму через запятую.\n"
            f"Пример: <code>go, went, gone</code>"
        )
        markup = None

    await query.edit_message_text(text, reply_markup=markup, parse_mode="HTML")
    return get_state_by_level(level)


async def next_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if context.user_data.get("round_total", 0) >= context.user_data.get("round_limit", 5):
        await send_round_summary(query, context)
        return get_state_by_level(context.user_data["current_level"])

    return await send_task(query, context, edit=True)


async def repeat_mistakes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not context.user_data.get("mistake_verbs"):
        await show_main_menu_query(query, query.from_user.id)
        return MAIN_MENU

    context.user_data["mistake_mode"] = True
    context.user_data["round_total"] = 0
    context.user_data["round_correct"] = 0
    context.user_data["round_mistake_forms"] = 0
    context.user_data["streak"] = 0
    context.user_data["best_streak"] = 0
    context.user_data["round_limit"] = len(context.user_data["mistake_verbs"])
    build_round_verbs(context, query.from_user.id)

    await query.edit_message_text(
        f"Повторяем только ошибки 🔁\n"
        f"Слов в раунде: <b>{context.user_data['round_limit']}</b>",
        parse_mode="HTML",
    )
    return await send_task(query, context, edit=True)


def finalize_answer(context: ContextTypes.DEFAULT_TYPE, user_id: int, verb: dict, correct: bool, errors: int):
    context.user_data["round_total"] += 1
    context.user_data["round_mistake_forms"] += errors

    if correct:
        context.user_data["round_correct"] += 1
        context.user_data["streak"] += 1
        mark_verb_status(user_id, verb["base"], known=True)

        if context.user_data["streak"] > context.user_data["best_streak"]:
            context.user_data["best_streak"] = context.user_data["streak"]
    else:
        context.user_data["streak"] = 0
        if verb not in context.user_data["mistake_verbs"]:
            context.user_data["mistake_verbs"].append(verb)

    update_user_progress(
        user_id=user_id,
        correct=correct,
        mistake_forms=errors,
        best_streak=context.user_data["best_streak"],
    )


async def pick_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    payload = query.data.split(":", 2)
    picked_id = payload[1]
    picked_word = payload[2]

    selected_answers = context.user_data.get("selected_answers", [])
    selected_ids = context.user_data.get("selected_ids", [])

    if len(selected_answers) >= 3:
        return get_state_by_level(context.user_data["current_level"])

    selected_answers.append(picked_word)
    selected_ids.append(picked_id)

    context.user_data["selected_answers"] = selected_answers
    context.user_data["selected_ids"] = selected_ids

    verb = context.user_data["current_verb"]
    ru = verb["ru"]
    correct = get_correct_forms(verb)
    current_level = context.user_data["current_level"]
    choice_options = context.user_data.get("choice_options", [])

    if len(selected_answers) < 3:
        text = (
            f"📘 Уровень {current_level}\n\n"
            f"Русский глагол: <b>{ru}</b>\n"
            f"Выбери 3 правильные формы по порядку.\n\n"
            f"Твой выбор: <b>{' – '.join(selected_answers)}</b>"
        )

        await query.edit_message_text(
            text,
            reply_markup=build_choice_keyboard(choice_options, selected_ids),
            parse_mode="HTML",
        )
        return get_state_by_level(current_level)

    errors = count_errors(selected_answers, correct)
    correct_text = " – ".join(correct)
    detail_lines = get_error_details(selected_answers, correct)
    correct_bool = errors == 0

    finalize_answer(context, query.from_user.id, verb, correct_bool, errors)

    if correct_bool:
        result_text = (
            f"Русский глагол: <b>{ru}</b>\n"
            f"Твой ответ: <b>{' – '.join(selected_answers)}</b>\n\n"
            f"Верно ✅\n"
            f"🔥 Серия: <b>{context.user_data['streak']}</b>"
        )
    else:
        result_text = (
            f"Русский глагол: <b>{ru}</b>\n"
            f"Твой ответ: <b>{' – '.join(selected_answers)}</b>\n"
            f"Правильный ответ: <b>{correct_text}</b>\n"
            f"Ошибок в ответе: <b>{errors}</b>\n"
            + "\n".join(detail_lines)
            + "\n\nНеверно ❌"
        )

    await query.edit_message_text(
        result_text,
        reply_markup=after_answer_keyboard(has_mistakes=len(context.user_data["mistake_verbs"]) > 0),
        parse_mode="HTML",
    )
    return get_state_by_level(current_level)


async def reset_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("Выбор сброшен")

    context.user_data["selected_answers"] = []
    context.user_data["selected_ids"] = []

    verb = context.user_data["current_verb"]
    current_level = context.user_data["current_level"]
    choice_options = context.user_data.get("choice_options", [])

    if current_level == 1:
        text = (
            f"📘 Уровень 1\n\n"
            f"Русский глагол: <b>{verb['ru']}</b>\n"
            f"Выбери 3 правильные формы по порядку.\n\n"
            f"Твой выбор: —"
        )
    else:
        text = (
            f"📗 Уровень 2\n\n"
            f"Русский глагол: <b>{verb['ru']}</b>\n"
            f"Выбери 3 правильные формы по порядку.\n\n"
            f"Твой выбор: —"
        )

    await query.edit_message_text(
        text,
        reply_markup=build_choice_keyboard(choice_options, []),
        parse_mode="HTML",
    )
    return get_state_by_level(current_level)


async def pick_triplet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chosen_triplet = query.data.split(":", 1)[1].split("|")
    verb = context.user_data["current_verb"]
    correct = get_correct_forms(verb)
    ru = verb["ru"]

    errors = count_errors(chosen_triplet, correct)
    details = get_error_details(chosen_triplet, correct)
    correct_text = " – ".join(correct)
    chosen_text = " – ".join(chosen_triplet)
    correct_bool = errors == 0

    finalize_answer(context, query.from_user.id, verb, correct_bool, errors)

    if correct_bool:
        text = (
            f"Русский глагол: <b>{ru}</b>\n"
            f"Твой ответ: <b>{chosen_text}</b>\n\n"
            f"Верно ✅\n"
            f"🔥 Серия: <b>{context.user_data['streak']}</b>"
        )
    else:
        text = (
            f"Русский глагол: <b>{ru}</b>\n"
            f"Твой ответ: <b>{chosen_text}</b>\n"
            f"Правильный ответ: <b>{correct_text}</b>\n"
            f"Ошибок в ответе: <b>{errors}</b>\n"
            + "\n".join(details)
            + "\n\nНеверно ❌"
        )

    await query.edit_message_text(
        text,
        reply_markup=after_answer_keyboard(has_mistakes=len(context.user_data["mistake_verbs"]) > 0),
        parse_mode="HTML",
    )
    return LEVEL3


async def level4_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()
    parts = [part.strip().lower() for part in user_text.split(",")]

    verb = context.user_data["current_verb"]
    correct = [verb["past"], verb["participle"]]
    ru = verb["ru"]

    if len(parts) != 2:
        await update.message.reply_text(
            "Нужно ввести ровно 2 формы через запятую.\n"
            "Пример: <code>went, gone</code>",
            parse_mode="HTML",
        )
        return LEVEL4

    errors = count_errors(parts, correct)
    details = get_error_details(parts, correct)
    correct_text = f"{verb['base']} – {verb['past']} – {verb['participle']}"
    correct_bool = errors == 0

    finalize_answer(context, update.effective_user.id, verb, correct_bool, errors)

    if correct_bool:
        text = (
            f"Русский глагол: <b>{ru}</b>\n"
            f"I : <b>{verb['base']}</b>\n"
            f"Твой ответ: <b>{parts[0]} – {parts[1]}</b>\n\n"
            f"Верно ✅\n"
            f"🔥 Серия: <b>{context.user_data['streak']}</b>"
        )
    else:
        text = (
            f"Русский глагол: <b>{ru}</b>\n"
            f"Твой ответ: <b>{parts[0]} – {parts[1]}</b>\n"
            f"Правильный ответ: <b>{correct_text}</b>\n"
            f"Ошибок в ответе: <b>{errors}</b>\n"
            + "\n".join(details)
            + "\n\nНеверно ❌"
        )

    await update.message.reply_text(
        text,
        reply_markup=after_answer_keyboard(has_mistakes=len(context.user_data["mistake_verbs"]) > 0),
        parse_mode="HTML",
    )
    return LEVEL4


async def level5_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()
    parts = [part.strip().lower() for part in user_text.split(",")]

    verb = context.user_data["current_verb"]
    correct = get_correct_forms(verb)
    ru = verb["ru"]

    if len(parts) != 3:
        await update.message.reply_text(
            "Нужно ввести ровно 3 формы через запятую.\n"
            "Пример: <code>go, went, gone</code>",
            parse_mode="HTML",
        )
        return LEVEL5

    errors = count_errors(parts, correct)
    details = get_error_details(parts, correct)
    correct_text = " – ".join(correct)
    correct_bool = errors == 0

    finalize_answer(context, update.effective_user.id, verb, correct_bool, errors)

    if correct_bool:
        text = (
            f"Русский глагол: <b>{ru}</b>\n"
            f"Твой ответ: <b>{' – '.join(parts)}</b>\n\n"
            f"Верно ✅\n"
            f"🔥 Серия: <b>{context.user_data['streak']}</b>"
        )
    else:
        text = (
            f"Русский глагол: <b>{ru}</b>\n"
            f"Твой ответ: <b>{' – '.join(parts)}</b>\n"
            f"Правильный ответ: <b>{correct_text}</b>\n"
            f"Ошибок в ответе: <b>{errors}</b>\n"
            + "\n".join(details)
            + "\n\nНеверно ❌"
        )

    await update.message.reply_text(
        text,
        reply_markup=after_answer_keyboard(has_mistakes=len(context.user_data["mistake_verbs"]) > 0),
        parse_mode="HTML",
    )
    return LEVEL5


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Команды:\n"
        "/start - открыть главное меню\n"
        "/help - помощь\n"
        "/levels - выбрать уровень"
    )


async def levels_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Выбери уровень:", reply_markup=levels_keyboard())
    return CHOOSE_LEVEL


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Остановились. Напиши /start, чтобы начать заново.")
    return ConversationHandler.END


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        allow_reentry=True,
        states={
            AUTH_PASSWORD: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, check_password),
                CallbackQueryHandler(back_main, pattern="^back_main$"),
            ],
            MAIN_MENU: [
                CallbackQueryHandler(
                    main_menu_handler,
                    pattern="^(dictionary|study_list|training|levels|reset_progress|back_main)$",
                ),
                CallbackQueryHandler(mark_learned_from_study, pattern="^learned:"),
            ],
            DICTIONARY_MODE: [
                CallbackQueryHandler(mark_known, pattern="^mark_known$"),
                CallbackQueryHandler(mark_unknown, pattern="^mark_unknown$"),
                CallbackQueryHandler(next_dictionary, pattern="^next_dictionary$"),
                CallbackQueryHandler(back_main, pattern="^back_main$"),
            ],
            CHOOSE_COUNT: [
                CallbackQueryHandler(choose_count, pattern="^(count_5|count_10|back_main)$"),
            ],
            CHOOSE_LEVEL: [
                CallbackQueryHandler(choose_level, pattern="^(level_[1-5]|back_main)$"),
            ],
            RESET_CONFIRM: [
                CallbackQueryHandler(reset_confirm_handler, pattern="^(confirm_reset|back_main)$"),
            ],
            LEVEL1: [
                CallbackQueryHandler(pick_word, pattern="^pick:"),
                CallbackQueryHandler(reset_choice, pattern="^reset_choice$"),
                CallbackQueryHandler(next_word, pattern="^next_word$"),
                CallbackQueryHandler(repeat_mistakes, pattern="^repeat_mistakes$"),
                CallbackQueryHandler(back_main, pattern="^back_main$"),
            ],
            LEVEL2: [
                CallbackQueryHandler(pick_word, pattern="^pick:"),
                CallbackQueryHandler(reset_choice, pattern="^reset_choice$"),
                CallbackQueryHandler(next_word, pattern="^next_word$"),
                CallbackQueryHandler(repeat_mistakes, pattern="^repeat_mistakes$"),
                CallbackQueryHandler(back_main, pattern="^back_main$"),
            ],
            LEVEL3: [
                CallbackQueryHandler(pick_triplet, pattern="^triplet:"),
                CallbackQueryHandler(next_word, pattern="^next_word$"),
                CallbackQueryHandler(repeat_mistakes, pattern="^repeat_mistakes$"),
                CallbackQueryHandler(back_main, pattern="^back_main$"),
            ],
            LEVEL4: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, level4_input),
                CallbackQueryHandler(next_word, pattern="^next_word$"),
                CallbackQueryHandler(repeat_mistakes, pattern="^repeat_mistakes$"),
                CallbackQueryHandler(back_main, pattern="^back_main$"),
            ],
            LEVEL5: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, level5_input),
                CallbackQueryHandler(next_word, pattern="^next_word$"),
                CallbackQueryHandler(repeat_mistakes, pattern="^repeat_mistakes$"),
                CallbackQueryHandler(back_main, pattern="^back_main$"),
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            CommandHandler("help", help_command),
            CommandHandler("levels", levels_command),
        ],
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("levels", levels_command))

    print("Бот запущен 🚀")
    app.run_polling()


if __name__ == "__main__":
    main()