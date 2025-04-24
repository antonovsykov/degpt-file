from langchain_community.document_loaders import UnstructuredPowerPointLoader
import subprocess
import os

class PptUtils:
    def tran_pdf(self, file_path: str):
        # 不是使用默认安装需指定soffice路径
        # soffice = "D:\ProgramFile\Liberoffice\program\soffice.exe"
        soffice = "soffice"
        # 生成目标路径（同一目录）
        doc_path = os.path.abspath(file_path)
        output_dir = os.path.dirname(file_path)
        # LibreOffice 命令行参数
        command = [
            soffice,
            "--headless",           # 无界面模式
            "--convert-to", "pdf",  # 目标格式
            "--outdir", output_dir, # 输出目录
            doc_path                # 输入文件
        ]
        try:
            # 执行命令
            subprocess.run(command, check=True)
            return f"{os.path.splitext(doc_path)[0]}.pdf"
        except subprocess.CalledProcessError as e:
            print(f"转换失败: {e}")
            return None
        
    def text_data(self, file_path: str):
        try:
            loader = UnstructuredPowerPointLoader(file_path)
            data = loader.load()
            return data
        except Exception as e:
            print("============", e)
            return None
        
PptUtilInstance = PptUtils()