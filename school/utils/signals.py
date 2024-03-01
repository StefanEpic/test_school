from rest_framework import status
from rest_framework.exceptions import ValidationError


def split_list_by_sublist(lst: list, num_sublists: int, min_len: int, max_len: int) -> list:
    """
    Converts a list into a list with sublists,
    taking into account the specified limit of sublists,
    their minimum and maximum length.
    """
    len_lst = len(lst)
    if len_lst < min_len:
        raise ValidationError(code=status.HTTP_400_BAD_REQUEST, detail="Too few clients to split by groups.")
    if len_lst > num_sublists * max_len:
        raise ValidationError(code=status.HTTP_400_BAD_REQUEST, detail="Need more groups to split clients.")

    while True:
        len_sublst = len_lst // num_sublists
        if len_sublst >= min_len:
            break
        if num_sublists == 1:
            break
        num_sublists -= 1

    result = [[] for _ in range(num_sublists)]
    lst_index = 0

    for sublist in result:
        while len(sublist) < min_len:
            sublist.append(lst[lst_index])
            lst_index += 1
    if lst_index < len_lst:
        run_cycle = True
        while run_cycle:
            for sublist in result:
                sublist.append(lst[lst_index])
                lst_index += 1
                if lst_index == len_lst:
                    run_cycle = False
                    break

    return result
