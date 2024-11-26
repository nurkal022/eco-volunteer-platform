import streamlit as st
import sqlite3
from pages.map import show_map
from pages.add_point import add_point
from pages.statistics import show_statistics
from pages.volunteer import show_volunteer
from pages.about import show_about
import os

# Инициализация базы данных
def init_db():
    # Проверяем, существует ли файл базы данных
    db_exists = os.path.exists('eco_monitoring.db')
    
    conn = sqlite3.connect('eco_monitoring.db')
    c = conn.cursor()
    
    if not db_exists:
        # Создание таблицы точек загрязнения
        c.execute('''
            CREATE TABLE IF NOT EXISTS pollution_points (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                latitude REAL,
                longitude REAL,
                description TEXT,
                pollution_level TEXT,
                status TEXT,
                pollution_type TEXT,
                created_at TIMESTAMP,
                photo BLOB,
                comments TEXT
            )
        ''')
        
        # Создание таблицы волонтеров
        c.execute('''
            CREATE TABLE IF NOT EXISTS volunteers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT UNIQUE,
                password TEXT,
                rating INTEGER DEFAULT 0,
                created_at TIMESTAMP
            )
        ''')
        
        # Создание таблицы выполненных задач
        c.execute('''
            CREATE TABLE IF NOT EXISTS completed_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                volunteer_id INTEGER,
                point_id INTEGER,
                completed_at DATE,
                cleanup_description TEXT,
                cleanup_photo BLOB,
                FOREIGN KEY (volunteer_id) REFERENCES volunteers (id),
                FOREIGN KEY (point_id) REFERENCES pollution_points (id)
            )
        ''')
        
        conn.commit()
    
    conn.close()

def main():
    st.set_page_config(page_title="Эко-мониторинг Казахстана", layout="wide")
    
    # Инициализация базы данных
    init_db()
    
    # Боковая панель навигации
    st.sidebar.title("Навигация")
    page = st.sidebar.radio(
        "Выберите страницу:",
        ["Карта", "Добавить точку", "Статистика", "Кабинет волонтера", "О проекте"]
    )
    
    if page == "Карта":
        show_map()
    elif page == "Добавить точку":
        add_point()
    elif page == "Статистика":
        show_statistics()
    elif page == "Кабинет волонтера":
        show_volunteer()
    elif page == "О проекте":
        show_about()

if __name__ == "__main__":
    main() 