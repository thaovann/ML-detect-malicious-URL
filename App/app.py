from flask import Flask, render_template, request, session, redirect, url_for
from data_preprocessing import (
    url_length,
    shortening_service,
    suspicious_words,
    no_of_dir,
    count_per,
    count_ques,
    count_equal,
    digit_count,
    letter_count,
    presence_in_suspicious_list,
    len_primary_domain,
    count_dot_primary_domain,
    count_hyphen_primary_domain,
    count_at_primary_domain,
    having_ip_address,
    count_www,
    count_https,
    count_http,
    count_doublez_forward_slash,
    fd_length,
    has_uppercase_directory,
    count_subdirectories,
    count_special_characters,
    count_zeroes,
    calculate_upper_lower_ratio,
    count_parameters_length,
    count_query_parameters,
    has_anchor,
)
from tld import get_tld
import numpy as np
from random_forest_model import rf

app = Flask(__name__)
app.secret_key = "thaovan"


@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    if request.method == "POST":
        test_url = request.form["url"]
        session["submitted_url"] = test_url
        prediction = get_prediction_from_url(test_url)
    return render_template("index.html", prediction=prediction, submitted_url=test_url)


def main(url):
    status = []

    def add_to_status(func):
        try:
            result = func(url)
            if isinstance(result, (int, float)):  # Kiểm tra nếu kết quả là numeric
                status.append(result)
            else:
                print(f"The function {func.__name__} didn't return a numeric value.")
        except Exception as e:
            print(f"An error occurred while executing {func.__name__}: {e}")

    # Kiểm tra và gọi các hàm
    add_to_status(url_length)
    add_to_status(shortening_service)
    add_to_status(suspicious_words)
    add_to_status(no_of_dir)
    add_to_status(count_per)
    add_to_status(count_ques)
    add_to_status(count_equal)
    add_to_status(digit_count)
    add_to_status(letter_count)
    add_to_status(presence_in_suspicious_list)
    add_to_status(having_ip_address)
    add_to_status(len_primary_domain)
    add_to_status(count_dot_primary_domain)
    add_to_status(count_hyphen_primary_domain)
    add_to_status(count_at_primary_domain)
    add_to_status(count_www)
    add_to_status(count_https)
    add_to_status(count_http)
    add_to_status(count_doublez_forward_slash)
    add_to_status(fd_length)
    add_to_status(has_uppercase_directory)
    add_to_status(count_subdirectories)
    add_to_status(count_special_characters)
    add_to_status(count_zeroes)
    add_to_status(calculate_upper_lower_ratio)
    add_to_status(count_parameters_length)
    add_to_status(count_query_parameters)
    add_to_status(has_anchor)

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
