#!/usr/bin/python3
import sys
import requests
from db_functions import create_db, save_posts, get_all_posts, get_post_by_id

# eBay Creds
# headers = {
#     'X-EBAY-API-CALL-NAME': 'GetCategories',
#     'X-EBAY-API-APP-NAME': 'EchoBay62-5538-466c-b43b-662768d6841',
#     'X-EBAY-API-CERT-NAME': '00dd08ab-2082-4e3c-9518-5f4298f296db',
#     'X-EBAY-API-DEV-NAME': '16a26b1b-26cf-442d-906d-597b60c41c19',
#     'X-EBAY-API-SITEID': 0,
#     'X-EBAY-API-COMPATIBILITY-LEVEL': 1077
# }
#
# xml_data = '''
# <?xml version="1.0" encoding="utf-8"?>
# <GetCategoriesRequest xmlns="urn:ebay:apis:eBLBaseComponents">
# <CategorySiteID>100</CategorySiteID>
# <ViewAllNodes>True</ViewAllNodes>
# <DetailLevel>ReturnAll</DetailLevel>
# <RequesterCredentials>
#   <eBayAuthToken>AgAAAA**AQAAAA**aAAAAA**PlLuWA**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wFk4GlDpaDpAudj6x9nY+seQ**LyoEAA**AAMAAA**wSd/jBCbxJHbYuIfP4ESyC0mHG2Tn4O3v6rO2zmnoVSF614aVDFfLSCkJ5b9wg9nD7rkDzQayiqvwdWeoJkqEpNQx6wjbVQ1pjiIaWdrYRq+dXxxGHlyVd+LqL1oPp/T9PxgaVAuxFXlVMh6wSyoAMRySI6QUzalepa82jSQ/qDaurz40/EIhu6+sizj0mCgjcdamKhp1Jk3Hqmv8FXFnXouQ9Vr0Qt+D1POIFbfEg9ykH1/I2CYkZBMIG+k6Pf00/UujbQdne6HUAu6CSj9wGsqQSAEPIXXvEnVmtU+6U991ZUhPuA/DMFEfVlibvNLBA7Shslp2oTy2T0wlpJN+f/Jle3gurHLIPc6EkEmckEpmSpFEyuBKz+ix4Cf4wYbcUk/Gr3kGdSi20XQGu/ZnJ7Clz4vVak9iJjN99j8lwA2zKW+CBRuHBjZdaUiDctSaADHwfz/x+09bIU9icgpzuOuKooMM5STbt+yJlJZdE3SRZHwilC4dToTQeVhAXA4tFZcDrZFzBmJsoRsJYrCdkJBPeGBub+fqomQYyKt1J0LAQ5Y0FQxLHBIp0cRZTPAuL/MNxQ/UXcxQTXjoCSdZd7B55f0UapU3EsqetEFvIMPxCPJ63YahVprODDva9Kz/Htm3piKyWzuCXfeu3siJvHuOVyx7Q4wyHrIyiJDNz5b9ABAKKauxDP32uqD7jqDzsVLH11/imKLLdl0U5PN+FP30XAQGBAFkHf+pAvOFLrdDTSjT3oQhFRzRPzLWkFg</eBayAuthToken>
# </RequesterCredentials>
# </GetCategoriesRequest>
# '''

# helper function to get command-line arguments
def get_arguments():
    """
    it should return a list containing the argument if there's an argument
    with message=None.
    if not it's returns a message, with arg=None
    """
    arg = sys.argv[1:]
    message = None
    if not arg:
        message = '############ You need to pass an argument #########'
        arg = None
        return arg, message
    elif len(arg) == 2:
        return arg, message
    elif len(arg) > 2:
        message = '########### Sorry you cannot have more than two arguments ###########'
        arg = None
        return arg, message
    else:
        return arg, message

# Get data from the jsonplaceholder api
def fetch_data():
    # get all posts
    response = requests.get('https://jsonplaceholder.typicode.com/posts')
    return response.json()

# Save posts into the database
def build_db(arg):
    if arg == '--rebuild':
        create_db()
        data = fetch_data()
        for post in data:
            save_posts(post.get('id'), post.get('title'), post.get('body'))
        return 'posts saved successfully'
    return '##### Please pass the argument "--rebuild" #####'

# Render post
def render_post(args):
    if args[0] == '--render':
        post = get_post_by_id(int(args[1]))
        if post:
            return post
        return '##### Post not found #####'
    return '##### Please pass "--render" as the first argument #####'



if __name__ == '__main__':
    args, msg = get_arguments()
    if msg:
        print(msg)
    elif len(args) == 1:
        db_msg = build_db(args[0])
        print(db_msg)
    else:
        post = render_post(args)
        print(post)
