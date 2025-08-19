#!/usr/bin/env python3
"""
DNS Record Dumper - Extract comprehensive DNS information for domain transfers
"""

import argparse
import json
import csv
import sys
import subprocess
from typing import Dict, List, Optional
from datetime import datetime

class DNSDumper:
    def __init__(self):
        self.common_record_types = [
            'A', 'AAAA', 'CNAME', 'MX', 'NS', 'TXT', 'SOA', 
            'PTR', 'SRV', 'CAA', 'DNSKEY', 'DS'
        ]
        self.common_subdomains = [
            'www', 'mail', 'ftp', 'smtp', 'pop', 'imap', 'webmail',
            'admin', 'blog', 'shop', 'store', 'api', 'cdn', 'static',
            'img', 'images', 'assets', 'files', 'download', 'uploads',
            'dev', 'test', 'staging', 'beta', 'demo', 'support',
            'help', 'docs', 'wiki', 'forum', 'news', 'mobile',
            'app', 'secure', 'vpn', 'remote', 'portal', 'login',
            'cpanel', 'whm', 'ns1', 'ns2', 'mx1', 'mx2'
        ]
        
    def run_dig_command(self, domain: str, record_type: str) -> Optional[str]:
        """Run dig command and return output"""
        try:
            cmd = ['dig', '+short', f'@8.8.8.8', domain, record_type]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            print(f"Error running dig for {record_type}: {e}", file=sys.stderr)
        return None
    
    def get_detailed_record(self, domain: str, record_type: str) -> Optional[str]:
        """Get detailed record information"""
        try:
            cmd = ['dig', f'@8.8.8.8', domain, record_type]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return result.stdout
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        return None

    def extract_dns_records(self, domain: str, include_subdomains: bool = True) -> Dict:
        """Extract all DNS records for a domain and its subdomains"""
        records = {
            'domain': domain,
            'timestamp': datetime.now().isoformat(),
            'records': {},
            'subdomains': {}
        }
        
        print(f"Extracting DNS records for: {domain}")
        
        # Extract records for main domain
        print(f"\n--- Main domain: {domain} ---")
        for record_type in self.common_record_types:
            print(f"  Checking {record_type} records...", end='')
            
            # Get short format
            short_result = self.run_dig_command(domain, record_type)
            
            if short_result:
                records['records'][record_type] = {
                    'values': short_result.split('\n'),
                    'count': len(short_result.split('\n'))
                }
                print(f" Found {len(short_result.split('\n'))} record(s)")
                
                # Get detailed format for important records
                if record_type in ['SOA', 'NS', 'MX']:
                    detailed = self.get_detailed_record(domain, record_type)
                    if detailed:
                        records['records'][record_type]['detailed'] = detailed
            else:
                print(" None found")
        
        # Extract records for subdomains
        if include_subdomains:
            print(f"\n--- Checking subdomains ---")
            subdomain_count = 0
            
            for subdomain in self.common_subdomains:
                full_subdomain = f"{subdomain}.{domain}"
                subdomain_records = {}
                has_records = False
                
                # Only check A, AAAA, and CNAME for subdomains (most relevant)
                for record_type in ['A', 'AAAA', 'CNAME']:
                    short_result = self.run_dig_command(full_subdomain, record_type)
                    
                    if short_result:
                        subdomain_records[record_type] = {
                            'values': short_result.split('\n'),
                            'count': len(short_result.split('\n'))
                        }
                        has_records = True
                
                if has_records:
                    records['subdomains'][full_subdomain] = subdomain_records
                    subdomain_count += 1
                    print(f"  Found records for: {full_subdomain}")
            
            print(f"  Total subdomains with records: {subdomain_count}")
        
        return records

    def output_text(self, data: Dict):
        """Output in human-readable text format"""
        print(f"\n{'='*60}")
        print(f"DNS RECORDS FOR: {data['domain']}")
        print(f"Extracted on: {data['timestamp']}")
        print(f"{'='*60}")
        
        # Main domain records
        print(f"\nMAIN DOMAIN RECORDS:")
        for record_type, info in data['records'].items():
            print(f"\n{record_type} Records ({info['count']} found):")
            print("-" * 40)
            for value in info['values']:
                print(f"  {value}")
            
            if 'detailed' in info:
                print(f"\nDetailed {record_type} Information:")
                print(info['detailed'])
        
        # Subdomain records
        if 'subdomains' in data and data['subdomains']:
            print(f"\n{'='*60}")
            print(f"SUBDOMAIN RECORDS ({len(data['subdomains'])} found):")
            print(f"{'='*60}")
            
            for subdomain, records in data['subdomains'].items():
                print(f"\n{subdomain}:")
                print("-" * len(subdomain))
                for record_type, info in records.items():
                    print(f"  {record_type}: {', '.join(info['values'])}")
        else:
            print(f"\nNo subdomain records found.")

    def output_csv(self, data: Dict, filename: str):
        """Output in CSV format"""
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Domain', 'Subdomain', 'Record Type', 'Value', 'Timestamp'])
            
            # Main domain records
            for record_type, info in data['records'].items():
                for value in info['values']:
                    writer.writerow([data['domain'], '', record_type, value, data['timestamp']])
            
            # Subdomain records
            if 'subdomains' in data:
                for subdomain, records in data['subdomains'].items():
                    for record_type, info in records.items():
                        for value in info['values']:
                            writer.writerow([data['domain'], subdomain, record_type, value, data['timestamp']])
        
        print(f"CSV output saved to: {filename}")

    def output_json(self, data: Dict, filename: str):
        """Output in JSON format"""
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2, ensure_ascii=False)
        
        print(f"JSON output saved to: {filename}")

def main():
    parser = argparse.ArgumentParser(
        description='Extract comprehensive DNS records for domain transfers'
    )
    parser.add_argument('domain', help='Domain to analyze')
    parser.add_argument('--csv', help='Save results to CSV file')
    parser.add_argument('--json', help='Save results to JSON file')
    parser.add_argument('--quiet', '-q', action='store_true', 
                       help='Suppress progress output')
    parser.add_argument('--no-subdomains', action='store_true',
                       help='Skip subdomain scanning')
    
    args = parser.parse_args()
    
    # Check if dig is available
    try:
        subprocess.run(['dig', '-v'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: 'dig' command not found. Please install bind-utils or dnsutils package.")
        sys.exit(1)
    
    dumper = DNSDumper()
    
    # Extract DNS records
    dns_data = dumper.extract_dns_records(args.domain, include_subdomains=not args.no_subdomains)
    
    # Output results
    if not args.quiet:
        dumper.output_text(dns_data)
    
    if args.csv:
        dumper.output_csv(dns_data, args.csv)
    
    if args.json:
        dumper.output_json(dns_data, args.json)
    
    # Summary
    total_main_records = sum(info['count'] for info in dns_data['records'].values())
    total_subdomain_records = 0
    if 'subdomains' in dns_data:
        for subdomain_records in dns_data['subdomains'].values():
            total_subdomain_records += sum(info['count'] for info in subdomain_records.values())
    
    print(f"\nSummary:")
    print(f"  Main domain: {total_main_records} DNS records across {len(dns_data['records'])} record types")
    if 'subdomains' in dns_data and dns_data['subdomains']:
        print(f"  Subdomains: {total_subdomain_records} records across {len(dns_data['subdomains'])} subdomains")
    print(f"  Total: {total_main_records + total_subdomain_records} DNS records")

if __name__ == '__main__':
    main()