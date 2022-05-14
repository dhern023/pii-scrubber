import dateutil.parser

def check_has_digits(string):
    return any(map(str.isdigit, string))

def count_digits(string):
    return sum(map(str.isdigit, string))

def check_valid_date_string(string):
    """
    single word with too few digits to discern a date contextually
    e.g., 1.0 by itself or even 2022?
    TODO: Train a model https://spacy.io/usage/training/
    """
    num_digits = count_digits(string)
    if check_has_digits(string) and num_digits <= 2:
        return False
    
    return True

def parse_dates_sliding(string):
    """
    Find the first instance of a parseable date
    Widen the window
    If the date parsed is the same, stop
    Else, widen the window by 1

    We read left to right, so the window will always increase to the right

    index_end will always be the index right after the parsed date ends
    """
    size_window = 1 # Default
    list_words = string.split()
    index_start_string = 0
    index_start_list = 0
    dt_best = None

    # Find the first dt
    for word in list_words:
        if not check_valid_date_string(word):
            continue
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
    while (index_end_list < len(list_words)):
        string_window = " ".join(list_words[index_start_list:index_end_list])
        try:
            dt_current = dateutil.parser.parse(string_window, fuzzy=True)
            if dt_best != dt_current:
                dt_best = dt_current # update the best one
            else:
                break
        except dateutil.parser.ParserError as error:
            pass
        
        index_end_list += 1
    
    # Shrink the window back
    string_window = " ".join(list_words[index_start_list:index_end_list - 1])
    index_start_string = string.find(string_window)
    index_end_string = index_start_string + len(string_window)

    return dt_best, index_start_string, index_end_string

def clean_dates(string):
    """
    Replace all legitimate datetime instances with "[date]" regardless of accuracy
    """
    list_dict_dates = []
    string_p = string[::]

    dt, index_start, index_end = parse_dates_sliding(string)
    index_sliding = 0
    while dt and index_sliding < len(string_p):
        string_date = string_p[index_sliding + index_start: index_sliding + index_end]
        index_sliding += string_p.find(string_date) + len(string_date)
        if string_date == '':
            dt, index_start, index_end = parse_dates_sliding(string_p[index_sliding:])
            continue

        dict_date = { 'dt' : dt, 'text' : string_date}
        list_dict_dates.append(dict_date)

        string_p_tail = string_p[index_sliding:]
        string_p = string_p[:index_sliding].replace(string_date, '[date]') + string_p_tail

        dt, index_start, index_end = parse_dates_sliding(string_p_tail)

    return string_p, list_dict_dates