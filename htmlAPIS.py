from datetime import datetime
from flask import Flask, jsonify, request, current_app
from flask_restful import Api, reqparse
from elasticsearch import Elasticsearch

es = Elasticsearch('http://localhost:9200') #change this address to the host/port you're using
app = Flask(__name__)
api = Api(app)

#contactOperation function contains code for GET, POST methods
@app.route('/contact', methods=['GET', 'POST'])
def contactOperation():
    #On Get request: get the pageSize, page, and query args from URL
    #Loop through the results page times and print the results
    if request.method == 'GET':
        pageSize= request.args.get('pageSize', default = 10000, type= int)
        page = request.args.get('page', default = 1, type= int)
        query = request.args.get('query', default = {"query": {"match_all" : {}}})
        for i in range (page):
            res = es.search(index='contact', doc_type='info', body=query, size=pageSize, from_ = pageSize*i)
            for hit in res["hits"]["hits"]:
                print("%s) %s" % (hit['_id'], hit['_source']))
        return ("Finished",201)
    
    #On Post request: parse URL for name, address, and cell # and create doc if valid
    #Make sure name doesn't already exist in database and cell number has <= 16 digits
    if request.method == 'POST':
        parser = reqparse.RequestParser()
        parser.add_argument("name", required = True, type=str)
        parser.add_argument("address")
        parser.add_argument("cell", type=int)
        parser.add_argument("id", required= True, type=int)

        args = parser.parse_args()

        
        search_object = {'query': {'match': {'name': args["name"]}}}
        res = es.search(index ='contact', doc_type='info', body= search_object)
        
        if(res['hits']['total'] > 0): #check if name exists
            return ("Contact with that name already exists", 400)

        if len(str(args["cell"])) > 16: #check if cell number is less than 16 character
            return ("Phone number is too large, only <16 digits is accepted", 400)

        if len(args["address"]) > 60:   #check if address is less than 60 characters
            return ("Address is too large, please shorten it", 400)
    
        info = {
            "name": args["name"],
            "address": args["address"],
            "cell": args["cell"]
            }
        #create doc if all inputs are valid:
        es.create(index='contact', doc_type='info', body= info, id=args["id"])  
        return ("Created contact!", 201)


#nameOperation function contains code for GET, PUT, DELETE methods
@app.route('/contact/<name>', methods =['GET','PUT','DELETE'])
def nameOperation(name):
    #On Get request: query for the input name and print it
    if request.method == 'GET':
        search_object = {'query': {'match': {'name': name}}}
        res = es.search(index ='contact', doc_type='info', body= search_object)
        
        if res['hits']['total'] == 0:
            return "Name returns no hits", 400
        else:
            for doc in res['hits']['hits']:
                return("%s) %s" % (doc['_id'], doc['_source']))
            
    #On Put request: query for input name and run update_by_query function           
    elif request.method == 'PUT':
        search_object = {'query': {'match': {'name': name}}}
        res = es.search(index ='contact', doc_type='info', body= search_object)
        if res['hits']['total'] == 0:
            return( "Name returns no hits", 400)
        else:
            es.update_by_query(index='contact', doc_type='info', body= search_object)
            return ("Updated", 200)
        
    #On Delete request: query for input name and run delete_by_query function 
    elif request.method == 'DELETE':
        search_object = {"query": {"match": {"name": name}}}
        res = es.search(index ='contact', doc_type='info', body= search_object)
        if res['hits']['total'] == 0:
            return ("Name returns no hits", 400)
        else:
            es.delete_by_query(index='contact', doc_type='info', body= search_object)
            return ("Deleted", 200)



if __name__ == '__main__':
    app.run(debug= True, port=8080) #running on port 8080
    print "good :)"
