#!/usr/bin/env python3
"""
Unit tests for WordSources class in random_domain_generator.py
"""

import unittest
from unittest.mock import patch
from random_domain_generator import WordSources, WordCategory


class TestWordSources(unittest.TestCase):
    """Test cases for WordSources class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.word_sources = WordSources()
    
    def test_load_word_lists(self):
        """Test that word lists are properly loaded"""
        word_lists = self.word_sources.word_lists
        
        # Check that all expected categories are present
        expected_categories = [
            WordCategory.NOUNS.value,
            WordCategory.ADJECTIVES.value,
            WordCategory.BUSINESS_SUFFIXES.value,
            WordCategory.GERMAN_WORDS.value
        ]
        
        for category in expected_categories:
            self.assertIn(category, word_lists)
            self.assertIsInstance(word_lists[category], list)
            self.assertGreater(len(word_lists[category]), 0)
    
    def test_get_random_word_valid_category(self):
        """Test getting random word from valid category"""
        # Test each category
        for category in [WordCategory.NOUNS.value, WordCategory.ADJECTIVES.value, 
                        WordCategory.BUSINESS_SUFFIXES.value, WordCategory.GERMAN_WORDS.value]:
            word = self.word_sources.get_random_word(category)
            self.assertIsInstance(word, str)
            self.assertIn(word, self.word_sources.word_lists[category])
    
    def test_get_random_word_invalid_category(self):
        """Test that invalid category raises ValueError"""
        with self.assertRaises(ValueError) as context:
            self.word_sources.get_random_word("invalid_category")
        
        self.assertIn("Unknown word category", str(context.exception))
    
    def test_get_random_word_empty_category(self):
        """Test that empty category raises ValueError"""
        # Mock an empty word list
        self.word_sources.word_lists["empty_category"] = []
        
        with self.assertRaises(ValueError) as context:
            self.word_sources.get_random_word("empty_category")
        
        self.assertIn("Empty word list", str(context.exception))
    
    def test_get_international_words_german(self):
        """Test getting German words with international characters"""
        german_words = self.word_sources.get_international_words("german")
        
        self.assertIsInstance(german_words, list)
        self.assertGreater(len(german_words), 0)
        
        # Check that some words contain German special characters
        has_special_chars = any(
            any(char in word for char in ['ä', 'ö', 'ü', 'ß']) 
            for word in german_words
        )
        self.assertTrue(has_special_chars, "German word list should contain special characters")
    
    def test_get_international_words_unsupported_language(self):
        """Test that unsupported language raises ValueError"""
        with self.assertRaises(ValueError) as context:
            self.word_sources.get_international_words("french")
        
        self.assertIn("Unsupported language", str(context.exception))
    
    def test_generate_business_name_format(self):
        """Test that generated business names are properly formatted"""
        for _ in range(10):  # Test multiple generations
            business_name = self.word_sources.generate_business_name()
            
            # Check basic format requirements
            self.assertIsInstance(business_name, str)
            self.assertGreater(len(business_name), 0)
            self.assertEqual(business_name, business_name.lower())  # Should be lowercase
            self.assertFalse(business_name.isspace())  # Should not be just whitespace
    
    def test_generate_business_name_contains_valid_words(self):
        """Test that generated business names contain words from our lists"""
        # Generate multiple names to test different patterns
        for _ in range(20):
            business_name = self.word_sources.generate_business_name()
            
            # Check that the name contains at least one word from our categories
            all_words = []
            for category_words in self.word_sources.word_lists.values():
                all_words.extend(category_words)
            
            # The business name should contain at least one of our words
            contains_our_word = any(word in business_name for word in all_words)
            self.assertTrue(contains_our_word, 
                          f"Business name '{business_name}' should contain words from our lists")
    
    def test_generate_business_name_patterns(self):
        """Test that business names follow realistic patterns"""
        # Mock random.choice to test specific patterns
        with patch('random_domain_generator.random.choice') as mock_choice:
            # Test single noun pattern
            mock_choice.side_effect = [
                lambda: "tech",  # Pattern selection
                "tech"  # Word selection
            ]
            
            # We need to create a new instance to get the mocked behavior
            word_sources = WordSources()
            name = word_sources.generate_business_name()
            self.assertEqual(name, "tech")
    
    def test_generate_international_business_name_german(self):
        """Test generating German business names with international characters"""
        german_name = self.word_sources.generate_international_business_name("german")
        
        self.assertIsInstance(german_name, str)
        self.assertGreater(len(german_name), 0)
        self.assertEqual(german_name, german_name.lower())
        
        # Should contain either a German word or end with common suffixes
        german_words = self.word_sources.get_international_words("german")
        contains_german_word = any(word in german_name for word in german_words)
        has_tech_suffix = german_name.endswith(('tech', 'solutions', 'group'))
        
        self.assertTrue(contains_german_word or has_tech_suffix,
                       f"German name '{german_name}' should contain German words or tech suffixes")
    
    def test_generate_international_business_name_unsupported_language(self):
        """Test that unsupported language raises ValueError"""
        with self.assertRaises(ValueError) as context:
            self.word_sources.generate_international_business_name("french")
        
        self.assertIn("Unsupported language", str(context.exception))
    
    def test_word_list_quality(self):
        """Test that word lists contain quality, realistic words"""
        # Test that noun list contains tech-related words
        nouns = self.word_sources.word_lists[WordCategory.NOUNS.value]
        tech_words = ['tech', 'data', 'cloud', 'digital', 'software']
        for word in tech_words:
            self.assertIn(word, nouns, f"Noun list should contain '{word}'")
        
        # Test that adjectives list contains descriptive words
        adjectives = self.word_sources.word_lists[WordCategory.ADJECTIVES.value]
        descriptive_words = ['smart', 'global', 'secure', 'advanced', 'innovative']
        for word in descriptive_words:
            self.assertIn(word, adjectives, f"Adjective list should contain '{word}'")
        
        # Test that business suffixes contain common business terms
        suffixes = self.word_sources.word_lists[WordCategory.BUSINESS_SUFFIXES.value]
        business_terms = ['tech', 'solutions', 'group', 'corp', 'inc']
        for word in business_terms:
            self.assertIn(word, suffixes, f"Business suffix list should contain '{word}'")
    
    def test_business_name_generation_variety(self):
        """Test that business name generation produces variety"""
        # Generate multiple names and check for variety
        names = set()
        for _ in range(50):
            name = self.word_sources.generate_business_name()
            names.add(name)
        
        # Should generate at least 20 unique names out of 50 attempts
        self.assertGreaterEqual(len(names), 20, 
                               "Business name generation should produce variety")
    
    def test_international_name_generation_variety(self):
        """Test that international business name generation produces variety"""
        # Generate multiple German names and check for variety
        names = set()
        for _ in range(30):
            name = self.word_sources.generate_international_business_name("german")
            names.add(name)
        
        # Should generate at least 10 unique names out of 30 attempts
        self.assertGreaterEqual(len(names), 10, 
                               "International name generation should produce variety")


if __name__ == '__main__':
    unittest.main()