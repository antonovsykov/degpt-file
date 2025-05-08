from config import DATA_DIR
from datetime import datetime
import requests
import zipfile
import rarfile
import os

UNCOMPRESS_DIR = f"{DATA_DIR}/uploads"

class CompressUtils:

    # 计算文件数量 
    def count_files(self, file_path, file_ext):
        try:
            if file_ext == "zip":
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    file_count = 0
                    for file_info in zip_ref.infolist():
                        # 若文件名不以 / 结尾，表明它是文件而非文件夹
                        if not file_info.filename.endswith('/'):
                            file_count = file_count + 1
                    return file_count
            elif file_ext == "rar":
                # 创建 RarFile 对象
                rf = rarfile.RarFile(file_path)
                file_count = 0
                # 遍历 RAR 文件中的所有文件信息
                for file_info in rf.infolist():
                    # 若不是文件夹，则文件数量加 1
                    if not file_info.isdir():
                        file_count = file_count + 1
                # 关闭 RarFile 对象
                rf.close()
                return file_count
        except FileNotFoundError:
            print("错误: 文件未找到!")
        except Exception as e:
            print(f"错误: 发生了一个未知错误: {e}")
        return None
    
    # 解压文件
    def uncompose_file(self, file_path, file_ext):
        file_name = os.path.basename(file_path)
        # 格式化为年月日字符串（示例输出：2023-10-05）
        current_date = datetime.now()
        date_str = current_date.strftime("%Y-%m-%d")
        # 再去除文件后缀
        file_name_without_ext = os.path.splitext(file_name)[0]
        uncompress_dri = f'{UNCOMPRESS_DIR}/{date_str}/{file_name_without_ext}'
        # 创建文件夹
        os.makedirs(uncompress_dri, exist_ok=True)
        try:
            if file_ext == "zip":
                # 打开 ZIP 文件
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    for info in zip_ref.infolist():
                        # 尝试使用不同编码解码文件名
                        try:
                            info.filename = info.filename.encode('cp437').decode('gbk')
                        except UnicodeDecodeError:
                            pass
                        zip_ref.extract(info, uncompress_dri)
            elif file_ext == "rar":
                rarfile.UNRAR_TOOL = r"D:\ITSoft\tool\UnRAR.exe"
                # 打开 RAR 文件
                with rarfile.RarFile(file_path) as rf:
                    # 解压文件到指定路径
                    rf.extractall(uncompress_dri)
            return True
        except Exception as e:
            print(f"错误: 发生了一个未知错误: {e}")
        return False
    
    # 模型回复后台处理
    def conversation_file(self, file_path, prompt):
        return True
    
    # 调用模型
    def generate_aichat(self, data):
        try:
            url = "https://korea-chat.degpt.ai/api/v0/chat/completion/proxy"
            data = {
                "model": "QwQ-32B",
                "messages": [
                    {
                        "role": "user",
                        "content": "美食分享"
                    }
                ],
                "project": "DecentralGPT",
                "stream": False
            }
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, headers, data)
            response.raise_for_status()  # 自动检查状态码
            result = response.json()
            print("请求成功，数据:", result)
        except Exception as e:
            print(e)

CompressUtilInstance = CompressUtils()