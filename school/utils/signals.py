def split_list(lst: list, n: int) -> list:
    """
    Split list by N lists.
    """
    lst_len = len(lst)
    k = lst_len // n
    return [lst[i : i + k] for i in range(0, lst_len, k)]
