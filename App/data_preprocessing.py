import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from urllib.parse import urlparse
from tld import get_tld
import numpy as np
import re
from urllib.parse import urlparse
from tld import get_tld
import os.path
from urllib.parse import urlparse
from googlesearch import search


# Load the dataset
df = pd.read_csv("MaliciousURL.csv", nrows=1000)


# ... Feature engineering code ...
def having_ip_address(url):
    match = re.search(
        "(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\."
        "([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|"  # IPv4
        "((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)"  # IPv4 in hexadecimal
        "(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}",
        url,
    )  # Ipv6
    if match:
        # print match.group()
        return 1
    else:
        # print 'No matching pattern found'
        return 0


df["use_of_ip"] = df["url"].apply(lambda i: having_ip_address(i))


def abnormal_url(url):
    hostname = urlparse(url).hostname  # Extracts the hostname from the URL
    if hostname:
        hostname = re.escape(
            hostname
        )  # Escape special characters in hostname if it's not None
        match = re.search(hostname, url)  # Searches for the escaped hostname in the URL
        if match:
            return 1  # Returns 1 if the escaped hostname is found in the URL
        else:
            return 0  # Returns 0 if the escaped hostname is not found in the URL
    else:
        return 0  # Returns 0 if the hostname is None or couldn't be extracted


df["abnormal_url"] = df["url"].apply(lambda i: abnormal_url(i))


# def google_index(url):
#     site = search(url, 5)
#     return 1 if site else 0


# df["google_index"] = df["url"].apply(lambda i: google_index(i))
# print(df["google_index"])


def count_dot(url):
    count_dot = url.count(".")
    return count_dot


df["count."] = df["url"].apply(lambda i: count_dot(i))


def count_www(url):
    url.count("www")
    return url.count("www")


df["count-www"] = df["url"].apply(lambda i: count_www(i))


def count_atrate(url):
    return url.count("@")


df["count@"] = df["url"].apply(lambda i: count_atrate(i))


def no_of_dir(url):
    urldir = urlparse(url).path
    return urldir.count("/")


df["count_dir"] = df["url"].apply(lambda i: no_of_dir(i))


def no_of_embed(url):
    urldir = urlparse(url).path
    return urldir.count("//")


df["count_embed_domian"] = df["url"].apply(lambda i: no_of_embed(i))


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


def count_https(url):
    return url.count("https")


df["count-https"] = df["url"].apply(lambda i: count_https(i))


def count_http(url):
    return url.count("http")


df["count-http"] = df["url"].apply(lambda i: count_http(i))


def count_per(url):
    return url.count("%")


df["count%"] = df["url"].apply(lambda i: count_per(i))


def count_ques(url):
    return url.count("?")


df["count?"] = df["url"].apply(lambda i: count_ques(i))


def count_hyphen(url):
    return url.count("-")


df["count-"] = df["url"].apply(lambda i: count_hyphen(i))


def count_equal(url):
    return url.count("=")


df["count="] = df["url"].apply(lambda i: count_equal(i))


def url_length(url):
    return len(str(url))


df["url_length"] = df["url"].apply(lambda i: url_length(i))


def hostname_length(url):
    return len(urlparse(url).netloc)


df["hostname_length"] = df["url"].apply(lambda i: hostname_length(i))
df.head()


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


def digit_count(url):
    digits = 0
    for i in url:
        if i.isnumeric():
            digits = digits + 1
    return digits


df["count-digits"] = df["url"].apply(lambda i: digit_count(i))


def letter_count(url):
    letters = 0
    for i in url:
        if i.isalpha():
            letters = letters + 1
    return letters


df["count-letters"] = df["url"].apply(lambda i: letter_count(i))


def fd_length(url):
    urlpath = urlparse(url).path
    try:
        return len(urlpath.split("/")[1])
    except:
        return 0


df["fd_length"] = df["url"].apply(lambda i: fd_length(i))

df["tld"] = df["url"].apply(lambda i: get_tld(i, fail_silently=True))


def tld_length(tld):
    try:
        return len(tld)
    except:
        return -1


df["tld_length"] = df["tld"].apply(lambda i: tld_length(i))


# Label encoding
lb_make = LabelEncoder()
df["type_code"] = lb_make.fit_transform(df["type"])

# Predictor Variables

X = df[
    [
        "use_of_ip",
        "count.",
        "abnormal_url",
        "count-www",
        "count@",
        "count_dir",
        "count_embed_domian",
        "short_url",
        "count-https",
        "count-http",
        "count%",
        "count?",
        "count-",
        "count=",
        "url_length",
        "hostname_length",
        "sus_url",
        "fd_length",
        "tld_length",
        "count-digits",
        "count-letters",
    ]
]
# Target Variable
y = df["type_code"]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, stratify=y, test_size=0.2, shuffle=True, random_state=5
)
