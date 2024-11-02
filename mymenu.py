import streamlit as st
import webbrowser

# 세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state.page = 'main'
if 'query' not in st.session_state:
    st.session_state.query = ''

def switch_to_second_page():
    st.session_state.page = 'second'
    second_page()

def go_to_main():
    st.session_state.page = 'main'

def handle_form_submit():
    st.success(f"제출되었습니다!\n이름: {st.session_state.name}\n이메일: {st.session_state.email}")

def show_korean_form():
    st.write("### 외국인 체류지변경 신고서 작성")

    # 신고서 폼 필드들
    col1, col2 = st.columns(2)

    with col1:
        st.text_input("성명 (한글)", key="name_kr")
        st.text_input("성명 (영문)", key="name_en")
        st.date_input("생년월일", key="birth_date")
        st.text_input("외국인등록번호", key="alien_reg_no")

    with col2:
        st.text_input("국적", key="nationality")
        st.text_input("전화번호", key="phone")
        st.text_input("이메일", key="email")

    st.subheader("이전 주소")
    st.text_input("이전 거주지 주소", key="prev_address")

    st.subheader("새로운 주소")
    st.text_input("새로운 거주지 주소", key="new_address")
    st.date_input("전입 일자", key="move_date")

    if st.button("신고서 제출"):
        st.success("신고서가 성공적으로 제출되었습니다!")
        # 여기에 실제 제출 로직을 추가할 수 있습니다

# 메인 페이지
def main_page():
    st.title("Foreigner Civil Complaint Assistant - English")
    st.write("This page provides information related to foreigner residence change notifications.")

    
    query = st.text_input("Enter your question below", "I want to move, what administrative procedures should I follow?")
    
    # Submit 버튼
    if st.button("Submit Question"):
        st.session_state.query = query
        switch_to_second_page()

# 두번째 페이지
def second_page():
   
    default_response = """
    First, you need to report your residence change. The residence change must be reported within 15 days of moving.
    For late reporting, visit the Immigration Office of your new residence area, or you may report at a local government office.
    Required documents:
    1. Residence change notification form
    2. ID: Alien Registration Card
    3. Proof of residence (lease agreement, accommodation receipt, etc.)
    """
    
    st.write("### Response")
    st.write(default_response)
    
    # 라디오 버튼으로 선택지 제공
    choice = st.radio(
        "Would you like to:",
        ["Get the form link",
         "Fill out the form in Korean",
         "View sample filled form"
        ]
    )
    
    if choice == "Get the form link":
        if st.button("Get the form link"):
            st.markdown("[You can download the form here: [Foreign Residence Change Form]](https://www.hygn.go.kr/00428/00435/00501.web)")
            
    elif choice == "Fill out the form in Korean":
        show_korean_form()      
                    
    else:  # PDF 문서 열기
        if st.button("PDF 열기"):
            # PDF URL을 여기에 입력하세요
            pdf_url = "https://example.com/sample.pdf"
            st.markdown(f"[PDF 문서 바로가기]({pdf_url})")
    
    # 메인 페이지로 돌아가기 버튼
    if st.button("처음으로 돌아가기"):
        go_to_main()

# 메인 앱 로직
def main():
    if st.session_state.page == 'main':
        main_page()
    elif st.session_state.page == 'second':
        second_page()

if __name__ == "__main__":
    main()
