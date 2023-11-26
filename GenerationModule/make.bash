#!/bin/bash

# Step 1: Run make_mongo_collections.py
echo "Step 1: Running make_mongo_collections.py"
python make_mongo_collections.py

# Check if make_mongo_collections.py completed successfully
if [ $? -ne 0 ]; then
  echo "Error: make_mongo_collections.py failed"
  exit 1
fi

# Step 2: Run synthasize_streamlit.py
echo "Step 2: Running synthasize_streamlit.py"
python synthasize_streamlit.py

# Check if synthasize_streamlit.py completed successfully
if [ $? -ne 0 ]; then
  echo "Error: synthasize_streamlit.py failed"
  exit 1
fi

# Step 3: Run Streamlit app main.py
echo "Step 3: Running Streamlit app main.py"
streamlit run main.py

# Check if streamlit run completed successfully
if [ $? -ne 0 ]; then
  echo "Error: Streamlit app main.py failed"
  exit 1
fi

echo "All steps completed successfully"