import fitz  # PyMuPDF
import pandas as pd
import streamlit as st
import os

# PDF 파일 경로 설정
pdf_files = {
    "외국인 체류지변경 신고서": "pdf_documents/외국인_체류지변경_신고서.pdf"
}
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



# 고정된 표 형식으로도 표시

st.table(df)  # 고정된 표 형식으로 표시

# 지정된 두 개의 이미지 파일 로드 및 표시
image_files = ["pdf_documents/체류지변경신고서1.png", "pdf_documents/체류지변경신고서2.png"]

# 이미지 파일을 Streamlit에 표시
st.title("Loaded Images from pdf_documents Folder")
for image_file in image_files:
    if os.path.exists(image_file):
        st.image(image_file, caption=os.path.basename(image_file))
    else:
        st.write(f"Image {image_file} not found.")