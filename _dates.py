import itertools
from urllib.parse import _NetlocResultMixinBytes
import dateutil.parser

def parse_dates_sliding(string):
    """
    Find the first instance of a parseable date
    Widen the window
    If the date parsed is the same, stop
    Else, widen the window by 1

    We read left to right, so the window will always increase to the right
    """
    size_window = 1 # Default
    list_words = string.split()
    index_start_string = 0
    index_start_list = 0
    dt_best = None

    # Find the first dt
    for word in list_words:
        try:
            dt_best = dateutil.parser.parse(word, fuzzy=True)
            index_start_string = string.find(word)
            index_start_list = list_words.index(word)
            break
        except dateutil.parser.ParserError as error:
            continue
    
    if dt_best is None:
        return None, -1, -1
    
    # Widen the window
    index_end_list = index_start_list + 2 # caution: could be bigger than list
    while (index_end_list != len(list_words) - 1):
        string_window = " ".join(list_words[index_start_list:index_end_list])
        dt_current = dateutil.parser.parse(string_window, fuzzy=True)
        if dt_best != dt_current:
            dt_best = dt_current # update the best one
        else:
            # Shrink the window back
            string_window = " ".join(list_words[index_start_list:index_end_list - 1])
            index_start_string = string.find(string_window)
            index_end_string = index_start_string + len(string_window)
            return dt_best, index_start_string, index_end_string
        
        index_end_list += 1

def clean_dates(string):
    """
    Replace all legitimate datetime instances with "[date]"

    Needs some work as a failure will result in overwriting the entire string
    """
    list_dict_dates = []
    string_p = string[::]

    dt, index_start, index_end = parse_dates_sliding(string)
    index_sliding = 0
    while dt is not None:
        string_date = string_p[index_start + index_sliding:index_sliding + index_end]
        dict_date = { 'dt' : dt, 'text' : string_date}
        list_dict_dates.append(dict_date)

        string_p = string_p[:index_start + index_sliding] + '[date] ' + string_p[index_sliding + index_end + 1:]
        # prevent overlap
        index_sliding += index_end + 1
        dt, index_start, index_end = parse_dates_sliding(string_p[index_sliding:])

    return string_p, list_dict_dates