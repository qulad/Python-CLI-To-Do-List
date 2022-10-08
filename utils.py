def take_input(input_text:str, low:int, high:int) -> int:
    """
    Takes input from user and validates it, returns the validated input value.
    """
    validated = False
    while not validated:
        print(input_text)
        selected = input()
        validated = select_validated(low=low, high=high, selected=selected)
    return int(selected)


def select_validated(low:int, high:int, selected:str) -> bool:
    """
    Takes a value that has given by the user and checks if it is between given boundaries.
    """
    try:
        selected = int(selected)
    except:
        return False
    if selected >= low and selected <= high:
        return True
    else:
        return False