#!/usr/bin/python3
import os
import sys
import requests
import xml.etree.ElementTree as ET
from db_functions import create_db, save_categories, get_category_by_id, get_all_categories

# eBay Creds
headers = {
    'X-EBAY-API-CALL-NAME': 'GetCategories',
    'X-EBAY-API-APP-NAME': 'EchoBay62-5538-466c-b43b-662768d6841',
    'X-EBAY-API-CERT-NAME': '00dd08ab-2082-4e3c-9518-5f4298f296db',
    'X-EBAY-API-DEV-NAME': '16a26b1b-26cf-442d-906d-597b60c41c19',
    'X-EBAY-API-SITEID': '0',
    'X-EBAY-API-COMPATIBILITY-LEVEL': '1077'
}

xml_data = '''
<?xml version="1.0" encoding="utf-8"?>
<GetCategoriesRequest xmlns="urn:ebay:apis:eBLBaseComponents">
<CategorySiteID>100</CategorySiteID>
<ViewAllNodes>True</ViewAllNodes>
<DetailLevel>ReturnAll</DetailLevel>
<RequesterCredentials>
  <eBayAuthToken>AgAAAA**AQAAAA**aAAAAA**deDIWw**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wFk4ajDpSBog2dj6x9nY+seQ**eb8EAA**AAMAAA**OsKsWxMqzKnukqE43scHW//ocS/gXuL/MApTzF/frcZ0Jt9yWqvLDujM+x1mAYti5KnBco7CFwYBd7WkrauwVAHDG/mZ59CRxYSH7fT3deo0mMhLXWiZ+JDgtBKcomZ+HQkPWc9ftYCaMMqsWUYT8fTwOsDbr++yo4bSGofD1NSZSTb9uUZfO3Sg5gK9L3xgrBHF/nR7coKzWlAwa0rgtMuh8HYKvtVO0IYpXAJZniLkgyBa4BZ+POcYOh1l1PHTdazz4Wadco2G3u/RP9ust14ksFMZ/Q/z5Rra86a7ymEouScCD2AS3guY/YwqsUo92seueNEDGCbSASNz5TMb6cBbCleNHw1pe5C1wlWJDWW0zFIQAcVaY/cRWykhqAX+quDPM/p4gz8gDg+T2o9JoThD3ZNVVQJwz6JLCHXPYTNZBS9w2dAidAi3kvlMIVWIhPlNmviT6wYSPS463Xmh1/i0AApToYrCLpnfggZicGLbRBi90PUz4ZqTYM8WXvhtPSKhatTVszGRAI7xISQbbIS4LkRmnFgkbRyuaJmNzzr91orygpRq1z7WJN3ClKwYrDxHXCBI+M6LkWUQWxJ9Jyd9Qg8ScE6n/B3UVcAfsgB97Du6RKvOgmZraxoQnG31lNeDqi4j0q9np9mga/RuMvEf13HURWU0dejPGsINCjF1ljkHR2wR2SPkxJwqCxCr/K4B9M8ZRDUSS7Q/re2m6WhfdoExUhwZ0hu/uIZWW4NaOvVja0VSEGASMRz3dsLY</eBayAuthToken>
</RequesterCredentials>
</GetCategoriesRequest>
'''

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

# Get data from the ebay api
def fetch_data():
    # Call the ebay api
    response = requests.post('https://api.sandbox.ebay.com/ws/api.dll',
                             headers=headers, data=xml_data)
    if response.status_code == 200:
        root = ET.fromstring(response.text.encode('utf-8'))
        categories = root.find('{urn:ebay:apis:eBLBaseComponents}CategoryArray')
        # convert categories into a list of dictionaries
        categories_list = []
        for child in categories.getchildren():
            category = {}
            category['name'] = child.find('{urn:ebay:apis:eBLBaseComponents}CategoryName').text
            category['id'] = int(child.find('{urn:ebay:apis:eBLBaseComponents}CategoryID').text)
            category['level'] = int(child.find('{urn:ebay:apis:eBLBaseComponents}CategoryLevel').text)
            category['offer'] = child.find('{urn:ebay:apis:eBLBaseComponents}BestOfferEnabled').text
            category['parentId'] = int(child.find('{urn:ebay:apis:eBLBaseComponents}CategoryParentID').text)
            categories_list.append(category)
        return categories_list
    return "Something went wrong with the API call, the status code is: {}".format(
        response.status_code
    )

# Save categories into the database
def build_db(arg):
    if arg == '--rebuild':
        create_db()
        data = fetch_data()
        save_categories(data)
        return 'categories saved successfully'
    return '##### Please pass the argument "--rebuild" #####'

# Generate html
def generate_html(id, category):
    file_name = '{}.{}'.format(id, 'html')
    with open(file_name, 'w') as html_file:
        head = '''
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="utf-8">
        <title>Generated With Python</title>
        <style>
        body {
        background-color: linen;
        }
        table, th, td {
        border: 1px solid black;
        }
        </style>
        </head>
        '''
        html_file.write(head)
        bd_head = '''
        <body>
        <h2>Parent Category ID: {parentId}</h2>
        '''.format(parentId=id)
        html_file.write(bd_head)
        tb_header = '''
        <table style="width:100%">
        <tr>
          <td>Category ID</td>
          <td>Category Name</td>
          <td>Category Leve</td>
          <td>Best Offer Enabled</td>
          <td>Parent ID</td>
        </tr>
        '''
        html_file.write(tb_header)
        for item in category:
            tb_body = '''
            <tr>
              <td>{}</td>
              <td>{}</td>
              <td>{}</td>
              <td>{}</td>
              <td>{}</td>
            </tr>
            '''.format(item[0], item[1], item[2], item[3], item[4])
            html_file.write(tb_body)
        footer = '''
        </body>
        </html>
        '''
        html_file.write(footer)
    if file_name in os.listdir():
        return '##### html generated successfully #####'
    return '##### Sorry something went wrong #####'

# Render post
def render_categories(args):
    if args[0] == '--render' and 'categories.db' in os.listdir():
        category = get_category_by_id(int(args[1]))
        if category:
            msg = generate_html(int(args[1]), category)
            return msg
        return '##### Category not found #####'
    return '''##### Please pass "--render" as the first argument,
    and make sure you've built the database first
    with the command-line "--rebuild" #####'''



if __name__ == '__main__':
    args, msg = get_arguments()
    if msg:
        print(msg)
    elif len(args) == 1:
        db_msg = build_db(args[0])
        print(db_msg)
    else:
        category_msg = render_categories(args)
        print(category_msg)
