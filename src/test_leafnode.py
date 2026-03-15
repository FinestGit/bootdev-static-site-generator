import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_node(self):
        tag = "p"
        value = "This is some paragraph text"
        props = {"href": "https://www.google.com", "target": "_blank"}
        node = LeafNode(tag, value, props)
        self.assertEqual(node.tag, tag)
        self.assertEqual(node.value, value)
        self.assertEqual(node.props, props)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        tag = "a"
        value = "Click me!"
        props = {"href": "https://www.google.com", "target": "_blank"}
        node = LeafNode(tag, value, props)
        result = '<a href="https://www.google.com" target="_blank">Click me!</a>'
        self.assertEqual(node.to_html(), result)

    def test_repr(self):
        tag = "p"
        value = "This is some paragraph text"
        props = None
        node = LeafNode(tag, value, props)
        result = f"LeafNode({tag}, {value}, {props})"
        self.assertEqual(result, repr(node))
        result = f"LeafNode({tag}, {value}, None, {props})"
        self.assertNotEqual(result, repr(node))


if __name__ == "__main__":
    unittest.main()
