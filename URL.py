import socket
import ssl

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


def show(body: str):
    in_tag = False
    for c in body:
        if c == '<':
            in_tag = True
        elif c == '>':
            in_tag = False
        elif not in_tag:
            print(c, end='')


def load(url: URL):
    body = url.request()
    show(body)


if __name__ == '__main__':
    import sys
    load(URL(sys.argv[1]))
