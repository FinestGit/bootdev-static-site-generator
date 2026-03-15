import re


def extract_markdown_images(text):
    alt_text = re.findall(r"\[(.*?)\]", text)
    url = re.findall(r"\((.*?)\)", text)
    markdown_images = []
    for i in range(len(alt_text)):
        markdown_images.append((alt_text[i], url[i]))
    return markdown_images


def extract_markdown_links(text):
    alt_text = re.findall(r"\[(.*?)\]", text)
    url = re.findall(r"\((.*?)\)", text)
    markdown_links = []
    for i in range(len(alt_text)):
        markdown_links.append((alt_text[i], url[i]))
    return markdown_links
