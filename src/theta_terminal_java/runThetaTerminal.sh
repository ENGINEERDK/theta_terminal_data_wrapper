#!/bin/bash

# Set the path to your .jar file
JAR_PATH="src/theta_terminal_java/ThetaTerminal.jar"

# Pass in the username and password as arguments to this script
USERNAME='suresh2398kumar@gmail.com'
PASSWORD='$India23'

# Run the .jar file with the provided username and password
java -jar "$JAR_PATH" "$USERNAME" "$PASSWORD"

