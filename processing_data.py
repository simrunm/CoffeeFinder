import pandas as pd
import nltk
import numpy as npy


def list_of_sentences(text):
    """
    Given a string, divide it into a list of the sentences.

    Args:
        text: string of text.

    Returns:
        sentence_list: list of sentences that make up text.
    """
    sentence_list = []
    start_i = 0
    for index in range(len(text)):
        if text[index] in ".!?":
            sentence = text[start_i:index]
            sentence_list.append(sentence)
            start_i = index + 2
    # if reached the end of the text and there is
    # no ending punctuation, append that last sentence
    if index == len(text) - 1 and text[index] not in ".!?":
        sentence = text[start_i:index + 1]
        sentence_list.append(sentence)
    # if the text does not have any punctuation,
    # assume the entire text is a sentence
    if sentence_list == []:
        return text
    return sentence_list


def df_to_review_list(df):
    """
    Given a dataframe, return a list with each review as one list item.

    Args:
        df: A pandas dataframe with all the reviews for one coffee.

    Returns:
        review_list: A list of all reviews for one coffee.
    """
    # The contents of the dataframe under the header 'Review_text'
    # contains all the reviews for one coffee
    reviews_list = df['Review_text'].to_list()
    return reviews_list


def total_number_of_reviews(df):
    """
    Finds the number of reviews by finding the row count.

    Args:
        df: A pandas dataframe with all the reviews for one coffee.

    Returns:
        An integer containing the number of reviews.
    """
    # this returns the number of rows which is the number of reviews
    return df.shape[0]


def adjectives_for_flavor(reviews_list, nouns_to_disregard):
    """
    Create a list of adjectives that are in the review list.

    To filter out adjectives from the list, we created a list of nouns
    related to shipping, packaging and expiry. If any of those nouns are in a
    sentence, then any adjectives in that sentence are not included.
    The assumption is that all adjectives that are not related to
    shipping, packaging and expiry are related to flavor.

    Args:
        reviews_list: A list of all reviews for one coffee.
        nouns_to_disregard: A list of words that are related to
        packaging and expiry and this list is used to get rid
        of adjectives that are not related to flavor.

    Returns:
        adjectives: A list containing adjectives that are related to flavor.
    """
    adjectives = []
    # Making each review lowercase and making each
    # sentence in all the reviews a new list item
    # in the setence_list.
    for review in reviews_list:
        review = review.lower()
        sentence_list = list_of_sentences(review)
        # Using the nltk library to give each word a token and its tag which
        # represents a list of tuples containing each word and its
        #  corresponding part of speech
        for sentence in sentence_list:
            tokens = nltk.word_tokenize(sentence)
            for token in tokens:
                token = token.lower()
            tagged = nltk.pos_tag(tokens)
            # creating a loop that wont include the adjective in the final
            # list if there are nouns related to shipping and packaging in
            # that sentence
            include_adj = True
            for noun in nouns_to_disregard:
                if noun in sentence.lower():
                    include_adj = False
                    break
            # Including the word in a list if it was tagged as an adjective
            # and the sentence it is in doesnt contains any of the nouns to
            # disregard.
            for i in range(len(tagged)):
                if tagged[i][1] == 'JJ' and include_adj is True:
                    # If the adjective has the word not or never in front of it
                    # include both in the adjectives list
                    if (tagged[i - 1][0].lower() == 'not' or (
                            tagged[i - 1][0].lower() == 'never')):
                        adjectives.append(tagged[i - 1][0] + ' ' + tagged[i][0])
                    else:
                        # otherwise just include the adjective
                        adjectives.append(tagged[i][0])
    return adjectives


def count_adjectives(adjective_list):
    """
    Returns a dictionary with the count of adjectives in the list.

    Args:
        adjective_list: A list containing adjectives related to flavor.

    Returns:
        adj_dict: A dictionary containing each adjective in the list
        and how many times it shows up in that same list.
    """
    adj_dict = {}
    for adjective in adjective_list:
        # Adding a count to the value for the dictionary if it
        # is already in the dictionary
        if adjective in adj_dict:
            adj_dict[adjective] += 1
        # Make the count one if its the first time the adjective
        # has appeared.
        else:
            adj_dict[adjective] = 1
    return adj_dict


def cleaning_dictionary(adj_dict, percentage, number_reviews):
    """
    Given a dictionary, filter unneeded words and characters.

    This filters out words that show up as single or double characters because
    they arent adjectives. We are also filtering adjectives that dont show up
    often enough in the reviews. We are assuming that if number of times an
    adjective shows up in the list is higher than the input percentage,
    it means that this adjective is representative of what the coffee actually
    tastes like.

    Args:
        adj_dict: A dictionary with adjectives as keys and their count as values
        percentage: An integer which represents the cutoff percentage for
        whether this adjective shows up in enough reviews or not.
        number_reviews: An integer representing the total number of
        reviews for any given coffee.

    Returns:
        clean_dict: A dictionary containing adjectives that are above
        a certain threshold percentage for how many people used them.
    """
    clean_dict = {}
    for key in adj_dict:
        # removing the single and double characters and also removing the
        # words that are not over the cutoff percentage
        if (len(key) >= 3 and adj_dict[key] > (
                ((percentage / 100) * number_reviews))):
            clean_dict[key] = adj_dict[key]
    return clean_dict


def find_optimal_percentage(adj_dict, desired_num, number_of_reviews):
    """
    Find the cutoff percentage that will return the desired number of words.

    This function is used to find what is the optimal cutoff percentage to input
    into the cleaning_dictionary function so that the desired number of
    words is returned.

    Args:
        adj_dict: A dictionary with adjectives as keys and their count as
        values.
        desired_num: integer representing how many adjectives are wanted
        for each brand of coffee.
        number_of_reviews: An integer representing the total number of reviews
        for any brand.

    Returns:
        optimal_percentage: An int that is the optimal percentage that will make
        the cleaning_dictionary function return the desired number of words.
    """
    # creating a range of precentages and sweeping through them
    # to find the number of words in the adjectives dictionary
    for percentage in npy.arange(1, 100, 0.5).tolist():
        clean_dict = (cleaning_dictionary(adj_dict, percentage, (
            number_of_reviews)))
        clean_dict_keys = list(clean_dict.keys())
        # The percentage that leads to the number of words in the dictionary
        # being closest to what was inputted as the desired number is returned
        # as the optimum percentage
        if len(clean_dict_keys) <= desired_num:
            optimal_percentage = percentage
            break
    return optimal_percentage


def all_the_data(brand_names, nouns_to_disregard):
    """
    Return a dictionary of adjectives for each coffee brand.

    Args:
        brand_names: A list of all the brand names for the various coffees.
        nouns_to_disregard: A list of words that are related to
        packaging and expiry and this list is used to get rid
        of adjectives that are not related to flavor.
    Returns:
        all_data: A dictionary with the brands as keys mapping to a
        dictionary of adjectives for the corresponding coffee brand.

    """
    all_data = {}
    # creating a dictionary of adjectives for each brand by looping through
    # the brand names and using all the previous functions
    for brand in brand_names:
        df = pd.read_csv(brand)
        number_of_reviews = total_number_of_reviews(df)
        reviews_list = df_to_review_list(df)
        adjective_list = adjectives_for_flavor(reviews_list, nouns_to_disregard)
        adj_dict = count_adjectives(adjective_list)
        optimal_percentage = find_optimal_percentage(adj_dict, 15, (
            number_of_reviews))
        clean_dict = cleaning_dictionary(adj_dict, optimal_percentage, (
            number_of_reviews))
        all_data[brand] = clean_dict
    return all_data


def identify_common_adjs(all_data, common_index, brand_names):
    """
    Find the words that are commonly shared across different brands.

    Args:
        all_data: A dictionary with the brands as keys mapping to a
        dictionary of adjectives for the corresponding coffee brand.
        common_index: index that defines the number of brands that an adjective
        has to appear in to be considered a common word.
        brand_names: A list of all the brand names for the various coffees.

    Returns:
        common_words: list of words that are highly shared across brands.
    """
    all_adjs = []
    # populate all_adjs list with all adjectives in each brand
    for brand in brand_names:
        keys = list(all_data[brand].keys())
        all_adjs += (keys)
    all_adjs_count = {}
    # create dictionary that contains each adj as a key
    # with the number of brands it appears in as the value
    for adj in set(all_adjs):
        for brand in brand_names:
            keys = list(all_data[brand].keys())
            if adj in keys:
                if adj in all_adjs_count:
                    all_adjs_count[adj] += 1
                else:
                    all_adjs_count[adj] = 1
    common_words = []
    # loop through dictionary of adjs
    # if a word appears in at least common_index number of brands,
    # add it to common_words list
    for adj in all_adjs_count:
        if all_adjs_count[adj] >= common_index:
            common_words.append(adj)
    common_words = set(common_words)
    return list(common_words)


def find_unique_words(all_data, common_words, brand_names):
    """
    Given the adjectives of all brands and a list of common words,
    return the adjectives with common words removed as a dictionary.

    Args:
        all_data: A dictionary with the brands as keys mapping to a
        dictionary of adjectives for the corresponding coffee brand.
        common_words: list of words that are highly shared across brands.
        brand_names: A list of all the brand names for the various coffees.

    Returns:
        unique_words: A dictionary with brands as its keys mapping
        to their unique words.
    """
    unique_words = {brand: [] for brand in brand_names}
    for brand in brand_names:
        # if the key is not a common word, add it to unique words dictionary
        for key in all_data[brand]:
            if key in common_words:
                continue
            else:
                unique_words[brand].append(key)
    return unique_words
