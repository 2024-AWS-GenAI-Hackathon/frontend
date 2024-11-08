import streamlit as st
import base64
import requests

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

category_map = {
    "제품/가격": "Product/Price",
    "분위기": "Ambiance",
    "고객": "Customer",
    "기타": "Other"
}

# 컨텐츠
with st.container():
    st.title('어떤 제품을 홍보하고 싶으신가요?')
    st.text('고객의 리뷰를 분석해 제품의 장점을 강조한 홍보 문구와 이미지를 제작해 보세요!')

st.write("")

# 카테고리 선택
st.markdown("""<h3 class="subheader-custom">리뷰 카테고리</h3>""", unsafe_allow_html=True)
selected_category_kor = st.radio(
    "",
    list(category_map.keys()),  # 한글로 표시
    horizontal=True
)

st.write("")

# 이미지 업로드
st.markdown('<h3 class="subheader-custom">홍보물에 들어갈 이미지 추가</h3>', unsafe_allow_html=True)
uploaded_image = st.file_uploader("", type=["jpg", "png", "jpeg"])

st.write("")

# 추가 요청사항 
st.markdown('<h3 class="subheader-custom">추가 요청사항 (옵션)</h3>', unsafe_allow_html=True)
additional_requests = st.text_input(
    label="",
    placeholder="ex) 인기 항목을 강조해주세요"
)

st.write("")

# 데이터 전송 버튼
if st.button("데이터 전송하기"):
    if uploaded_image is not None:
        # 이미지를 Base64로 인코딩
        image_data = uploaded_image.read()
        encoded_image = base64.b64encode(image_data).decode("utf-8")

        # 하드코딩된 게시 기간
        posting_time = "2023-01-01 to 2023-12-31"

        # 서버로 보낼 데이터
        data = {
            "category": category_map[selected_category_kor],  # 영어로 변환
            "image": encoded_image,  # Base64 인코딩된 이미지
            "posting_time": posting_time,  # 하드코딩된 값
            "additional_requests": additional_requests
        }

        # 서버 요청
        response = requests.post(
            "https://k4y2o4tnw8.execute-api.ap-northeast-2.amazonaws.com/dev/input",
            json=data
        )

        # 서버 응답 처리
        if response.status_code == 200:
            st.success("데이터가 성공적으로 전송되었습니다!")
            response_data = response.json()

            st.write("")    

            # 응답 안내 문구 추가
            st.markdown("**고객들의 리뷰**를 기반으로 한 인스타그램 **홍보 문구 3가지**를 추천드릴게요 :)")

            # 필요한 데이터 매핑
            first_title = response_data.get("first_title", "제목 없음")
            first_content = response_data.get("first_content", "내용 없음")
            second_title = response_data.get("second_title", "제목 없음")
            second_content = response_data.get("second_content", "내용 없음")
            third_title = response_data.get("third_title", "제목 없음")
            third_content = response_data.get("third_content", "내용 없음")

            # 데이터 출력
            st.markdown(f"#### {first_title}")
            st.write(first_content)

            st.markdown(f"#### {second_title}")
            st.write(second_content)

            st.markdown(f"#### {third_title}")
            st.write(third_content)
        else:
            st.error("데이터 전송 실패!")
            st.write("상태 코드:", response.status_code)
            st.write("응답 내용:", response.text)





    else:
        st.warning("이미지를 업로드해주세요.")

# 스타일을 위한 빈 줄
st.write("")
