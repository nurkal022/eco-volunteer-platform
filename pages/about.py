import streamlit as st

def show_about():
    # Заголовок с стилизацией
    st.markdown("""
        <h1 style='text-align: center; color: #2e7d32; margin-bottom: 30px;'>
            🌍 О проекте "Эко-мониторинг Казахстана"
        </h1>
    """, unsafe_allow_html=True)
    
    # Миссия проекта
    st.markdown("""
        <div style='background-color: #f5f5f5; padding: 25px; border-radius: 10px; margin-bottom: 30px;'>
            <h2 style='color: #1b5e20; margin-bottom: 20px;'>🎯 Наша миссия</h2>
            <p style='font-size: 18px; line-height: 1.6;'>
                Создать эффективную платформу для мониторинга экологической ситуации в Казахстане 
                и объединить усилия граждан и волонтеров для решения экологических проблем. 
                Мы стремимся сделать нашу страну чище и зеленее вместе с вами!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Принципы работы
    st.markdown("""
        <div style='background-color: white; padding: 25px; border-radius: 10px; margin-bottom: 30px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);'>
            <h2 style='color: #1b5e20; margin-bottom: 20px;'>💫 Принципы работы</h2>
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px;'>
                <div style='background-color: #f8f9fa; padding: 20px; border-radius: 8px;'>
                    <h3 style='color: #2e7d32; font-size: 20px;'>🔍 Открытость</h3>
                    <p>Все данные о загрязнениях доступны каждому гражданину</p>
                </div>
                <div style='background-color: #f8f9fa; padding: 20px; border-radius: 8px;'>
                    <h3 style='color: #2e7d32; font-size: 20px;'>👥 Вовлеченность</h3>
                    <p>Каждый может внести свой вклад в улучшение экологии</p>
                </div>
                <div style='background-color: #f8f9fa; padding: 20px; border-radius: 8px;'>
                    <h3 style='color: #2e7d32; font-size: 20px;'>🤝 Сотрудничество</h3>
                    <p>Эффективное взаимодействие волонтеров и организаций</p>
                </div>
                <div style='background-color: #f8f9fa; padding: 20px; border-radius: 8px;'>
                    <h3 style='color: #2e7d32; font-size: 20px;'>✅ Достоверность</h3>
                    <p>Проверка и подтверждение всех данных</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Инструкция для пользователей
    st.markdown("""
        <div style='background-color: #e8f5e9; padding: 25px; border-radius: 10px; margin-bottom: 30px;'>
            <h2 style='color: #1b5e20; margin-bottom: 20px;'>📖 Как это работает</h2>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div style='background-color: white; padding: 20px; border-radius: 8px; height: 100%;'>
                <h3 style='color: #2e7d32; font-size: 20px;'>🎯 Для пользователей:</h3>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("1. Найдите точку загрязнения на карте или добавьте новую")
        st.write("2. Заполните информацию о проблеме")
        st.write("3. Загрузите фотографии")
        st.write("4. Следите за статусом решения проблемы")
    
    with col2:
        st.markdown("""
            <div style='background-color: white; padding: 20px; border-radius: 8px; height: 100%;'>
                <h3 style='color: #2e7d32; font-size: 20px;'>🌟 Для волонтеров:</h3>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("1. Зарегистрируйтесь в системе")
        st.write("2. Выберите доступные задачи на карте")
        st.write("3. Примите участие в уборке территории")
        st.write("4. Загрузите отчет о проделанной работе")
        st.write("5. Получайте баллы и повышайте свой рейтинг")
    
    # Контакты
    st.markdown("""
        <div style='background-color: white; padding: 25px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);'>
            <h2 style='color: #1b5e20; margin-bottom: 20px;'>📞 Контакты</h2>
            <div style='display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px;'>
                <div style='text-align: center; padding: 20px; background-color: #f8f9fa; border-radius: 8px;'>
                    <h3 style='color: #2e7d32; font-size: 20px;'>📧 Email</h3>
                    <p>eco@monitoring.kz</p>
                </div>
                <div style='text-align: center; padding: 20px; background-color: #f8f9fa; border-radius: 8px;'>
                    <h3 style='color: #2e7d32; font-size: 20px;'>📱 Телефон</h3>
                    <p>+7 (777) 777-77-77</p>
                </div>
                <div style='text-align: center; padding: 20px; background-color: #f8f9fa; border-radius: 8px;'>
                    <h3 style='color: #2e7d32; font-size: 20px;'>📍 Адрес</h3>
                    <p>г. Астана, ул. Примерная, 123</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_about() 