<img src="img/goggle-chrome.jpg" alt="Goggle Chrome!" width="400"/>

# Web Browser from Scratch
This project is a minimalist Python-based web browser using socket, ssl, and tkinter for rendering simple HTML documents. It demonstrates basic HTML parsing, rendering, and networking functionalities, making HTTP/HTTPS requests, and displaying the responses.


## Features
- URL Parsing: Parses URLs and handles both HTTP and HTTPS protocols.
- Basic HTTP/HTTPS Request Handling: Uses sockets for making requests and reading responses from servers.
- Simple HTML Rendering: A custom HTML parser that handles text, paragraphs, and basic tags like `<i>, <b>, <small>, <big>, and <br>`.
- Scroll Support: Uses arrow keys or mwheel to scroll through the rendered page.

## Requirements
- Python 3.x
- tkinter (usually included in standard Python installations)
- Internet connection (for making requests)

## Installation
1.	Clone the repository:
```
git clone https://github.com/yourusername/simple-python-browser.git
cd simple-python-browser
```

2.	Install any necessary dependencies (in most cases, tkinter is already available):
- For Ubuntu/Debian:
	```
	sudo apt-get install python3-tk
	```
- For **macOS**: tkinter is included with the standard Python installation.
- For **Windows**:
If you installed Python from the official installer, tkinter is included by default.

## Usage

To run the browser and load a webpage, execute the following command in the terminal:
```
python3 main.py https://www.google.com
```


## License
Built from following: https://browser.engineering/layout.html

MIT License. See LICENSE for details.
