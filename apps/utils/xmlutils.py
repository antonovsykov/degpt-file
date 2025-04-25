from langchain_community.document_loaders import UnstructuredXMLLoader

class XmlUtils:
        
    def text_data(self, file_path: str):
        try:
            loader = UnstructuredXMLLoader(file_path)
            data = loader.load()
            return data
        except Exception as e:
            print("============", e)
            return None
    
XmlUtilInstance = XmlUtils()