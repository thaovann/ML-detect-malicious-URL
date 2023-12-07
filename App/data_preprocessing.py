import pandas as pd
from sklearn.model_selection import train_test_split
import string
from sklearn.preprocessing import LabelEncoder
import numpy as np
import re
from tld import get_tld
from urllib.parse import urlparse, parse_qs
from googlesearch import search
import tldextract

# Load the dataset
df = pd.read_csv("MaliciousURL.csv", nrows= 10000)


# URL
def url_length(url):
    return len(str(url))


df["url_length"] = df["url"].apply(lambda i: url_length(i))


def shortening_service(url):
    match = re.search(
        "bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|"
        "yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|"
        "short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|"
        "doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|"
        "db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|"
        "q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|"
        "x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|"
        "tr\.im|link\.zip\.net",
        url,
    )
    if match:
        return 1
    else:
        return 0


df["short_url"] = df["url"].apply(lambda i: shortening_service(i))


def suspicious_words(url):
    match = re.search(
        "PayPal|login|signin|bank|account|update|free|lucky|service|bonus|ebayisapi|webscr",
        url,
    )
    if match:
        return 1
    else:
        return 0


df["sus_url"] = df["url"].apply(lambda i: suspicious_words(i))


def count_per(url):
    return url.count("%")


df["count%"] = df["url"].apply(lambda i: count_per(i))


def count_ques(url):
    return url.count("?")


df["count?"] = df["url"].apply(lambda i: count_ques(i))


def count_equal(url):
    return url.count("=")


df["count="] = df["url"].apply(lambda i: count_equal(i))


def digit_count(url):
    digits = 0
    for i in url:
        if i.isnumeric():
            digits = digits + 1
    return digits


df["number-digits"] = df["url"].apply(lambda i: digit_count(i))


def letter_count(url):
    letters = 0
    for i in url:
        if i.isalpha():
            letters = letters + 1
    return letters


df["number-letters"] = df["url"].apply(lambda i: letter_count(i))


# Top level domain--------------------------------------------------------------
def presence_in_suspicious_list(url):
    suspicious_tlds = [
        "zip",
        "review",
        "country",
        "kim",
        "cricket",
        "science",
        "work",
        "party",
        "gq",
        "Link",
    ]

    extracted = tldextract.extract(url)
    extracted_tld = extracted.suffix

    # Checking if the extracted TLD is suspicious
    if extracted_tld in suspicious_tlds:
        return 1
    else:
        return 0


df["suspicious_tdl"] = df["url"].apply(lambda i: presence_in_suspicious_list(i))


# Primary domain-----------------------------------------------------------------------------------------------------------------------
def having_ip_address(url):
    match = re.search(
        "(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\."
        "([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|"  # IPv4
        "((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)"  # IPv4 in hexadecimal
        "(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}",
        url,
    )  # Ipv6
    if match:
        return 1
    else:
        return 0


df["use_of_ip"] = df["url"].apply(lambda i: having_ip_address(i))


def len_primary_domain(url):
    try:
        parsed_url = urlparse(url)
        if parsed_url.scheme == "http" or parsed_url.scheme == "https":
            primary_domain = parsed_url.netloc
            if "www." in primary_domain:
                primary_domain = primary_domain.replace("www.", "")

            return len(primary_domain)
        else:
            return 0
    except ValueError:
        return 0


df["len_primary_domain"] = df["url"].apply(lambda i: len_primary_domain(i))


def count_dot_primary_domain(url):
    try:
        parsed_url = urlparse(url)
        if parsed_url.scheme == "http" or parsed_url.scheme == "https":
            primary_domain = parsed_url.netloc
            if "www." in primary_domain:
                primary_domain = primary_domain.replace("www.", "")

            return primary_domain.count(".")
        else:
            return 0
    except ValueError:
        return 0


df["count_dot_primary_domain"] = df["url"].apply(lambda i: count_dot_primary_domain(i))


def count_hyphen_primary_domain(url):
    try:
        parsed_url = urlparse(url)
        if parsed_url.scheme == "http" or parsed_url.scheme == "https":
            primary_domain = parsed_url.netloc
            if "www." in primary_domain:
                primary_domain = primary_domain.replace("www.", "")

            return primary_domain.count("-")
        else:
            return 0
    except ValueError:
        return 0


df["count_hyphen_primary_domain"] = df["url"].apply(
    lambda i: count_hyphen_primary_domain(i)
)


def count_at_primary_domain(url):
    try:
        parsed_url = urlparse(url)
        if parsed_url.scheme == "http" or parsed_url.scheme == "https":
            primary_domain = parsed_url.netloc
            if "www." in primary_domain:
                primary_domain = primary_domain.replace("www.", "")

            return primary_domain.count("@")
        else:
            return 0
    except ValueError:
        return 0


df["count_at_primary_domain"] = df["url"].apply(lambda i: count_at_primary_domain(i))


# Sub domain -----------------------------------------------------------------------------
def count_www(url):
    return url.count("www")


df["count-www"] = df["url"].apply(lambda i: count_www(i))


# Giao thức kết nối Scheme -------------------------------------------------------
def count_https(url):
    return url.count("https")


df["count-https"] = df["url"].apply(lambda i: count_https(i))


def count_http(url):
    return url.count("http")


df["count-http"] = df["url"].apply(lambda i: count_http(i))


# Path-------------------------------------------------------------------------------------------------
def count_doublez_forward_slash(url):
    return url.count("//")


df["count_double_forward_slash"] = df["url"].apply(
    lambda i: count_doublez_forward_slash(i)
)


def no_of_dir(url):
    try:
        urldir = urlparse(url).path
        return urldir.count("/")
    except ValueError:
        return 0


df["count_dir"] = df["url"].apply(lambda i: no_of_dir(i))


def fd_length(url):
    try:
        urlpath = urlparse(url).path
        return len(urlpath.split("/")[1])
    except (ValueError, IndexError):
        return 0


df["fd_length"] = df["url"].apply(lambda i: fd_length(i))


def has_uppercase_directory(url):
    try:
        url_path = urlparse(url).path
        path_components = url_path.split("/")

        for component in path_components[1:]:
            if component.isupper():
                return 0
        return 1
    except:
        return 0


df["has_uppercase_directory"] = df["url"].apply(lambda i: has_uppercase_directory(i))


def count_subdirectories(url):
    try:
        parsed_url = urlparse(url)
        path_components = parsed_url.path.split("/")
        subdirectories_count = len(
            [directory for directory in path_components[1:] if directory]
        )
        return subdirectories_count
    except ValueError:
        return 0


df["count_subdirectories"] = df["url"].apply(lambda i: count_subdirectories(i))


def count_special_characters(url):
    try:
        parsed_url = urlparse(url)
        path = parsed_url.path
        alphanumeric_chars = set(string.ascii_letters + string.digits)
        special_char_count = sum(
            1 for char in path if char not in alphanumeric_chars and char != "/"
        )
        return special_char_count
    except ValueError:
        return 0


df["count_special_characters"] = df["url"].apply(lambda i: count_special_characters(i))


def count_zeroes(url):
    try:
        parsed_url = urlparse(url)
        path = parsed_url.path
        zero_count = sum(1 for char in path if char == "0")
        return zero_count
    except ValueError:
        return 0


df["count_zeroes"] = df["url"].apply(lambda i: count_zeroes(i))


def calculate_upper_lower_ratio(url):
    try:
        parsed_url = urlparse(url)
        path = parsed_url.path
        uppercase_count = sum(1 for char in path if char.isupper())
        lowercase_count = sum(1 for char in path if char.islower())
        if lowercase_count > 0:  # To avoid division by zero
            ratio = uppercase_count / lowercase_count
        else:
            ratio = 0

        return ratio
    except ValueError:
        return 0


df["calculate_upper_lower_ratio"] = df["url"].apply(
    lambda i: calculate_upper_lower_ratio(i)
)


# Function to count length of parameters in query string
def count_parameters_length(url):
    try:
        parsed_url = urlparse(url)
        query_string = parsed_url.query
        params_length = len(query_string)
        return params_length
    except ValueError:
        return 0


df["count_parameters_length"] = df["url"].apply(lambda i: count_parameters_length(i))


def count_query_parameters(url):
    try:
        parsed_url = urlparse(url)
        query_string = parsed_url.query
        parameters = parse_qs(query_string)

        num_queries = len(parameters)
        return num_queries
    except ValueError:
        return 0


df["count_query_parameters"] = df["url"].apply(lambda i: count_query_parameters(i))


def has_anchor(url):
    try:
        parsed_url = urlparse(url)
        if parsed_url.fragment:
            return 1
        else:
            return 0
    except ValueError:
        return 0


df["has_anchor"] = df["url"].apply(lambda i: has_anchor(i))

# Label encoding
lb_make = LabelEncoder()
df["type_code"] = lb_make.fit_transform(df["type"])

# Predictor Variables
X = df[
    [
        "url_length",
        "short_url",
        "sus_url",
        "count_dir",
        "count%",
        "count?",
        "count=",
        "number-digits",
        "number-letters",
        "suspicious_tdl",
        "use_of_ip",
        "len_primary_domain",
        "count_dot_primary_domain",
        "count_hyphen_primary_domain",
        "count_at_primary_domain",
        "count-www",
        "count-https",
        "count-http",
        "count_double_forward_slash",
        "fd_length",
        "has_uppercase_directory",
        "count_subdirectories",
        "count_special_characters",
        "count_zeroes",
        "calculate_upper_lower_ratio",
        "count_parameters_length",
        "count_query_parameters",
        "has_anchor",
    ]
]

# Target Variable
y = df["type_code"]


# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, stratify=y, test_size=0.2, shuffle=True, random_state=5
)
