import sys
import logging
import os
from dotenv import load_dotenv

sys.path.insert(0, "/home/danylo_hnyp_ir_2023/cloud-nulp")

load_dotenv("/home/danylo_hnyp_ir_2023/cloud-nulp/.env")

from main import app as application
