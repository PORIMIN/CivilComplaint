import os
import fitz  # PyMuPDF
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from langchain_upstage import UpstageDocumentParseLoader, UpstageEmbeddings, ChatUpstage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter
# 환경 변수 로드
load_dotenv()
api_key = os.getenv("UPSTAGE_API_KEY")

# PDF 파일 경로 설정
pdf_files = {
    "외국인 체류지변경 신고서": "pdf_documents/외국인_체류지변경_신고서.pdf"
    # 필요한 다른 PDF 파일 경로도 추가할 수 있습니다.
}

# 데이터셋 준비 함수
def read_dataset(file_path):
    all_docs = []
    file1_load = UpstageDocumentParseLoader(file_path, split="page", api_key=api_key)
    docs = file1_load.load()
    for doc in docs:
        all_docs.append(doc)
    return all_docs


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
    # PDF 파일 경로 설정
    pdf_files = {
    "외국인 체류지변경 신고서": "pdf_documents/외국인_체류지변경_신고서.pdf"}
    pdf_document = pdf_files["외국인 체류지변경 신고서"]

# PDF 열기 및 텍스트 추출
    doc = fitz.open(pdf_document)
    extracted_text = ""

# 페이지별로 텍스트 추출
    for page_num in range(doc.page_count):
        page = doc[page_num]
        extracted_text += page.get_text()

# PDF 문서 닫기
    doc.close()

    # 빈칸에 대응하는 임의의 텍스트 채우기
    filled_text = extracted_text.replace("Surname", "Kim") \
                                .replace("Given names", "Alex") \
                                .replace("Chinese characters", "金") \
                                .replace("Sex", "M") \
                                .replace("Date of birth", "1990-01-01") \
                                .replace("Nationality", "South Korea") \
                                .replace("Former address", "123 Old Street, Seoul") \
                                .replace("New address", "456 New Avenue, Busan") \
                                .replace("Tel", "010-1234-5678") \
                                .replace("Registration NO.", "123456-7890123") \
                                .replace("Date of registration", "2024-11-02") \
                                .replace("Name in full", "Lee Alex") \
                                .replace("Relation", "Son") \
                                .replace("Date of report", "2024-11-02") \
                                .replace("Signature of applicant", "Lee Alex")

    # 영어 해석과 채운 텍스트를 테이블로 정리
    data = {
    "Field": [
        "Surname", "Given names", "Chinese characters", "Sex", 
        "Date of birth", "Nationality", "Former address", "New address", 
        "Tel", "Registration NO.", "Date of registration", 
        "Name in full", "Relation", "Date of report", "Signature of applicant"
    ],
    "Filled Text": [
        "Kim", "Alex", "金", "M", 
        "1990-01-01", "South Korea", "123 Old Street, Seoul", "456 New Avenue, Busan", 
        "010-1234-5678", "123456-7890123", "2024-11-02", 
        "Lee Alex", "Son", "2024-11-02", "Lee Alex"
    ],
    "English Interpretation": [
        "The person's surname", "The person's given names", "Name in Chinese characters", "Sex (M/F)", 
        "Date of birth", "Nationality", "Previous residence", "New residence", 
        "Telephone number", "Foreigner registration number", "Date of registration", 
        "Full name of dependent", "Relation to applicant", "Date of report", "Applicant's signature"
    ]
}

# DataFrame 생성
    df = pd.DataFrame(data)

# Streamlit 앱 표시
    st.title("Extracted and Filled Text with English Interpretation😊")
    st.write("\n")

    st.table(df)  # 고정된 표 형식으로 표시

# 지정된 두 개의 이미지 파일 로드 및 표시
    image_files = ["pdf_documents/체류지변경신고서1.png", "pdf_documents/체류지변경신고서2.png"]

# 이미지 파일을 Streamlit에 표시
    for image_file in image_files:
        if os.path.exists(image_file):
            st.image(image_file)
        else:
            st.write(f"Image {image_file} not found.")

    if st.button("Submit"):
        st.success("Submission sucessful!")
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
            st.markdown("[You can download the form here: [Foreign Residence Change Form]](https://www.hygn.go.kr/00428/00435/00501.web)")
    elif choice == "Fill out the form in Korean":
        show_korean_form()      
                    
    else:  # PDF 문서 열기
        if st.button("PDF VIEW"):
            # PDF URL을 여기에 입력하세요
            pdf_url = "https://lumpy-bovid-b54.notion.site/pdf-132b4c6b88db803b9cffe221fe0c736c?pvs=4"
            
            st.markdown(f"[Go to PDF]({pdf_url})")      
    
    # 메인 페이지로 돌아가기 버튼
    if st.button("Back to main"):
        go_to_main()

# 메인 앱 로직
def main():
    if st.session_state.page == 'main':
        main_page()
    elif st.session_state.page == 'second':
        second_page()

if __name__ == "__main__":
    main()