login_box_error_message = "//*[@data-test='error']"


def descendant_text(text: str, contains: bool = True) -> str:
    if contains:
        return f"[descendant::text()[contains(.,'{text}')]]"
    return f"[descendant::text()='{text}']"


def inner_text(text: str, contains: bool = True) -> str:
    if contains:
        return f"[text()[contains(.,'{text}')]]"
    return f"[text()='{text}']"


def descendant_text_with_quotes(text: str, contains: bool = True) -> str:
    if "'" in text:
        parts = text.split("'")
        concat_parts = "concat('" + "', \"'\", '".join(parts) + "')"
        xpath_expression = f"contains(.,{concat_parts})" if contains else f".={concat_parts}"
    else:
        xpath_expression = f"contains(.,'{text}')" if contains else f".='{text}'"
    return f"[descendant::text()[{xpath_expression}]]"


def inner_text_with_quotes(text: str, contains: bool = True) -> str:
    if "'" in text:
        parts = text.split("'")
        concat_parts = "concat('" + "', \"'\", '".join(parts) + "')"
        xpath_expression = f"contains(.,{concat_parts})" if contains else f".={concat_parts}"
    else:
        xpath_expression = f"contains(.,'{text}')" if contains else f".='{text}'"
    return f"[text()[{xpath_expression}]]"


def input_with_id(_id: str) -> None:
    return f"//input[contains(@id,'{_id}')]"


def button_with_id(_id: str) -> None:
    return f"//button[contains(@id,'{_id}')]"


def button_with_text(text: str, contains: bool = False) -> str:
    return "//button" + descendant_text(text, contains)
