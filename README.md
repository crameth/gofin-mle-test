# Introduction

GoFin's coding challenge / Web Service.

# Dependencies

* gzip (for unarchiving the compressed CSV)
* docker-compose (task 4, requirement #3)
* All required Python packages are documented under `requirements.txt` and installed during Docker build process

# Usage

Put the compressed dataset `cs_assignment.gz` inside `./data` folder.

`bash install.sh` will do the rest.

To teardown: `docker-compose down`

# Major Design Decisions

* FastAPI because it's... fast.
* MariaDB because the test asked for SQL.
* XGBoost because it's the most efficient traditional ML method to train and run inference considering the length of the test.

The trained model is included as part of the deployment; no training will be done during deployment.
