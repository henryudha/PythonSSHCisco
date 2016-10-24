#!/usr/bin/python

## (c) henryudha@gmail.com

# permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "software"), to deal
# in the software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the software, and to permit persons to whom the software is
# furnished to do so, subject to the following conditions:
#
# the above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the software.
#
# the software is provided "as is", without warranty of any kind, express or
# implied, including but not limited to the warranties of merchantability,
# fitness for a particular purpose and noninfringement. in no event shall the
# authors or copyright holders be liable for any claim, damages or other
# liability, whether in an action of contract, tort or otherwise, arising from,
# out of or in connection with the software or the use or other dealings in
# the software.

import paramiko

class Cisco:
    _ip = ""
    _port = 22
    _username= ""
    _password = ""

    def __init__(self,ip,port,username, password):
        self._ip = ip
        self._port = port
        self._username = username
        self._password = password
        self.connection = None
        self.channel = None

    def connect(self):
        self.connection = paramiko.SSHClient()
        self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.connection.connect(self._ip,
                        port=self._port,
                        username=self._username,
                        password=self._password,
                        allow_agent=False, look_for_keys=False)
        self.channel = self.connection.invoke_shell()
        buff = ""
        while not buff.rstrip().endswith("#") :
            resp = self.channel.recv(9999)
            buff += resp.decode("utf-8")
        return buff
    def execute_command(self, command):
        buff = ""
        self.channel.send(command + "\n")
        while not buff.rstrip().endswith("#"):
            buff += self.channel.recv(9999).decode('utf-8')
        buff.split("\n")
        return buff
    def close(self):
        self.connection.close()
        self.channel = None
        self.connection = None

