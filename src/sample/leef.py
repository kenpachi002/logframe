"""
Sample LEEF log lines for the ULPF test lab and UI examples page.
LEEF (Log Event Extended Format) is used by IBM QRadar and compatible devices.
Covers: IBM QRadar LEEF 1.0, LEEF 2.0, Juniper SA, generic security event.
"""

SAMPLE_LEEF_LOGS = [
    # LEEF 1.0 — Juniper Steel-Belted Radius authentication event
    "LEEF:1.0|Juniper|Steel-Belted Radius|6.1.3|DiscardAuthRequest\tsrc=192.168.10.22\tdst=10.0.0.1\tsrcPort=1812\tdstPort=1812\tproto=UDP\tdevTime=Jan 15 2024 08:00:00\tusrName=jdoe\tmsg=Auth request discarded - invalid credentials",

    # LEEF 1.0 — IBM QRadar network connection allowed
    "LEEF:1.0|IBM|QRadar|7.4.0|NetworkAllow\tsrc=10.0.0.5\tdst=203.0.113.20\tsrcPort=52000\tdstPort=443\tproto=TCP\tdevTime=Jan 15 2024 09:15:00\tmsg=Outbound HTTPS connection permitted",

    # LEEF 2.0 — pipe-delimited extension with custom delimiter
    "LEEF:2.0|Cisco|IDS|12.1|TCP_SYN_Flood|^\tsrc=198.51.100.1\tdstPort=80\tproto=TCP\tdevTime=Jan 15 2024 10:30:00\tmsg=SYN Flood detected - threshold exceeded",

    # LEEF 1.0 — Firewall block event
    "LEEF:1.0|Check Point|Firewall-1|R80.30|FirewallDrop\tsrc=172.16.100.5\tdst=10.10.10.1\tsrcPort=45678\tdstPort=22\tproto=TCP\tdevTime=Jan 15 2024 14:00:00\tmsg=SSH connection attempt blocked by policy",
]
