from collections import deque
from personal_rag.document_split.utils.analyzer_helper import process_page, judge_cur_slice, make_SliceSchema, get_type_rank, judge_title_base_on_number
from personal_rag.document_split.utils.extractor_helper import get_line_hight

MinWindowSize=400
MaxWindowSize=600
end_pum = ["。" , "！"]
other_end_pum = ["。" , "！", "，", "；"]
class PDFLayout():
    def __init__(self):
        pass

    def analize(self, extractor_slices):
        self.extractor_slices = extractor_slices
        self.merge_analysis()
        self.layout_analysis()
        return self.layout_slices

    def merge_analysis(self):
        segment_index = 0
        analizer_slices = []
        past_pages = []
        past_location = []
        past_type = "paragraph"
        past_txt_type = 0
        past_txt_type_anchored = 12
        cur_slices = ""
        # line_hight = get_line_hight()
        for index, obj in enumerate(self.extractor_slices):
            if obj['type'] != "paragraph" and obj['type'] != "title" :
                if index >= 1 and self.extractor_slices[index-1]['type'] == "paragraph":
                    cur_slices =  "##" + self.extractor_slices[index-1]['content'].strip() + "## " + obj['content']
                    cur_slice_schema = make_SliceSchema(past_type=obj['type'], cur_slices=cur_slices, segment_index=segment_index, pages=obj['pages'], location=obj['location'], past_txt_type=obj['text_type'])
                    analizer_slices.append(cur_slice_schema)
                    past_pages, past_location = [], []
                    segment_index += 1
                elif index < len(self.extractor_slices) - 1 and self.extractor_slices[index+1]['type'] == "paragraph":
                    cur_slices =  "##" + self.extractor_slices[index+1]['content'].strip() + "## " + obj['content']
                    cur_slice_schema = make_SliceSchema(past_type=obj['type'], cur_slices=cur_slices, segment_index=segment_index, pages=obj['pages'], location=obj['location'], past_txt_type=obj['text_type'])
                    analizer_slices.append(cur_slice_schema)
                    past_pages, past_location = [], []
                    segment_index += 1
                else:
                    cur_slices =  obj['content']
                    cur_slice_schema = make_SliceSchema(past_type=obj['type'], cur_slices=cur_slices, segment_index=segment_index, pages=obj['pages'], location=obj['location'], past_txt_type=obj['text_type'])
                    analizer_slices.append(cur_slice_schema)
                    past_pages, past_location = [], []
                    segment_index += 1
            else:
                if len(cur_slices.strip()) == 0:
                    cur_slices += obj['content']
                    past_pages = process_page(past_pages, obj['pages'])
                    past_type, past_txt_type = "paragraph", past_txt_type_anchored
                    continue
                if len(obj['content'].strip()) > 1 and "•" == obj['content'].strip()[0]:
                    # print("=====================")
                    cur_slices += obj['content']
                    past_pages = process_page(past_pages, obj['pages'])
                    past_type, past_txt_type = "paragraph", past_txt_type_anchored
                    continue
                if obj['paragraph_type'] >= 20 and len(obj['content'].strip())<15:
                    cur_slice_schema = make_SliceSchema(past_type="paragraph", cur_slices=cur_slices, segment_index=segment_index, pages=past_pages, location=past_location, past_txt_type=past_txt_type)
                    if len(cur_slice_schema.slice_content) >= 10:
                        analizer_slices.append(cur_slice_schema)
                        segment_index += 1
                    else:
                        pass
                    past_pages, past_location = [], []
                    cur_slices = obj['content'] + ": "
                    past_pages = process_page(past_pages, obj['pages'])
                    past_type, past_txt_type = "paragraph", past_txt_type_anchored
                    continue
                if judge_title_base_on_number(obj['content']):
                    cur_slice_schema = make_SliceSchema(past_type=past_type, cur_slices=cur_slices, segment_index=segment_index, pages=past_pages, location=past_location)
                    analizer_slices.append(cur_slice_schema)
                    segment_index += 1
                    cur_slices = obj['content']
                    past_pages, past_location = [], []
                    past_pages = process_page(past_pages, obj['pages'])
                    past_type, past_txt_type = "title", 20
                    continue
                if len(cur_slices.strip()) < MinWindowSize:
                    cur_slices += obj['content']
                    past_pages = process_page(past_pages, obj['pages'])
                    past_type, past_txt_type = "paragraph", past_txt_type_anchored
                elif len(cur_slices.strip()) >= MinWindowSize and len(cur_slices.strip()) < MaxWindowSize-50:
                    if cur_slices.strip()[-1] in end_pum:
                        cur_slice_schema = make_SliceSchema(past_type="paragraph", cur_slices=cur_slices, segment_index=segment_index, pages=past_pages, location=past_location, past_txt_type=past_txt_type)
                        analizer_slices.append(cur_slice_schema)
                        segment_index += 1
                        past_pages, past_location = [], []
                        cur_slices = obj['content']
                        past_pages = process_page(past_pages, obj['pages'])
                        past_type, past_txt_type = "paragraph", past_txt_type_anchored
                    else:
                        cur_slices += obj['content']
                        past_pages = process_page(past_pages, obj['pages'])
                        past_type, past_txt_type = "paragraph", past_txt_type_anchored
                elif len(cur_slices.strip()) >= MaxWindowSize-100 and len(cur_slices.strip()) < MaxWindowSize:
                    if cur_slices.strip()[-1] in other_end_pum:
                        cur_slice_schema = make_SliceSchema(past_type="paragraph", cur_slices=cur_slices, segment_index=segment_index, pages=past_pages, location=past_location, past_txt_type=past_txt_type)
                        analizer_slices.append(cur_slice_schema)
                        segment_index += 1
                        past_pages, past_location = [], []
                        cur_slices = obj['content']
                        past_pages = process_page(past_pages, obj['pages'])
                        past_type, past_txt_type = "paragraph", past_txt_type_anchored
                    else:
                        cur_slices += obj['content']
                        past_pages = process_page(past_pages, obj['pages'])
                        past_type, past_txt_type = "paragraph", past_txt_type_anchored
                else:
                    len_cur_slice = len(cur_slices)
                    start = 0
                    flag = False
                    while len_cur_slice - start > MaxWindowSize:
                        try:
                            tmp_end_index = cur_slices.find("。", start + MinWindowSize, start + MaxWindowSize)
                        except:
                            pass
                        if tmp_end_index == -1:
                            tmp_end_index = start + MinWindowSize
                            flag = True
                        cur_slice_schema = make_SliceSchema(past_type=past_type, cur_slices=cur_slices[start:tmp_end_index+1], segment_index=segment_index, pages=past_pages, location=past_location)
                        analizer_slices.append(cur_slice_schema)
                        if len(past_pages) >= 1:
                            past_pages = [past_pages[-1]]
                        else:
                            past_pages = []
                        if len(past_location) >= 1:
                            past_location = [past_location[-1]]
                        else:
                            past_location = []
                        if flag:
                            start = tmp_end_index - 99
                        else:
                            start = tmp_end_index + 1
                        segment_index += 1

                    cur_slices = cur_slices[start:] + obj['content']
                    past_type = obj['type']
                    past_pages = process_page(past_pages, obj['pages'])

        if len(cur_slices) != 0:
            cur_slice_schema = make_SliceSchema(past_type=past_type, cur_slices=cur_slices, segment_index=segment_index, pages=past_pages, location=past_location, past_txt_type=past_txt_type)
            analizer_slices.append(cur_slice_schema)
        self.analyzer_slcies = analizer_slices

    def layout_analysis(self):
        layout_slices = []
        analizer_slices = self.analyzer_slcies
        tree_deque = deque()
        for item in analizer_slices:
            if tree_deque.__len__() == 0:
                if item['slice_detail_type'] == "table":
                    item['superior_id'] = None
                    item['subordinate_ids'] = []
                    item['slice_type'] = 1
                    layout_slices.append(item)
                else:
                    item['slice_type'] = 1
                    item['superior_id'] = None
                    item['subordinate_ids'] = []
                    tree_deque.append(item)
            else:
                if item['slice_detail_type'] == "image" or item['slice_detail_type'] == "table":
                    tree_deque[-1]['slice_type'] = 1
                    tree_deque[-1]['subordinate_ids'].append(item['id'])
                    item['superior_id'] = tree_deque[-1]['id']
                    item['subordinate_ids'] = []
                    item['slice_type'] = 1
                    layout_slices.append(item)
                else:
                    cur_item_hight = item['slice_hight']
                    if cur_item_hight - tree_deque[-1]['slice_hight'] == -1:
                        cur_item_hight = tree_deque[-1]['slice_hight']
                    if cur_item_hight < tree_deque[-1]['slice_hight']:
                        tree_deque[-1]['slice_type'] = 1
                        tree_deque[-1]['subordinate_ids'].append(item['id'])
                        item['superior_id'] = tree_deque[-1]['id']
                        item['subordinate_ids'] = []
                        tree_deque.append(item)
                    else:
                        while tree_deque.__len__() != 0 and cur_item_hight >= tree_deque[-1]['slice_hight']:
                            layout_slices.append(tree_deque.pop())
                        if tree_deque.__len__() != 0:
                            tree_deque[-1]['slice_type'] = 1
                            tree_deque[-1]['subordinate_ids'].append(item['id'])
                            item['superior_id'] = tree_deque[-1]['id']
                            item['subordinate_ids'] = []
                            tree_deque.append(item)
                        else:
                            item['slice_type'] = 1
                            item['superior_id'] = None
                            item['subordinate_ids'] = []
                            tree_deque.append(item)
        while tree_deque.__len__() != 0:
            cur_pop = tree_deque.pop()
            cur_pop['slice_type'] = 1
            layout_slices.append(cur_pop)
        # document.layout_slices = layout_slices
        try:
            self.layout_slices = layout_slices = sorted(layout_slices, key=lambda x: (x['pages'][:1], x['location'][0][1]))
        except:
            self.layout_slices = layout_slices = layout_slices
        return
