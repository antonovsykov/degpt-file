from langchain_community.document_loaders import TextLoader

class TxtUtils:
        
    def text_data(self, file_path: str):
        try:
            loader = TextLoader(file_path, autodetect_encoding=True)
            data = loader.load()
            return data
        except Exception as e:
            print("============", e)
            return None
    
TxtUtilInstance = TxtUtils()