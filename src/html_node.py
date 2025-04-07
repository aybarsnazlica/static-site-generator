class HTMLNode:
    """Base class representing an HTML node.

    Attributes:
        tag (str | None): The HTML tag name (e.g., 'div', 'p').
        value (str | None): The textual content for leaf nodes.
        children (list[HTMLNode] | None): List of child HTMLNode objects.
        props (dict[str, str] | None): Dictionary of HTML attributes (e.g., {'class': 'main'}).
    """

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        """Generates the HTML string representation of the node.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.

        Returns:
            str: HTML string representation.
        """
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self) -> str:
        """Converts props dictionary into a string of HTML attributes.

        Returns:
            str: A string of HTML attributes (e.g., ' class="main" id="top"').
        """
        if self.props is None:
            return ""
        props_html = ""

        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'

        return props_html

    def __repr__(self) -> str:
        """Returns a string representation of the HTML node for debugging.

        Returns:
            str: Debug string showing tag, value, children, and props.
        """
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):
    """Represents an HTML node with no children (a leaf node)."""

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        """Converts the leaf node to its HTML string representation.

        Raises:
            ValueError: If the node has no value when a tag is present.

        Returns:
            str: The HTML string representation of the leaf node.
        """
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        """Returns a string representation of the LeafNode for debugging.

        Returns:
            str: Debug string showing tag, value, and props.
        """
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    """Represents an HTML node that contains other child nodes."""

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        """Recursively converts the parent node and its children into HTML.

        Raises:
            ValueError: If the tag or children are missing.

        Returns:
            str: The HTML string representation of the parent node and its children.
        """
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if self.children is None:
            raise ValueError("invalid HTML: no children")
        children_html = ""

        for child in self.children:
            children_html += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self) -> str:
        """Returns a string representation of the ParentNode for debugging.

        Returns:
            str: Debug string showing tag, children, and props.
        """
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
