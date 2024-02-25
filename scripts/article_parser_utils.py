class Author:
    def __init__(self, name: str):
        self.name = name
    def __repr__(self) -> str:
        return f"{self.name}"

class ArticleText:
    def __init__(self, id_str, text):
        self.id_str = id_str
        self.text = text
    
    def __repr__(self) -> str:
        return f"{type(self).__name__}(id={self.id_str}\n body={self.text})"

def safe_get_text_value(obj, *arg):
    """
    Get text value of the object (string) given a set of keys in correct order
    
    Returns: str
    """
    def get_text_value(obj, *arg):
        if len(arg) <= 0:
            raise IndexError("Length of key input is 0. Value not found")
        first_key = arg[0]
        if first_key not in obj:
            raise KeyError("1. Key values not found")
        if len(arg) == 1 and type(obj[first_key]) == str:
            return obj[first_key]
        return get_text_value(obj[first_key], *arg[1:])
    try:
        return get_text_value(obj, *arg)
    except Exception as e:
        print(e)
        return ''