import base64
open_icon = open("multChrome.ico","rb")
b64str = base64.b64encode(open_icon.read())
open_icon.close()
write_data = "img = '{0}'".format(b64str)
f = open("icon.py","w+")
f.write(write_data)
f.close()


