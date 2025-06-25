#!/usr/bin/env python3
"""
Example usage of the Network Testing Tool
Educational purposes only - Use responsibly
"""

from layer7.layer7_tester import Layer7Tester
from layer4.layer4_tester import Layer4Tester
from cloudflare.cloudflare_bypass import CloudflareBypass
from fivem.fivem_tester import FiveMTester
from minecraft.minecraft_tester import MinecraftTester

def example_layer7_test():
    """Example Layer 7 test"""
    print("=== Layer 7 Test Example ===")
    target = "example.com"
    port = 80
    
    tester = Layer7Tester(target, port, threads=5, duration=30, verbose=True)
    tester.run_tests()

def example_layer4_test():
    """Example Layer 4 test"""
    print("=== Layer 4 Test Example ===")
    target = "192.168.1.1"
    port = 22
    
    tester = Layer4Tester(target, port, threads=5, duration=30, verbose=True)
    tester.run_tests()

def example_cloudflare_bypass():
    """Example Cloudflare bypass test"""
    print("=== Cloudflare Bypass Test Example ===")
    target = "example.com"
    port = 443
    
    bypass = CloudflareBypass(target, port, threads=5, duration=30, verbose=True)
    bypass.run_tests()

def example_fivem_test():
    """Example FiveM server test"""
    print("=== FiveM Server Test Example ===")
    target = "server.fivem.net"
    port = 30120
    
    tester = FiveMTester(target, port, threads=5, duration=30, verbose=True)
    tester.run_tests()

def example_minecraft_test():
    """Example Minecraft server test"""
    print("=== Minecraft Server Test Example ===")
    target = "mc.example.com"
    port = 25565
    
    tester = MinecraftTester(target, port, threads=5, duration=30, verbose=True)
    tester.run_tests()

if __name__ == "__main__":
    print("Network Testing Tool - Example Usage")
    print("Educational purposes only - Use responsibly")
    print("=" * 50)
    
    # Uncomment the test you want to run
    # example_layer7_test()
    # example_layer4_test()
    # example_cloudflare_bypass()
    # example_fivem_test()
    # example_minecraft_test()
    
    print("\nTo run tests, uncomment the desired example function above.")
    print("Remember to only test systems you own or have permission to test.") 