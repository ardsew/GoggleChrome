class Text:
    def __init__(self, text: str, parent):
        self.text = text
        self.children = []
        self.parent = parent

    def __str__(self):
        return repr(self.text)
