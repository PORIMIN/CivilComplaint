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