import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 1. 영화관 더미 데이터 (위치 포함)
data = [
    {"도": "서울특별시", "영화관": "CGV 강남", "위도": 37.501, "경도": 127.026, "영화": "범죄도시4", "시간": "14:30", "좌석": 12},
    {"도": "서울특별시", "영화관": "롯데시네마 월드타워", "위도": 37.513, "경도": 127.104, "영화": "퓨리오사", "시간": "15:20", "좌석": 24},
    {"도": "경기도", "영화관": "CGV 수원", "위도": 37.266, "경도": 127.000, "영화": "쿵푸팬더4", "시간": "13:45", "좌석": 10},
    {"도": "강원도", "영화관": "메가박스 원주", "위도": 37.342, "경도": 127.933, "영화": "범죄도시4", "시간": "16:10", "좌석": 15},
    {"도": "전라북도", "영화관": "롯데시네마 전주", "위도": 35.823, "경도": 127.147, "영화": "퓨리오사", "시간": "13:10", "좌석": 8},
    {"도": "경상남도", "영화관": "CGV 창원", "위도": 35.228, "경도": 128.681, "영화": "쿵푸팬더4", "시간": "17:40", "좌석": 20},
    {"도": "제주특별자치도", "영화관": "메가박스 제주", "위도": 33.500, "경도": 126.531, "영화": "범죄도시4", "시간": "14:50", "좌석": 14},
    {"도": "세종특별자치시", "영화관": "CGV 세종", "위도": 36.480, "경도": 127.288, "영화": "퓨리오사", "시간": "17:10", "좌석": 20},
]

df = pd.DataFrame(data)

# 2. Streamlit 설정
st.set_page_config(page_title="🎥 영화 상영 정보", layout="wide")
st.title("🎬 대한민국 8도 지역별 영화 상영 정보")

# 3. 지역 선택
regions = df['도'].unique()
selected_region = st.selectbox("지역을 선택하세요", sorted(regions))

# 4. 해당 지역의 영화 목록 추출
region_df = df[df['도'] == selected_region]
available_movies = region_df['영화'].unique()
selected_movie = st.selectbox("상영 중인 영화를 선택하세요", available_movies)

# 5. 영화관 필터링
filtered = region_df[region_df['영화'] == selected_movie]

# 6. 지도 생성
if not filtered.empty:
    avg_lat = filtered['위도'].mean()
    avg_lon = filtered['경도'].mean()
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=11)

    for _, row in filtered.iterrows():
        popup = f"""
        <b>{row['영화관']}</b><br>
        상영 시간: {row['시간']}<br>
        남은 좌석: {row['좌석']}석
        """
        folium.Marker(
            location=[row['위도'], row['경도']],
            tooltip=row['영화관'],
            popup=popup
        ).add_to(m)

    st.subheader("🗺️ 영화관 위치")
    st_folium(m, width=800, height=500)

    # 7. 가장 빠른 상영 시간 표시
    earliest = filtered.sort_values(by='시간').iloc[0]
    st.success(
        f"🎞️ **가장 빠른 상영**: {earliest['영화관']} — {earliest['시간']} / 남은 좌석: {earliest['좌석']}석"
    )
else:
    st.warning("이 지역에서 해당 영화를 상영하는 영화관이 없습니다.")
