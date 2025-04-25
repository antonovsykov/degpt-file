from fastapi import File, UploadFile
from datetime import datetime
from config import DATA_DIR
import uuid
import os
import base64
from PIL import Image
from io import BytesIO
import shutil

# 定义文件上传文件夹并创建
UPLOAD_DIR = f"{DATA_DIR}/uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

class FileUtil:
    def contain_ext(self):
        know_program_ext = [
            "html",
            "htm",
            "css",
            "ts",
            "js",
            "cpp",
            "asp",
            "aspx",
            "config",
            "sql",
            "plsql",
            "py",
            "go",
            "php",
            "vue",
            "java",
            "c",
            "cs",
            "h",
            "hsc",
            "bash",
            "swift",
            "svelte",
            "env",
            "r",
            "lua",
            "m",
            "mm",
            "perl",
            "rb",
            "rs",
            "db2",
            "scala",
            "dockerfile",
            "yml"
        ]
        return know_program_ext
    
    # 校验文件后缀名
    def check_ext(self, filename: str):
        file_ext = filename.split(".")[-1].lower()
        known_type = False
        anaylis_type = "file"
        known_file_ext = [
            "pdf",
            "ppt",
            "pptx",
            "doc",
            "docx",
            "rtf",
            "xls",
            "xlsx",
            "csv",
            "txt",
            "log",
            "xml",
            "ini",
            "json",
            "md"
        ]
        
        if file_ext in known_file_ext:
            anaylis_type = "file"
            known_type = True
        elif file_ext in self.contain_ext():
            anaylis_type = "progrem"
            known_type = True

        return file_ext, known_type, anaylis_type
    
    # 将文件内容保存到本地
    def save_file(self, file_ext: str, file: UploadFile = File(...)):
        # 获取当前日期时间
        current_date = datetime.now()
        # 格式化为年月日字符串（示例输出：2023-10-05）
        date_str = current_date.strftime("%Y-%m-%d")
        file_dir = f"{UPLOAD_DIR}/{date_str}"
        # 创建文件夹
        os.makedirs(file_dir, exist_ok=True)
        
        file_path = f"{file_dir}/{str(uuid.uuid4())}.{file_ext}"
        contents = file.file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
            f.close()
        return file_path
    
    # 删除文件
    def remove_file(self, file_path: str):
        if os.path.exists(file_path):
            os.remove(file_path)
           
    # 删除文件夹
    def remove_folder(self, folder_path: str):
        try:
            # 检查文件夹是否存在
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
        except Exception as e:
            print(f"删除文件夹时出现错误: {e}")

    # 合并base64图片为一张图片
    def merge_base64_images(self, base64_list, direction='horizontal',size=600, spacing=10, bg_color=(255, 255, 255)):
        try:
            # 将 Base64 转换为 PIL 图片对象列表
            images = []
            for b64Obj in base64_list:
                b64 = b64Obj["img"]
                # 清理前缀 (如 data:image/png;base64)
                if "," in b64:
                    b64 = b64.split(",", 1)[1]
                
                img_data = base64.b64decode(b64)
                img = Image.open(BytesIO(img_data)).convert("RGBA")
                images.append(img)

            # 统一尺寸 (取最小尺寸)
            if direction == 'horizontal':
                # 横向拼接：统一高度
                min_height = size
                resized_images = [img.resize((int(img.width * min_height / img.height), min_height)) 
                                for img in images]
                widths = [img.width for img in resized_images]
                total_width = sum(widths) + spacing * (len(images) - 1)
                max_height = min_height
            else:
                # 纵向拼接：统一宽度
                # min_width = min(img.width for img in images)
                min_width = size
                resized_images = [img.resize((min_width, int(img.height * min_width / img.width))) 
                                for img in images]
                heights = [img.height for img in resized_images]
                total_height = sum(heights) + spacing * (len(images) - 1)
                max_width = min_width

            # 创建画布
            if direction == 'horizontal':
                canvas = Image.new('RGB', (total_width, max_height), bg_color)
                x_offset = 0
                for img in resized_images:
                    canvas.paste(img, (x_offset, 0), mask=img.split()[3] if img.mode == 'RGBA' else None)
                    x_offset += img.width + spacing
            else:
                canvas = Image.new('RGB', (max_width, total_height), bg_color)
                y_offset = 0
                for img in resized_images:
                    canvas.paste(img, (0, y_offset), mask=img.split()[3] if img.mode == 'RGBA' else None)
                    y_offset += img.height + spacing

            # 转换为 Base64
            buffered = BytesIO()
            canvas.save(buffered, format="PNG")  # 可选 JPG
            img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
            
            # 添加前缀标识
            return f"data:image/png;base64,{img_base64}"
        except Exception as e:
            raise ValueError(f"图片合成失败: {str(e)}")
    

FileUtilInstance = FileUtil()