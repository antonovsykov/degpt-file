from langchain_community.document_loaders import UnstructuredWordDocumentLoader
import subprocess
import zipfile
import base64
import os
import concurrent.futures

class WordUtils:
    def doc_tran_docx(self, file_path: str):
        # 不是使用默认安装需指定soffice路径
        soffice = "D:\ProgramFile\Liberoffice\program\soffice.exe"
        # soffice = "soffice"
        # 生成目标路径（同一目录）
        doc_path = os.path.abspath(file_path)
        output_dir = os.path.dirname(file_path)
        # LibreOffice 命令行参数
        command = [
            soffice,
            "--headless",          # 无界面模式
            "--convert-to", "docx",# 目标格式
            "--outdir", output_dir,# 输出目录
            doc_path               # 输入文件
        ]
        try:
            # 执行命令
            subprocess.run(command, check=True)
            print(f"转换成功: {os.path.splitext(doc_path)[0]}.docx")
            return f"{os.path.splitext(doc_path)[0]}.docx"
        except subprocess.CalledProcessError as e:
            print(f"转换失败: {e}")
            return None
        
    def rtf_tran_docx(self, file_path: str):
        # 不是使用默认安装需指定soffice路径
        soffice = "D:\ProgramFile\Liberoffice\program\soffice.exe"
        # soffice = "soffice"
        # 生成目标路径（同一目录）
        doc_path = os.path.abspath(file_path)
        output_dir = os.path.dirname(file_path)
        # LibreOffice 命令行参数
        command = [
            soffice,
            "--headless",          # 无界面模式
            "--convert-to", "docx",# 目标格式
            "--outdir", output_dir,# 输出目录
            doc_path               # 输入文件
        ]
        try:
            # 执行命令
            subprocess.run(command, check=True)
            print(f"转换成功: {os.path.splitext(doc_path)[0]}.docx")
            return f"{os.path.splitext(doc_path)[0]}.docx"
        except subprocess.CalledProcessError as e:
            print(f"转换失败: {e}")
            return None
        
    def text_data(self, file_path: str):
        try:
            loader = UnstructuredWordDocumentLoader(file_path)
            data = loader.load()
            return data
        except Exception as e:
            print("============", e)
            return None
        
    def image_data(self, file_path: str):
        image_mime_types = {
            'png': 'image/png',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'gif': 'image/gif',
            'bmp': 'image/bmp',
            'webp': 'image/webp',
            'tiff': 'image/tiff',
        }
        base64_images = []

        def process_image(file_info, index):
            # 读取图片二进制数据
            image_data = docx.read(file_info)

            # 提取文件名和扩展名
            filename = os.path.basename(file_info.filename)
            file_ext = os.path.splitext(filename)[1].lower().strip('.')

            # 获取对应的MIME类型，默认使用'application/octet-stream'
            mime_type = image_mime_types.get(file_ext, 'application/octet-stream')

            # 转换为Base64字符串
            base64_str = base64.b64encode(image_data).decode('utf-8')

            # 组合成完整的数据URI
            data_uri = f'data:{mime_type};base64,{base64_str}'

            def verify_base64_image(base64_str):
                # 去除可能存在的前缀
                if base64_str.startswith('data:image'):
                    # 找到逗号位置，截取逗号之后的部分
                    comma_index = base64_str.find(',')
                    if comma_index != -1:
                        return True
                return False

            if verify_base64_image(data_uri):
                return {"page": index, "img": data_uri}
            return None

        with zipfile.ZipFile(file_path, 'r') as docx:
            # 遍历zip内的所有文件
            image_files = [file_info for file_info in docx.infolist() if file_info.filename.startswith('word/media/')]
            with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                results = executor.map(process_image, image_files, range(len(image_files)))
                for result in results:
                    if result:
                        base64_images.append(result)

        return base64_images
    
WordUtilInstance = WordUtils()