import streamlit as st
import folium
from streamlit_folium import folium_static
import sqlite3
import pandas as pd

def show_map():
    # Стилизация заголовка
    st.markdown("""
        <h1 style='text-align: center; color: #2e7d32; margin-bottom: 30px;'>
            🗺️ Карта экологических проблем Казахстана
        </h1>
    """, unsafe_allow_html=True)
    
    # Контейнер для фильтров
    with st.container():
        st.markdown("""
            <div style='background-color: #f5f5f5; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
                <h3 style='color: #1b5e20; margin-bottom: 15px;'>🔍 Фильтры</h3>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            pollution_level = st.selectbox(
                "🎚️ Уровень загрязнения",
                ["Все", "Низкий", "Средний", "Высокий"],
                help="Выберите уровень загрязнения для фильтрации точек"
            )
        with col2:
            status = st.selectbox(
                "📊 Статус",
                ["Все", "Открытые", "Закрытые"],
                help="Фильтр по статусу очистки"
            )
        with col3:
            pollution_type = st.selectbox(
                "🏭 Тип загрязнения",
                ["Все", "Бытовые отходы", "Промышленные отходы", "Химические отходы"],
                help="Выберите тип загрязнения"
            )
    
    # Создание карты с улучшенным стилем
    m = folium.Map(
        location=[48.0196, 66.9237],
        zoom_start=5,
        tiles='CartoDB positron'  # Более современный стиль карты
    )
    
    # Получение точек из базы данных
    conn = sqlite3.connect('eco_monitoring.db')
    query = "SELECT * FROM pollution_points"
    conditions = []
    params = []
    
    if pollution_level != "Все":
        conditions.append("pollution_level = ?")
        params.append(pollution_level)
    if status != "Все":
        conditions.append("status = ?")
        params.append(status)
    if pollution_type != "Все":
        conditions.append("pollution_type = ?")
        params.append(pollution_type)
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    points_df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    
    # Добавление маркеров с улучшенным стилем
    for idx, point in points_df.iterrows():
        # Определение цвета маркера в зависимости от уровня загрязнения
        color = {
            'Низкий': 'green',
            'Средний': 'orange',
            'Высокий': 'red'
        }.get(point['pollution_level'], 'gray')
        
        # HTML для всплывающего окна
        popup_html = f"""
            <div style="width: 200px;">
                <h4 style="color: #2e7d32; margin-bottom: 10px;">Точка #{point['id']}</h4>
                <p><strong>📍 Координаты:</strong><br>{point['latitude']}, {point['longitude']}</p>
                <p><strong>⚠️ Уровень:</strong><br>{point['pollution_level']}</p>
                <p><strong>🏭 Тип:</strong><br>{point['pollution_type']}</p>
                <p><strong>📝 Описание:</strong><br>{point['description']}</p>
                <p><strong>📊 Статус:</strong><br>{point['status']}</p>
            </div>
        """
        
        folium.Marker(
            [point['latitude'], point['longitude']],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color=color, icon='info-sign'),
            tooltip=f"Точка #{point['id']}"
        ).add_to(m)
    
    # Добавление легенды
    legend_html = """
        <div style="position: fixed; bottom: 50px; right: 50px; z-index: 1000; background-color: white;
                    padding: 10px; border-radius: 5px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
            <h4 style="margin-bottom: 10px;">Легенда</h4>
            <p><i class="fa fa-circle" style="color: green;"></i> Низкий уровень</p>
            <p><i class="fa fa-circle" style="color: orange;"></i> Средний уровень</p>
            <p><i class="fa fa-circle" style="color: red;"></i> Высокий уровень</p>
        </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Отображение карты в Streamlit с настроенной высотой
    st.markdown("""
        <div style='background-color: white; padding: 10px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);'>
    """, unsafe_allow_html=True)
    folium_static(m, height=600)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Статистика под картой
    st.markdown("""
        <div style='background-color: #f5f5f5; padding: 20px; border-radius: 10px; margin-top: 20px;'>
            <h3 style='color: #1b5e20; margin-bottom: 15px;'>📊 Статистика</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Всего точек", len(points_df))
    with col2:
        st.metric("Открытых", len(points_df[points_df['status'] == 'Открытые']))
    with col3:
        st.metric("Закрытых", len(points_df[points_df['status'] == 'Закрытые']))
    with col4:
        high_pollution = len(points_df[points_df['pollution_level'] == 'Высокий'])
        st.metric("Критических", high_pollution)

if __name__ == "__main__":
    show_map() 