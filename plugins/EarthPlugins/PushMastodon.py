from mastodon import Mastodon

def pushMessage(message):
    client_id = '96ab52006dace8443c2d30abc66de3f61608238312f09893a9c0239bcb80c5ce'
    client_secret = '7b43092c55019e55aa52a28b2ebc30bc91cb7343a64fa42ded930cc6a7d5fe6b'
    access_token = '2b07f4ba4de2505c188455228e962cfcd4c409e2c7fb38c343cdcd117e87bd5a'
    api = Mastodon(client_id, client_secret, access_token,
            api_base_url="https://sn.angry.im")
    api.toot(message)
