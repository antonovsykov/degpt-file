from langchain_community.document_loaders import UnstructuredExcelLoader

class ExcelUtils:
    def text_data(self, file_path: str):
        try:
            loader = UnstructuredExcelLoader(file_path)
            data = loader.load()
            return data
        except Exception as e:
            print("============", e)
            return None
        
ExcelUtilInstance = ExcelUtils()