import streamlit as st
import sqlite3
from datetime import datetime
from PIL import Image
import io

def add_point():
    st.markdown("""
        <h1 style='text-align: center; color: #2e7d32; margin-bottom: 30px;'>
            📍 Добавление новой точки
        </h1>
    """, unsafe_allow_html=True)
    
    # Контейнер для формы
    with st.container():
        st.markdown("""
            <div style='background-color: #f5f5f5; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
                <h3 style='color: #1b5e20; margin-bottom: 15px;'>📝 Информация о загрязнении</h3>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("add_point_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                    <div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>
                        <h4 style='color: #2e7d32;'>📍 Местоположение</h4>
                    </div>
                """, unsafe_allow_html=True)
                
                latitude = st.number_input("🌍 Широта", value=48.0196, format="%.6f")
                longitude = st.number_input("🌍 Долгота", value=66.9237, format="%.6f")
                description = st.text_area("📝 Описание проблемы", 
                                         help="Подробно опишите проблему и ее масштаб")
                
            with col2:
                st.markdown("""
                    <div style='background-color: white; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>
                        <h4 style='color: #2e7d32;'>⚠️ Характеристики загрязнения</h4>
                    </div>
                """, unsafe_allow_html=True)
                
                pollution_level = st.select_slider(
                    "🎚️ Уровень загрязнения",
                    options=["Низкий", "Средний", "Высокий"],
                    value="Средний"
                )
                
                pollution_type = st.selectbox(
                    "🏭 Тип загрязнения",
                    ["Бытовые отходы", "Промышленные отходы", "Химические отходы"]
                )
                
                photo = st.file_uploader("📸 Загрузить фото", type=['jpg', 'png'])
                if photo:
                    st.image(photo, caption="Предпросмотр фото", use_column_width=True)
                
                comments = st.text_area("💭 Дополнительные комментарии")
            
            submit = st.form_submit_button("✅ Добавить точку", 
                                         use_container_width=True,
                                         type="primary")
            
            if submit:
                try:
                    conn = sqlite3.connect('eco_monitoring.db')
                    c = conn.cursor()
                    
                    photo_bytes = None
                    if photo:
                        photo_bytes = photo.read()
                    
                    c.execute('''
                        INSERT INTO pollution_points 
                        (latitude, longitude, description, pollution_level, status, 
                         pollution_type, created_at, photo, comments)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (latitude, longitude, description, pollution_level, 'Открытые',
                          pollution_type, datetime.now(), photo_bytes, comments))
                    
                    conn.commit()
                    conn.close()
                    
                    st.success("🎉 Точка успешно добавлена!")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Ошибка при добавлении точки: {str(e)}")

if __name__ == "__main__":
    add_point()
