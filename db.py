import web

db = web.database(dbn="sqlite", db="rest.db")
db.printing = False # Turns of debug output and sheisse
