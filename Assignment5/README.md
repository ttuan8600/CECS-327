If you are testing the system locally, you can keep the host as 'localhost'.

If you want to test the system on a remote machine, you need to replace 'localhost' with the IP address of the remote machine.

Here is a simple way to do this:

    On the remote machine, open the terminal.

    Run the command ipconfig (for Windows) or ifconfig (for macOS/Linux).

    Note down the IPv4 address of the remote machine.

    In your code, replace 'localhost' with the IPv4 address of the remote machine.

    Save the changes and run the updated code.

Make sure that the remote machine and the machine running the code are connected to the same network. Also, ensure that the required port is open and accessible.

For example, if the IPv4 address of the remote machine is 192.168.1.10, the host will be:

```python

host = '192.168.1.10'
```

This updated host value should be used by both the client and the server in their respective code. This way, they can communicate with each other over the network.

Remember to replace the port number in the host value if the default port is not being used.
