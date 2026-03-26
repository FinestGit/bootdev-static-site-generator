import unittest
from textnode import TextNode, TextType
from split_nodes import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    to_text_nodes,
)


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

    def test_split_image_node(self):
        alt_text = "image"
        url = "https://i.imgur.com/zjjcJKZ.png"
        text = f"This is text with an "
        formatted_text = f"{text}![{alt_text}]({url})"
        node = TextNode(formatted_text, TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode(text, TextType.TEXT), TextNode(alt_text, TextType.IMAGE, url)],
            new_nodes,
        )

    def test_split_multiple_image_nodes(self):
        alt_text = "rick roll"
        url = "https://i.imgur.com/aKaOqIh.png"
        alt_text2 = "obi wan"
        url2 = "https://i.imgur.com/fJRm4Vk.jpeg"
        beginning_text = "This is text with a "
        middle_text = " and "
        end_text = " and some end text!"
        formatted_text = f"{beginning_text}![{alt_text}]({url}){middle_text}![{alt_text2}]({url2}){end_text}"
        node = TextNode(formatted_text, TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode(beginning_text, TextType.TEXT),
                TextNode(alt_text, TextType.IMAGE, url),
                TextNode(middle_text, TextType.TEXT),
                TextNode(alt_text2, TextType.IMAGE, url2),
                TextNode(end_text, TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_node(self):
        alt_text = "lorem ipsum generator"
        url = "https://www.lipsum.com"
        beginning_text = "This takes you to a "
        formatted_text = f"{beginning_text}[{alt_text}]({url})"
        node = TextNode(formatted_text, TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode(beginning_text, TextType.TEXT),
                TextNode(alt_text, TextType.LINK, url),
            ],
            new_nodes,
        )

    def test_split_multiple_link_nodes(self):
        alt_text = "to boot dev"
        url = "https://www.boot.dev"
        alt_text2 = "to youtube"
        url2 = "https://www.youtube.com"
        beginning_text = "This is text with a link "
        middle_text = " and "
        end_text = " and some end text!"
        formatted_text = f"{beginning_text}[{alt_text}]({url}){middle_text}[{alt_text2}]({url2}){end_text}"
        node = TextNode(formatted_text, TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode(beginning_text, TextType.TEXT),
                TextNode(alt_text, TextType.LINK, url),
                TextNode(middle_text, TextType.TEXT),
                TextNode(alt_text2, TextType.LINK, url2),
                TextNode(end_text, TextType.TEXT),
            ],
            new_nodes,
        )

    def test_to_text_nodes(self):
        text = "This is a text with a **bold** word and a _italic_ word and a `code` word and an image ![alt text](https://www.google.com) and a link [link text](https://www.google.com)"
        text_nodes = to_text_nodes(text)
        self.assertListEqual(
            [
                TextNode("This is a text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" word and an image ", TextType.TEXT),
                TextNode("alt text", TextType.IMAGE, "https://www.google.com"),
                TextNode(" and a link ", TextType.TEXT),
                TextNode("link text", TextType.LINK, "https://www.google.com"),
            ],
            text_nodes,
        )

    def test_delimiter_unbalanced_raises(self):
        node = TextNode("this has **unclosed bold", TextType.TEXT)
        with self.assertRaises(Exception) as ctx:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertIn("invalid Markdown syntax", str(ctx.exception))

    def test_delimiter_plain_text_no_delimiter(self):
        node = TextNode("no special markers here", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual([node], result)

    def test_delimiter_non_text_node_passthrough(self):
        bold = TextNode("already bold", TextType.BOLD)
        text = TextNode("plain", TextType.TEXT)
        result = split_nodes_delimiter([bold, text], "**", TextType.BOLD)
        self.assertListEqual(
            [bold, TextNode("plain", TextType.TEXT)],
            result,
        )

    def test_delimiter_multiple_text_nodes(self):
        a = TextNode("**a**", TextType.TEXT)
        b = TextNode(" then **b**", TextType.TEXT)
        result = split_nodes_delimiter([a, b], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("", TextType.TEXT),
                TextNode("a", TextType.BOLD),
                TextNode("", TextType.TEXT),
                TextNode(" then ", TextType.TEXT),
                TextNode("b", TextType.BOLD),
                TextNode("", TextType.TEXT),
            ],
            result,
        )

    def test_split_image_only_no_surrounding_text(self):
        alt, url = "solo", "https://example.com/x.png"
        node = TextNode(f"![{alt}]({url})", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertListEqual([TextNode(alt, TextType.IMAGE, url)], result)

    def test_split_image_at_start_then_text(self):
        alt, url = "pic", "https://example.com/i.png"
        tail = " trailing words"
        node = TextNode(f"![{alt}]({url}){tail}", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertListEqual(
            [TextNode(alt, TextType.IMAGE, url), TextNode(tail, TextType.TEXT)],
            result,
        )

    def test_split_image_no_images_returns_unchanged(self):
        node = TextNode("just words and [not a bare image](url)", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertListEqual([node], result)

    def test_split_image_non_text_node_without_image_markdown_passthrough(self):
        # split_nodes_image still parses by text content; BOLD without ![ ]( ) is unchanged.
        bold = TextNode("emphasized caption", TextType.BOLD)
        result = split_nodes_image([bold])
        self.assertListEqual([bold], result)

    def test_split_link_only_no_surrounding_text(self):
        label, url = "solo", "https://example.com"
        node = TextNode(f"[{label}]({url})", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertListEqual([TextNode(label, TextType.LINK, url)], result)

    def test_split_link_does_not_match_image_syntax(self):
        alt, href = "photo", "https://example.com/p.png"
        node = TextNode(f"![{alt}]({href})", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertListEqual([node], result)

    def test_split_link_no_links_returns_unchanged(self):
        node = TextNode("no brackets here", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertListEqual([node], result)

    def test_to_text_nodes_empty_string(self):
        self.assertListEqual([TextNode("", TextType.TEXT)], to_text_nodes(""))

    def test_to_text_nodes_plain_text_only(self):
        text = "hello world without markdown"
        self.assertListEqual(
            [TextNode(text, TextType.TEXT)],
            to_text_nodes(text),
        )

    def test_to_text_nodes_image_then_link_same_line(self):
        text = "x ![i](https://a.com) y [l](https://b.com) z"
        self.assertListEqual(
            [
                TextNode("x ", TextType.TEXT),
                TextNode("i", TextType.IMAGE, "https://a.com"),
                TextNode(" y ", TextType.TEXT),
                TextNode("l", TextType.LINK, "https://b.com"),
                TextNode(" z", TextType.TEXT),
            ],
            to_text_nodes(text),
        )


if __name__ == "__main__":
    unittest.main()
