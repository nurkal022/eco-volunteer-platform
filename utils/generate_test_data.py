import sqlite3
import random
from datetime import datetime, timedelta
import os
from PIL import Image
import io
import numpy as np

def generate_test_data():
    conn = sqlite3.connect('eco_monitoring.db')
    c = conn.cursor()
    
    # Генерация тестовых волонтеров
    volunteers_data = [
        ("Асан Серіков", "asan@test.kz", "password123"),
        ("Айгуль Каримова", "aigul@test.kz", "password123"),
        ("Бауыржан Омаров", "baur@test.kz", "password123"),
        ("Динара Сатпаева", "dinara@test.kz", "password123"),
        ("Ерлан Нұрланов", "erlan@test.kz", "password123")
    ]
    
    for name, email, password in volunteers_data:
        try:
            c.execute('''
                INSERT INTO volunteers (name, email, password, rating, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, email, password, random.randint(0, 100), datetime.now()))
        except sqlite3.IntegrityError:
            pass  # Пропускаем, если email уже существует
    
    # Генерация тестовых точек загрязнения
    cities = [
        (51.1801, 71.446, "Астана"),
        (43.2567, 76.9286, "Алматы"),
        (42.3417, 69.5901, "Шымкент"),
        (47.0945, 51.9238, "Атырау"),
        (49.9561, 82.6097, "Өскемен"),
        (53.2198, 63.6354, "Костанай"),
        (50.4201, 80.2659, "Семей")
    ]
    
    pollution_types = ["Бытовые отходы", "Промышленные отходы", "Химические отходы"]
    pollution_levels = ["Низкий", "Средний", "Высокий"]
    statuses = ["Открытые", "Закрытые"]
    
    # Создание тестового изображения
    def create_test_image():
        img = Image.new('RGB', (400, 300), color=tuple(np.random.randint(0, 255, 3)))
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()
    
    # Генерация точек загрязнения вокруг городов
    for city_lat, city_lon, city_name in cities:
        for _ in range(random.randint(3, 7)):
            # Случайное смещение от центра города
            lat = city_lat + random.uniform(-0.1, 0.1)
            lon = city_lon + random.uniform(-0.1, 0.1)
            
            description = f"Загрязнение около {city_name}: {random.choice(['парк', 'река', 'пустырь', 'промзона'])}"
            pollution_type = random.choice(pollution_types)
            pollution_level = random.choice(pollution_levels)
            status = random.choice(statuses)
            
            # Генерация случайной даты за последний год
            created_at = datetime.now() - timedelta(days=random.randint(0, 365))
            
            c.execute('''
                INSERT INTO pollution_points 
                (latitude, longitude, description, pollution_level, status, 
                 pollution_type, created_at, photo, comments)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (lat, lon, description, pollution_level, status,
                  pollution_type, created_at, create_test_image(),
                  f"Тестовый комментарий для точки в {city_name}"))
    
    # Генерация выполненных задач
    points = c.execute("SELECT id FROM pollution_points WHERE status = 'Закрытые'").fetchall()
    volunteers = c.execute("SELECT id FROM volunteers").fetchall()
    
    for point_id in points:
        volunteer_id = random.choice(volunteers)[0]
        completed_at = datetime.now() - timedelta(days=random.randint(0, 180))
        
        c.execute('''
            INSERT INTO completed_tasks 
            (volunteer_id, point_id, completed_at, cleanup_description, cleanup_photo)
            VALUES (?, ?, ?, ?, ?)
        ''', (volunteer_id, point_id[0], completed_at,
              "Территория очищена, мусор вывезен",
              create_test_image()))
        
        # Обновление рейтинга волонтера
        c.execute("""
            UPDATE volunteers 
            SET rating = rating + ? 
            WHERE id = ?
        """, (random.randint(5, 15), volunteer_id))
    
    conn.commit()
    conn.close()
    
    print("Тестовые данные успешно сгенерированы!")

if __name__ == "__main__":
    generate_test_data() 