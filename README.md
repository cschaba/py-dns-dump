# DNS Record Dumper

A Python script to extract comprehensive DNS information for domain transfers when dealing with uncooperative domain hosters.

## Prerequisites

- Python 3.6+
- `dig` command (install via `brew install bind` on macOS or `apt-get install dnsutils` on Ubuntu)

## Usage

### Basic usage (text output):
```bash
python3 dns_dumper.py example.com
```

### Save to CSV:
```bash
python3 dns_dumper.py example.com --csv dns_records.csv
```

### Save to JSON:
```bash
python3 dns_dumper.py example.com --json dns_records.json
```

### Save to both formats:
```bash
python3 dns_dumper.py example.com --csv records.csv --json records.json
```

### Quiet mode (minimal output):
```bash
python3 dns_dumper.py example.com --quiet --json records.json
```

### Skip subdomain scanning:
```bash
python3 dns_dumper.py example.com --no-subdomains
```

### Use custom subdomain list:
```bash
python3 dns_dumper.py example.com --subdomain-list custom_subdomains.txt
```

### Fast scanning (skip RFC subdomains):
```bash
python3 dns_dumper.py example.com --skip-rfc-subdomains
```

### Combine built-in and custom subdomains:
```bash
python3 dns_dumper.py example.com --subdomain-list my_subdomains.txt --csv complete_scan.csv
```

## What it extracts

### Main Domain Records
The script queries for these DNS record types:
- A (IPv4 addresses)
- AAAA (IPv6 addresses)  
- CNAME (Canonical names)
- MX (Mail exchange)
- NS (Name servers)
- TXT (Text records)
- SOA (Start of authority)
- PTR (Pointer records)
- SRV (Service records)
- CAA (Certificate authority authorization)
- DNSKEY (DNS public keys)
- DS (Delegation signer)

### Subdomain Records
Automatically checks these common subdomains for A, AAAA, and CNAME records:

**Standard Subdomains:**
- **Web**: www, blog, shop, store, api, cdn, static, img, images, assets
- **Mail**: mail, smtp, pop, imap, webmail, mx1, mx2
- **File Services**: ftp, files, download, uploads
- **Development**: dev, test, staging, beta, demo
- **Support**: support, help, docs, wiki, forum, news
- **Admin**: admin, cpanel, whm, portal, login, secure
- **Infrastructure**: ns1, ns2, vpn, remote
- **Mobile**: mobile, app

**RFC-Defined Service Discovery Subdomains:**
- **Email Services**: _submission._tcp, _submissions._tcp, _imap._tcp, _imaps._tcp, _pop3._tcp, _pop3s._tcp, _smtp._tcp, _smtps._tcp
- **SIP/VoIP**: _sip._tcp, _sip._udp, _sips._tcp, _sips._udp
- **XMPP/Jabber**: _xmpp-client._tcp, _xmpp-server._tcp, _xmpps-client._tcp, _xmpps-server._tcp
- **Web Services**: _http._tcp, _https._tcp, _caldav._tcp, _carddav._tcp, _webdav._tcp
- **Directory Services**: _ldap._tcp, _ldaps._tcp
- **Authentication**: _kerberos._tcp, _kerberos._udp, _kpasswd._tcp, _kpasswd._udp
- **Security Records**: _dmarc, _domainkey, _adsp._domainkey, _spf, _caa, _acme-challenge
- **Other Services**: _dns._tcp, _ntp._udp, _ssh._tcp, _sftp._tcp, _matrix._tcp, _minecraft._tcp

## Output formats

- **Text**: Human-readable console output
- **CSV**: Spreadsheet-compatible format
- **JSON**: Machine-readable structured data

## Custom Subdomain Lists

You can provide your own list of subdomains to scan using the `--subdomain-list` option:

1. Create a text file with one subdomain per line
2. Use `#` for comments
3. Empty lines are ignored
4. Custom subdomains are added to the built-in list (no duplicates)

**Example custom_subdomains.txt:**
```
# My company's subdomains
app1
app2
dashboard
# Regional sites
us
eu
asia
# Multi-level subdomains (full domain names)
api.v2.example.com
```

**Note**: You can include both simple subdomains (like `app1`) and full multi-level domain names (like `www.home.example.com`). The script automatically detects and handles both types.

Perfect for documenting your current DNS setup before transferring domains!