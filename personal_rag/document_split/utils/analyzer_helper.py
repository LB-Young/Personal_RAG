import uuid
import hashlib


def process_page(past_pages, cur_pages):
    if cur_pages[0] in past_pages:
        return past_pages
    else:
        past_pages.extend(cur_pages)
        return past_pages
    

table_presentation_words = ['表','示','如下']
def judge_cur_slice(cur_slice):
    for item in table_presentation_words:
        if item in cur_slice:
            return True
    return False


def get_slice_type(string, past_txt_type):
    if past_txt_type > 12:
        return 1
    # try:
    #     if past_txt_type > min_hight:
    #         return 0
    # except:
    #     pass
    if "表标题" in string or "table" in string:
        return 2
    elif "图表题" in string or "image" in string:
        return 3
    elif "标题" in string:
        return 0
    elif "段" in string or "paragraph" in string:
        return 1
    else:
        return 4
    

def post_process(text):
    text = text.replace("\uf0d8 \n", "·").replace("\uf0d8", "·").replace("\uf06c", "+").replace("\uf0a7"," + ").replace("\u2002"," ").replace("\u2003"," ").replace("\u200b"," ").replace("\n\n", "\n")
    return text


def get_md5(string):
    md5_machine = hashlib.md5()
    md5_machine.update(str(string).encode("utf-8"))
    return md5_machine.hexdigest()


def make_SliceSchema(past_type, cur_slices, segment_index, pages=[0], location=[0,0,0,0], past_txt_type=-1):
    cur_slice_schema = {}
    cur_slice_schema['slice_detail_type']=past_type
    cur_slice_schema['slice_hight'] = past_txt_type
    cur_slice_schema['slice_type'] = get_slice_type(past_type, past_txt_type)
    cur_slice_schema['slice_content']=post_process(cur_slices)
    cur_slice_schema['pages'] = pages
    cur_slice_schema['location'] = location
    cur_slice_schema['segment_id'] = segment_index
    cur_slice_schema['id'] = str(uuid.uuid4())
    cur_slice_schema['slice_md5'] = get_md5(cur_slice_schema['slice_content'])
    return cur_slice_schema

title_rank = {
    "目次":2,
    "前言":2,
    "引言":2,
    "附录内容":2,
    "章标题":2,
    "一级":3,
    "二级":4,
    "三级":5,
    "四级":6,
    "五级":7,
    "六级":8,
    "七级":9,
    "八级":10,
    "九级":11,
    "Heading 1":2,
    "Heading 2":3,
    "Heading 3":4,
    "Heading 4":5,
    "Heading 5":6,
    "Heading 6":7,
    "Heading 7":8,
    "Heading 8":9,
    "Heading 9":10,
    "Title":3,
    "Subtitle":4,
    "段":12,
    "正文表标题":12,
    "表标题":12,
}
def get_type_rank(slice_detail_type):
    for key in title_rank.keys():
        if key in slice_detail_type:
            return title_rank[key]
    return 20


tmp_list = list("一二三四五六七八九十")
list_1_to_10 = [f"{item} " for item in tmp_list] + [f"{item}、" for item in tmp_list]
list_1_to_10_parentheses = [f"({item})" for item in tmp_list] + [f"（{item}）" for item in tmp_list]
list_1_to_10_segment = [f"第{item}章" for item in tmp_list] + [f"第{item}节" for item in tmp_list]
title_start_num_list = list_1_to_10 + list_1_to_10_parentheses + list_1_to_10_segment
def judge_title_base_on_number(content_text):
    for num_item in title_start_num_list:
        if content_text.strip().startswith(num_item):
            return True
    return False