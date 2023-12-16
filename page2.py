import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

from PIL import Image

# 레이아웃
st.set_page_config(
      page_title = ':card_index:내가 만드는 여행 팜플렛',
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

# 2.짠내투어: 여행경비 조사하기
st.subheader('활동2. 짠내투어: 여행경비 조사하기', divider='rainbow')

con1, con2 = st.columns([0.3,0.7])

with con1: 
    # 데이터 프레임 생성(호주 시드니 샘플 데이터 입력)
    df = pd.DataFrame(
        [
            {"month": "1", "lowest": 724500, "highest": 1216300},
            {"month": "2", "lowest": 667100, "highest": 1005600},
            {"month": "3", "lowest": 609600, "highest": 980532},
            {"month": "4", "lowest": 584478, "highest": 890800},
            {"month": "5", "lowest": 549672, "highest": 728071},
            {"month": "6", "lowest": 570206, "highest": 807233},
            {"month": "7", "lowest": 549672, "highest": 874686},
            {"month": "8", "lowest": 549672, "highest": 700206},
            {"month": "9", "lowest": 549672, "highest": 950206},
            {"month": "10", "lowest": 549672, "highest": 996800},
            {"month": "11", "lowest": 837951, "highest": 876800},
            {"month": "12", "lowest": 764700, "highest": 980000},
        ]
    )

    # 학생 데이터 프레임 채우기(활동)
    edited_df = st.data_editor(
        df,
        column_config={
            "month": "출발 시기(월)",
            "lowest": st.column_config.NumberColumn(
                "최저가",
                help="이달의 제일 저렴한 가격을 찾아주세요!",
                step=1,
                format="%d 원",
            ),
            "highest": st.column_config.NumberColumn(
                "최고가",
                help="이달의 제일 비싼 가격을 찾아주세요!",
                step=1,
                format="%d 원",
            )
        },
        disabled=["month"],
        hide_index=True, height = 458
    )


with con2: 
    with st.container(border = True):
        st.markdown("#### 비행기표 가격을 조사해봅시다 :airplane_departure:")
        st.markdown('1. 링크를 클릭하여 [**구글 항공권 예약하기**](https://www.google.com/travel/flights) 로 이동하세요.')
        st.markdown('2. 여행가고 싶은 국가명을 고르고, 여행기간을 **오늘 날짜부터 7일**로 설정하세요.')
        st.markdown('3. 아래 그림과 같이 **가격 그래프 버튼**을 누르세요.')
        st.markdown('4. 월별 최저가와 최고가를 찾아 왼쪽 표를 채우세요.' )
        st.markdown('5. 아래 **그래프 그리기 버튼**을 통해 데이터를 분석해보세요.' )

        img1_path = os.getcwd() + '/img/google_flight1.png'
        google_flight1 = Image.open(img1_path)
        st.image(google_flight1)

months = df['month'].tolist()

with st.container(border = True):
    operation = st.radio("데이터를 어떻게 연산할까요?", ("최고가 + 최저가", "최고가 - 최저가", "최고가 × 최저가", "최고가 ÷ 최저가"), 
                        help = '입력한 데이터를 사칙연산 해보고, 어느 시기에 여행을 갈지 고민해보세요.',
                        horizontal = True,)


    # 그래프 그리기
    if st.button('입력한 데이터 바탕으로 그래프 그리기', use_container_width = True):

        con3, con4 = st.columns([0.5,0.5])
        with con3: 
            plt.figure(figsize=(10, 6))

            bar_width = 0.35
            index = range(len(months)) 

            plt.bar(index, edited_df['lowest'], bar_width, label='최저가', color='blue')
            plt.bar([i + bar_width for i in index], edited_df['highest'], bar_width, label='최고가', color='orange', alpha=0.7)

            plt.xlabel('월', fontproperties = font_prop)
            plt.ylabel('가격(원)', fontproperties = font_prop)
            plt.title('월별 최저가와 최고가', fontproperties = font_prop)
            plt.legend(prop=font_prop)
            plt.xticks(range(len(months)), months, rotation=45)
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot(plt)

        with con4:
            # 선택된 연산에 따라 계산
            result = None
            if operation == "최고가 + 최저가":
                result = edited_df['highest'] + edited_df['lowest']
            elif operation == "최고가 - 최저가":
                result = edited_df['highest'] - edited_df['lowest']
            elif operation == "최고가 × 최저가":
                result = edited_df['highest'] * edited_df['lowest']
            elif operation == "최고가 ÷ 최저가":
                result = edited_df['highest'] / edited_df['lowest']

            plt.figure(figsize=(10, 6))
            plt.bar(range(len(months)), result, label=operation, color='green')
            plt.xlabel('월', fontproperties=font_prop)
            plt.ylabel('계산 결과', fontproperties=font_prop)
            plt.title(f'월별 {operation} 결과', fontproperties=font_prop)
            plt.legend(prop=font_prop)
            plt.xticks(range(len(months)), months, rotation=45)
            st.pyplot(plt)

st.divider()


# 빅맥지수 (추후 가이드북 제작 시 물가를 판단할 수 있는 기준)
st.markdown('#### 여행지의 물가는 비싼편일까? : 빅맥지수 :hamburger: ')

with st.container(border = True):
    st.markdown('[**빅맥 지수**](https://ko.wikipedia.org/wiki/%EB%B9%85%EB%A7%A5_%EC%A7%80%EC%88%98)는 각 나라의 환율의 상대적 가치를 비교하기 위해 맥도날드의 빅맥 버거를 기준으로 환율을 비교하는 경제적 지표입니다.')
    st.markdown(r"$빅맥 지수 = \cfrac{{\text{{국가 A의 빅맥 가격}}}}{{\text{{국가 B의 빅맥 가격}}}} \times 100$")

con3, con4 = st.columns([0.5,0.5])

with con3: 
    A_bigmac = st.number_input(':pencil: **우리나라의 빅맥 가격을 조사해 입력해주세요:**', step = int(1))
    st.write('**우리나라(A)의 빅맥 가격:**', A_bigmac)

with con4:
    B_bigmac = st.number_input(':pencil: **여행지의 빅맥 가격을 조사해 입력해주세요:**', step = int(1))
    st.write('**여행지(B)의 빅맥 가격:**', B_bigmac)

bigmac_index = str('계산을 위한 정보가 필요합니다.')
if B_bigmac != 0:
    bigmac_index = (A_bigmac / B_bigmac) * 100
    print(f"빅맥 지수: {bigmac_index}")
    st.write('우리나라 & 여행지의 빅맥지수는 ', bigmac_index, '입니다.')        

else:
    st.write('**여행지의 빅맥 가격이 입력되지 않아 빅맥 지수를 계산할 수 없습니다.**')

with st.container(border = True):    
    if B_bigmac != 0:
        if bigmac_index > 100:
            st.write('따라서, 이 나라에 여행을 가면 물가가 **싸게** 느껴집니다!')
        
        elif bigmac_index < 100:
            st.write('따라서, 이 나라에 여행을 가면 물가가 **비싸게** 느껴집니다!')
         
        else:
            st.write('**물가를 판단하기 위해서는 정보가 더 필요합니다!**')
            
    else:
        pass

with st.form(key='my_form'):
    st.markdown('**생각해 보기** :pencil:')
    student_result = st.text_input("위의 자료들을 여행 가이드북 제작에에 어떻게 활용할 수 있을지 짧은 글을 작성해봅시다! :blush:")

    if st.form_submit_button('한줄 보고서 제출'):
        st.write(f"**'{student_result}'** (이)라고 정리했군요! 수고했어요 :clap:")

st.divider()
st.subheader(':white_check_mark: 오늘 조사한 자료는 꼭 기록해둡시다!!! :tada:')