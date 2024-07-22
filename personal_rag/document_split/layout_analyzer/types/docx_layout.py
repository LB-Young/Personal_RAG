from collections import deque
from personal_rag.document_split.utils.analyzer_helper import process_page, judge_cur_slice, make_SliceSchema, get_type_rank

kBlockLow = 400 
kBlockHigh = 600

class DocxLayout:
    def __init__(self):
        self.extractor_slices = None
        self.analyzer_slcies = None
        self.layout_slices = None

    def analize(self, extractor_slices):
        self.extractor_slices = extractor_slices
        self.merge_analysis()
        self.layout_analysis()
        return self.layout_slices
    
    def merge_analysis(self):
        segment_index = 0
        analyzer_slices = []
        past_pages = []
        past_type = "start"
        cur_slice = ""
        for index, obj in enumerate(self.extractor_slices):
            if past_type == "start":
                cur_slice += obj['content'] + "\n"
                past_type = obj['paragraph_type']
                past_pages = process_page(past_pages, obj['pages'])
            elif len(set(obj['content'])) <=1 and " " in obj['content']:
                continue
            elif obj['type'] == "table" and ("表标题" in past_type or judge_cur_slice(cur_slice)):
                cur_slice += obj['content'] + "\n"
                past_pages = process_page(past_pages, obj['pages'])
            elif "toc" in obj['paragraph_type'] or '列项' in obj['paragraph_type'] or "List" in obj['paragraph_type'] or "其他" in obj['paragraph_type'] or "封面" in obj['paragraph_type']:
                cur_slice += obj['content'] + "\n"
                past_pages = process_page(past_pages, obj['pages'])  
            elif "标识" in obj['paragraph_type']:
                cur_slice_schema = make_SliceSchema(past_type=past_type, cur_slices=cur_slice, segment_index=segment_index, pages=past_pages)
                analyzer_slices.append(cur_slice_schema)
                segment_index += 1
                past_type = "start"
                cur_slice = obj['content'] + "\n"
                past_pages = process_page(past_pages, obj['pages'])  
            elif obj['paragraph_type'] != past_type:
                cur_slice_schema = make_SliceSchema(past_type=past_type, cur_slices=cur_slice, segment_index=segment_index, pages=past_pages)
                analyzer_slices.append(cur_slice_schema)
                segment_index += 1
                past_type = obj['paragraph_type']
                cur_slice = obj['content'] + "\n"
                past_pages = process_page(past_pages, obj['pages'])  
            else:
                if len(set(cur_slice)) > 1:
                    len_cur_slice = len(cur_slice)
                    start = 0
                    if "表标题" in past_type:
                        cur_slice_schema = make_SliceSchema(past_type=past_type, cur_slices=cur_slice[start:], segment_index=segment_index, pages=past_pages)
                        analyzer_slices.append(cur_slice_schema)
                        segment_index += 1
                    else:
                        tmp_end_index = -1
                        while len_cur_slice - start > kBlockHigh:
                            try:
                                tmp_end_index = cur_slice.find("。", start, start + kBlockLow)
                            except:
                                pass
                            if tmp_end_index == -1:
                                tmp_end_index = start + kBlockLow
                            cur_slice_schema = make_SliceSchema(past_type=past_type, cur_slices=cur_slice[start:tmp_end_index+1], segment_index=segment_index, pages=past_pages)
                            analyzer_slices.append(cur_slice_schema)
                            start += tmp_end_index+1
                            segment_index += 1
                        cur_slice_schema = make_SliceSchema(past_type=past_type, cur_slices=cur_slice[start:], segment_index=segment_index, pages=past_pages)
                        analyzer_slices.append(cur_slice_schema)
                        segment_index += 1
                else:
                    pass
                past_type = obj['paragraph_type']
                cur_slice = obj['content'] + "\n"  
                past_pages = process_page(past_pages, obj['pages'])  
            
        self.analyzer_slcies = analyzer_slices

    def layout_analysis(self):
        layout_slices = []
        analizer_slices = self.analyzer_slcies
        tree_deque = deque()
        # print("tree_deque.__len__()", tree_deque.__len__())
        past_type_rank = 21
        for item in analizer_slices:
            cur_type_rank = get_type_rank(item['slice_detail_type'])
            if tree_deque.__len__() == 0:
                item['superior_id'] = None
                item['subordinate_ids'] = []
                tree_deque.append(item)
            else:
                if cur_type_rank > past_type_rank:
                    tree_deque[-1]['subordinate_ids'].append(item['id'])
                    item['superior_id'] = tree_deque[-1]['id']
                    item['subordinate_ids'] = []
                    tree_deque.append(item)
                else:
                    while tree_deque.__len__() != 0 and cur_type_rank <= get_type_rank(tree_deque[-1]['slice_detail_type']):
                        layout_slices.append(tree_deque.pop())
                    if tree_deque.__len__() != 0:
                        tree_deque[-1]['subordinate_ids'].append(item['id'])
                        item['superior_id'] = tree_deque[-1]['id']
                        item['subordinate_ids'] = []
                        tree_deque.append(item)
                    else:
                        item['superior_id'] = None
                        item['subordinate_ids'] = []
                        tree_deque.append(item)
            past_type_rank = cur_type_rank
        while tree_deque.__len__() != 0:
            layout_slices.append(tree_deque.pop())
        
        # print("len(layout_slices)", len(layout_slices))
        self.layout_slices = layout_slices