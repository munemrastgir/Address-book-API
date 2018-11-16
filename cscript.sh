#!/bin/bash

curl -X PUT "localhost:9200/contact?pretty"
curl -X GET "localhost:9200/_cat/indices?v"

#Generic Adressbook input:
curl -X PUT "localhost:9200/customer/info/1?pretty" -H 'Content-Type: application/json' -d'
{
  "name": "John Doe",
  "address": "123 South Rd"
  "cell": 1018765234
}
'
