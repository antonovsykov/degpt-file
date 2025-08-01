import easyocr
from ultralytics import YOLO
import pytesseract
from paddleocr import PaddleOCR
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
from transformers import pipeline
import torch
from PIL import Image
import base64
import io


# 加载预训练模型和工具
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

# 设置生成参数
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
max_length = 100  # 生成文本的最大长度
num_beams = 4    # 控制生成多样性

# 加载图像描述生成模型（BLIP）
image_captioner = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")

class CaptionUtils:

    # 加载图片中得文本-easyocr
    def extract_text(self, image_path, languages):
        try:
            reader = easyocr.Reader(languages)
            # 文本识别
            result_easy = reader.readtext(image_path, beamWidth=10, text_threshold=0.5)
            text_easy = " ".join([res[1] for res in result_easy])
            return text_easy
        except Exception as e:
            print(f'发生错误: {e}')
            return None
        
    # 加载图片中得文本-pytesseract
    def extract_text2(self, image_path, languages):
        try:
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            # 加载图像
            image = Image.open(image_path)
            # 文本识别
            text = pytesseract.image_to_string(image, lang=languages, config='--psm 6')
            return text
        except Exception as e:
            print(f'发生错误: {e}')
            return None
        
    # 加载图片中得文本-paddleocr
    def extract_text3(self, image_path, language):
        try:
            # PaddleOCR（中文+英文）
            ocr_paddle = PaddleOCR(use_angle_cls=True, lang=language, use_gpu=True)
            # 加载图像
            result_paddle = ocr_paddle.ocr(image_path, cls=True)
            # 处理PaddleOCR 2.10.0的双层列表结构
            text_paddle = " ".join([line[1][0] for line in result_paddle[0]])
            return text_paddle
        except Exception as e:
            print(f'发生错误: {e}')
            return None
    
    # 检测物体
    def detect_objects(self, image_path):
        model = YOLO("yolov8n.pt")  # 加载预训练模型
        results = model(image_path)
        detections = []
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                class_name = result.names[class_id]
                detections.append({"物体类别": class_name, "置信度": float(box.conf[0])})
        return detections

    # 加载图片并生成描述
    def generate_caption_desc(self, image_path):
        image = Image.open(image_path)
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        # 预处理图像并生成特征
        pixel_values = feature_extractor(images=image, return_tensors="pt").pixel_values.to(device)
        
        # 生成文字描述
        output_ids = model.generate(
            pixel_values,
            max_length=max_length,
            num_beams=num_beams,
            early_stopping=True
        )
        
        caption = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return caption
    
    # 生成描述（自动识别场景元素）
    def generate_scene_description(self, image_path):
        result = image_captioner(image_path)
        return result[0]['generated_text']
    
CaptionUtilInstance = CaptionUtils()