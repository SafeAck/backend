from re import compile

regexs = {
    "name": compile("^[a-zA-Z]+$"),
    "full_name": compile("^[a-z\\sA-Z]+$"),
}
