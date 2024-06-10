class HTMLnode:
    def __init__(
        self,
        tag=None,
        value=None,
        children=None,
        props=None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""

        props_string = ""
        for key, value in self.props.items():
            props_string += f' {key}="{value}"'

        return props_string

    def __repr__(self):
        return f"Tag:{self.tag} \n  \
        Value:{self.value} \n       \
        Children:{self.children} \n \
        Props:{self.props}"


class LeafNode(HTMLnode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError()

        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLnode):
    def __init__(self, children, tag=None, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("No tag, cannot make html")
        if self.children is None:
            raise ValueError("Must have child")

        html_string = ""

        for child in self.children:
            html_string += child.to_html()

        return f"<{self.tag}>{html_string}</{self.tag}>"
