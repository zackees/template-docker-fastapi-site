#!/bin/bash

# Attempt to change directory to the directory containing the script
script_dir=$(dirname "$(realpath "${BASH_SOURCE[0]}")")
cd "$script_dir" || { 
    echo "Error: Failed to change to the script's directory. Please check the path."
    exit 1
}

# echo out the current directory
echo "Running docker-compose in $(pwd)"

# parse the published port in the docker-compose.yml file
port=$(grep -A 1 "ports:" docker-compose.yml | grep "published" | cut -d ':' -f 2 | tr -d '[:space:]')
echo "Starting docker-compose on port $port"

if command -v python3 &>/dev/null; then
	alias python=python3
	PYTHON_CMD=python3
elif command -v python &>/dev/null; then
	PYTHON_CMD=python
else
	echo "Neither python nor python3 is available. Exiting."
	exit 1
fi

if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker and try again."
    exit 1
fi
docker-compose down --rmi all
echo -e "\n##########################\n# Launching a web browser to http://localhost:$port in 20 seconds"
echo -e "# If you don't see a web browser, please open one and navigate to http://localhost:$port\n##########################\n"
# finish
echo "Starting docker-compose in $(pwd)"
(sleep 20; $PYTHON_CMD -c "import webbrowser; webbrowser.open('http://localhost:$port')") &
docker-compose up
