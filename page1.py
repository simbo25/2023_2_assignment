import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

from geopy.geocoders import Nominatim
from st_pages import Page, show_pages, add_page_title
from PIL import Image

# 레이아웃
st.set_page_config(
      page_title = '내가 만드는 여행 가이드북',
      page_icon = ':card_index:',
      layout = 'wide'
)

header_path = os.getcwd() + '/img/header.jpg'
image = Image.open(header_path)
st.image(image)

# CSS
st.markdown("""
            
<style>

.element-container div {
    diplay: felx;
    justify-content: center;
}
           

</style>

""", unsafe_allow_html = True)

# 글자체
font_path = os.path.join(os.getcwd(), 'NanumGothic.ttf')
font_prop = fm.FontProperties(fname=font_path)

# 제목
st.header(':bookmark_tabs:오늘의 활동') 

# 1. 문화의 발견! 여행지 탐색하기
st.subheader('활동1. 문화의 발견! 여행지 탐색하기', divider='rainbow')

st.markdown('#### 다음 과정에 따라 가이드북을 만들 자료를 수집합시다 :smiley: ')
st.markdown(" 1. 조원들과 함께 **방문하고 싶은 여행지**를 선정합니다.")
st.markdown(" 2. 여행지를 **아래 검색 기능**을 활용하여 위치를 확인합니다.")
st.markdown(" 3. 해당 여행지와 관련된 **여러 정보를 수집**합니다. 대표적으로 아래 정보가 있습니다.")
st.markdown(" 4. 수집한 자료는 조별로 **종이에 잘 기록**해둡니다. ")

with st.container(border = True):
    st.markdown("환율, 시차, 기후, 특이한 지형, 랜드마크, 문화적 주의사항")
st.divider()

# 도시명 검색
city_name = st.text_input('검색할 도시명을 입력하세요')
geolocator = Nominatim(user_agent="Making tour guide")
location = geolocator.geocode(city_name)

# 검색 결과 표시
if location:
    st.write(f"{city_name}의 위치: **위도 {location.latitude}**, **경도 {location.longitude}**")
    loc = pd.DataFrame({
        'LAT': [location.latitude],
        'LON': [location.longitude]
    })
    
    st.map(loc)
else:
    st.write(f"{city_name}을(를) 찾을 수 없습니다.")

st.divider()
st.subheader(':white_check_mark: 오늘 조사한 자료는 꼭 기록해둡시다!!! :tada:')

# 페이지 연결
show_pages(
    [
        Page("page1.py", " 문화의 발견! 여행지 탐색하기", ":airplane_departure:"),
        Page("page2.py", " 짠내투어: 여행경비 조사하기", ":money_with_wings:"),
        Page("page3.py", " 과학으로 만드는 여행 가이드북", ":umbrella:")
    ]
)