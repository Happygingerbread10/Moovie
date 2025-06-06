import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import st_folium
from datetime import datetime, timedelta

# KOBIS API 키 설정
KOBIS_API_KEY = 'YOUR_KOBIS_API_KEY'  # 발급받은 API 키로 대체하세요

# 전국 영화상영관 데이터 로드
@st.cache_data
def load_theater_data():
    df = pd.read_csv('theaters.csv', encoding='utf-8')
    df = df[['사업장명', '소재지도로명주소', '위도', '경도']]
    df = df.dropna(subset=['위도', '경도'])
    return df

# 일별 박스오피스 데이터 가져오기
def get_daily_box_office(date_str):
    url = f"http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={KOBIS_API_KEY}&targetDt={date_str}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['boxOfficeResult']['dailyBoxOfficeList']
    else:
        return []

# Streamlit 앱 시작
st.set_page_config(page_title="영화 상영 정보", layout="wide")
st.title("🎬 지역별 영화 상영 정보 확인")

# 지역 선택
regions = ['서울특별시', '경기도', '강원도', '충청북도', '충청남도', '전라북도', '전라남도', '경상북도', '경상남도', '제주특별자치도', '세종특별자치시']
selected_region = st.selectbox("지역을 선택하세요", regions)

# 데이터 로드
theater_df = load_theater_data()

# 선택한 지역의 영화관 필터링
region_theaters = theater_df[theater_df['소재지도로명주소'].str.contains(selected_region[:2])]

# 어제 날짜로 박스오피스 데이터 가져오기
yesterday = datetime.now() - timedelta(days=1)
date_str = yesterday.strftime('%Y%m%d')
box_office_data = get_daily_box_office(date_str)

# 상영 중인 영화 목록 생성
movies = [movie['movieNm'] for movie in box_office_data]
selected_movie = st.selectbox("영화를 선택하세요", movies)

# 지도 생성
if not region_theaters.empty:
    m = folium.Map(location=[region_theaters['위도'].mean(), region_theaters['경도'].mean()], zoom_start=10)
    for idx, row in region_theaters.iterrows():
        folium.Marker(
            location=[row['위도'], row['경도']],
            popup=f"{row['사업장명']}",
            tooltip=row['사업장명']
        ).add_to(m)
    st.subheader("🎥 지도에서 상영관 위치 확인")
    st_data = st_folium(m, width=800, height=500)
else:
    st.warning("선택한 지역에 영화관 정보가 없습니다.")
