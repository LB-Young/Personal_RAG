from personal_rag.rag.LLM_step.prompt import Prompt


def slice_merge_prompt(query, slices):
    prompt_all = Prompt()
    prompt = prompt_all.prompt
    reference = slice_merge_reference(slices)
    prompt = prompt.replace("{query}", query)
    prompt = prompt.replace("{content}", reference)
    return prompt

def slice_merge_reference(slice_list):
    slice_sort(slice_list)
    reference_str = f"文件名《{slice_list[0]['file_name']}》:"
    for slice in slice_list:
        reference_str += slice['slice_content']
    return reference_str

def fine_index(slice_list, cur_slice):
    for index in range(len(slice_list)):
        if slice_list[index]['segment_id'] == cur_slice['segment_id']:
            return index

def slice_sort(slice_list):
    result = []
    sequence = []
    start_positions = {}
    slice_list_sorted = sorted(slice_list, key=lambda x:x['segment_id'])

    for cur_slice in slice_list_sorted:
        if not sequence or cur_slice['segment_id'] == sequence[-1]['segment_id'] + 1:
            if not sequence:
                start_positions[cur_slice['segment_id']] = fine_index(slice_list, cur_slice)
            sequence.append(cur_slice)
        else:
            result.append(sequence)
            sequence = [cur_slice]
            start_positions[cur_slice['segment_id']] = fine_index(slice_list, cur_slice)
    if sequence:
        result.append(sequence)

    result_sorted = sorted(result, key=lambda x: start_positions[x[0]['segment_id']])
    flattened_result = [item for sublist in result_sorted for item in sublist]
    return flattened_result