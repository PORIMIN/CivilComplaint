import streamlit as st
import webbrowser

# 세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state.page = 'main'
if 'keyword' not in st.session_state:
    st.session_state.keyword = ''

def switch_to_second_page():
    st.session_state.page = 'second'

def go_to_main():
    st.session_state.page = 'main'

def handle_form_submit():
    st.success(f"제출되었습니다!\n이름: {st.session_state.name}\n이메일: {st.session_state.email}")

# 메인 페이지
def main_page():
    st.title("키워드 입력 페이지")
    
    # 키워드 입력
    keyword = st.text_input("키워드를 입력하세요:", 
                           key="keyword_input",
                           value=st.session_state.keyword)
    
    # Submit 버튼
    if st.button("Submit"):
        if keyword.strip():  # 키워드가 비어있지 않은 경우
            st.session_state.keyword = keyword
            switch_to_second_page()
        else:
            st.error("키워드를 입력해주세요.")

# 두번째 페이지
def second_page():
    st.title("선택 페이지")
    st.write(f"입력된 키워드: {st.session_state.keyword}")
    
    # 라디오 버튼으로 선택지 제공
    choice = st.radio(
        "원하시는 작업을 선택하세요:",
        ["네이버 방문하기", "정보 입력하기", "PDF 문서 열기"]
    )
    
    if choice == "네이버 방문하기":
        if st.button("네이버로 이동"):
            st.markdown("[네이버 바로가기](http://naver.com)")
            
    elif choice == "정보 입력하기":
        with st.form("contact_form"):
            st.text_input("이름:", key="name")
            st.text_input("이메일:", key="email")
            submit_button = st.form_submit_button("제출")
            
            if submit_button:
                if st.session_state.name and st.session_state.email:
                    handle_form_submit()
                else:
                    st.error("모든 필드를 입력해주세요.")
                    
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
