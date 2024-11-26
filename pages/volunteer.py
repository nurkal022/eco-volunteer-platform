import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from PIL import Image
import io

def show_volunteer_dashboard(volunteer_id, conn):
    # Получаем данные волонтера
    volunteer_data = pd.read_sql_query(
        "SELECT name, rating FROM volunteers WHERE id = ?",
        conn,
        params=(volunteer_id,)
    )
    
    if not volunteer_data.empty:
        volunteer_name = volunteer_data.iloc[0]['name']
        volunteer_rating = volunteer_data.iloc[0]['rating']
        
        # Приветствие и профиль
        st.markdown(f"""
        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 20px'>
            <h2>Добро пожаловать, {volunteer_name}! 🌟</h2>
            <p>Ваш рейтинг: {volunteer_rating} очков</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Показать доступные точки
    st.markdown("### 🗺️ Доступные точки для уборки")
    points_df = pd.read_sql_query(
        "SELECT id, latitude, longitude, description, pollution_level, pollution_type, photo FROM pollution_points WHERE status = 'Открытые'",
        conn
    )
    
    if len(points_df) > 0:
        for _, point in points_df.iterrows():
            with st.expander(f"📍 Точка #{point['id']} - {point['description'][:50]}..."):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("""
                    <style>
                        .info-box {
                            background-color: #ffffff;
                            padding: 15px;
                            border-radius: 5px;
                            border: 1px solid #e0e0e0;
                        }
                    </style>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class='info-box'>
                        <p>🌍 Координаты: {point['latitude']}, {point['longitude']}</p>
                        <p>⚠️ Уровень загрязнения: {point['pollution_level']}</p>
                        <p>🗑️ Тип загрязнения: {point['pollution_type']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Отображение фото точки загрязнения
                    if point['photo'] is not None:
                        try:
                            image = Image.open(io.BytesIO(point['photo']))
                            st.image(image, caption="Фото места загрязнения", use_column_width=True)
                        except Exception as e:
                            st.warning("Фото недоступно")
                
                with col2:
                    st.markdown("#### 📝 Отчет о выполненной работе")
                    # Форма отчета
                    with st.form(f"cleanup_report_{point['id']}"):
                        cleanup_date = st.date_input("📅 Дата уборки", datetime.now())
                        cleanup_description = st.text_area("✍️ Описание выполненной работы")
                        cleanup_photo = st.file_uploader("📸 Фото после уборки", type=['jpg', 'png'])
                        
                        submit = st.form_submit_button("✅ Отправить отчет", 
                                                     use_container_width=True,
                                                     type="primary")
                        
                        if submit:
                            try:
                                c = conn.cursor()
                                photo_bytes = cleanup_photo.read() if cleanup_photo else None
                                
                                # Обновление статуса точки
                                c.execute("UPDATE pollution_points SET status = 'Закрытые' WHERE id = ?", 
                                        (point['id'],))
                                
                                # Добавление записи в completed_tasks
                                c.execute("""
                                    INSERT INTO completed_tasks 
                                    (volunteer_id, point_id, completed_at, cleanup_description, cleanup_photo) 
                                    VALUES (?, ?, ?, ?, ?)
                                """, (volunteer_id, point['id'], cleanup_date, cleanup_description, photo_bytes))
                                
                                # Обновление рейтинга
                                c.execute("UPDATE volunteers SET rating = rating + 10 WHERE id = ?", 
                                        (volunteer_id,))
                                
                                conn.commit()
                                st.success("🎉 Отчет успешно отправлен! +10 к рейтингу")
                                st.balloons()
                                st.rerun()
                            except Exception as e:
                                st.error(f"Ошибка при отправке отчета: {str(e)}")
    else:
        st.info("🎉 На данный момент нет доступных точек для уборки")
    
    # История выполненных задач
    st.markdown("### 📋 История выполненных задач")
    tasks_df = pd.read_sql_query("""
        SELECT 
            ct.id,
            ct.completed_at,
            pp.description as point_description,
            ct.cleanup_description,
            pp.latitude,
            pp.longitude,
            pp.photo as original_photo,
            ct.cleanup_photo
        FROM completed_tasks ct
        JOIN pollution_points pp ON ct.point_id = pp.id
        WHERE ct.volunteer_id = ?
        ORDER BY ct.completed_at DESC
    """, conn, params=(volunteer_id,))
    
    if len(tasks_df) > 0:
        for _, task in tasks_df.iterrows():
            with st.expander(f"📅 Задача от {task['completed_at']}"):
                st.markdown(f"""
                <div style='background-color: #ffffff; padding: 15px; border-radius: 5px; border: 1px solid #e0e0e0'>
                    <p>📍 Место: {task['point_description']}</p>
                    <p>🌍 Координаты: {task['latitude']}, {task['longitude']}</p>
                    <p>✍️ Выполненная работа: {task['cleanup_description']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Фото "до" и "после"
                col1, col2 = st.columns(2)
                with col1:
                    if task['original_photo'] is not None:
                        try:
                            image = Image.open(io.BytesIO(task['original_photo']))
                            st.image(image, caption="До уборки", use_column_width=True)
                        except:
                            st.warning("Фото 'до' недоступно")
                
                with col2:
                    if task['cleanup_photo'] is not None:
                        try:
                            image = Image.open(io.BytesIO(task['cleanup_photo']))
                            st.image(image, caption="После уборки", use_column_width=True)
                        except:
                            st.warning("Фото 'после' недоступно")
    else:
        st.info("📝 У вас пока нет выполненных задач")

def show_volunteer():
    st.markdown("""
    <h1 style='text-align: center; color: #2e7d32;'>🌿 Кабинет волонтера</h1>
    """, unsafe_allow_html=True)
    
    if 'volunteer_id' not in st.session_state:
        tab1, tab2 = st.tabs(["🔑 Вход", "📝 Регистрация"])
        
        with tab1:
            with st.form("login_form"):
                st.markdown("### Вход в систему")
                email = st.text_input("📧 Email")
                password = st.text_input("🔒 Пароль", type="password")
                
                if st.form_submit_button("Войти", use_container_width=True, type="primary"):
                    conn = sqlite3.connect('eco_monitoring.db')
                    c = conn.cursor()
                    
                    c.execute("SELECT id FROM volunteers WHERE email = ? AND password = ?",
                             (email, password))
                    volunteer = c.fetchone()
                    
                    if volunteer:
                        st.session_state.volunteer_id = volunteer[0]
                        st.success("Успешный вход!")
                        st.rerun()
                    else:
                        st.error("Неверный email или пароль")
                    conn.close()
        
        with tab2:
            with st.form("registration_form"):
                st.markdown("### Регистрация нового волонтера")
                
                name = st.text_input("👤 Имя и Фамилия")
                reg_email = st.text_input("📧 Email")
                reg_password = st.text_input("🔒 Пароль", type="password")
                reg_password_confirm = st.text_input("🔒 Подтвердите пароль", type="password")
                
                if st.form_submit_button("Зарегистрироваться", use_container_width=True, type="primary"):
                    if not all([name, reg_email, reg_password, reg_password_confirm]):
                        st.error("Пожалуйста, заполните все поля")
                    elif reg_password != reg_password_confirm:
                        st.error("Пароли не совпадают")
                    else:
                        conn = sqlite3.connect('eco_monitoring.db')
                        c = conn.cursor()
                        
                        c.execute("SELECT * FROM volunteers WHERE email = ?", (reg_email,))
                        if c.fetchone():
                            st.error("Пользователь с таким email уже существует")
                        else:
                            try:
                                c.execute('''
                                    INSERT INTO volunteers (name, email, password, rating, created_at)
                                    VALUES (?, ?, ?, ?, ?)
                                ''', (name, reg_email, reg_password, 0, datetime.now()))
                                
                                conn.commit()
                                st.success("🎉 Регистрация успешно завершена! Теперь вы можете войти.")
                            except Exception as e:
                                st.error(f"Ошибка при регистрации: {str(e)}")
                            finally:
                                conn.close()
    else:
        conn = sqlite3.connect('eco_monitoring.db')
        
        if st.sidebar.button("🚪 Выйти", type="primary"):
            del st.session_state.volunteer_id
            st.rerun()
        
        show_volunteer_dashboard(st.session_state.volunteer_id, conn)
        conn.close()

if __name__ == "__main__":
    show_volunteer() 