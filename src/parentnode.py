from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag is None:
            raise ValueError("parent node must have a tag attribute")
        if self.children is None or len(self.children) < 1:
            raise ValueError("parent node must have children")
        html = ""
        if self.props:
            html = f"<{self.tag}{self.props_to_html()}>"
        else:
            html = f"<{self.tag}>"
        for child in self.children:
            html += child.to_html()
        return html + f"</{self.tag}>"
