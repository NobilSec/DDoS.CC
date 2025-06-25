#!/usr/bin/env python3
"""
Configuration file for Network Testing Tool
"""

# Default settings
DEFAULT_THREADS = 10
DEFAULT_DURATION = 60
DEFAULT_TIMEOUT = 10
DEFAULT_VERBOSE = False

# Layer 7 settings
LAYER7_SETTINGS = {
    'max_requests_per_second': 100,
    'user_agent_rotation': True,
    'path_fuzzing': True,
    'method_fuzzing': True
}

# Layer 4 settings
LAYER4_SETTINGS = {
    'tcp_connect_timeout': 5,
    'udp_timeout': 3,
    'syn_flood_enabled': True,
    'port_scan_enabled': True
}

# Cloudflare settings
CLOUDFLARE_SETTINGS = {
    'bypass_techniques': [
        'user_agent_rotation',
        'header_manipulation',
        'direct_ip_access',
        'ssl_verification_disable',
        'dns_manipulation'
    ],
    'max_bypass_attempts': 1000
}

# FiveM settings
FIVEM_SETTINGS = {
    'default_ports': [30120, 30121, 30122, 30123, 30124, 30125],
    'query_types': ['info', 'players', 'rules', 'ping'],
    'handshake_timeout': 10
}

# Minecraft settings
MINECRAFT_SETTINGS = {
    'default_ports': [25565, 25566, 25567, 25568, 25569, 25570],
    'protocol_versions': [47, 107, 210, 315, 335, 338, 340, 393, 401, 404],
    'packet_types': ['handshake', 'status_request', 'ping', 'login_start']
}

# Logging settings
LOGGING_SETTINGS = {
    'log_level': 'INFO',
    'log_file': 'network_test.log',
    'console_output': True
}

# Safety settings
SAFETY_SETTINGS = {
    'max_connections_per_second': 1000,
    'max_total_connections': 10000,
    'cooldown_period': 5,  # seconds
    'rate_limiting': True
} 