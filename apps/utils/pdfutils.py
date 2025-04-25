from langchain_community.document_loaders import PyPDFLoader
import fitz
import base64
import concurrent.futures
from datetime import datetime

class PdfUtils:
    def text_data(self, file_path: str):
        try:
            loader = PyPDFLoader(file_path)
            data = loader.load()
            return data
        except Exception as e:
            print("============", e)
            return None
        
    def image_data(self, file_path: str, dpi=20):
        base64_images = []
        try:
            doc = fitz.open(file_path)

            def process_page(page_num):
                page = doc.load_page(page_num)
                pix = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))
                img_bytes = pix.tobytes()
                img_base64 = base64.b64encode(img_bytes).decode("utf-8")
                return {"page": page_num, "img": img_base64}
            
            print("=============pdf读取图片开始================", datetime.now())
            with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                futures = [executor.submit(process_page, page_num) for page_num in range(len(doc))]
                for future in concurrent.futures.as_completed(futures):
                    base64_images.append(future.result())
            print("=============pdf读取图片结束================", datetime.now())
            doc.close()
        except Exception as e:
            print("==================", e)
        return base64_images
        
PdfUtilInstance = PdfUtils()