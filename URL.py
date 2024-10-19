import socket

class URL:
    def __init__(self, request_url):
        self.port = 80
        self.scheme, url = request_url.split("://", 1)
        assert self.scheme == "http" or self.scheme == "https"
        assert url is not None

        if '/' not in url:
            url = url + '/'

        self.host, url = url.split("/", 1)
        self.path = '/' + url
    
    def request(self):
        s = socket.socket(
            family=socket.AF_INET, # AF = addressfamily
            type=socket.SOCK_STREAM, # stream of data, can also do datagrams (packets)
            proto=socket.IPPROTO_TCP, 
        )
        s.connect((self.host, self.port))
        request = "GET {} HTTP/1.0\r\n".format(self.path)
        request += "Host: {}\r\n".format(self.host)
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

        print(response_headers)
        print(body)
        return body







c = URL("https://www.google.com/path/to/wowzers")
d = URL("http://www.example.org")
d.request()