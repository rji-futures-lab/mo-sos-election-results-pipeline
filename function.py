import os

import requests

import s3


USE_TEST_RESULTS = os.getenv('USE_TEST_RESULTS', default=False)


def get_test_results():
    url = "https://mo-gen-election-results-2020.s3.us-east-2.amazonaws.com/sos/latest.xml"
    return requests.get(url, headers=headers)


def get_prod_results():
    url = "https://enrarchives.sos.mo.gov/apfeed/apfeed.asmx/GetElectionResults"
    headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:83.0) Gecko/20100101 Firefox/83.0"}
    params = {'AccessKey': os.getenv("ACCESS_KEY")}
    return requests.get(url, headers=headers, params=params)


def lambda_handler(event, context):
    main()


def main():
    if USE_TEST_RESULTS:
        r = get_test_results()
    else:
        r = get_prod_results()

    r.raise_for_status()

    s3.archive(
        r.content, r.headers['Content-Type'], path='sos'
        )

if __name__ == '__main__':
    main()
