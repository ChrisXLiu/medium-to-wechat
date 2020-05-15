def style(tag):
    if tag.name == "h3":
        tag["style"] = "font-size:21px;font-weight:bold;line-height:2em;"
    elif tag.name == "h4":
        tag["style"] = "font-size:19px;font-weight:bold;line-height:2em;"
    elif tag.name in ["p", "ul", "ol"]:
        tag["style"] = "font-size:17px;margin:17px 0;"
