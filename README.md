# eBay-api-testing
**Note: The program uses the (jsonplaceholder) api, because the eBay api wasn't working**

#### Install
*git clonse 'repo'*
**You don't need to install anything because the program only uses the standard library**

#### How To Test The Program

*Run the tests first*
*python3 tests.py*

*Run '--rebuild' to download the data and create the database*
*python3 posts.py --rebuild*

*Run '--render' 'id' to generate a html page with an 'ids' post data*
*python3 posts.py --render 100*

#### You can also use the bash script to execute the commands

*to run the tests*
*./posts.sh tests*

*to download the data and create the database*
*./posts.sh --rebuild*

*to generate a html page with an 'ids' post data*
*./posts.sh --render 100*
