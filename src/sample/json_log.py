"""
Sample JSON-formatted network/security log events for testing and demo.
"""

SAMPLE_JSON_LOGS = [
    # Firewall JSON log (ALLOW)
    '{"time":"2026-09-22T14:05:31Z","severity":2,"src_ip":"192.168.1.10","src_port":54321,"dst_ip":"8.8.8.8","dst_port":443,"protocol":"TCP","message":"ALLOW outbound HTTPS","hostname":"firewall01","vendor":"Cisco","product":"ASA","version":"9.1"}',

    # IDS alert JSON (high severity DENY)
    '{"time":"2026-09-22T14:09:18Z","severity":4,"src_ip":"203.0.113.50","src_port":445,"dst_ip":"192.168.1.20","dst_port":445,"protocol":"TCP","message":"DENY lateral movement attempt","hostname":"ids01","vendor":"Snort","product":"Snort IDS","version":"3.1"}',

    # Router log JSON (traffic monitoring)
    '{"timestamp":1758585600,"severity":1,"srcip":"10.0.0.10","srcport":5000,"dstip":"10.0.0.20","dstport":8080,"proto":"UDP","msg":"TRAFFIC internal subnet","hostname":"router01","vendor_name":"Juniper","product_name":"SRX345"}',

    # Application firewall JSON (BLOCK)
    '{"time":"2026-09-22T14:12:33Z","severity":5,"source_ip":"198.51.100.77","source_port":0,"destination_ip":"192.0.2.5","destination_port":0,"protocol":"HOPOPT","message":"BLOCK unknown protocol","device_hostname":"fw-dmz01","device_vendor_name":"Fortinet","device_product_name":"FortiGate","device_version":"7.0.1"}',

    # Switch syslog-style JSON (info)
    '{"time":"2026-09-22T14:20:00Z","severity":1,"src_ip":"192.168.1.100","dst_ip":"192.168.1.1","protocol":"ICMP","message":"ACCEPT ping response","hostname":"switch01","product":"Catalyst 9300"}',
]
