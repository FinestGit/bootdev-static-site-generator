from textnode import TextNode, TextType
from extract_urls import extract_markdown_links, extract_markdown_images


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_text_by_delimiter = old_node.text.split(delimiter)
        if len(split_text_by_delimiter) % 2 == 0:
            raise Exception("invalid Markdown syntax")
        for i in range(len(split_text_by_delimiter)):
            if i == 0 or i == len(split_text_by_delimiter) - 1:
                new_nodes.append(TextNode(split_text_by_delimiter[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(split_text_by_delimiter[i], text_type))
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        markdown_images = extract_markdown_images(old_node.text)
        if len(markdown_images) == 0:
            new_nodes.append(old_node)
            continue
        remaining = old_node.text
        for i in range(len(markdown_images)):
            alt_text, url = markdown_images[i]
            sections = remaining.split(f"![{alt_text}]({url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            remaining = sections[1]
        if remaining != "":
            new_nodes.append(TextNode(remaining, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        markdown_links = extract_markdown_links(old_node.text)
        if len(markdown_links) == 0:
            new_nodes.append(old_node)
            continue
        remaining = old_node.text
        for i in range(len(markdown_links)):
            alt_text, url = markdown_links[i]
            sections = remaining.split(f"[{alt_text}]({url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.LINK, url))
            remaining = sections[1]
        if remaining != "":
            new_nodes.append(TextNode(remaining, TextType.TEXT))
    return new_nodes


def to_text_nodes(text):
    text_nodes = []
    text_nodes.append(TextNode(text, TextType.TEXT))
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes
