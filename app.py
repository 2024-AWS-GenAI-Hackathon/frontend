import streamlit as st

st.set_page_config(
  page_title="promi",
  page_icon="./images/promi_favicon.png",
  layout="centered"
)

# CSS 파일 로드
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("./styles.css")

# 컨텐츠
with st.container():
  st.title('어떤 제품을 홍보하고 싶으신가요?')
  st.text('이미지와 키워드를 입력하여, 손쉽게 가게 홍보에 필요한 이미지, 문구, 해시태그를 제작해 보세요!')

st.write("")

# 기간 설정
st.markdown("""<h3 class="subheader-custom">리뷰 카테고리</h3>""", unsafe_allow_html=True)
review_category = st.radio(
    "", 
    ["제품/가격", "분위기", "고객", "기타"],
    horizontal=True
)

st.write("")

# 이미지 업로드
st.markdown('<h3 class="subheader-custom">홍보물에 들어갈 이미지 추가</h3>', unsafe_allow_html=True)
uploaded_image = st.file_uploader("", type=["jpg", "png", "jpeg"]) 

st.write("")

# 추가 요청사항
st.markdown('<h3 class="subheader-custom">추가 요청사항</h3>', unsafe_allow_html=True)
keywords = st.text_input(
    label="",  
    placeholder="ex) 따뜻한 느낌으로 만들어줘"
)

st.write("")

# 기간 설정
st.markdown("""<h3 class="subheader-custom">홍보물 제작을 위해 참고할 기간 설정</h3>""", unsafe_allow_html=True)
review_period = st.radio(
    "", 
    ["1주", "2주", "3주", "4주"],
    horizontal=True
)

st.write("")
# st.divider()

# 버튼 구현
st.markdown("""
<div class="center-button-container">
    <button class="center-button">문구 먼저 생성하기</button>
</div>
""", unsafe_allow_html=True)