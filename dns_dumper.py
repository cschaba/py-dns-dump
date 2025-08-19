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
    
    def load_custom_subdomains(self, filename: str) -> List[str]:
        """Load custom subdomains from a file"""
        custom_subdomains = []
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    subdomain = line.strip()
                    # Skip empty lines and comments
                    if subdomain and not subdomain.startswith('#'):
                        custom_subdomains.append(subdomain)
            print(f"Loaded {len(custom_subdomains)} custom subdomains from {filename}")
        except FileNotFoundError:
            print(f"Warning: Custom subdomain file '{filename}' not found. Using default list only.")
        except Exception as e:
            print(f"Error reading subdomain file '{filename}': {e}")
        return custom_subdomains
    
    def get_subdomain_list(self, custom_file: Optional[str] = None, target_domain: str = None) -> tuple[List[str], List[str]]:
        """Get the complete list of subdomains to check and full domains to check"""
        subdomains = self.common_subdomains.copy()
        full_domains = []
        
        if custom_file:
            custom_subdomains = self.load_custom_subdomains(custom_file)
            # Separate regular subdomains from full domain names
            added_count = 0
            full_domain_count = 0
            
            for item in custom_subdomains:
                # Check if it's a full domain (contains dots)
                if '.' in item:
                    # If it ends with the target domain, it's a multi-level subdomain
                    if target_domain and item.endswith('.' + target_domain):
                        full_domains.append(item)
                        full_domain_count += 1
                    # If it doesn't contain the target domain at all, it's a completely different domain
                    elif target_domain and target_domain not in item:
                        full_domains.append(item)
                        full_domain_count += 1
                    # If it contains the target domain but doesn't end with it, it's also a full domain
                    elif target_domain and target_domain in item and not item.endswith(target_domain):
                        full_domains.append(item)
                        full_domain_count += 1
                    else:
                        # It's just a regular subdomain with dots
                        if item not in subdomains:
                            subdomains.append(item)
                            added_count += 1
                elif item not in subdomains:
                    subdomains.append(item)
                    added_count += 1
            
            print(f"Added {added_count} new subdomains and {full_domain_count} full domains from custom list")
            print(f"Total: {len(subdomains)} subdomains, {len(full_domains)} full domains")
        else:
            print(f"Using built-in subdomain list ({len(subdomains)} subdomains)")
        
        return subdomains, full_domains
        
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

    def extract_dns_records(self, domain: str, include_subdomains: bool = True, custom_subdomain_file: Optional[str] = None) -> Dict:
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
            
            # Get the complete list of subdomains and full domains to check
            subdomains_to_check, full_domains_to_check = self.get_subdomain_list(custom_subdomain_file, domain)
            
            # Check regular subdomains
            for subdomain in subdomains_to_check:
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
            
            # Check full domains from custom list
            for full_domain in full_domains_to_check:
                subdomain_records = {}
                has_records = False
                
                # Check A, AAAA, and CNAME for full domains
                for record_type in ['A', 'AAAA', 'CNAME']:
                    short_result = self.run_dig_command(full_domain, record_type)
                    
                    if short_result:
                        subdomain_records[record_type] = {
                            'values': short_result.split('\n'),
                            'count': len(short_result.split('\n'))
                        }
                        has_records = True
                
                if has_records:
                    records['subdomains'][full_domain] = subdomain_records
                    subdomain_count += 1
                    print(f"  Found records for: {full_domain}")
            
            print(f"  Total domains/subdomains with records: {subdomain_count}")
        
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
    parser.add_argument('--subdomain-list', metavar='FILE',
                       help='Load additional subdomains from file (one per line)')
    
    args = parser.parse_args()
    
    # Check if dig is available
    try:
        subprocess.run(['dig', '-v'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: 'dig' command not found. Please install bind-utils or dnsutils package.")
        sys.exit(1)
    
    dumper = DNSDumper()
    
    # Extract DNS records
    dns_data = dumper.extract_dns_records(
        args.domain, 
        include_subdomains=not args.no_subdomains,
        custom_subdomain_file=args.subdomain_list
    )
    
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