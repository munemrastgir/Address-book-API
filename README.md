# Address-book-API
Defined Get, Post, Put, and Delete methods using Flask and Elasticsearch database

To run, first start up a Node instance on Elasticsearch, and add to it the contact index, CURL command provided in shell script.
Contact looks like 
{
  "name": "John Smith", 
  "address": "123 South Ave", 
  "cell": 1012910555 
}
Address is limited to 60 chars and cell is limited to 16 digits

Then you can run the python file "htmlAPIS.py" which runs the app on port 8080.

Testing the commands was done on Postman. Some sample tests are given in tests.txt
