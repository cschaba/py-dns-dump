# Design Document

## Overview

The Random Domain Generator is a Python script that creates realistic-sounding domain names for testing, development, and educational purposes. The system will generate domains that combine authentic word patterns with diverse TLDs and common subdomains, including support for international domain names with special characters.

The design leverages existing patterns from the DNS dumper codebase, particularly the comprehensive subdomain lists and command-line argument handling patterns already established in the project.

## Architecture

The system follows a modular architecture with clear separation of concerns:

```
RandomDomainGenerator
├── WordSources (manages word lists and combinations)
├── TLDManager (handles TLD selection and weighting)
├── SubdomainManager (manages subdomain patterns)
├── InternationalDomainHandler (handles IDN and punycode)
├── DomainAssembler (combines components into valid domains)
└── OutputFormatter (handles output and deduplication)
```

## Components and Interfaces

### 1. WordSources Class
**Purpose:** Manages word lists and realistic name generation patterns

**Key Methods:**
- `load_word_lists()`: Loads categorized word lists (nouns, adjectives, business terms)
- `generate_business_name()`: Creates realistic business name combinations
- `get_random_word(category)`: Returns random word from specified category
- `get_international_words(language)`: Returns words with international characters

**Word Categories:**
- Common nouns (tech, business, general)
- Descriptive adjectives
- Business suffixes (tech, solutions, group, inc, corp)
- International words (German with äöüß, etc.)

### 2. TLDManager Class
**Purpose:** Handles TLD selection with realistic weighting

**Key Methods:**
- `load_tld_list()`: Loads comprehensive TLD list with weights
- `get_weighted_tld()`: Returns TLD based on realistic usage patterns
- `get_country_tld(country)`: Returns country-specific TLD

**TLD Categories:**
- Generic TLDs (.com, .org, .net) - high weight
- Country code TLDs (.de, .uk, .ca) - medium weight  
- New generic TLDs (.tech, .shop, .app) - lower weight
- Specialized TLDs (.edu, .gov, .mil) - very low weight

### 3. SubdomainManager Class
**Purpose:** Manages subdomain selection and patterns

**Key Methods:**
- `get_random_subdomain()`: Returns random subdomain or None
- `should_include_subdomain()`: Determines if subdomain should be added
- `load_subdomain_patterns()`: Loads subdomain lists

**Subdomain Sources:**
- Reuses existing subdomain lists from dns_dumper.py
- Standard web subdomains (www, mail, api, cdn)
- Technical subdomains (admin, dev, staging)
- Service subdomains (blog, shop, support)

### 4. InternationalDomainHandler Class
**Purpose:** Handles international domain names and encoding

**Key Methods:**
- `encode_to_punycode(domain)`: Converts IDN to punycode
- `is_international_domain(domain)`: Checks if domain contains international chars
- `get_international_word(language)`: Returns word with special characters
- `validate_idn(domain)`: Ensures IDN compliance

**Supported Languages:**
- German (äöüß characters)
- Extensible for other languages in future

### 5. DomainAssembler Class
**Purpose:** Combines components into valid domain names

**Key Methods:**
- `assemble_domain(components)`: Creates complete domain from parts
- `validate_domain_format(domain)`: Ensures valid domain format
- `apply_domain_rules()`: Applies domain naming rules and constraints

**Assembly Logic:**
- Combines word components into realistic business names
- Adds appropriate TLD based on name characteristics
- Optionally prepends subdomain
- Ensures proper formatting (lowercase, valid characters)

### 6. OutputFormatter Class
**Purpose:** Handles output formatting and deduplication

**Key Methods:**
- `format_output(domains)`: Formats domain list for output
- `ensure_no_duplicates(domains)`: Removes duplicate domains
- `display_summary(count)`: Shows generation summary

## Data Models

### Domain Components Structure
```python
@dataclass
class DomainComponents:
    business_name: str
    tld: str
    subdomain: Optional[str] = None
    is_international: bool = False
    language: Optional[str] = None
```

### Word Lists Structure
```python
WORD_CATEGORIES = {
    'nouns': ['tech', 'data', 'cloud', 'digital', 'systems', ...],
    'adjectives': ['smart', 'global', 'secure', 'advanced', 'rapid', ...],
    'business_suffixes': ['tech', 'solutions', 'group', 'corp', 'inc', ...],
    'german_words': ['müller', 'bäcker', 'größe', 'weiß', ...]
}
```

### TLD Weights Structure
```python
TLD_WEIGHTS = {
    '.com': 40,
    '.org': 15,
    '.net': 10,
    '.de': 8,
    '.co.uk': 5,
    '.tech': 3,
    '.app': 2,
    # ... more TLDs with appropriate weights
}
```

## Error Handling

### Input Validation
- Validate command-line arguments (count must be positive integer)
- Handle invalid or missing word list files gracefully
- Provide clear error messages for malformed inputs

### Generation Errors
- Handle cases where word lists are empty or corrupted
- Implement fallback mechanisms for failed domain generation
- Ensure graceful degradation when international character encoding fails

### Output Errors
- Handle file system errors for output operations
- Manage memory constraints for large domain generation requests
- Provide progress feedback for long-running operations

## Testing Strategy

### Unit Tests
- Test each component class independently
- Verify word list loading and selection logic
- Test TLD weighting and selection algorithms
- Validate international domain encoding/decoding
- Test domain assembly and validation rules

### Integration Tests
- Test complete domain generation workflow
- Verify realistic domain output patterns
- Test command-line interface functionality
- Validate output formatting and deduplication

### Property-Based Tests
- Generate large numbers of domains and verify all are valid
- Test that no duplicates are produced in single runs
- Verify international domains are properly encoded
- Ensure all generated domains follow naming conventions

### Performance Tests
- Measure generation speed for various domain counts
- Test memory usage for large generation requests
- Verify reasonable response times for typical use cases

## Implementation Notes

### Leveraging Existing Code
- Reuse subdomain lists from existing dns_dumper.py
- Follow established command-line argument patterns
- Use similar project structure and coding style

### Extensibility Considerations
- Design word lists to be easily expandable
- Make TLD weights configurable via external files
- Structure international support for easy language additions
- Allow custom word list injection for specialized use cases

### Performance Optimizations
- Pre-load and cache word lists at startup
- Use efficient random selection algorithms
- Implement lazy loading for large word lists
- Consider memory-efficient approaches for very large generation requests