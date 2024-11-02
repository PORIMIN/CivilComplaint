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
            import fitz  # PyMuPDF
import os

def fill_pdf_form(input_pdf_path, output_pdf_path):
    # 여기에 변수들을 함수 내부로 이동
    filled_text = {
        "Surname": "Smith",
        "Given names": "Alex",
        "Sex": "M",
        "Date of birth": "1990-01-01",
        "Nationality": "America",
        "Former address": "123 Old Street, Seoul",
        "New address": "456 New Avenue, Busan",
        "Tel": "010-1234-5678",
        "Registration NO.": "123456-7890123",
        "Date of registration": "2024-11-02",
        "Name in full": "Yeon-Ju Oh",
        "Relation": "Wife",
        "Date of report": "2024-11-02",
        "Signature of applicant": "Kim Alex"
    }

    field_positions = {
        "Surname": (170, 195),           # 성
        "Given names": (170, 215),       # 이름
        "Chinese characters": (350, 150), # 한자
        "Sex": (450, 175),               # 성별 (M)
        
        # 생년월일, 국적
        "Date of birth": (240, 240),     # 생년월일
        "Nationality": (480, 240),       # 국적
        
        # 주소 및 연락처 섹션
        "Former address": (220, 280),    # 전 체류지
        "New address": (220, 320),       # 신 체류지
        "Tel": (420, 310),               # 전화번호
        
        # 등록정보 섹션
        "Registration NO.": (230, 350),   # 외국인등록번호
        "Date of registration": (450, 350), # 등록일자
        
        # 동반자 정보 섹션 (중간 부분)
        "Name in full": (240, 380),       # 동반자 성명
        "Relation": (240, 480),           # 관계
        
        # 하단 서명 섹션
        "Date of report": (120, 620),     # 신고일
        "Signature of applicant": (120, 660) # 신고자 성명
    }

    try:
        # PDF 문서 열기
        doc = fitz.open(input_pdf_path)
        page = doc[0]
        
        # 텍스트 삽입
        for field, value in filled_text.items():
            x, y = field_positions.get(field, (0, 0))
            print(f"Adding text: {value} at position ({x}, {y})")
            page.insert_text((x, y), value, fontsize=12)
        
        # 변경사항 저장
        doc.save(output_pdf_path)
        doc.close()
        print(f"Successfully created PDF: {output_pdf_path}")
        return True
        
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        return False

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_pdf_path = os.path.join(script_dir, "pdf_documents", "외국인_체류지변경_신고서.pdf")
    output_pdf_path = os.path.join(script_dir, "pdf_documents", "체류지변경_신고서_완성본.pdf")
    
    print("Starting PDF form filling process...")
    print(f"Input PDF path: {input_pdf_path}")
    print(f"Input PDF exists: {os.path.exists(input_pdf_path)}")
    print(f"Output PDF path: {output_pdf_path}")
    
    # 함수 호출 (이제 filled_text와 field_positions를 인자로 전달하지 않음)
    success = fill_pdf_form(input_pdf_path, output_pdf_path)
    
    if success:
        print("Process completed successfully")
    else:
        print("Process failed")

if __name__ == "__main__":
    main()
    
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
