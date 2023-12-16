import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

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

# 2.과학으로 만드는 여행 가이드북
st.subheader('활동3. 과학으로 만드는 여행 가이드북 ', divider='rainbow')

with st.container(border = True):
    st.markdown("#### 기후 정보를 세부적으로 분석해 봅시다! :thermometer:")
    st.markdown('1. 아래 **기상청 날씨누리**에서 여행지 기후 데이터를 조회합니다.')
    st.markdown('2. **활동1**에서 기록한 여행지의 위도와 경도값을 준비합니다.')
    st.markdown('2. [**링크**](https://oneweather.org/archive/)로 접속하여 위도(Latitude)와 경도(longtitude)값, 여행 날짜(date)를 입력하여 **이슬점(dew point)** 데이터를 수집합니다.')
    st.markdown('3. 위 링크에서 **수집한 이슬점 csv 파일**을 이용하여 그래프를 추가로 그려봅니다.')
    st.markdown('4. 모든 기후 정보를 종합하여 여행 시기의 날씨 특징을 **과학적 용어**를 활용해 설명해봅니다.')
    st.markdown('5. 이 정보를 여행지 가이드북 제작에 어떻게 활용할 수 있을지 조원들과 함께 고민해봅니다.')
        
# 세계 날씨 정보 얻기
st.markdown("#### 기상청 날씨누리")
weather_URL = "https://www.weather.go.kr/w/theme/world-weather.do?nolayout=Y"
iframe_code1 = f'<iframe src="{weather_URL}" width="100%" height="1200" frameborder="1"></iframe>'
st.markdown(iframe_code1, unsafe_allow_html=True)


# csv 파일 업로드
csv_file = st.file_uploader(':file_folder: **링크에서 다운받은 이슬점 데이터 파일을 업로드하세요.**', type = ['csv'])

if csv_file is not None:
    df = pd.read_csv(csv_file)

    # 데이터 프레임 생성 및 가공
    selected_columns = ['Time', 'Dewpoint (°C)']
    filtered_df = df[selected_columns]
    filtered_df['Time'] = pd.to_datetime(filtered_df['Time'], format='%Y-%m-%d %H:%M')
    filtered_df['Date'] = filtered_df['Time'].dt.date
    filtered_df['Hour'] = filtered_df['Time'].dt.hour

    # 그래프 그리기
    plt.figure(figsize=(10, 6))
    plt.plot(filtered_df['Hour'], filtered_df['Dewpoint (°C)'], marker='o')
    plt.xlabel('시간(시)', fontproperties=font_prop)
    plt.ylabel('이슬점 (°C)', fontproperties=font_prop)
    plt.title('이슬점 시계열 데이터', fontproperties=font_prop)
    plt.xticks(rotation=45)  # x축 레이블 회전
    

    # 그래프 제목에 날짜 정보 추가
    start_date = filtered_df['Time'].min().strftime("%Y-%m-%d")
    end_date = filtered_df['Time'].max().strftime("%Y-%m-%d")
    plt.title(f'이슬점 시계열 데이터 ({start_date} ~ {end_date})')
    
    plt.xticks(range(filtered_df['Hour'].min(), filtered_df['Hour'].max() + 1, 1))

    st.pyplot(plt)
else:
    st.warning('파일을 업로드하지 않았습니다.')

with st.form(key='my_form'):
    st.markdown('**생각 나누기** :pencil:')
    student_result = st.text_input("새롭게 깨달은 내용을 공유해주세요! :blush:")

    if st.form_submit_button('한줄 보고서 제출'):
        st.write(f"**'{student_result}'** (이)라고 정리했군요! 수고했어요 :clap:")

st.divider()

# 태양의 일변화 정보 얻기
with st.container(border = True):
    st.markdown("#### 태양의 일변화 고려해 동선을 계획해봅시다! :sun_with_face: :full_moon_with_face:")
    st.markdown('1. **시뮬레이션 링크**에 접속해 내가 여행지를 방문했을 때, 태양의 운동을 관찰합니다.')
    st.markdown("2. 시간 및 위치 조절(Time and Location Controls)에서 **방문 시기**와 **위도**를 조절합니다.")
    st.markdown("3. **관찰자의 위도(the observer's latitude)**에 따라 태양의 운동은 다르게 관찰됩니다.")
    st.markdown("4. **animation mode**에서 **loop day를 체크**하면 하루동안 태양의 변화를 반복하여 관찰할 수 있습니다.")
    st.markdown("5. 적절한 여행 동선을 계획하기 위해 **애니메이션을 다양하게 조작하고 탐구** 해봅니다.")
    st.markdown("6. 이 정보를 여행지 가이드북 제작에 어떻게 활용할 수 있을지 조원들과 함께 고민해봅니다.")

st.markdown("##### ㅤ[시뮬레이션 사이트 접속](https://astro.unl.edu/classaction/animations/coordsmotion/sunmotions.html)")
sim_path = os.getcwd() + '/img/sunmotions.png'
image_sun = Image.open(sim_path)
st.image(image_sun)

# 로컬 실행시 실행 가능 코드
#sunmotion_URL = "http://astro.unl.edu/classaction/animations/coordsmotion/sunmotions.html"
#iframe_code2 = f'<iframe src="{sunmotion_URL}" width="100%" height="725" scrolling="no"></iframe>'
#st.markdown(iframe_code2, unsafe_allow_html=True)

with st.form(key='my_form1'):
    st.markdown('**생각 나누기** :pencil:')
    student_result = st.text_input("새롭게 깨달은 내용을 공유해주세요! :blush:")

    if st.form_submit_button('한줄 보고서 제출'):
        st.write(f"**'{student_result}'** (이)라고 정리했군요! 수고했어요 :clap:")

st.divider()
st.subheader(':white_check_mark: 오늘 조사한 자료는 꼭 기록해둡시다!!! :tada:')