import socket
import ssl
import tkinter
import tkinter.font
from typing import List


WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18
SCROLL_STEP = 100
FONTS = {}  # caching purposes


class URL:
    def __init__(self, request_url):
        self.port = 80
        self.scheme, url = request_url.split("://", 1)
        assert self.scheme in ["http", "https"]
        assert url is not None
        
        if '/' not in url:
            url = url + '/'

        self.host, url = url.split("/", 1)
        self.path = '/' + url

        if self.scheme == 'https':
            self.port = 443
        if ':' in self.host:
            self.host, port = self.host.split(':', 1)
            self.port = int(port)
    
    def request(self) -> str:
        s = socket.socket(
            family=socket.AF_INET, # AF = addressfamily
            type=socket.SOCK_STREAM, # stream of data, can also do datagrams (packets)
            proto=socket.IPPROTO_TCP, 
        )

        connection = "close"
        useragent = "python-vscode"
        
        if self.scheme == 'https':
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host)
        
        s.connect((self.host, self.port))
        # TODO: make it easier to add request headers/values
        request = f"GET {self.path} HTTP/1.0\r\n"
        request += f"Host: {self.host}\r\n"
        request += f"Connection: {connection}\r\n"
        request += f"User-Agent: {useragent}\r\n"
        request += "\r\n"
        s.send(request.encode("utf8"))

        response = s.makefile("r", encoding="utf8", newline="\r\n")
        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)

        response_headers = {}
        while True:
            line = response.readline()
            if line == "\r\n":
                break
            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()

        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers

        body = response.read()
        s.close()

        print('Response Headers: \n', response_headers)
        # print(body)
        return body


class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window, 
            width=WIDTH,
            height=HEIGHT
        )
        self.canvas.pack()
        self.scroll = 0
        self.window.bind("<Down>", self.scrolldown)
    
    def scrolldown(self, e):
        self.scroll += SCROLL_STEP
        self.draw()

    def load(self, url: URL):
        body = url.request()
        tokens = lex(body)
        self.display_list = Layout(tokens).display_list
        self.draw()
    
    def draw(self):
        self.canvas.delete('all')
        for x, y, c, font in self.display_list:
            if y > self.scroll + HEIGHT:
                continue
            if y + VSTEP < self.scroll:
                continue
            self.canvas.create_text(x, y - self.scroll, text=c, anchor='nw', font=font)


class Text:
    def __init__(self, text: str):
        self.text = text

    def __str__(self):
        return f"Text object with value: {self.text}"


class Tag:
    def __init__(self, tag: str):
        self.tag = tag

    def __str__(self):
        return f"Tag object with value: {self.tag}"


class Layout:
    def __init__(self, tokens: List[Tag] | List[Text]):
        self.display_list = []
        self.cursor_x = HSTEP
        self.cursor_y = VSTEP
        self.weight = "normal"
        self.style = "roman"
        self.line = []
        self.size = 12  # font size

        for tok in tokens:
            self.token(tok)

        self.flush()

    def token(self, tok: Tag | Text):
        if isinstance(tok, Text):
            for word in tok.text.split():
                self.word(word)
        elif tok.tag == "i":
            self.style = "italic"
        elif tok.tag == "/i":
            self.style = "roman"
        elif tok.tag == "b":
            print('self.weight has changed to BOLD!!')
            self.weight = "bold"
        elif tok.tag == "/b":
            self.weight = "normal"
        elif tok.tag == "small":
            self.size -= 2
        elif tok.tag == "/small":
            self.size += 2
        elif tok.tag == "big":
            self.size += 4
        elif tok.tag == "/big":
            self.size -= 4
        elif tok.tag == "br":
            self.flush()
        elif tok.tag == "/p":
            self.flush()
            self.cursor_y += VSTEP
    
    def word(self, word: Text):
        font = get_font(self.size, self.weight, self.style)
        w = font.measure(word)
        if self.cursor_x + w > WIDTH - HSTEP:
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
        self.cursor_x = HSTEP
        self.line = []


def lex(body: str) -> List[Tag] | List[Text]:
    out = []
    buffer = ""
    in_tag = False
    for c in body:
        if c == '<':
            in_tag = True
            if buffer:
                out.append(Text(buffer))
            buffer = ""
        elif c == '>':
            in_tag = False
            out.append(Tag(buffer))
            buffer = ""
        else:
            buffer += c
    if not in_tag and buffer:
        out.append(Text(buffer))
    return out


def get_font(size, weight, style):
    key = (size, weight, style)
    if key not in FONTS:
        font = tkinter.font.Font(
            size=size, 
            weight=weight,
            slant=style
        )
        label = tkinter.Label(font=font)
        FONTS[key] = (font, label)
    return FONTS[key][0]


if __name__ == '__main__':
    import sys
    Browser().load(URL(sys.argv[1]))
    tkinter.mainloop()
