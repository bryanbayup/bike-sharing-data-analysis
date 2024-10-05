# dashboard/dashboard.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Mengatur tema seaborn
sns.set_theme(style="darkgrid")

# Judul Dashboard
st.title("Bike Sharing Data Analysis Dashboard")

# Membaca dataset
day_df = pd.read_csv('../data/day.csv')
hour_df = pd.read_csv('../data/hour.csv')

# Data Preprocessing
# Mengubah tipe data 'dteday' menjadi datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Mengubah tipe data beberapa kolom menjadi kategori
category_columns = ['season', 'yr', 'mnth', 'holiday', 'weekday', 'weathersit']
for col in category_columns:
    day_df[col] = day_df[col].astype('category')
    hour_df[col] = hour_df[col].astype('category')

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

# Mengonversi nilai kategori
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
options = st.sidebar.radio('Pilih Halaman:', ['Overview', 'Hourly Analysis', 'Seasonal Analysis', 'User Type Analysis'])

if options == 'Overview':
    st.header("Data Overview")
    st.write("Dataset Day:")
    st.dataframe(day_df.head())
    st.write("Dataset Hour:")
    st.dataframe(hour_df.head())
    st.write("Statistik Deskriptif:")
    st.write(day_df.describe())
elif options == 'Hourly Analysis':
    st.header("Hourly Rental Analysis")

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
elif options == 'Seasonal Analysis':
    st.header("Seasonal Rental Analysis")

    # Menghitung total penyewaan per musim
    season_counts = day_df.groupby('season')['total_count'].sum().reset_index()

    # Visualisasi penyewaan per musim
    fig, ax = plt.subplots(figsize=(8,6))
    sns.barplot(x='season', y='total_count', data=season_counts, palette='autumn', ax=ax)
    ax.set_title('Total Penyewaan Sepeda per Musim')
    ax.set_xlabel('Musim')
    ax.set_ylabel('Jumlah Penyewaan')
    st.pyplot(fig)
elif options == 'User Type Analysis':
    st.header("User Type Analysis")

    # Menghitung total penyewaan oleh pengguna registered dan casual
    total_casual = day_df['casual'].sum()
    total_registered = day_df['registered'].sum()

    # Membuat dataframe untuk visualisasi
    user_type_counts = pd.DataFrame({
        'User_Type': ['Casual', 'Registered'],
        'Total_Count': [total_casual, total_registered]
    })

    # Visualisasi perbandingan penyewaan
    fig, ax = plt.subplots(figsize=(8,6))
    sns.barplot(x='User_Type', y='Total_Count', data=user_type_counts, palette=['gray', 'skyblue'], ax=ax)
    ax.set_title('Perbandingan Penyewaan antara Pengguna Casual dan Registered')
    ax.set_xlabel('Tipe Pengguna')
    ax.set_ylabel('Jumlah Penyewaan')
    st.pyplot(fig)

    # Menampilkan persentase
    total_users = total_casual + total_registered
    casual_percentage = (total_casual / total_users) * 100
    registered_percentage = (total_registered / total_users) * 100

    st.write(f"Persentase Casual Users: **{casual_percentage:.1f}%**")
    st.write(f"Persentase Registered Users: **{registered_percentage:.1f}%**")
