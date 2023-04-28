import os

from deta import Deta

from dotenv import load_dotenv



load_dotenv(".env")
#---database key--------
DETA_KEY = os.getenv("DETA_KEY")


#------connect to database--------
deta = Deta["DETA_KEY"]


db = deta.Base("emissions")