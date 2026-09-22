import os
import sys

# Ensure backend folder is in Python path for Vercel Serverless Function execution
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import app