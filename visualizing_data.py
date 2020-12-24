import matplotlib.pyplot as plt
import matplotlib.pyplot as pPlot
from wordcloud import WordCloud, STOPWORDS
import numpy as npy


def words_with_count(words, brands_dict, brand_names):
    """
    Given a list containing words or a dictionary containing lists of words,
    create a dictionary, with the words as keys and their frequency
    as the values.

    Args:
        words: either a list containing words or a dictionary that has, as
        its values, lists of words.
        brands_dict: dictionary of words mapping to their frequency.
        brand_names: list of strings that correspond to the keys in brands_dict.

    Returns:
        words_with_count: dictionary with the input words as keys
        and their frequency as values.
    """
    # if words is a dictionary, initialize a dictionary with
    # each brand in brand_names as a key
    if type(words) == dict:
        words_with_count = dict.fromkeys(brand_names)
        is_dictionary = True
    # if words is a list, initialize a dictionary with
    # each word as a key, mapping to 0
    else:
        words_with_count = {word: 0 for word in words}
        is_dictionary = False

    for brand in brand_names:
        # if words is a dictionary, map the word_with_count dictionary
        # to a new dictionary with words as keys
        if is_dictionary is True:
            words_with_count[brand] = dict.fromkeys(words[brand])
            # for each word, map the word to its frequency
            # its frequency can be accessed in brands_dict
            for word in words[brand]:
                words_with_count[brand][word] = brands_dict[brand][word]
        # for each word in the brands_dict, if this word is in
        # words, update the frequency count for word in words_with_count
        else:
            keys = list(brands_dict[brand].keys())
            for key in keys:
                if key in words:
                    words_with_count[key] += brands_dict[brand][key]
    return words_with_count


def string_for_wordle(words_with_count, brand_name=None):
    """
    Creates a string of words from a dictionary.

    Every adjective in the input dictionary has its assigned count as the value.
    This creates a string with the adjectives repeated for the amount of times
    given in the count.

    Args:
        words_with_count: A dictionary with adjectives and
        their respective count.
        brand_name: A string which is one of the coffee brands.


    Returns:
        adjectives_string: String with all the adjectives and their count.
    """
    # checking if words_with_count is a dictionary within a dictionary
    first_key = list(words_with_count.keys())[0]
    if type(words_with_count[first_key]) is dict:
        word_count = words_with_count[brand_name]
    else:
        word_count = words_with_count

    # initializing a string and adding the adjective for as many times
    # as it is counted into the string.
    adjectives_string = ''
    for key in word_count:
        count = word_count[key]
        adjectives_string += ((key + ' ') * (count))
    return adjectives_string


def create_word_cloud(adjectives_string, brand='Common Words'):
    """
    Creates a word cloud.

    Args:
        adjectives_string: A string with the number of adjectives.
        brand: The brand that corresponds to the given string of adjectives.
        If no brand is given, it is assumed that the input string is for
        the function are the common words.
    Returns:
        cloud: A cloud which can be plotted as a word cloud.
    """
    # creating a word cloud from a string
    cloud = WordCloud(background_color="beige", colormap='copper',
                      collocations=False)
    cloud.generate(adjectives_string)
    return cloud
