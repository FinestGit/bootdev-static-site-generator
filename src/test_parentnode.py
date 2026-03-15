import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        result = "<div><span>child</span></div>"
        self.assertEqual(parent_node.to_html(), result)

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        result = "<div><span><b>grandchild</b></span></div>"
        self.assertEqual(parent_node.to_html(), result)

    def test_to_html_with_props_and_children(self):
        child_node = LeafNode("b", "Click me!")
        parent_node = ParentNode(
            "a", [child_node], {"href": "https://www.google.com", "target": "_blank"}
        )
        result = '<a href="https://www.google.com" target="_blank"><b>Click me!</b></a>'
        self.assertEqual(parent_node.to_html(), result)

    def test_to_html_empty_children(self):
        parent_node = ParentNode("span", [])
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()

        expected_message = "parent node must have children"
        actual_message = str(context.exception)
        self.assertEqual(actual_message, expected_message)

    def test_to_html_no_children(self):
        parent_node = ParentNode("span", None)
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()

        expected_message = "parent node must have children"
        actual_message = str(context.exception)
        self.assertEqual(actual_message, expected_message)

    def test_to_html_no_tag(self):
        parent_node = ParentNode(None, None)
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()

        expected_message = "parent node must have a tag attribute"
        actual_message = str(context.exception)
        self.assertEqual(actual_message, expected_message)


if __name__ == "__main__":
    unittest.main()
