import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_html_node(self):
        tag = "p"
        value = "This is some paragraph text"
        children = []
        props = {"href": "https://www.google.com", "target": "_blank"}
        node = HTMLNode(tag, value, children, props)
        self.assertEqual(node.tag, tag)
        self.assertEqual(node.value, value)
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

    def test_props_to_html(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )

    def test_repr(self):
        tag = "p"
        value = "This is some paragraph text"
        children = None
        props = None
        node = HTMLNode(tag, value, children, props)
        self.assertEqual(f"HTMLNode({tag}, {value}, {children}, {props})", repr(node))

    def test_empty_props_to_html(self):
        tag = "p"
        value = "This is some paragraph text"
        children = None
        props = {}
        node = HTMLNode(tag, value, children, props)
        self.assertEqual(node.props_to_html(), "")
        props = None
        self.assertEqual(node.props_to_html(), "")


if __name__ == "__main__":
    unittest.main()
