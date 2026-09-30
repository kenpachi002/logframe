"""
Sample CSV log lines for the ULPF test lab and UI examples page.
Format: header_row\\ndata_row (two lines) or single data row.
Covers: Fortinet traffic log, pfSense firewall, Cisco Meraki.
"""

# Each entry is a two-line string (header + data) for realistic testing
SAMPLE_CSV_LOGS = [
    # Fortinet FortiGate traffic log
    "date,time,device,action,srcip,srcport,dstip,dstport,proto,msg\n2024-01-15,08:23:41,FortiGate-100F,deny,10.0.0.5,49212,8.8.8.8,443,TCP,Outbound HTTPS blocked by policy",

    # pfSense firewall log
    "timestamp,interface,action,protocol,src_ip,src_port,dst_ip,dst_port,reason\n2024-01-15T09:30:00Z,em0,block,TCP,192.168.1.50,55001,203.0.113.10,3389,Default deny rule",

    # Cisco Meraki MX firewall
    "timestamp,src_ip,dst_ip,protocol,src_port,dst_port,action,msg\n1705293600,172.16.5.22,10.10.10.1,tcp,44567,22,deny,SSH connection blocked by L7 firewall rule",

    # Generic IDS/SIEM CSV export
    "event_id,timestamp,severity,src_ip,src_port,dst_ip,dst_port,protocol,action,description\nEVT-001,2024-01-15T12:00:00Z,high,198.51.100.9,41000,10.0.0.100,8080,TCP,block,Possible port scan detected from external host",
]
