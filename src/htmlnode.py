

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        tag = self.tag or "None"
        value = self.value or "None"
        children = self.children or "None"
        props = self.props or "None"
        return f"HTMLNode(tag={tag}, value={value}, children={children}, props={props})"

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        ret = ""
        for prop_key in self.props:
            ret += f"{prop_key}=\"{self.props[prop_key]}\" "
        return ret.strip()

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        if value == None:
            raise ValueError("leafnode value cannot be none")
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.tag == None:
            return self.value
        if self.props != None:
            props_txt = self.props_to_html()
            return '<{tag} {props}>{value}</{tag}>'.format(tag=self.tag, value=self.value, props=props_txt)
        return '<{tag}>{value}</{tag}>'.format(tag=self.tag, value=self.value)

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag=tag, children=children, props=props)
        if tag == None: 
            raise ValueError("parentnode tag cannot be none")
        if children == None:
            raise ValueError("parentnode children list cannot be none")
        # if len(children) == 0:
        #     raise ValueError("parentnode children len cannot be 0")
    def to_html(self):
        props_str = ""
        if self.props != None:
            props_str = " " + self.props_to_html()
        inner_html = ""
        for child in self.children:
            inner_html += child.to_html()
        return "<{tag}{props}>{inner}</{tag}>".format(tag=self.tag, inner=inner_html, props=props_str)
        

        