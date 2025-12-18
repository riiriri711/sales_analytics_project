import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Анализ продаж", layout="wide")
st.title("📊 Анализ продаж")

st.sidebar.header("📁 Загрузка данных")
uploaded_file = st.sidebar.file_uploader("Выберите CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df['date'] = pd.to_datetime(df['date'])
    st.sidebar.success("✅ Данные загружены!")
    
    st.sidebar.header("🔍 Фильтры")
    min_date = st.sidebar.date_input("С даты", df['date'].min().date())
    max_date = st.sidebar.date_input("По дату", df['date'].max().date())
    categories = st.sidebar.multiselect("Категории", sorted(df['category'].unique()), default=df['category'].unique())
    regions = st.sidebar.multiselect("Регионы", sorted(df['region'].unique()), default=df['region'].unique())
    
    mask = (df['date'] >= pd.to_datetime(min_date)) & \
           (df['date'] <= pd.to_datetime(max_date)) & \
           (df['category'].isin(categories)) & \
           (df['region'].isin(regions))
    
    df_filtered = df[mask].copy()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Заказы", len(df_filtered))
    with col2: st.metric("Выручка", f"{df_filtered['amount'].sum():,.0f} ₽")
    with col3: st.metric("Средний чек", f"{df_filtered['amount'].mean():,.0f} ₽")
    with col4: st.metric("Среднее кол-во", f"{df_filtered['quantity'].mean():.1f}")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Динамика", "📊 Категории", "🏆 Топ", "🗺️ Регионы"])
    
    with tab1:
        daily = df_filtered.groupby(df_filtered['date'].dt.date)['amount'].sum().reset_index()
        fig1 = px.line(daily, x='date', y='amount', title="Динамика продаж")
        st.plotly_chart(fig1, use_container_width=True)
    
    with tab2:
        cat = df_filtered.groupby('category')['amount'].sum().reset_index()
        fig2 = px.bar(cat, x='category', y='amount', title="По категориям")
        st.plotly_chart(fig2, use_container_width=True)
    
    with tab3:
        top = df_filtered.groupby('product')['quantity'].sum().nlargest(10).reset_index()
        fig3 = px.bar(top, x='quantity', y='product', title="Топ-10", orientation='h')
        st.plotly_chart(fig3, use_container_width=True)
    
    with tab4:
        reg = df_filtered.groupby('region')['amount'].sum().reset_index()
        fig4 = px.pie(reg, values='amount', names='region', title="По регионам")
        st.plotly_chart(fig4, use_container_width=True)
    
    st.dataframe(df_filtered)
