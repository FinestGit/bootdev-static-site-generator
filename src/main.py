from textnode import TextNode, TextType
from htmlnode import HTMLNode


def main():
    new_text_node = TextNode(
        "This is some anchor text", TextType.LINK, "https://www.boot.dev"
    )
    print(new_text_node)
    new_html_node = HTMLNode(
        "p",
        "This is some paragraph text",
        None,
        {
            "href": "https://www.google.com",
            "target": "_blank",
        },
    )
    print(new_html_node)
    print(new_html_node.props_to_html())


if __name__ == "__main__":
    main()
