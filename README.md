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
- **Web**: www, blog, shop, store, api, cdn, static, img, images, assets
- **Mail**: mail, smtp, pop, imap, webmail, mx1, mx2
- **File Services**: ftp, files, download, uploads
- **Development**: dev, test, staging, beta, demo
- **Support**: support, help, docs, wiki, forum, news
- **Admin**: admin, cpanel, whm, portal, login, secure
- **Infrastructure**: ns1, ns2, vpn, remote
- **Mobile**: mobile, app

## Output formats

- **Text**: Human-readable console output
- **CSV**: Spreadsheet-compatible format
- **JSON**: Machine-readable structured data

Perfect for documenting your current DNS setup before transferring domains!