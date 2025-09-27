curl -s -X POST http://localhost:8080/products -H 'content-type: application/json' \
  -d '{"name":"Harina","unit":"g"}'
curl -s http://localhost:8080/products
