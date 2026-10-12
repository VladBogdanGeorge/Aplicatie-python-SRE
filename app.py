import sys
from fastapi import FastAPI
from db import init_db, add_persoana, delete_persoana, get_persoane

app = FastAPI()
init_db()

@app.post("/add")
def add(nume: str, prenume: str):
    add_persoana(nume, prenume)
    return {"status": "added"}

@app.delete("/delete")
def delete(nume: str, prenume: str):
    delete_persoana(nume, prenume)
    return {"status": "deleted"}

@app.get("/get")
def get():
    return {"persoane": get_persoane()}

# CLI usage
if __name__ == "__main__":
    init_db()
    args = sys.argv[1:]
    if len(args) == 3 and args[2].upper() == "ADD":
        add_persoana(args[0], args[1])
        print("Adaugat!")
    elif len(args) == 3 and args[2].upper() == "DELETE":
        delete_persoana(args[0], args[1])
        print("Sters!")
    elif len(args) == 1 and args[0].upper() == "GET":
        print(get_persoane())
    else:
        print("Argumente invalide.")