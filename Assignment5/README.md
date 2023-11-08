
You run your server by providing the IP address and port number as command-line arguments when you start the server script, like this:

```python
    python server.py <server_ip> <server_port>
```

If you are testing the system locally, you can keep the host as 'localhost'.

If you want to test the system on a remote machine, you need to replace 'localhost' with the IP address of the remote machine.

Here is a simple way to do this:

    On the remote machine, open the terminal.

    Run the command ipconfig (for Windows) or ifconfig (for macOS/Linux).

    Note down the IPv4 address of the remote machine.

    In your code, replace 'localhost' with the IPv4 address of the remote machine.

    Save the changes and run the updated code.

For example, if the IPv4 address of the remote machine is 192.168.1.108, the host will be:

```python

host = '192.168.1.108'
```

Make sure your partner's server is running and listening on the specified IP address and port.

Ensure that your partner's server is not blocked by firewalls or security settings that might prevent incoming connections.

Make sure your partner's IP address and port are correctly provided as command-line arguments when running the client program.

Verify that your client and your partner's server are on the same network or can reach each other over the internet if you're not on the same local network.

Remember to replace the port number in the host value if the default port is not being used.
