import os
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

# 임베딩 및 문서 저장 함수
def prepare_embeddings(file_path):
    embeddings = UpstageEmbeddings(
        upstage_api_key=api_key,
        model="solar-embedding-1-large"
    )
    docs = read_dataset(file_path)
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    docs_split = text_splitter.split_documents(docs)
    db = FAISS.from_documents(docs_split, embeddings)
    return db

# 베트남어 안내 페이지 콘텐츠 함수
def vietnamese_page():
    st.title("Trợ Lý Hỗ Trợ Thay Đổi Nơi Cư Trú Cho Người Nước Ngoài - Tiếng Việt")
    st.write("Trang này cung cấp thông tin liên quan đến thủ tục thông báo thay đổi nơi cư trú cho người nước ngoài.")

    # 질문 입력
    query = st.text_input("Nhập câu hỏi của bạn bên dưới", "Ví dụ: Tôi muốn chuyển nhà, thủ tục hành chính tôi cần thực hiện là gì?")

    # 질문이 특정 내용일 경우 기본 응답을 설정
    default_response = """
    Trước tiên, bạn cần thông báo thay đổi nơi cư trú. Thông báo thay đổi nơi cư trú phải được thực hiện trong vòng 15 ngày sau khi chuyển nhà.
    Nếu thông báo trễ, vui lòng đến Văn phòng quản lý xuất nhập cảnh tại khu vực cư trú mới, hoặc có thể thông báo tại văn phòng chính quyền địa phương.
    Tài liệu cần thiết:
    1. Mẫu đơn thông báo thay đổi nơi cư trú
    2. ID: Thẻ đăng ký người nước ngoài
    3. Bằng chứng cư trú (hợp đồng thuê nhà, biên lai chỗ ở, v.v.)
    """

    # 질문 버튼
    if st.button("Gửi câu hỏi"):
        if "move" in query.lower() or "procedures" in query.lower():
            st.write("### Trả lời")
            st.write(default_response)

            # 추가 질문 제공
            follow_up = st.radio(
                "Bạn có muốn xem mẫu đơn thay đổi nơi cư trú bằng tiếng Anh hay điền bằng tiếng Hàn?",
                ("Tôi sẽ tự xử lý; chỉ cần dẫn tôi đến địa chỉ có mẫu đơn.", "Có, điền bằng tiếng Hàn", "Không, cảm ơn")
            )

            # 사용자 선택에 따른 응답
            if follow_up == "Tôi sẽ tự xử lý; chỉ cần dẫn tôi đến địa chỉ có mẫu đơn.":
                st.write("### Mẫu đơn thay đổi nơi cư trú cho người nước ngoài (Tiếng Anh)")
                form_url = "https://www.hygn.go.kr/00428/00435/00501.web"
                st.markdown(f"[Mở mẫu đơn tiếng Anh]({form_url})", unsafe_allow_html=True)

            elif follow_up == "Có, điền bằng tiếng Hàn":
                st.write("### Điền mẫu đơn thay đổi nơi cư trú cho người nước ngoài")
                st.write("Vui lòng tiến hành điền mẫu đơn bằng tiếng Hàn.")

        else:
            # 일반적인 질문 처리
            selected_file_path = pdf_files.get("외국인 체류지변경 신고서", "Không tìm thấy tệp")
            print(selected_file_path)
            db = prepare_embeddings(selected_file_path)
            retriever = db.as_retriever()

            # 프롬프트 템플릿 설정
            template = """
              Bạn là một trợ lý AI hỗ trợ truy xuất thông tin từ tệp PDF. Vui lòng chỉ sử dụng ngữ cảnh để trả lời và không tự bịa thông tin.
              Câu hỏi: {query}
              {context}
            """
            prompt = ChatPromptTemplate.from_template(template)

            # 대화 체인 생성
            model = ChatUpstage()
            chain = (
                {
                    "context": retriever,
                    "query": RunnablePassthrough()
                }
                | prompt | model | StrOutputParser()
            )

            response = chain.invoke(query)
            st.write("### Trả lời")
            st.write(response)

# 베트남어 안내 페이지 렌더링
vietnamese_page()
