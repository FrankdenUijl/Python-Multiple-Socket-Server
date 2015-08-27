Python-Multiple-Socket-Server
=============================

Python Multiple Socket Server easy to use.

Currently this seems stable enough to use for X amount of connections and messages.

Please note that the admin user is not finished.

## Features
* Run a multiple socket server in python
* Ready to use, but some admin functions are not ready
* Build in admin user

## Example

Planning to make a chatroom example with CoronaSDK in LUA

## How to use

Add in Client.py in function client_functions your own game/chat logic

``` python

def client_functions(self, msg_obj):
		if msg_obj['t'] == 0: #example login
			msg_obj['c'] #game or chatroom logic here

```

This is in lua but you can use other languages!

``` lua

sock, err = socket.connect( server,  port )
--and other logic to setup a server!

--first you need to send a handshake so the server accept you, check settings.ini
c = {
	hsid = handshake -- cb72d33a-15f2-4fdd-b0a9-f30313cb910a
}
sock:send( '{"t" : 0, "c" : '..json.encode(c)..'}\0'  ) --t is type of message, 0 is handshake

--then you can send whatever you want

message = {
  t = 100, --if you use 100 your message go to client_functions in python
  c = {
    t = 0, --you can use this to give your own message a type
    message = "Hello world" -- whatever you want
  }
}

local send_result, err, num_byes = self.sock:send( json.encode(message) ..'@end\0'  ) --@end\0 is needed!

```
