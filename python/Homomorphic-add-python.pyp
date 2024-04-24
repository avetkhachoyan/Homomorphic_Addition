from http.server import SimpleHTTPRequestHandler, HTTPServer
import webbrowser
from Crypto.Util.number import getRandomRange, inverse
from Crypto.PublicKey import RSA
from functools import reduce

class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)

class Paillier:
    def __init__(self, key_length=1024):
        self.key = RSA.generate(key_length)
        self.n = self.key.n
        self.g = self.n + 1
        self.n_squared = self.n ** 2
        self.lmbda = self.lcm(self.key.p - 1, self.key.q - 1)
        self.mu = inverse(self.L(self.g**self.lmbda % self.n_squared), self.n)

    def encrypt(self, plaintext):
        r = getRandomRange(1, self.n)
        return pow(self.g, plaintext, self.n_squared) * pow(r, self.n, self.n_squared) % self.n_squared

    def decrypt(self, ciphertext):
        return (self.L(pow(ciphertext, self.lmbda, self.n_squared)) * self.mu) % self.n

    def L(self, x):
        return (x - 1) // self.n

    def lcm(self, a, b):
        return abs(a*b) // self.gcd(a, b)

    def gcd(self, a, b):
        while b != 0:
            a, b = b, a % b
        return a

def homomorphic_addition(paillier, ciphertexts):
    return reduce(lambda x, y: (x * y) % paillier.n_squared, ciphertexts)

def generate_html():
    paillier = Paillier()
    a = 10
    b = 20
    c_a = paillier.encrypt(a)
    c_b = paillier.encrypt(b)
    c = homomorphic_addition(paillier, [c_a, c_b])
    result = paillier.decrypt(c)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Homomorphic Addition</title>
    </head>
    <body>
        <h1>Homomorphic Addition</h1>
        <div id="results">
            <p>Encrypted a: {c_a}</p>
            <p>Encrypted b: {c_b}</p>
            <p>Encrypted sum: {c}</p>
            <p>Decrypted sum: {result}</p>
        </div>
    </body>
    </html>
    """
    return html_content

def start_web_server():
    server_address = ('', 8000)  # Host: localhost, Port: 8000
    httpd = HTTPServer(server_address, MyHTTPRequestHandler)
    print("Server running at http://localhost:8000/")
    httpd.serve_forever()

if __name__ == "__main__":
    # Generate HTML content
    html_content = generate_html()

    # Write HTML content to a file
    with open("index.html", "w") as f:
        f.write(html_content)

    # Open the browser automatically
    webbrowser.open_new_tab("http://localhost:8000/")

    # Start the web server
    start_web_server()
