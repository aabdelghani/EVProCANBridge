#!/bin/bash

# Calculate the absolute path to the canLogger.py script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PYTHON_SCRIPT="$SCRIPT_DIR/src/canLogger.py"
LOG_DIR="$SCRIPT_DIR/log"
LOG_FILE="$LOG_DIR/canLogger.log"

# Ensure log directory exists
mkdir -p "$LOG_DIR"

# Command to add to rc.local, using the calculated paths, and ensure it runs in the background
CMD="sudo python3 $PYTHON_SCRIPT > $LOG_FILE 2>&1 &"

# Check for presence of rc.local, and ensure it's executable
RC_LOCAL="/etc/rc.local"
if [ ! -f "$RC_LOCAL" ]; then
    echo "#!/bin/bash" | sudo tee "$RC_LOCAL"
    echo "exit 0" | sudo tee -a "$RC_LOCAL"
    sudo chmod +x "$RC_LOCAL"
    echo "rc.local file created and made executable."
fi

# Check if the command already exists in rc.local to avoid duplicates
if grep -qF -- "$CMD" "$RC_LOCAL"; then
    echo "Command already exists in /etc/rc.local."
else
    # Add the command to rc.local before 'exit 0', and run in the background
    sudo sed -i "/^exit 0/i $CMD" "$RC_LOCAL"
    echo "Command added to /etc/rc.local."
fi
