#/bin/bash
sleep 5

uvicorn api:gojek --reload --host 0.0.0.0 --port 3000