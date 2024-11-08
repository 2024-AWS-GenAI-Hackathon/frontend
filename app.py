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

# HTML로 선택 버튼 구현
st.markdown("""
<div class="custom-radio">
  <input type="radio" id="social" name="category" value="소셜미디어" checked>
  <label for="social">소셜미디어</label>

  <input type="radio" id="print" name="category" value="인쇄물">
  <label for="print">인쇄물</label>
</div>
""", unsafe_allow_html=True)


  # 이미지 업로드
st.markdown('<h4 class="subheader-custom">이미지 추가</h4>', unsafe_allow_html=True)
uploaded_image = st.file_uploader("홍보물에 들어갈 이미지 파일을 업로드해 주세요.")
st.write("")

# 키워드 입력
st.markdown('<h3 class="subheader-custom">이미지에 넣을 키워드</h3>', unsafe_allow_html=True)
keywords = st.text_input("키워드를 입력하세요 (예: 꿀, 가을, 밤)")
st.write("")

# 리뷰 기간 설정
st.markdown("""<h3 class="subheader-custom">리뷰 기간 설정</h3>""", unsafe_allow_html=True)
review_period = st.radio(
  "원하는 홍보물 생성을 위해 참고할 기간을 선택해 주세요.",
  ["1주", "2주", "3주", "4주"],
  horizontal=True
)

st.divider()

# 문구 생성 버튼
if st.button("문구 생성하기"):
  st.success("문구가 성공적으로 생성되었습니다!")
