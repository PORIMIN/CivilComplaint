import os
import re
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

# 영어 안내 페이지 콘텐츠 함수
def english_page():
    st.title("Foreigner Civil Complaint Assistant - English")
    st.write("This page provides information related to foreigner residence change notifications.")

    # 질문 입력
    query = st.text_input("Enter your question below", "I want to move, what administrative procedures should I follow?")

    # 질문이 특정 내용일 경우 기본 응답을 설정
    default_response = """
    First, you need to report your residence change. The residence change must be reported within 15 days of moving.
    For late reporting, visit the Immigration Office of your new residence area, or you may report at a local government office.
    Required documents:
    1. Residence change notification form
    2. ID: Alien Registration Card
    3. Proof of residence (lease agreement, accommodation receipt, etc.)
    """

    # 질문 버튼
    if st.button("Submit Question"):
        # 'move'와 'residence' 또는 'procedures'와 관련된 특정 표현이 있는지 확인
        if ("move" in query.lower() and "residence" in query.lower()) or re.search(r"\b(residence change|administrative procedures|move to new residence)\b", query.lower()):
            st.write("### Response")
            st.write(default_response)


        else:
            # 일반적인 질문 처리
            selected_file_path = pdf_files.get("외국인 체류지변경 신고서", "파일을 찾을 수 없습니다")
            print(selected_file_path)
            db = prepare_embeddings(selected_file_path)
            retriever = db.as_retriever()

            # 프롬프트 템플릿
            template = """
              Role : You are a PDF file information retrieval AI chat assistant.
              Audience : Foreigners living in Korea who want to submit civil affairs documents.
              Style : Informative, Systematic
              Mission : Your role is to help foreign users retrieve information from PDF file in `Context`.
              Policy : Format the retrieved information as text.
              Output Format : Markdown (No HTML)
              Constraint : Please use only the context for your answers, do not make up any information.
              Example : 
                Query -> "What documents are required for residence change?"
                Expected Output -> "To report a residence change, you need the following documents: 1. Residence change notification form 2. ID: Alien Registration Card 3. Proof of residence (lease agreement, accommodation receipt, etc.)."

              Query : {query}
              Context : {context}
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
            st.write("### Response")
            st.write(response)


# 영어 안내 페이지 렌더링
english_page()