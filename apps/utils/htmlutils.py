from langchain_community.document_loaders import BSHTMLLoader

class HtmlUtils:
        
    def text_data(self, file_path: str):
        try:
            loader = BSHTMLLoader(file_path, open_encoding="unicode_escape")
            data = loader.load()
            return data
        except Exception as e:
            print("============", e)
            return None
    
HtmlUtilInstance = HtmlUtils()