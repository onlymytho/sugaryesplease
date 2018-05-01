def apiReturnValue(code, data="", error_type="", error_message=""):
    # 형식은 Instagra API Endpoint Structure를 참고함: https://www.instagram.com/developer/endpoints/
    """
    아래 형식을 따르며, 에러가 아닌 경우, code와 data만 입력.
    {"meta": {
        "error_type": "OAuthException",
        "code": 400,
        "error_message": "..."},
     "data": {...}}
    """
    if code == 200:
        return {"meta": {"code": code}, "data": data}
    if code != 200:
