FROM mongo

COPY prices.json /prices.json

CMD mongoimport --host mongo --db stockkly --collection prices --type json --file prices.json --jsonArray

# COPY products.json /products.json

# CMD mongoimport --host mongo --db stockkly --collection products --type json --file products.json --jsonArray