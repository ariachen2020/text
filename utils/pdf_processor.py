from PyPDF2 import PdfReader
import io

class PDFProcessor:
    def __init__(self):
        self.supported_types = ['.pdf']
    
    def process_pdf(self, file_content):
        try:
            # 將上傳的文件內容轉換為 BytesIO 對象
            pdf_file = io.BytesIO(file_content)
            
            # 使用 PyPDF2 讀取 PDF
            reader = PdfReader(pdf_file)
            text = ""
            
            # 遍歷所有頁面並提取文本
            for page in reader.pages:
                text += page.extract_text() + "\n"
                
            return text.strip()
            
        except Exception as e:
            raise Exception(f"PDF 處理錯誤: {str(e)}")
    
    def is_supported_file(self, filename):
        return any(filename.lower().endswith(ext) for ext in self.supported_types)

    def process_pdfs(self, files):
        documents = {}
        for file in files:
            if self.is_supported_file(file.name):
                content = file.read()
                text = self.process_pdf(content)
                documents[file.name] = text
        return documents