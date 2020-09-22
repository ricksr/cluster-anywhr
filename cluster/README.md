# cluster-Backend-installation

1. npm i
2. pip install -r requirements.txt 
3. sls offline start (should point too localhost:3000/prod/{API*})

API 's

// query_hex
// https://24tflrq9y9.execute-api.us-east-1.amazonaws.com/prod/get-hex-by-name?name=a

{
  "hexagons": [
    {
      "hex": {
        "n1": "NO",
        "n2": "81717846-1ca5-4486-bc3f-d224f7600ceb",
        "n3": "91f9607c-aeec-46ff-95ce-5ed59c353318",
        "n4": "NO",
        "n5": "5c88c0cc-819d-4708-8ee3-d701adfd7441",
        "n6": "e39e5cbd-c2de-4c48-9418-62bb5192fb87"
      },
      "is_active": "TRUE",
      "name": "a"
    }
  ]
}

// add_hex
// https://24tflrq9y9.execute-api.us-east-1.amazonaws.com/prod/add-hex?src=ll_4&new=ll_5&loc=5

{
  "response": [
    {
      "hexagon_id": "5151c9e6-271a-45e7-8093-690510539920",
      "n1": "NO",
      "n2": "NO",
      "n3": "NO",
      "n4": "44d076dd-f99b-473b-9071-a08414a2605e",
      "n5": "NO",
      "n6": "4881e703-c111-4fcf-a83a-7b9f4e9105fd"
    }
  ],
  "statusCode": 200
}

// Removed - ll_5
querying its neighbour ll_4
https://24tflrq9y9.execute-api.us-east-1.amazonaws.com/prod/get-hex-by-name?name=ll_4
 
// ll_5 removed from border 5 - n6 , 

{
  "hexagons": [
    {
      "hex": {
        "n1": "NO",
        "n2": "NO",
        "n3": "NO",
        "n4": "44d076dd-f99b-473b-9071-a08414a2605e",
        "n5": "NO",
        "n6": "NO"
      },
      "is_active": "TRUE",
      "name": "ll_4"
    }
  ]
}