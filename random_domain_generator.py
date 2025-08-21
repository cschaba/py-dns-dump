#!/usr/bin/env python3
"""
Random Domain Generator - Generate realistic-sounding domain names for testing and development
"""

import argparse
import sys
from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum


@dataclass
class DomainComponents:
    """Core data structure representing components of a domain name"""
    business_name: str
    tld: str
    subdomain: Optional[str] = None
    is_international: bool = False
    language: Optional[str] = None


class WordCategory(Enum):
    """Enumeration of word categories for domain generation"""
    NOUNS = "nouns"
    ADJECTIVES = "adjectives"
    BUSINESS_SUFFIXES = "business_suffixes"
    GERMAN_WORDS = "german_words"


# Word categories for realistic domain name generation
WORD_CATEGORIES = {
    WordCategory.NOUNS.value: [
        'tech', 'data', 'cloud', 'digital', 'systems', 'solutions', 'services',
        'network', 'security', 'software', 'web', 'mobile', 'app', 'platform',
        'innovation', 'consulting', 'development', 'design', 'media', 'marketing'
    ],
    WordCategory.ADJECTIVES.value: [
        'smart', 'global', 'secure', 'advanced', 'rapid', 'modern', 'dynamic',
        'innovative', 'professional', 'reliable', 'efficient', 'creative',
        'strategic', 'premium', 'elite', 'expert', 'leading', 'prime', 'core', 'next'
    ],
    WordCategory.BUSINESS_SUFFIXES.value: [
        'tech', 'solutions', 'group', 'corp', 'inc', 'ltd', 'company', 'enterprises',
        'systems', 'services', 'consulting', 'partners', 'associates', 'ventures',
        'innovations', 'dynamics', 'works', 'labs', 'studio', 'agency'
    ],
    WordCategory.GERMAN_WORDS.value: [
        'müller', 'bäcker', 'größe', 'weiß', 'straße', 'büro', 'geschäft',
        'lösung', 'größer', 'schön', 'grün', 'blau', 'süß', 'heiß', 'kühl'
    ]
}


# TLD weights for realistic distribution
TLD_WEIGHTS = {
    '.com': 40,
    '.org': 15,
    '.net': 10,
    '.de': 8,
    '.co.uk': 5,
    '.ca': 4,
    '.au': 3,
    '.fr': 3,
    '.tech': 3,
    '.io': 2,
    '.app': 2,
    '.dev': 2,
    '.shop': 2,
    '.online': 1,
    '.store': 1,
    '.site': 1,
    '.website': 1,
    '.biz': 1,
    '.info': 1,
    '.eu': 1,
    '.us': 1,
    '.jp': 1,
    '.cn': 1,
    '.in': 1,
    '.br': 1,
    '.mx': 1,
    '.es': 1,
    '.it': 1,
    '.nl': 1,
    '.se': 1,
    '.no': 1,
    '.dk': 1,
    '.fi': 1,
    '.pl': 1,
    '.cz': 1,
    '.at': 1,
    '.ch': 1,
    '.be': 1,
    '.pt': 1,
    '.gr': 1,
    '.ru': 1,
    '.kr': 1,
    '.sg': 1,
    '.hk': 1,
    '.tw': 1,
    '.th': 1,
    '.my': 1,
    '.id': 1,
    '.ph': 1,
    '.vn': 1,
    '.nz': 1,
    '.za': 1
}


class RandomDomainGenerator:
    """Main class for generating realistic random domain names"""
    
    def __init__(self):
        """Initialize the domain generator with default settings"""
        self.word_categories = WORD_CATEGORIES
        self.tld_weights = TLD_WEIGHTS
        
    def generate_domains(self, count: int) -> List[str]:
        """
        Generate the specified number of random domain names
        
        Args:
            count: Number of domains to generate
            
        Returns:
            List of generated domain names
        """
        # Placeholder implementation - will be implemented in later tasks
        domains = []
        for i in range(count):
            domains.append(f"example{i+1}.com")
        return domains
    
    def validate_count(self, count: int) -> bool:
        """
        Validate that the domain count is valid
        
        Args:
            count: Number of domains to generate
            
        Returns:
            True if count is valid, False otherwise
        """
        return isinstance(count, int) and count > 0


def main():
    """Main entry point for the random domain generator"""
    parser = argparse.ArgumentParser(
        description='Generate realistic-sounding random domain names for testing and development'
    )
    parser.add_argument(
        'count', 
        nargs='?', 
        type=int, 
        default=10,
        help='Number of domains to generate (default: 10)'
    )
    parser.add_argument(
        '--quiet', '-q', 
        action='store_true',
        help='Suppress summary output'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not isinstance(args.count, int) or args.count <= 0:
        print("Error: Domain count must be a positive integer.", file=sys.stderr)
        sys.exit(1)
    
    # Initialize generator
    generator = RandomDomainGenerator()
    
    # Validate count
    if not generator.validate_count(args.count):
        print("Error: Invalid domain count specified.", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Generate domains
        domains = generator.generate_domains(args.count)
        
        # Output domains (one per line)
        for domain in domains:
            print(domain)
        
        # Display summary unless quiet mode
        if not args.quiet:
            print(f"\nGenerated {len(domains)} domain names.", file=sys.stderr)
            
    except Exception as e:
        print(f"Error generating domains: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()