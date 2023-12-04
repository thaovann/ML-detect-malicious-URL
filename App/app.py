from flask import Flask, render_template, request
from data_preprocessing import (
    having_ip_address,
    abnormal_url,
    count_dot,
    count_www,
    count_atrate,
    no_of_dir,
    no_of_embed,
    shortening_service,
    count_https,
    count_http,
)
from data_preprocessing import (
    count_per,
    count_ques,
    count_hyphen,
    count_equal,
    url_length,
    hostname_length,
    suspicious_words,
    digit_count,
    letter_count,
    fd_length,
)
from tld import get_tld
import numpy as np
from random_forest_model import rf

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    if request.method == "POST":
        test_url = request.form["url"]
        prediction = get_prediction_from_url(test_url)
    return render_template("index.html", prediction=prediction)


def main(url):
    status = []

    status.append(having_ip_address(url))
    status.append(abnormal_url(url))
    status.append(count_dot(url))
    status.append(count_www(url))
    status.append(count_atrate(url))
    status.append(no_of_dir(url))
    status.append(no_of_embed(url))

    status.append(shortening_service(url))
    status.append(count_https(url))
    status.append(count_http(url))

    status.append(count_per(url))
    status.append(count_ques(url))
    status.append(count_hyphen(url))
    status.append(count_equal(url))

    status.append(url_length(url))
    status.append(hostname_length(url))
    status.append(suspicious_words(url))
    status.append(digit_count(url))
    status.append(letter_count(url))
    status.append(fd_length(url))
    tld = get_tld(url, fail_silently=True)
    if tld:
        tld_length = len(tld)
        status.append(tld_length)
    else:
        status.append(0)
    return status

def get_prediction_from_url(test_url):
    features_test = main(test_url)
    features_test = np.array(features_test).reshape((1, -1))
    pred = rf.predict(features_test)
    if int(pred[0]) == 0:
        return "BENGIN"
    elif int(pred[0]) == 1:
        return "DEFACEMENT"
    elif int(pred[0]) == 2:
        return "PHISHING"
    elif int(pred[0]) == 3:
        return "MALWARE"


if __name__ == "__main__":
    app.run(port=3000, debug=True)
