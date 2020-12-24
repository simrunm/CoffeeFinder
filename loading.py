def load_nouns_to_disregard():
    """
    Loads a list of nouns from a text file are used in other functions.

    Returns:
        nouns = A list containing the nouns to disregard.
    """
    # creating the list from the text file
    with open('nouns-to-disregard.txt') as reader:
        text = reader.read()
        nouns = text.split(",")
    return nouns


def load_brands_info():
    """
    Depending on the input string, return either a list of brand names
    or a list of brand urls.

    Args:
        names_or_urls: string that is either 'names' or 'urls'.

    Returns:
        brand_names: A list of brand names for each coffee.
        brand_urls: A list of brand urls for each coffee.
    """
    # brands.txt contains the brand names and corresponding
    # links to the Amazon reviews
    with open('brands.txt') as reader:
        brand_names = []
        brand_urls = []

        # adding the brand names to one list and the corresponding
        # urls to another list
        for line in reader:
            split = line.split(",")
            brand_names.append(split[0])
            brand_urls.append(split[1][:-1])
    return brand_names, brand_urls
