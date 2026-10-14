Deploy app first :)

http://localhost:8000/ -- api for checking the Postgres contents

## Examples of adding/deleting users

curl -X POST -H "Content-Type: application/json" -d '{"nume":"Popescu","prenume":"Ion"}' http://localhost:8000/users

curl -X DELETE -H "Content-Type: application/json" -d '{"nume":"Popescu","prenume":"Ion"}' http://localhost:8000/users

curl http://localhost:8000/get  -- get users
