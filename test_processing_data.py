from collections import Counter
import pytest
from loading import load_nouns_to_disregard

from processing_data import (
    list_of_sentences,
    df_to_review_list,
    total_number_of_reviews,
    adjectives_for_flavor,
    count_adjectives,
    cleaning_dictionary,
    find_optimal_percentage,
    all_the_data,
    identify_common_adjs,
    find_unique_words
)

NOUNS_TO_DISREGARD = load_nouns_to_disregard()
BRAND_NAMES = ['Peets', 'Community', 'Folgers']


# Define sets of test cases.
list_of_sentences_cases = [
    # Check that this function works with an exclamation point.
    ("This is the first test!", ["This is the first test"]),
    # Check that this function works with a period.
    ("This is just a basic test.", ["This is just a basic test"]),
    # Check that this function works with a comma.
    ("Test case, with a comma.", ["Test case, with a comma"]),
    # Check that if there is no punctuation, the entire text is returned.
    ("When I don't have any punctuation", ["When I don't have any\
     punctuation"]),
]

adjectives_for_flavor_cases = [
    # Check that this function will look at more than one review.
    (["Review 1 is great", "Review 2 is fantastic"], ["great", "fantastic"]),
    # Check that function works with negated word.
    (["This review is not good"], ["not good"]),
]

count_adjectives_cases = [
    # Checking to see that the dictionary counts one of each adjective.
    (['spicy', 'sweet', 'bad', 'good'], {'spicy': 1, 'sweet': 1,
     'bad': 1, 'good': 1}),
    # Checking to see that it counts one word multiple times and
    # another word once.
    (['spicy', 'spicy', 'spicy', 'spicy', 'sweet'], {'spicy': 4,
     'sweet': 1}),
]

cleaning_dictionary_cases = [
    # Checking that it doesnt keep strings that are 3 characters or less.
    ({'as': 10, 'bad': 12}, {'bad': 12}),
    # Checking a case where the count is the same, one count higher and
    # one count lower than the cutoff.
    ({'bad': 5, 'good': 4, 'great': 6}, {'great': 6}),
]

identify_common_adjs_cases = [
    # Checking common index as the words here repeat once, twice or three times
    ({'Peets': {'bad': 5, 'good': 4, 'great': 6}, 'Community': {'bad': 1,
     'goody': 4, 'great': 1}, 'Folgers': {'spicy': 1, 'sweet': 4, 'great': 1}},
     ['great', 'bad']),
    # Check what happens when there are no common words
    ({'Peets': {'bad': 5, 'good': 4, 'great': 6}, 'Community': {'spicy':
     1, 'sweet': 4, 'nice': 1}, 'Folgers': {'happy': 23}}, []),
    # Checking common words on the given index.
    ({'Peets': {'bad': 5, 'good': 4, 'great': 6}, 'Community': {'bad':
     1, 'good': 4, 'great': 1}, 'Folgers': {'nice': 1}}, ['bad', 'good',
     'great']),
]

find_unique_words_cases = [
    # Check that function works for basic case.
    ({'Peets': {'full': 5, 'good': 4, 'great': 2}, 'Community': {'full': 1,
     'good': 4, 'dark': 4}, 'Folgers': {'full': 1, 'good': 2, 'heavy': 4}},
     ['full', 'good'], {'Peets': ['great'], 'Community': ['dark'], 'Folgers':
     ['heavy']}),

    # Check that if all the words for one brand are common words,
    # the function will return no words for that brand.
    ({'Peets': {'full': 5, 'good': 4}, 'Community': {'full': 1, 'good': 4,
     'dark': 4}, 'Folgers': {'full': 5, 'good': 2}}, ['full', 'good'],
     {'Peets': [], 'Community': ['dark'], 'Folgers': []}),

    # Check that if common_words is an empty list, the function will return
    # a dict with the same words.
    ({'Peets': {'full': 5, 'good': 4}, 'Community': {'full': 1, 'good': 4,
     'dark': 4}, 'Folgers': {'dark': 4}}, [], {'Peets': ['full', 'good'],
     'Community': ['full', 'good', 'dark'], 'Folgers': ['dark']}),

    # Check that if none of the words in dictionary match the common_words,
    # the function will return a dict with the same words.
    ({'Peets': {'full': 5, 'good': 4}, 'Community': {'full': 1, 'good': 4,
     'dark': 4}, 'Folgers': {'dark': 4}}, ['fruity', 'sweet'], {'Peets':
     ['full', 'good'], 'Community': ['full', 'good', 'dark'], 'Folgers':
     ['dark']}),
]

################################################################################


# Define standard testing functions to check functions' outputs given certain
# inputs defined above.
@pytest.mark.parametrize("text, sentence_list", list_of_sentences_cases)
def test_list_of_sentences(text, sentence_list):
    assert list_of_sentences(text) == sentence_list


@pytest.mark.parametrize("reviews_list, adj_list", adjectives_for_flavor_cases)
def test_adjectives_for_flavor(reviews_list, adj_list):
    assert adjectives_for_flavor(reviews_list, NOUNS_TO_DISREGARD) == adj_list


@pytest.mark.parametrize("adjective_list, adj_dict", count_adjectives_cases)
def test_count_adjectives(adjective_list, adj_dict):
    assert count_adjectives(adjective_list) == adj_dict


@pytest.mark.parametrize("adj_dict, clean_dict", cleaning_dictionary_cases)
def test_cleaning_dictionary(adj_dict, clean_dict):
    assert cleaning_dictionary(adj_dict, 5, 100) == clean_dict


@pytest.mark.parametrize("all_data, common_adjs", identify_common_adjs_cases)
def test_identify_common_adjs(all_data, common_adjs):
    assert Counter(identify_common_adjs(all_data, 2, BRAND_NAMES)) \
        == Counter(common_adjs)


@pytest.mark.parametrize("all_data, common_words, unique_adjs",
                         find_unique_words_cases)
def test_find_unique_words(all_data, common_words, unique_adjs):
    assert find_unique_words(all_data, common_words, BRAND_NAMES) == unique_adjs
