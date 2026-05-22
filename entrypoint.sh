#!/bin/bash
# Stop execution immediately if any command fails
set -e

echo "========================================"
echo "Starting FastAPI & Ray Serve..."
echo "========================================"

# We assume the model/data is already inside the container
# because we copied it during the docker build phase.
exec python madewithml/serve.py --run_id "$RUN_ID"