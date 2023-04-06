# Title: File Sending Simulator

## Description
Please create a file sending simulator using UDP ( no connect(), just use send-to and recv-from) in which file are fragmented and sent using block per 1 kb.
implement client and server at different PC.

[1]: Client can pick file name that would be sent (minimum text file size 10mb)
[2]: then client send the file seqentially
[3]: after it finished sending, server and client will display how many % data is sucessfully delivered

## Usage
run `server.py` to start the server, then run `client.py` to start the client.
Enter the path of the file you want to send to the server. The server will receive the file and save it in the same directory as `server.py`.