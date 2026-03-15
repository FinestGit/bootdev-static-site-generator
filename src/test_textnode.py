import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node = TextNode("This is a text node", TextType.LINK, "http://test.com")
        node2 = TextNode("This is a text node", TextType.LINK, "http://test.com")
        self.assertEqual(node, node2)

    def test_not_equal(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

        node = TextNode("This is a link", TextType.LINK, "http://test.com")
        node2 = TextNode("This is not a link", TextType.LINK, None)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "http://test.com")
        self.assertEqual(
            "TextNode(This is a text node, text, http://test.com)", repr(node)
        )


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        text = "This is some bold text"
        expected_tag = "b"
        node = TextNode(text, TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, expected_tag)
        self.assertEqual(html_node.value, text)

    def test_italic(self):
        text = "This is some italic text"
        expected_tag = "i"
        node = TextNode(text, TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, expected_tag)
        self.assertEqual(html_node.value, text)

    def test_code(self):
        text = "This is some code"
        expected_tag = "code"
        node = TextNode(text, TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, expected_tag)
        self.assertEqual(html_node.value, text)

    def test_link(self):
        text = "Link text"
        expected_tag = "a"
        url = "https://www.google.com"
        node = TextNode(text, TextType.LINK, url)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, expected_tag)
        self.assertEqual(html_node.value, text)
        self.assertEqual(html_node.props["href"], url)

    def test_image(self):
        text = "Alternative text"
        expected_tag = "img"
        url = "https://www.google.com"
        node = TextNode(text, TextType.IMAGE, url)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, expected_tag)
        self.assertEqual(html_node.props["src"], url)
        self.assertEqual(html_node.props["alt"], text)


if __name__ == "__main__":
    unittest.main()
