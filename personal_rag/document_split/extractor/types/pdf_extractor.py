import pdfplumber
from personal_rag.document_split.utils.extractor_helper import find_top, set_line_hight

class PDFExtractor:
    def __init__(self):
        pass

    def extract(self, file_path):
        pdf_document = pdfplumber.open(file_path)

        all_slices = []
        all_text_slices = []
        all_table_slices = []
        line_hight = {}
        for page_number, page in enumerate(pdf_document.pages):
            tables = page.extract_tables()
            tables_obj = page.find_tables()
            if len(tables) >= 2:
                for index, table in enumerate(tables):
                    table_data = ""
                    for row in table:
                        row_data = ""
                        for cell in row:
                            if cell:
                                row_data += "|" + cell.replace("\n", " ")
                            else:
                                row_data += "|" + "None"
                        if len(table_data) > 1:
                            table_data += "\n"
                        table += row_data[1:]
                    for item in table_data:
                        if item not in ["[", "]", ",", "'", " "] and len(table_data) > 2 and "|" in item:
                            all_table_slices.append(
                                {
                                    "type":"table",
                                    "content":table_data,
                                    "paragraph_type":"table",
                                    "pages":[page_number+1],
                                    "location":list(tables_obj[index].bbox)
                                }
                            )
                            break
                        else:
                            continue
            else:
                for index, table in enumerate(tables):
                    table_data = ""
                    for row in table:
                        row_data = ""
                        for cell in row:
                            if cell:
                                row_data += "|" + cell.replace("\n", " ")
                            else:
                                row_data += "|" + "None"
                        if len(table_data) > 1:
                            table_data += "\n"
                        table += row_data[1:]
                    for item in table_data:
                        if item not in ["[", "]", ",", "'", " "] and len(table_data) > 2 and "|" in item:
                            all_table_slices.append(
                                {
                                    "type":"table",
                                    "content":table_data,
                                    "paragraph_type":"table",
                                    "pages":[page_number+1],
                                    "location":list(tables_obj.bbox)
                                }
                            )
                            break
                        else:
                            continue
            
            for line in page.extract_words():
                block = [line['x0'], line['top'], line['x0']+line['width'], line['x0']+line['height'], line['text']]
                if len(set(block[4])) > 2:
                    height = int(line['height'])
                    line_hight[height] = line_hight.get(height, 0) + 1
                    if len(block[4]) > 30 and len(block[4].split("\n")) >= 2:
                        height = -1
                    all_text_slices.append(
                        {
                            'type':"paragraph",
                            "content":block[4].strip(),
                            "paragraph_type":height,
                            "pages":[page_number+1],
                            "location":block[4]
                        }
                    )
                else:
                    continue
        
        set_line_hight(line_hight)
        all_slices = self.merge_slices(all_slices, all_table_slices, all_text_slices)
        return all_slices
    
    def merge_slices(self, all_slices, all_table_slices, all_text_slices):
        len_txt = len(all_text_slices)
        len_tables = len(all_table_slices)
        table_index = 0
        txt_index = 0
        while table_index < len_tables or txt_index < len_txt:
            if table_index < len_tables:
                cur_table = all_table_slices[table_index]
            else:
                cur_table = None
            if txt_index < len_txt:
                cur_txt = all_text_slices[txt_index]
            else:
                cur_txt = None
            top_slices, slice_flag = find_top(cur_table, cur_txt)
            all_slices.append(top_slices)
            if slice_flag == "paragraph":
                txt_index += 1
            elif slice_flag == "table":
                table_index += 1
            else:
                txt_index += 1
        return all_slices