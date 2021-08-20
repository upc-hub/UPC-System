import requests
import json
import os
import codecs

def connect_Sam_schedule_api(typea, typeb, typec, typed, typee, typef):
  url = "http://localhost:9000/aplas/scheduling"      #connect to Sam's scheduling api
  
  S1 = "BasixAppX1"      #types of APLAS jobs
  S2 = "BasixAppX2"
  S3 = "ColorGameX"
  S4 = "SoccerMatch"
  S5 = "AnimalTour"
  S6 = "MyLibrary"
 
  payload = json.dumps({     #input parameters to the scheduling api
    "params": [
      {
        "job_type": "S1",
        "job_amount": typea
      },
      {
        "job_type": "S2",
        "job_amount": typeb
      },
      {
        "job_type": "S3",
        "job_amount": typec
      },
      {
        "job_type": "S4",
        "job_amount": typec
      },
      {
        "job_type": "S5",
        "job_amount": typec
      },
      {
        "job_type": "S6",
        "job_amount": typec
      }
    ]
  })
  headers = {
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)               #receive api response
  json_data = json.loads(response.text)
  
  with codecs.open('/home/heinhtet/Desktop/UPC_Master/data.json', 'w', 'utf8') as f:    #save as the json file
    f.write(json.dumps(json_data, sort_keys = True, ensure_ascii=False))
  
if __name__ == "__main__":                                                              #receive the input parameters dynamically from the UPC master program
  import argparse
  parser = argparse.ArgumentParser(description="Sam san shceduling")
  parser.add_argument("type1", help="number of type-1 jobs")
  parser.add_argument("type2", help="number of type-2 jobs")
  parser.add_argument("type3", help="number of type-3 jobs")
  parser.add_argument("type4", help="number of type-4 jobs")
  parser.add_argument("type5", help="number of type-5 jobs")
  parser.add_argument("type6", help="number of type-6 jobs")
  args = parser.parse_args()
  typea = args.type1
  typeb = args.type2
  typec = args.type3
  typed = args.type4
  typee = args.type5
  typef = args.type6
  connect_Sam_schedule_api(typea, typeb, typec, typed, typee, typef)