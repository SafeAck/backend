"""
Regex utils
"""

from re import compile

regexs = {
    "name": compile("^[a-zA-Z]+$"),
    "full_name": compile("^[a-z\\sA-Z]+$"),
    # s3://test/safeack-results/03ac6cafbea141e185570985c6316ad3.json
    "s3_result_path": compile(
        r"s3:\/\/[a-zA-Z0-9.\-_]{1,255}\/safeack-results\/[0-9a-f]{32}\.json"
    ),
    "extract_s3_result_path": compile(r"s3://([^/]+)/(.+)"),
}
