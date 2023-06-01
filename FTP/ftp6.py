# Information:
# - For testing on local machines, install an FTP server (Filezilla, vsFTPd, etc.)
# - Specify username and password
# - Do the questions below with the ftplib library

# [FTP-1] Name and version of FTP server

# Print the name and version of the FTP server.
# Example of expected output:
# vsFTPd 3.0.2


# [FTP-2] System emulated FTP server

# Print the system emulated by the FTP server. An example of the expected output is as follows:
# 220 (vsFTPd 3.0.2)
# 331 Please specify the password.
# 230 Login successful.
# 215 UNIX Type: L8
# 221 Goodbyes.


# [FTP-3] List of files on the FTP server

# Show all files in their respective home directories on the FTP server.

# An example of the expected output is as follows:
# directory-name
# .bash_logout
# .bashrc
# .profile

# [FTP-4] Uploading files

# Upload a file to the FTP server.
# Example of expected output:
# 220 (vsFTPd 3.0.2)
# 331 Please specify the password.
# 230 Login successful.
# 200 Switching to ASCII mode.
# 150 Ok to send data.
# 226 Complete transfers.
# 221 Goodbyes.

# [FTP-5] Creates a directory

# Create a directory named "test".
# An example of the expected output is as follows:
# 220 (vsFTPd 3.0.2)
# 331 Please specify the password.
# 230 Login successful.
# 257 "/test" created
# 221 Goodbyes.



# [FTP-6] The current directory on the FTP server

# Print the current active directory in the home directory on the FTP server.
# An example of the expected output is as follows:
# 220 (vsFTPd 3.0.2)
# 331 Please specify the password.
# 230 Login successful.
# 257"/"
# 221 Goodbyes.

from ftplib import FTP

f = FTP()
res = f.connect(host='localhost')
print(res)

res = f.login(user='hugof', passwd='azerty')
print(res)

res = f.pwd()
print(res)

res = f.quit()
print(res)

# [FTP-7] Renamed directory

# Replace the name of the "test" directory created in the FTP-5 problem with "test2".
# An example of the expected output is as follows:
# 220 (vsFTPd 3.0.2)
# 331 Please specify the password.
# 230 Login successful.
# 350 Ready for RNTO.
# 250 Rename successfully.
# 221 Goodbyes.

# [FTP-8] Delete directory

# Delete the "test2" directory processed in the FTP-7 problem.
# Example of expected output:
# 250 Remove directory operation successful.

