import tkinter
import constants
from htmlparser import HTMLParser
from layout import Layout
from url import URL


class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window, 
            width=constants.WIDTH,
            height=constants.HEIGHT
        )
        self.canvas.pack()
        self.scroll = 0
        self.binds()
    
    def binds(self):
        self.window.bind("<Down>", self.scrolldown)
        self.window.bind("<Up>", self.scrollup)
        self.window.bind("<MouseWheel>", self.on_mousewheel)  # Windows and MacOS
        self.window.bind("<Button-4>", self.scrollup)         # Linux - scroll up
        self.window.bind("<Button-5>", self.scrolldown)       # Linux - scroll down

    def on_mousewheel(self, event):
        if event.delta > 0:
            self.scrollup(event)
        else:
            self.scrolldown(event)
    
    def scrolldown(self, foo):
        self.scroll += constants.SCROLL_STEP
        self.draw()
    
    def scrollup(self, foo):
        self.scroll -= constants.SCROLL_STEP
        self.draw()

    def load(self, url: URL):
        body = url.request()
        self.nodes = HTMLParser(body).parse()
        self.display_list = Layout(self.nodes).display_list
        self.draw()
    
    def draw(self):
        self.canvas.delete('all')
        for x, y, c, font in self.display_list:
            if y > self.scroll + constants.HEIGHT:
                continue
            if y + constants.VSTEP < self.scroll:
                continue
            self.canvas.create_text(x, y - self.scroll, text=c, anchor='nw', font=font)
