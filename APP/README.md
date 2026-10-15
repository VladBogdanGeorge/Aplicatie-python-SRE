Deploy app first :)

http://localhost:8000/ -- api for checking the Postgres contents

## Examples of adding/deleting users

 curl -X POST http://localhost:8000/add   -H "Content-Type: application/json"   -d '{"nume":"Popescu","prenume":"Ion"}'

 curl -X DELETE http://localhost:8000/delete   -H "Content-Type: application/json"   -d '{"nume":"Popescu","prenume":"Ion"}'

curl http://localhost:8000/get  -- get users
