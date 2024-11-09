#!/bin/bash

# Path to your .jar file
JAR_PATH="src/theta_terminal_java/ThetaTerminal.jar"

# username and password of ThetaData account
USERNAME='*****@gmail.com'
PASSWORD='*******'

# Run the .jar file with the provided username and password
java -jar "$JAR_PATH" "$USERNAME" "$PASSWORD"

