import re


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    # Do not match the "[alt]" of "![alt](url)" — only true [text](url) links.
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)
