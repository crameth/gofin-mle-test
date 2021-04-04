echo "Unzipping ./data/cs_assignment.gz"
gzip -d ./data/cs_assignment.gz

echo "Setting up API and DB"
docker-compose up --build