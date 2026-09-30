"""
Sample XML log lines for the ULPF test lab and UI examples page.
Covers: Windows Event Log style, vendor syslog-over-XML, generic network event XML.
"""

SAMPLE_XML_LOGS = [
    # Windows Firewall / Security Event Log style
    '<Event><System><EventID>5156</EventID><TimeCreated>2024-01-15T08:23:41Z</TimeCreated><Computer>WIN-FW01</Computer></System><EventData><Direction>Inbound</Direction><Protocol>6</Protocol><SourceAddress>192.168.10.5</SourceAddress><SourcePort>54321</SourcePort><DestAddress>10.0.0.100</DestAddress><DestPort>445</DestPort><Action>Permit</Action></EventData></Event>',

    # Generic firewall drop event
    '<LogEvent><timestamp>2024-01-15T09:45:00Z</timestamp><action>DROP</action><proto>TCP</proto><src_ip>203.0.113.42</src_ip><src_port>63021</src_port><dst_ip>10.10.10.1</dst_ip><dst_port>22</dst_port><reason>Policy violation: SSH blocked</reason><device>FortiGate-100F</device></LogEvent>',

    # IDS/IPS alert XML
    '<Alert><AlertID>IDS-2024-001</AlertID><Time>2024-01-15T11:00:00Z</Time><Severity>high</Severity><Category>Intrusion</Category><SrcIP>198.51.100.5</SrcIP><DstIP>10.0.0.50</DstIP><DstPort>80</DstPort><Protocol>TCP</Protocol><Message>SQL Injection attempt detected</Message><Action>BLOCK</Action></Alert>',

    # Syslog-over-XML (Juniper SRX style)
    '<syslog><priority>22</priority><timestamp>Jan 15 14:30:00</timestamp><hostname>SRX-EDGE</hostname><application>RT_FLOW</application><message>session denied 172.16.0.10/58433 -&gt; 8.8.8.8/53 None TCP (Trust_Untrust) 4</message></syslog>',
]
