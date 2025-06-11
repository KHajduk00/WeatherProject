#!/bin/bash
cd "$(dirname "$0")"
streamlit run app.py --server.port 8501 --server.address localhost