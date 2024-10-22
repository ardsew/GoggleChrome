import tkinter
import tkinter.font
import constants
from text import Text

class Layout:

    FONTS = {}

    def __init__(self, nodes):
        self.display_list = []
        self.cursor_x = constants.HSTEP
        self.cursor_y = constants.VSTEP
        self.weight = "normal"
        self.style = "roman"
        self.line = []
        self.size = 12  # font size

        self.recurse(nodes)
        self.flush()
    
    def open_tag(self, tag):
        if tag == "i":
            self.style = "italic"
        elif tag == "b":
            self.weight = "bold"
        elif tag == "small":
            self.size -= 2
        elif tag == "big":
            self.size += 4
        
    def close_tag(self, tag):
        if tag == "i":
            self.style = "roman"
        elif tag == "b":
            self.weight = "normal"
        elif tag == "small":
            self.size += 2
        elif tag == "big":
            self.size -= 4
        elif tag == "br":
            self.flush()
        elif tag == "p":
            self.flush()
            self.cursor_y += constants.VSTEP
    
    def recurse(self, tree):
        if isinstance(tree, Text):
            for word in tree.text.split():
                self.word(word)
        else:
            self.open_tag(tree.tag)
            for child in tree.children:
                self.recurse(child)
            self.close_tag(tree.tag)
    
    def word(self, word: Text):
        font = self.get_font(self.size, self.weight, self.style)
        w = font.measure(word)
        if self.cursor_x + w > constants.WIDTH - constants.HSTEP:
            self.flush()
        self.line.append((self.cursor_x, word, font))
        self.cursor_x += w + font.measure(' ')
    
    def flush(self):
        if self.line == []:
            return
        metrics = [font.metrics() for x, word, font in self.line]
        max_ascent = max([metric["ascent"] for metric in metrics])
        max_descent = max([metric["descent"] for metric in metrics])

        baseline = self.cursor_y + 1.25 * max_ascent
        for x, word, font in self.line:
            y = baseline - font.metrics("ascent")
            self.display_list.append((x, y, word, font))
        
        self.cursor_y = baseline + 1.25 * max_descent
        self.cursor_x = constants.HSTEP
        self.line = []


    def get_font(self, size, weight, style):
        key = (size, weight, style)
        if key not in self.FONTS:
            font = tkinter.font.Font(
                size=size, 
                weight=weight,
                slant=style
            )
            label = tkinter.Label(font=font)
            self.FONTS[key] = (font, label)
        return self.FONTS[key][0]
