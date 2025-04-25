from fastapi import APIRouter, File, UploadFile, Form
from typing import Optional
import os
from datetime import datetime

from apps.utils.fileutils import FileUtilInstance
from apps.utils.ossutils import OssUtilInstance
from apps.utils.pdfutils import PdfUtilInstance
from apps.utils.wordutils import WordUtilInstance
from apps.utils.pptutils import PptUtilInstance
from apps.utils.excelutils import ExcelUtilInstance
from apps.utils.csvutils import SafeCSVLoader
from apps.utils.txtutils import TxtUtilInstance
from apps.utils.mdutils import MdUtilsInstance
from apps.utils.xmlutils import XmlUtilInstance

router = APIRouter()

@router.post("/analysis")
def store_doc(
    collection_name: Optional[str] = Form(None),
    file: UploadFile = File(...),
):
    result = {
        "collection_name": "",
        "known_type": False,
        "anaylis_type": "file",
        "text": "",
        "image": []
    }
    try:
        unsanitized_filename = file.filename
        filename = os.path.basename(unsanitized_filename)
        result["collection_name"] = filename

        # 校验文件是否支持分析
        file_ext, known_type, anaylis_type = FileUtilInstance.check_ext(filename)
        result["known_type"] = known_type
        result["anaylis_type"] = anaylis_type

        # 将文件内容保存到本地
        file_path = FileUtilInstance.save_file(file_ext, file)

        # 根据文件类型加载文件内容
        if file_ext in ["ppt", "pptx", "pdf"]:
            pdf_path = file_path
            if file_ext in ["ppt", "pptx"]:
                pdf_path = PptUtilInstance.tran_pdf(file_path)
            text_data = PdfUtilInstance.text_data(pdf_path)
            result["text"] = text_data
            image_data = PdfUtilInstance.image_data(pdf_path)
            if len(image_data) > 0:
                image_list = sorted(image_data, key=lambda x: x["page"])
                marge_base64 = FileUtilInstance.merge_base64_images(image_list, 'vertical', 600)
                oss_url = OssUtilInstance.upload_base64_to_oss(marge_base64)
                result["image"].append(oss_url)
            
            FileUtilInstance.remove_file(pdf_path)

        elif file_ext in ["doc", "rtf", "docx"]:
            word_path = file_path
            if file_ext == "doc":
                word_path = WordUtilInstance.doc_tran_docx(file_path)
            if file_ext == "rtf":
                word_path = WordUtilInstance.rtf_tran_docx(file_path)

            text_data = WordUtilInstance.text_data(word_path)
            result["text"] = text_data
            image_data = WordUtilInstance.image_data(word_path)
            if len(image_data) > 0:
                image_list = sorted(image_data, key=lambda x: x["page"])
                marge_base64 = FileUtilInstance.merge_base64_images(image_list, 'vertical', 1000)
                oss_url = OssUtilInstance.upload_base64_to_oss(marge_base64)
                result["image"].append(oss_url)
            FileUtilInstance.remove_file(word_path)

        elif file_ext in ["xls", "xlsx"]:
            text_data = ExcelUtilInstance.text_data(file_path)
            result["text"] = text_data

        elif file_ext == "csv":
            csv_loader = SafeCSVLoader(file_path)
            text_data = csv_loader.text_data(file_path)
            result["text"] = text_data

        elif file_ext == "txt":
            text_data = TxtUtilInstance.text_data(file_path)
            result["text"] = text_data

        elif file_ext == "md":
            text_data = MdUtilsInstance.text_data(file_path)
            result["text"] = text_data
        
        elif file_ext == "xml":
            text_data = XmlUtilInstance.text_data(file_path)
            result["text"] = text_data

        elif file_ext in FileUtilInstance.contain_ext():
            text_data = TxtUtilInstance.text_data(file_path)
            result["text"] = text_data

        # 删除本地文件
        FileUtilInstance.remove_file(file_path)

    except Exception as e:
        print("====================", e)
    
    return result