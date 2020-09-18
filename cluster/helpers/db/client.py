import os
import requests


def run_query(query, variables):
    body = {
        'query': query,
        'variables': variables
    }
    response = _make_post_call(body)
    if response.get('data') is not None:
        return response.get('data')
    raise RuntimeError('query failed: ' + str(response))


def _make_post_call(body):
    url = os.environ['HASURA_GRAPHQL_ENDPOINT']
    # url = 'https://anywhr-cluster.herokuapp.com/v1/graphql'
    secret = os.environ['HASURA_ADMIN_SECRET']
    # secret = 'random'
    headers = {
        'Content-type': 'application/json',
        'x-hasura-admin-secret': secret
    }
    print("HASURA_CLIENT_POST_CALL")
    # print("URL : " + url)
    # print("BODY : " + str(body))
    response = requests.post(url, json=body, headers=headers, timeout=10)
    print("RESPONSE : " + str(response.json()))
    return response.json()
