#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Variables
EC2_USER="ec2-user"
EC2_HOST="your-ec2-instance-public-dns"
PEM_FILE="path/to/your-key-pair.pem"
REMOTE_DIR="/home/ec2-user/your-app"
LOCAL_DIR="."

# Print the start of the deployment
echo "Starting deployment to EC2 instance..."

# Copy files to the EC2 instance
echo "Copying files to EC2 instance..."
scp -i $PEM_FILE -r $LOCAL_DIR/* $EC2_USER@$EC2_HOST:$REMOTE_DIR

# SSH into the EC2 instance and run deployment commands
echo "Running deployment commands on EC2 instance..."
ssh -i $PEM_FILE $EC2_USER@$EC2_HOST << EOF
  # Navigate to the application directory
  cd $REMOTE_DIR

  # Pull the latest changes from the repository
  git pull origin main

  # Install dependencies
  pip install -r requirements.txt

  # Run database migrations (if applicable)
  # python manage.py migrate

  # Restart the application (assuming a systemd service)
  sudo systemctl restart your-app.service

  # Print the status of the application
  sudo systemctl status your-app.service
EOF

# Print the end of the deployment
echo "Deployment to EC2 instance completed successfully."
