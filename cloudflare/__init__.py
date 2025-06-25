# Cloudflare bypass testing module 

def worker(self):
    while self.running:
        self.http_test()  # sau metoda de test
        # elimină orice time.sleep() aici! 