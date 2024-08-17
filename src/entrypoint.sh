#!/bin/bash

cd /app/core
python3 fetch_and_organize_data.py
python3 api.py &

cd /app/frontend
yarn dev