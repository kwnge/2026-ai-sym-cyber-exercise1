import paramiko
from typing import Optional

class SSHClient:
    """Persistent SSH client that maintains connection state"""
    
    def __init__(
        self,
        hostname: str,
        username: str,
        password: Optional[str] = None,
        key_filename: Optional[str] = None,
        port: int = 22
    ):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.key_filename = key_filename
        self.port = port
        self.client: Optional[paramiko.SSHClient] = None
    
    def _ensure_connected(self) -> bool:
        """Ensure SSH connection is active, reconnect if needed"""
        if self.client is not None:
            try:
                # Test if connection is alive
                self.client.exec_command('echo test', timeout=2)
                return True
            except:
                self.client = None
        
        # Establish new connection
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            if self.key_filename:
                self.client.connect(
                    hostname=self.hostname,
                    port=self.port,
                    username=self.username,
                    key_filename=self.key_filename
                )
            elif self.password:
                self.client.connect(
                    hostname=self.hostname,
                    port=self.port,
                    username=self.username,
                    password=self.password
                )
            else:
                raise ValueError("Either password or key_filename must be provided")
            
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
    
    def execute_command(self, command: str) -> str:
        """
        Execute a command on the remote server via SSH.
        
        Args:
            command: The shell command to execute
            
        Returns:
            String containing the command output or error message
        """
        if not self._ensure_connected():
            return "ERROR: Could not connect to SSH server"
        
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            exit_code = stdout.channel.recv_exit_status()
            
            stdout_text = stdout.read().decode('utf-8')
            stderr_text = stderr.read().decode('utf-8')
            
            if exit_code == 0:
                return stdout_text if stdout_text else "Command executed successfully (no output)"
            else:
                return f"Command failed (exit code {exit_code}):\n{stderr_text}"
        except Exception as e:
            return f"ERROR: {str(e)}"
    
    def close(self):
        """Close SSH connection"""
        if self.client:
            self.client.close()
            self.client = None
