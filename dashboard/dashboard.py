# dashboard.py

import os
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Mengatur style untuk seaborn
sns.set_style('darkgrid')

# Judul Dashboard
st.title("Dashboard Analisis Data Penyewaan Sepeda")

script_dir = os.path.dirname(os.path.abspath(__file__))
day_data_path = os.path.join(script_dir, '..', 'data', 'day.csv')
hour_data_path = os.path.join(script_dir, '..', 'data', 'hour.csv')

# Membaca dataset
day_df = pd.read_csv(day_data_path)
hour_df = pd.read_csv(hour_data_path)

# Data Preprocessing

# Mengubah tipe data 'dteday' menjadi datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Mengganti nama kolom untuk meningkatkan keterbacaan
day_df.rename(columns={
    'yr': 'year',
    'mnth': 'month',
    'weekday': 'day_of_week',
    'weathersit': 'weather_situation',
    'hum': 'humidity',
    'cnt': 'total_count'
}, inplace=True)

hour_df.rename(columns={
    'yr': 'year',
    'mnth': 'month',
    'hr': 'hour',
    'weekday': 'day_of_week',
    'weathersit': 'weather_situation',
    'hum': 'humidity',
    'cnt': 'total_count'
}, inplace=True)

# Mengubah tipe data beberapa kolom menjadi kategori
category_columns = ['season', 'year', 'month', 'holiday', 'day_of_week', 'weather_situation']
for col in category_columns:
    if col in day_df.columns:
        day_df[col] = day_df[col].astype('category')
    if col in hour_df.columns:
        hour_df[col] = hour_df[col].astype('category')

# Mengonversi nilai kategori untuk interpretasi yang lebih baik
# Mapping untuk season
season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
day_df['season'] = day_df['season'].map(season_mapping)
hour_df['season'] = hour_df['season'].map(season_mapping)

# Mapping untuk month
month_mapping = {
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr',
    5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
    9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
}
day_df['month'] = day_df['month'].map(month_mapping)
hour_df['month'] = hour_df['month'].map(month_mapping)

# Mapping untuk day_of_week
weekday_mapping = {
    0: 'Sunday', 1: 'Monday', 2: 'Tuesday',
    3: 'Wednesday', 4: 'Thursday', 5: 'Friday',
    6: 'Saturday'
}
day_df['day_of_week'] = day_df['day_of_week'].map(weekday_mapping)
hour_df['day_of_week'] = hour_df['day_of_week'].map(weekday_mapping)

# Mapping untuk weather_situation
weather_mapping = {
    1: 'Clear', 2: 'Mist', 3: 'Light Rain/Snow', 4: 'Heavy Rain/Snow'
}
day_df['weather_situation'] = day_df['weather_situation'].map(weather_mapping)
hour_df['weather_situation'] = hour_df['weather_situation'].map(weather_mapping)

# Mapping untuk year
year_mapping = {0: 2011, 1: 2012}
day_df['year'] = day_df['year'].map(year_mapping)
hour_df['year'] = hour_df['year'].map(year_mapping)

# Menambahkan kolom 'day_type' untuk membedakan antara weekday dan weekend
def categorize_day(day):
    if day in ['Saturday', 'Sunday']:
        return 'Weekend'
    else:
        return 'Weekday'

day_df['day_type'] = day_df['day_of_week'].apply(categorize_day)
hour_df['day_type'] = hour_df['day_of_week'].apply(categorize_day)

# Sidebar untuk navigasi
st.sidebar.title("Navigasi")
options = st.sidebar.radio('Pilih Halaman:', ['Overview', 'Analisis Penyewaan per Jam', 'Analisis Penyewaan per Musim'])

# Halaman Overview
if options == 'Overview':
    st.header("Data Overview")
    st.write("Dataset Penyewaan Harian:")
    st.dataframe(day_df.head())
    st.write("Dataset Penyewaan per Jam:")
    st.dataframe(hour_df.head())

    st.subheader("Statistik Deskriptif (Dataset Harian)")
    st.write(day_df.describe())

# Halaman Analisis Penyewaan per Jam
elif options == 'Analisis Penyewaan per Jam':
    st.header("Analisis Penyewaan Sepeda per Jam")

    # Menghitung total penyewaan per jam
    hourly_counts = hour_df.groupby('hour')['total_count'].sum().reset_index()
    hourly_counts['hour'] = hourly_counts['hour'].astype(int)
    hourly_counts.sort_values('hour', inplace=True)

    # Visualisasi penyewaan per jam
    fig, ax = plt.subplots(figsize=(12,6))
    sns.barplot(x='hour', y='total_count', data=hourly_counts, palette='viridis', ax=ax)
    ax.set_title('Total Penyewaan Sepeda per Jam')
    ax.set_xlabel('Jam')
    ax.set_ylabel('Jumlah Penyewaan')
    st.pyplot(fig)

    # Insight
    st.subheader("Insight")
    st.write("""
    - **Jam Puncak Penyewaan:** Jam 17:00 memiliki jumlah penyewaan tertinggi.
    - **Jam Terendah Penyewaan:** Jam 04:00 memiliki jumlah penyewaan terendah.
    - **Interpretasi:** Peningkatan penyewaan pada jam 17:00 kemungkinan besar karena jam pulang kerja, sementara rendahnya penyewaan pada jam 04:00 disebabkan oleh aktivitas yang minim pada dini hari.
    """)

# Halaman Analisis Penyewaan per Musim
elif options == 'Analisis Penyewaan per Musim':
    st.header("Analisis Penyewaan Sepeda per Musim")

    # Menghitung total penyewaan per musim
    season_counts = day_df.groupby('season')['total_count'].sum().reset_index()

    # Visualisasi penyewaan per musim
    fig, ax = plt.subplots(figsize=(8,6))
    sns.barplot(x='season', y='total_count', data=season_counts, palette='autumn', ax=ax)
    ax.set_title('Total Penyewaan Sepeda per Musim')
    ax.set_xlabel('Musim')
    ax.set_ylabel('Jumlah Penyewaan')
    st.pyplot(fig)

    # Insight
    st.subheader("Insight")
    st.write("""
    - **Musim dengan Penyewaan Tertinggi:** Musim Fall (Gugur) memiliki jumlah penyewaan tertinggi.
    - **Interpretasi:** Kondisi cuaca yang nyaman pada musim gugur mungkin mendorong lebih banyak orang untuk bersepeda.
    """)


