import streamlit as st
import json
import os
from datetime import datetime
import calendar
import random
import hashlib
import time

# Налаштування сторінки
st.set_page_config(
    page_title="My Aesthetic Planner 🌸",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DB_FILE = "users_database.json"

def make_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {}

def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=4)

if "db" not in st.session_state:
    st.session_state.db = load_db()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# Стильні пастельні CSS-шаблони та адаптивність для телефонів, планшетів і ноутбуків
st.markdown("""
    <style>
    .stApp { background-color: #F8F5F0; }
    h1, h2, h3 { font-family: 'Helvetica Neue', sans-serif; color: #222222; }
    
    @media (max-width: 768px) {
        .block-container { padding-left: 0.8rem !important; padding-right: 0.8rem !important; }
        h1 { font-size: 1.5rem !important; text-align: center; }
        .stButton>button { width: 100% !important; }
    }

    .stButton>button { border-radius: 12px; background-color: #E2ECE9; color: #222222; border: none; font-weight: bold; }
    .stButton>button:hover { background-color: #D3E2DD; }
    .quote-box { background-color: #F7EBE8; padding: 14px 18px; border-radius: 15px; margin-bottom: 15px; border-left: 5px solid #E2ECE9; font-size: 0.95rem; }
    .card-box { background-color: #FFFFFF; padding: 18px; border-radius: 16px; box-shadow: 0 4px 10px rgba(0,0,0,0.02); margin-bottom: 12px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================================
# 🔐 ВХІД ТА РЕЄСТРАЦІЯ
# ==========================================================
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center;'>My Aesthetic Planner 🌸</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #666;'>Особистий простір для цілей, навчання та натхнення</p>", unsafe_allow_html=True)
        
        auth_mode = st.radio("Режим", ["Вхід", "Реєстрація"], horizontal=True, label_visibility="collapsed")
        
        username = st.text_input("Логін", placeholder="Введіть логін").strip().lower()
        password = st.text_input("Пароль", type="password", placeholder="Введіть пароль")
        
        if auth_mode == "Реєстрація":
            if st.button("Створити акаунт ✨", use_container_width=True):
                if username and password:
                    if username in st.session_state.db:
                        st.error("Користувач із таким логіном вже існує!")
                    else:
                        st.session_state.db[username] = {
                            "password": make_hash(password),
                            "data": {
                                "subjects": [],
                                "gym_week": {day: {"type": "Відпочинок 🛋️", "done": False} for day in ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця", "Субота", "Неділя"]},
                                "water": 0,
                                "mood": "😊 Чудовий",
                                "playlist": "Lofi Girl - chill beats 🎧",
                                "notes": "",
                                "schedule": {},
                                "goals": {},
                                "gratitude": {},
                                "habits": {"Німецька мова 🇩🇪": [], "Догляд за шкірою 🌿": [], "Читання 📖": [], "Спорт/Зарядка ⚡": []},
                                "expenses": [],
                                "books": []
                            }
                        }
                        save_db(st.session_state.db)
                        st.success("Акаунт успішно створено! Перейдіть на вкладку 'Вхід'.")
                else:
                    st.warning("Заповніть усі поля!")
        else:
            if st.button("Увійти 🚀", use_container_width=True):
                if username in st.session_state.db and st.session_state.db[username]["password"] == make_hash(password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Невірний логін або пароль!")
    st.stop()

# ==========================================================
# 🌸 ОСНОВНИЙ ІНТЕРФЕЙС ПЛАНЕРА
# ==========================================================
username = st.session_state.username
user_data = st.session_state.db[username]["data"]

def save_user_data():
    st.session_state.db[username]["data"] = user_data
    save_db(st.session_state.db)

if "selected_date" not in st.session_state:
    st.session_state.selected_date = datetime.now().strftime("%Y-%m-%d")

QUOTES = [
    "✨ 'Дисципліна сьогодні — це бажане життя завтра.'",
    "🌿 'Маленькі кроки щодня ведуть до великих результатів.'",
    "☕ 'Твори свою історію у своєму власному темпі.'",
    "🌸 'Створи життя, у якому ти почуваєшся затишно.'"
]

top1, top2 = st.columns([4, 1])
with top1:
    st.title(f"Привіт, {username.capitalize()}! 🌸")
with top2:
    if st.button("Вийти 🚪"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

st.markdown(f'<div class="quote-box"><b>Порада дня:</b> {random.choice(QUOTES)}</div>', unsafe_allow_html=True)

tab = st.radio("Меню:", [
    "🗓 Календар", 
    "☀️ День & Вдячність", 
    "📚 Навчання", 
    "🏋️‍♀️ Спортзал", 
    "⏱️ Pomodoro", 
    "✨ Звички", 
    "📖 Книги", 
    "💰 Витрати", 
    "🎧 Вайб & Нотатки"
], horizontal=True)

# --- 1. КАЛЕНДАР ---
if tab == "🗓 Календар":
    st.subheader("🗓 Календар місяця (оберіть день для розкладу)")
    now = datetime.now()
    month_name = now.strftime("%B %Y")
    st.write(f"Поточний місяць: **{month_name}**")
    
    cal = calendar.monthcalendar(now.year, now.month)
    weekdays = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"]
    
    cols = st.columns(7)
    for i, w in enumerate(weekdays):
        cols[i].write(f"**{w}**")

    for week in cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            if day != 0:
                if cols[i].button(str(day), key=f"day_{day}"):
                    st.session_state.selected_date = datetime(now.year, now.month, day).strftime("%Y-%m-%d")
                    st.success(f"Обрано дату: {st.session_state.selected_date}! Перейдіть у вкладку 'День & Вдячність'.")

# --- 2. ДЕНЬ & ВДЯЧНІСТЬ ---
elif tab == "☀️ День & Вдячність":
    selected_date = st.session_state.selected_date
    st.subheader(f"⏰ Розклад та цілі на: {selected_date}")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### 🕒 Погодинний план")
        if selected_date not in user_data["schedule"]:
            user_data["schedule"][selected_date] = {}
        
        for h in range(7, 23):
            time_str = f"{h:02d}:00"
            curr_val = user_data["schedule"][selected_date].get(time_str, "")
            new_val = st.text_input(time_str, value=curr_val, key=f"time_{selected_date}_{time_str}")
            if new_val != curr_val:
                user_data["schedule"][selected_date][time_str] = new_val
                save_user_data()

    with col2:
        st.markdown("### ⭐ 3 Головні цілі дня")
        if selected_date not in user_data["goals"]:
            user_data["goals"][selected_date] = ["", "", ""]
        for i in range(3):
            g_val = user_data["goals"][selected_date][i]
            new_g = st.text_input(f"Ціль {i+1}", value=g_val, key=f"goal_{selected_date}_{i}")
            if new_g != g_val:
                user_data["goals"][selected_date][i] = new_g
                save_user_data()
        
        st.markdown("---")
        st.markdown("### 🌸 Щоденник вдячності")
        if selected_date not in user_data["gratitude"]:
            user_data["gratitude"][selected_date] = ""
        grat = st.text_area("За що ти вдячна сьогодні?", value=user_data["gratitude"][selected_date], height=120)
        if grat != user_data["gratitude"][selected_date]:
            user_data["gratitude"][selected_date] = grat
            save_user_data()

# --- 3. НАВЧАННЯ ---
elif tab == "📚 Навчання":
    st.subheader("📚 Мої Предмети та завдання")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Список предметів")
        if not user_data["subjects"]:
            st.info("Додайте свої предмети праворуч 🌸")
        else:
            for idx, subj in enumerate(user_data["subjects"]):
                st.markdown(f"""
                <div style="background-color: {subj['color']}; padding: 12px; border-radius: 12px; margin-bottom: 8px; color: #222;">
                    <strong>{subj['name']}</strong><br><small>🎯 {subj['task']}</small>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"🗑️ Видалити {subj['name']}", key=f"del_{idx}"):
                    user_data["subjects"].pop(idx)
                    save_user_data()
                    st.rerun()
    with c2:
        st.markdown("### ➕ Додати предмет")
        with st.form("subj_form"):
            name = st.text_input("Назва предмета")
            task = st.text_input("Поточна тема / задача")
            color = st.selectbox("Пастельний колір", ["#E8D7F1", "#FDE2E4", "#D8E2DC", "#FFF1E6", "#E2ECE9", "#F0EAE1"])
            if st.form_submit_button("Зберегти ✨") and name:
                user_data["subjects"].append({"name": name, "task": task or "Завдання...", "color": color})
                save_user_data()
                st.rerun()

# --- 4. СПОРТЗАЛ ---
elif tab == "🏋️‍♀️ Спортзал":
    st.subheader("🏋️‍♀️ Розклад та трекер спортзалу по днях")
    workout_types = ["Відпочинок 🛋️", "Силове 🏋️‍♀️", "Кардіо 🏃‍♀️", "Розтяжка 🧘‍♀️", "Легке тренування 🌸"]
    for day in ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця", "Субота", "Неділя"]:
        c1, c2, c3 = st.columns([2, 3, 1])
        with c1: st.markdown(f"**{day}**")
        with c2:
            curr_t = user_data["gym_week"][day]["type"]
            sel_t = st.selectbox("Тип", workout_types, index=workout_types.index(curr_t) if curr_t in workout_types else 0, key=f"gym_t_{day}", label_visibility="collapsed")
            if sel_t != curr_t:
                user_data["gym_week"][day]["type"] = sel_t
                save_user_data()
        with c3:
            curr_d = user_data["gym_week"][day]["done"]
            d_val = st.checkbox("ОК", value=curr_d, key=f"gym_d_{day}")
            if d_val != curr_d:
                user_data["gym_week"][day]["done"] = d_val
                save_user_data()

# --- 5. POMODORO ТАЙМЕР ---
elif tab == "⏱️ Pomodoro":
    st.subheader("⏱️ Таймер фокусу (Pomodoro)")
    st.write("Використовуйте цей таймер для глибокого фокусу під час навчання чи роботи:")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        minutes = st.number_input("Хвилини роботи:", min_value=1, max_value=60, value=25)
        if st.button("Запустити таймер 🚀"):
            ph = st.empty()
            for secs in range(minutes * 60, 0, -1):
                m, s = divmod(secs, 60)
                ph.markdown(f"# ⏳ {m:02d}:{s:02d}")
                time.sleep(1)
            ph.markdown("# 🎉 Час відпочити!")
            st.balloons()

# --- 6. ЗВИЧКИ ---
elif tab == "✨ Звички":
    st.subheader("✨ Трекер корисних звичок")
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    for habit, days_list in user_data["habits"].items():
        c1, c2 = st.columns([3, 1])
        with c1: st.markdown(f"**{habit}**")
        with c2:
            done_today = today_str in days_list
            is_checked = st.checkbox("Сьогодні", value=done_today, key=f"habit_{habit}")
            if is_checked and not done_today:
                user_data["habits"][habit].append(today_str)
                save_user_data()
            elif not is_checked and done_today:
                user_data["habits"][habit].remove(today_str)
                save_user_data()

# --- 7. КНИГИ ---
elif tab == "📖 Книги":
    st.subheader("📖 Трекер читання")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Моя бібліотека")
        if not user_data["books"]:
            st.info("Список книг порожній.")
        else:
            for b in user_data["books"]:
                st.markdown(f"• **{b['title']}** — {b['author']} ({b['status']})")
    with c2:
        st.markdown("### ➕ Додати книгу")
        with st.form("book_form"):
            btitle = st.text_input("Назва книги")
            bauthor = st.text_input("Автор")
            bstatus = st.selectbox("Статус", ["Читаю 📖", "Прочитано ✅", "У планах ⏳"])
            if st.form_submit_button("Зберегти книгу ✨") and btitle:
                user_data["books"].append({"title": btitle, "author": bauthor, "status": bstatus})
                save_user_data()
                st.rerun()

# --- 8. ВИТРАТИ ---
elif tab == "💰 Витрати":
    st.subheader("💰 Облік витрат")
    c1, c2 = st.columns(2)
    with c1:
        with st.form("expense_form"):
            item = st.text_input("Назва витрати (напр. Кава, Книги)")
            amount = st.number_input("Сума", min_value=0.0, step=10.0)
            if st.form_submit_button("Додати витрату 💸") and item:
                user_data["expenses"].append({"item": item, "amount": amount, "date": datetime.now().strftime("%d.%m.%Y")})
                save_user_data()
                st.success("Витрату додано!")
                st.rerun()
    with c2:
        st.markdown("### Історія витрат")
        if not user_data["expenses"]:
            st.info("Поки немає витрат.")
        else:
            total = sum(ex["amount"] for ex in user_data["expenses"])
            st.write(f"Загалом витрачено: **{total} грн / EUR**")
            for ex in user_data["expenses"][-5:]:
                st.text(f"• {ex['date']} | {ex['item']}: {ex['amount']}")

# --- 9. ВАЙБ & НОТАТКИ ---
elif tab == "🎧 Вайб & Нотатки":
    st.subheader("🎧 Настрій, музика та швидкі нотатки")
    c1, c2 = st.columns(2)
    with c1:
        moods = ["😊 Чудовий", "🌿 Спокійний", "⚡ Продуктивний", "😴 Втомлений", "☕ Затишний"]
        curr_m = user_data.get("mood", moods[0])
        mood = st.selectbox("Твій настрій", moods, index=moods.index(curr_m) if curr_m in moods else 0)
        if mood != curr_m:
            user_data["mood"] = mood
            save_user_data()

        playlist = st.text_input("🎧 Трек / Плейлист дня", value=user_data.get("playlist", ""))
        if playlist != user_data.get("playlist", ""):
            user_data["playlist"] = playlist
            save_user_data()

        water = st.slider("💧 Склянок води", 0, 10, user_data.get("water", 0))
        if water != user_data.get("water", 0):
            user_data["water"] = water
            save_user_data()
    with c2:
        notes = st.text_area("💡 Швидкі замітки (Brain Dump)", value=user_data.get("notes", ""), height=200)
        if notes != user_data.get("notes", ""):
            user_data["notes"] = notes
            save_user_data()