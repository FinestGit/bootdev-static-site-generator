import unittest
from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_delimiter(self):
        node = TextNode("This is a text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            result,
            [
                TextNode("This is a text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_bold_delimiter(self):
        node = TextNode("This is a text with a **bold** word", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            result,
            [
                TextNode("This is a text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_italic_delimiter(self):
        node = TextNode("This is a text with a _italic_ word", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            result,
            [
                TextNode("This is a text with a ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
        )


if __name__ == "__main__":
    unittest.main()
