import unittest

from utils.term_matching import contains_term


class TermMatchingTests(unittest.TestCase):
    def test_substrings_are_not_skills(self):
        for text, term in [('JavaScript developer', 'Java'), ('research', 'R'),
                           ('React', 'C'), ('MySQL', 'SQL'), ('C++ C#', 'C')]:
            with self.subTest(text=text, term=term):
                self.assertFalse(contains_term(text, term))

    def test_literal_languages_and_separators(self):
        for term in ['C++', 'C#', '.NET', 'Python', 'SQL', 'Java']:
            with self.subTest(term=term):
                self.assertTrue(contains_term('C++, C#, .NET; Python/SQL; Java-based', term))

    def test_phrases_case_and_empty(self):
        self.assertTrue(contains_term('MACHINE\n learning experience', 'machine learning'))
        self.assertFalse(contains_term('anything', '  '))
        self.assertFalse(contains_term('machine learnings', 'machine learning'))
