def find_top(cur_table, cur_txt):
    cur_list = []
    if cur_table is not None:
        cur_list.append(cur_table)
    if cur_txt is not None:
        cur_list.append(cur_txt)
    sorted_data = sorted(cur_list, key=lambda x:(x['pages'], x['location'][1]))
    return sorted_data[0], sorted_data[0]['type']

line_hight = -2
def set_line_hight(line_hight):
    line_count = 0
    for key, value in line_hight.items():
        if value > line_count:
            line_hight = key

def get_line_hight():
    return line_hight