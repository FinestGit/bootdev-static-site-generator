from textnode import TextNode, TextType


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
