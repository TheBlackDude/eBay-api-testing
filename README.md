# eBay-api-testing
**Note: The program uses the (jsonplaceholder) api, because the eBay api wasn't working**

#### Install
*git clonse 'repo'*
**You don't need to install anything because the program only uses the standard library**

#### How To Test The Program

*Run the tests first*

*python3 tests.py*

*Run '--rebuild' to download the data and create the database*

*python3 categories.py --rebuild*

*Run '--render' 'id' to generate a html page with categories, e.g: --render 6016*

*python3 categories.py --render 6449*

#### You can also use the bash script to execute the commands

*to run the tests*

*./categories.sh tests*

*to download the data and create the database*

*./categories.sh --rebuild*

*to generate a html page with categories*

*./categories.sh --render 6018*
