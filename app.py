import streamlit as st
import base64
import requests

st.set_page_config(
    page_title="promi",
    page_icon="./images/promi_favicon.png",
    layout="centered"
)

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

if "response_data" not in st.session_state:
    st.session_state["response_data"] = None

if "editing_content" not in st.session_state:
    st.session_state["editing_content"] = None

if "confirmed_content" not in st.session_state:
    st.session_state["confirmed_content"] = None

# 컨텐츠
with st.container():
    st.title('어떤 제품을 홍보하고 싶으신가요?')
    st.text('고객의 리뷰를 분석하여, 제품의 장점을 강조한 홍보 문구와 이미지를 제작해 보세요!')

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
    placeholder="ex) 따뜻한 느낌으로 만들어줘"
)

st.write("")


# 데이터 전송 버튼
if st.button("데이터 전송하기"):
    if uploaded_image is not None:
        image_data = uploaded_image.read()
        encoded_image = base64.b64encode(image_data).decode("utf-8")

        posting_time = "2023-01-01 to 2023-12-31"

        data = {
            "category": category_map[selected_category_kor],
            "image": encoded_image,
            "posting_time": posting_time,
            "additional_requests": additional_requests
        }

        # 홍보 문구 서버 요청
        response = requests.post(
            "https://k4y2o4tnw8.execute-api.ap-northeast-2.amazonaws.com/dev/input",
            json=data
        )

        if response.status_code == 200:
            st.success("데이터가 성공적으로 전송되었습니다!")
            st.session_state["response_data"] = response.json()  # 응답 데이터를 세션 상태에 저장
        else:
            st.error("데이터 전송 실패!")
            st.write("상태 코드:", response.status_code)
            st.write("응답 내용:", response.text)
    else:
        st.warning("이미지를 업로드해주세요.")

st.write("")

# 최종 문구 저장 함수
def save_final_text(user_id, final_title, final_content):
    data = {
        "user_id": user_id,
        "final_title": final_title,
        "final_content": final_content
    }
    response = requests.post(
        "https://l2bwgqe1s9.execute-api.ap-northeast-2.amazonaws.com/default/apps_save_final_text",
        json=data
    )
    if response.status_code == 200:
        st.success("성공")
        st.session_state["confirmed_content"] = (final_title, final_content)
    else:
        st.error("최종 문구 저장 실패!")
        st.write("상태 코드:", response.status_code)
        st.write("응답 내용:", response.text)

# 버튼 클릭 시 호출할 함수
def confirm_selection(index, title, content):
    user_id = "123987"
    save_final_text(user_id, title, content)

# 서버 응답 데이터 처리 및 버튼 액션
if st.session_state["response_data"]:
    response_data = st.session_state["response_data"]
    
    st.markdown("**고객들의 리뷰**를 기반으로 한 인스타그램 **홍보 문구 3가지**를 추천드릴게요 :)")

    first_title = response_data.get("first_title", "제목 없음")
    first_content = response_data.get("first_content", "내용 없음")
    second_title = response_data.get("second_title", "제목 없음")
    second_content = response_data.get("second_content", "내용 없음")
    third_title = response_data.get("third_title", "제목 없음")
    third_content = response_data.get("third_content", "내용 없음")

    # 생성된 문구 출력 및 버튼 액션
    for i, (title, content) in enumerate([
        (first_title, first_content),
        (second_title, second_content),
        (third_title, third_content)
    ], start=1):
        cols = st.columns([6, 1, 1])
        with cols[0]:
            st.markdown(f"#### {title}")
            st.write(content)
        with cols[1]:
            if st.button(f"확정 {i}", key=f"confirm_{i}"):
                confirm_selection(i, title, content)
        with cols[2]:
            if st.button(f"수정 {i}", key=f"edit_{i}"):
                st.session_state["editing_content"] = (title, content)

st.write("")

if st.session_state["editing_content"]:
    st.markdown("### 수정된 내용")
    title, content = st.session_state["editing_content"]
    edited_title = st.text_input("제목", title)
    edited_content = st.text_area("내용", content)

    if st.button("수정된 내용 확정"):
        confirm_selection(None, edited_title, edited_content)
        st.session_state["editing_content"] = None

# '문구를 기반으로 한 이미지 생성하기' 버튼 생성
if st.session_state["confirmed_content"]:
    st.markdown("### 이미지 생성")
    final_title, final_content = st.session_state["confirmed_content"]
    if st.button("문구를 기반으로 한 이미지 생성하기"):
        st.write("이미지 생성 기능은 현재 개발 중입니다.")
