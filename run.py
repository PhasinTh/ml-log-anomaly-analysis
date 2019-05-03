import os
import sys
from app import app

if __name__ == "__main__":
  workingPort = sys.argv[1]
  app.run(host="0.0.0.0", port=int(workingPort), debug=False)
# app.run(port=5000)

# To Run:
# python run.py
# or
# python -m flask run
