from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import json
import os


from app.contract_logic import load_contracts, add_contract, complete_contract
from app.contract_logic import validate_contract

from flask import Flask, request, jsonify
from app.contract_logic import add_contract

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    contract_name = data.get('contract_name')
    contract_details = data.get('contract_details')

    # Process the contract using a function from contract_logic.py
    result = add_contract(contract_name, contract_details)

    return jsonify({'status': 'success', 'result': result})

DATA_PATH = "contracts/saved_dads.json"


class DLARHandler(BaseHTTPRequestHandler):
   def do_GET(self):
       if self.path == "/":
           self.send_response(200)
           self.send_header("Content-type", "text/html")
           self.send_header("Access-Control-Allow-Origin", "*")  # ✅ Allow CORS for frontend JS if needed
           self.end_headers()
           with open("templates/index.html", "r") as f:
               self.wfile.write(f.read().encode())


       elif self.path == "/style.css":
           self.send_response(200)
           self.send_header("Content-type", "text/css")
           self.end_headers()
           with open("static/style.css", "r") as f:
               self.wfile.write(f.read().encode())


       elif self.path == "/static/script.js":  # ✅ NEW: Serve script.js
           self.send_response(200)
           self.send_header("Content-type", "application/javascript")
           self.end_headers()
           with open("static/script.js", "r") as f:
               self.wfile.write(f.read().encode())




       elif self.path == "/contracts":


           self.send_response(200)


           self.send_header("Content-type", "application/json")


           self.end_headers()


           contracts = load_contracts()


           self.wfile.write(json.dumps(contracts).encode())






       else:
           # ✅ NEW: Handle unknown GET paths
           self.send_response(404)
           self.end_headers()
           self.wfile.write(b"404 Not Found")


   def do_POST(self):
       print(f"POST request received at: {self.path}")
       try:
           # ✅ Defensive check for Content-Length
           content_length = int(self.headers.get('Content-Length', 0))
           if content_length == 0:
               self.send_response(400)
               self.end_headers()
               self.wfile.write(b"Missing form data.")
               return


           body = self.rfile.read(content_length).decode()
           print(f"Form data: {body}")


           data = parse_qs(body)


           if self.path == "/submit":
               content_length = int(self.headers['Content-Length'])
               body = self.rfile.read(content_length).decode()
               data = parse_qs(body)
               dad_text = data.get("dad", [""])[0]


               add_contract(dad_text)


               self.send_response(303)
               self.send_header("Location", "/")
               self.end_headers()

               errors = validate_contract(dad_text)
               if errors:
                   self.send_response(400)
                   self.send_header("Content-type", "application/json")
                   self.end_headers()
                   self.wfile.write(json.dumps({"errors": errors}).encode())
                   return


               # Load existing or create new list
               if os.path.exists(DATA_PATH):
                   with open(DATA_PATH, "r") as f:
                       existing = json.load(f)
               else:
                   existing = []


               existing.append(record)


               with open(DATA_PATH, "w") as f:
                   json.dump(existing, f, indent=2)


               print(f"Agreement saved. Redirecting.")
               self.send_response(303)
               self.send_header("Location", "/")
               self.end_headers()




           elif self.path == "/complete":


               content_length = int(self.headers['Content-Length'])


               body = self.rfile.read(content_length).decode()


               data = parse_qs(body)


               index = int(data.get("index", [None])[0])


               complete_contract(index)


               self.send_response(303)


               self.send_header("Location", "/")


               self.end_headers()


               print(f"Completing contract at index: {index}")


               # Load, modify, and save
               try:
                   with open(DATA_PATH, "r") as f:
                       contracts = json.load(f)


                   if 0 <= index < len(contracts):
                       contracts[index]["status"] = "completed"


                       with open(DATA_PATH, "w") as f:
                           json.dump(contracts, f, indent=2)


                   self.send_response(303)
                   self.send_header("Location", "/")
                   self.end_headers()


               except Exception as e:
                   print(f"Error during status update: {e}")
                   self.send_response(500)
                   self.end_headers()


           else:
               # ✅ Unknown POST endpoint
               self.send_response(404)
               self.end_headers()
               self.wfile.write(b"Unknown POST endpoint")


       except Exception as e:
           print(f"Error during POST handling: {e}")
           self.send_response(500)
           self.end_headers()






# ✅ Start the server
httpd = HTTPServer(("localhost", 8080), DLARHandler)
print("DLAR server running at http://localhost:8080")
httpd.serve_forever()
