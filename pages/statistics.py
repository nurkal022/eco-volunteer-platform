import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

def show_statistics():
    st.markdown("""
        <h1 style='text-align: center; color: #2e7d32; margin-bottom: 30px;'>
            📊 Статистика и аналитика
        </h1>
    """, unsafe_allow_html=True)
    
    conn = sqlite3.connect('eco_monitoring.db')
    points_df = pd.read_sql_query("SELECT * FROM pollution_points", conn)
    volunteers_df = pd.read_sql_query("SELECT * FROM volunteers", conn)
    tasks_df = pd.read_sql_query("SELECT * FROM completed_tasks", conn)
    conn.close()
    
    # Общая статистика
    st.markdown("""
        <div style='background-color: #f5f5f5; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
            <h3 style='color: #1b5e20; margin-bottom: 15px;'>📈 Общая статистика</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📍 Всего точек", len(points_df))
    with col2:
        st.metric("👥 Волонтеров", len(volunteers_df))
    with col3:
        st.metric("✅ Выполнено задач", len(tasks_df))
    with col4:
        completion_rate = len(tasks_df) / len(points_df) * 100 if len(points_df) > 0 else 0
        st.metric("📊 % выполнения", f"{completion_rate:.1f}%")
    
    # Графики
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div style='background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);'>
                <h4 style='color: #2e7d32;'>🎯 Распределение по уровням загрязнения</h4>
            </div>
        """, unsafe_allow_html=True)
        
        if not points_df.empty:
            fig1 = px.pie(points_df, 
                         names='pollution_level',
                         color_discrete_sequence=px.colors.sequential.Greens,
                         hole=0.4)
            fig1.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("Нет данных о точках загрязнения")
    
    with col2:
        st.markdown("""
            <div style='background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);'>
                <h4 style='color: #2e7d32;'>📊 Типы загрязнений</h4>
            </div>
        """, unsafe_allow_html=True)
        
        if not points_df.empty:
            pollution_type_counts = points_df['pollution_type'].value_counts().reset_index()
            pollution_type_counts.columns = ['type', 'count']
            
            fig2 = px.bar(pollution_type_counts,
                         x='type',
                         y='count',
                         color='type',
                         color_discrete_sequence=px.colors.sequential.Greens,
                         labels={'type': 'Тип загрязнения', 'count': 'Количество'})
            fig2.update_layout(showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Нет данных о типах загрязнения")
    
    # Временная динамика
    st.markdown("""
        <div style='background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-top: 20px;'>
            <h4 style='color: #2e7d32;'>📈 Динамика очистки территорий</h4>
        </div>
    """, unsafe_allow_html=True)
    
    if not tasks_df.empty:
        try:
            # Преобразуем строки дат в объекты datetime
            tasks_df['completed_at'] = pd.to_datetime(tasks_df['completed_at'], format='mixed')
            # Группируем по дате (без времени)
            timeline_data = tasks_df.groupby(tasks_df['completed_at'].dt.date).size().reset_index()
            timeline_data.columns = ['date', 'count']
            
            fig3 = go.Figure()
            fig3.add_trace(go.Scatter(x=timeline_data['date'], 
                                    y=timeline_data['count'],
                                    mode='lines+markers',
                                    line=dict(color='#2e7d32', width=2),
                                    marker=dict(size=8, color='#1b5e20')))
            fig3.update_layout(
                xaxis_title="Дата",
                yaxis_title="Количество выполненных задач",
                hovermode='x unified'
            )
            st.plotly_chart(fig3, use_container_width=True)
        except Exception as e:
            st.error(f"Ошибка при обработке дат: {str(e)}")
    else:
        st.info("📊 Пока нет данных о выполненных задачах")

    # Добавим рейтинг волонтеров
    if not volunteers_df.empty:
        st.markdown("""
            <div style='background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-top: 20px;'>
                <h4 style='color: #2e7d32;'>🏆 Рейтинг волонтеров</h4>
            </div>
        """, unsafe_allow_html=True)
        
        top_volunteers = volunteers_df.nlargest(10, 'rating')[['name', 'rating']]
        fig4 = px.bar(top_volunteers,
                     x='name',
                     y='rating',
                     color='rating',
                     color_continuous_scale='Greens',
                     labels={'name': 'Волонтер', 'rating': 'Рейтинг'})
        fig4.update_layout(showlegend=False)
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.info("👥 Пока нет данных о волонтерах")

if __name__ == "__main__":
    show_statistics() 