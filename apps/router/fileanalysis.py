from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from typing import Optional
import os

from apps.utils.fileutils import FileUtilInstance
from apps.utils.pdfutils import PdfUtilInstance
from apps.utils.wordutils import WordUtilInstance
from apps.utils.pptutils import PptUtilInstance
from apps.utils.excelutils import ExcelUtilInstance
from apps.utils.csvutils import SafeCSVLoader
from apps.utils.txtutils import TxtUtilInstance
from apps.utils.mdutils import MdUtilsInstance
from apps.utils.xmlutils import XmlUtilInstance
from apps.utils.compressutils import CompressUtilInstance
from apps.utils.captionutils import CaptionUtilInstance
from apps.utils.ossutils import OssUtilInstance
from apps.models.caption_info import CaptionBase64Req

from datetime import datetime

router = APIRouter()

files_count = 100

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
            print("=============pdf读取文字开始================", datetime.now())
            text_data = PdfUtilInstance.text_data(pdf_path)
            print("=============pdf读取文字结束================", datetime.now())
            result["text"] = text_data
            image_data = PdfUtilInstance.image_data(pdf_path)
            if len(image_data) > 0:
                image_list = sorted(image_data, key=lambda x: x["page"])
                print("=============pdf合并图片开始================", datetime.now())
                marge_base64 = FileUtilInstance.merge_base64_images(image_list, 'vertical', 1000)
                print("=============pdf合并图片结束================", datetime.now())
                # 获取图片描述
                base_dir = FileUtilInstance.base64_to_image(marge_base64)
                languages = "ch"
                print("=============pdf读取图片信息开始================", datetime.now())
                text = CaptionUtilInstance.extract_text3(base_dir, languages)
                desc = CaptionUtilInstance.generate_scene_description(base_dir)
                print("=============pdf读取图片信息结束================", datetime.now())
                result["text"].append({"page_content": text})
                result["text"].append({"page_content": desc})
                # 删除本地文件
                FileUtilInstance.remove_file(base_dir)
                # oss_url = OssUtilInstance.upload_base64_to_oss(marge_base64)
                # result["image"].append(oss_url)
            
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

                # 获取图片描述
                base_dir = FileUtilInstance.base64_to_image(marge_base64)
                languages = "ch"
                text = CaptionUtilInstance.extract_text3(base_dir, languages)
                desc = CaptionUtilInstance.generate_scene_description(base_dir)
                result["text"].append({"page_content": text})
                result["text"].append({"page_content": desc})
                # 删除本地文件
                FileUtilInstance.remove_file(base_dir)

                # oss_url = OssUtilInstance.upload_base64_to_oss(marge_base64)
                # result["image"].append(oss_url)

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

        elif file_ext in ["zip", "rar"]:
            zip_count = CompressUtilInstance.count_files(file_path, file_ext)
            if zip_count > files_count:
                raise HTTPException(status_code=400, detail="The number of files in the compressed file should not exceed 100")
            CompressUtilInstance.uncompose_file(file_path, file_ext)

        elif file_ext in FileUtilInstance.contain_ext():
            text_data = TxtUtilInstance.text_data(file_path)
            result["text"] = text_data

        # 删除本地文件
        FileUtilInstance.remove_file(file_path)
        return result
    except Exception as e:
        FileUtilInstance.remove_file(file_path)
        raise HTTPException(status_code=400, detail=e.detail)

@router.post("/upload")
def store_doc(
    collection_name: Optional[str] = Form(None),
    file: UploadFile = File(...),
):
    result = {
        "collection_name": "",
        "known_type": False,
        "anaylis_type": "file",
        "url": ""
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

        # 根据文件上传阿里OSS
        oss_path = OssUtilInstance.upload_file_to_oss(file_path, file_ext)
        result["url"] = oss_path

        # 删除本地文件
        FileUtilInstance.remove_file(file_path)
        return result
    except Exception as e:
        FileUtilInstance.remove_file(file_path)
        raise HTTPException(status_code=400, detail=e.detail)

@router.get("/aichat")
def ai_chat():
    CompressUtilInstance.generate_aichat("")

@router.post("/caption/info")
def caption_info(captioninfo: CaptionBase64Req):
    base_dir = FileUtilInstance.base64_to_image(captioninfo.base64str)
    languages = ['en', 'ch_sim']
    #text = CaptionUtilInstance.extract_text(base_dir, languages)
    text = CaptionUtilInstance.extract_text3(base_dir, "ch")
    desc = CaptionUtilInstance.generate_scene_description(base_dir)
    # 删除本地文件
    FileUtilInstance.remove_file(base_dir)
    return {"text": text, "desc": desc}

@router.post("/caption/info2")
def caption_info(captioninfo: CaptionBase64Req):
    base_dir = FileUtilInstance.base64_to_image(captioninfo.base64str)
    languages = "chi_sim"
    text = CaptionUtilInstance.extract_text2(base_dir, languages)
    desc = CaptionUtilInstance.generate_scene_description(base_dir)
    # 删除本地文件
    FileUtilInstance.remove_file(base_dir)
    return {"text": text, "desc": desc}
    