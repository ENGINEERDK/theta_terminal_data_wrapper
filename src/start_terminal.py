import logging
import os
import time
import subprocess
import threading
import theta_terminal_java
import signal
import sys
import psutil

class ThetaTerminalSingleton:
    _instance = None  # Class-level attribute to hold the singleton instance
    _started = False  # Track if the terminal has already been started

    def __new__(cls, *args, **kwargs):
        """
        Override __new__ to implement the singleton pattern.
        """
        if cls._instance is None:
            cls._instance = super(ThetaTerminalSingleton, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initialize the ThetaTerminalSingleton instance.
        """
        # Only initialize the terminal once
        if not self.__class__._started:
            self.logger = logging.getLogger("ThetaTerminalSingleton")
            self.__class__._started = True  # Mark as started to prevent reinitialization
            self._start_terminal()
        
        # Register cleanup handler for program exit
        signal.signal(signal.SIGINT, self._cleanup_and_exit)  # Handle Ctrl+C (SIGINT)
        signal.signal(signal.SIGTERM, self._cleanup_and_exit)  # Handle termination signals


    def _log_stream(self, stream, stream_type):
        for line in iter(stream.readline, ''):
            print(f"[{stream_type}]: {line.strip()}")
            if "CONNECTED" in line:
                if "MDDS" in line:
                    self.mdds_connected = True
                if "FPSS" in line:
                    self.fpss_connected = True
            # Log output to main logger as well
            self.logger.info(f"[{stream_type}]: {line.strip()}")

    def _start_terminal(self):
        """
        Start the Theta Terminal if it has not been started yet.
        """
        script_path = os.path.join(theta_terminal_java.__path__[0], "runThetaTerminal.sh")
        print(f"Starting Theta Terminal using script: {script_path}")

        try:
            # Start the process without blocking
            self.process = subprocess.Popen(
                ["bash", script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            print(f"Theta Terminal started with PID: {self.process.pid}")
            # Initialize connection flags
            self.mdds_connected = False
            self.fpss_connected = False
            
            # Start threads to log stdout and stderr
            threading.Thread(target=self._log_stream, args=(self.process.stdout, "STDOUT"), daemon=True).start()
            threading.Thread(target=self._log_stream, args=(self.process.stderr, "STDERR"), daemon=True).start()
            
            # Wait until both MDDS and FPSS connections are established
            while not (self.mdds_connected and self.fpss_connected):
                print("Waiting for MDDS and FPSS to connect...")
                time.sleep(1)  # Check every second

            print("Both MDDS and FPSS connected. Proceeding with further execution.")

        except Exception as e:
            self.logger.error(f"An error occurred while starting Theta Terminal: {e}")

    def _cleanup_and_exit(self, signum=None, frame=None):
        """Ensure cleanup of Theta Terminal process upon program exit."""
        if hasattr(self, 'process') and self.process and self.process.poll() is None:  # Check if process is running
            print("Terminating Theta Terminal...")
            
            try:
                # Try graceful termination
                self.process.terminate()  
                # Wait for a few seconds to ensure graceful exit
                self.process.wait(timeout=5)  
            except subprocess.TimeoutExpired:
                print("Graceful termination failed, forcefully killing the process...")
                # If graceful termination fails, kill the process forcefully
                self._force_kill_process(self.process)
            except Exception as e:
                self.logger.error(f"Error during process termination: {e}")
            
            print("Theta Terminal process terminated.")
        else:
            print("Theta Terminal process not running or already terminated.")
        
        # Ensure the program exits after cleanup
        print("Exiting program...")
        sys.exit(0)  # Exit the program

    def _force_kill_process(self, process):
        """
        Kill the process and all its children if any.
        """
        try:
            # Use psutil to get the process tree and kill the main process and its children
            parent_pid = process.pid
            parent = psutil.Process(parent_pid)

            # Terminate the child processes first
            for child in parent.children(recursive=True):
                print(f"Terminating child process with PID: {child.pid}")
                child.terminate()

            # Finally, kill the parent process itself
            print(f"Terminating parent process with PID: {parent_pid}")
            parent.terminate()

            # Wait for process termination
            parent.wait(timeout=5)
            print(f"Parent process {parent_pid} terminated successfully.")

        except psutil.NoSuchProcess:
            print("Process already terminated or does not exist.")
        except Exception as e:
            self.logger.error(f"Error during forceful process termination: {e}")
