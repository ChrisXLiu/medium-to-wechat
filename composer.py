from bs4 import BeautifulSoup
import json


def process_content(text_content, markups, soup, styler, tag_type):
    """
    Creates an element from text_content and markups into the content_tag.
    E.g.
    text_content = "this is cool"
    markups = [{"start": 8, "end": 12, "type": "STRONG"}]
    tag_type = "p"
    Returns "<p>this is <strong>cool</strong></p>"
    """
    content_tag = soup.new_tag(tag_type)
    last_end = 0
    for markup in markups:
        start = markup['start']
        end = markup['end']
        inner_tag = None
        if markup['type'] == 'STRONG':
            inner_tag = 'strong'
        if markup['type'] == 'EM':
            inner_tag = 'i'
        if inner_tag is not None:
            content_tag.append(text_content[last_end:start])
            markup_tag = soup.new_tag(inner_tag)
            markup_tag.string = text_content[start:end]
            styler.style(markup_tag)
            content_tag.append(markup_tag)
            text_content = text_content[end:]
            last_end = end
    if len(text_content) > 0:
        content_tag.append(text_content)
    return content_tag


def compose(article, upload_image_func, styler, footer_decorator, content_modifiers):
    soup = BeautifulSoup('<div></div>')
    root = soup.div

    title = article['title']
    subtitle = article['subtitle']
    for modifier in content_modifiers:
        title = modifier.modify(title)
        if subtitle is not None:
            subtitle = modifier.modify(subtitle)
    paragraphs = article['paragraphs']

    # Keep track of the current context:
    # 1) None
    # 2) in <ul>
    # 3) in <ol>
    # Embedded contexts are not allowed.
    context = None
    for p in paragraphs:
        if p['type'] == 'IMG':
            img_filename = p['img_filename']
            uploaded_url = upload_image_func(img_filename)
            img_tag = soup.new_tag('img')
            img_tag['src'] = uploaded_url
            styler.style(img_tag)
            root.append(img_tag)
        else:
            new_context = None
            if p['type'] == 'OLI':
                tag_type = 'li'
                new_context = 'ol'
            elif p['type'] == 'ULI':
                tag_type = 'li'
                new_context = 'ul'
            elif p['type'] == 'H3':
                tag_type = 'h3'
            elif p['type'] == 'H4':
                tag_type = 'h4'
            else:
                # TODO: handle "quote" paragraphs
                tag_type = 'p'

            if new_context != context:
                # Backtrack from either <ul> or <ol>
                if context is not None:
                    root = root.parent
                # Enter either <ul> or <ol>
                if new_context is not None:
                    new_root = soup.new_tag(new_context)
                    root.append(new_root)
                    styler.style(new_root)
                    root = new_root
                context = new_context

            text_content = p['text']
            for modifier in content_modifiers:
                text_content = modifier.modify(text_content)
            markups = p['markups']
            new_tag = process_content(text_content, markups, soup, styler, tag_type)
            styler.style(new_tag)
            root.append(new_tag)

    if footer_decorator is not None:
        footer_decorator.add_footer(soup, root)

    # soup: <html><body><div>real content</div></body></html>
    return {'title': title, 'subtitle': subtitle, 'content': str(soup.div)}
