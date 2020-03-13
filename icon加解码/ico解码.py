import base64,icon
with open('icon.py') as f_obj:
	for i in f_obj:
		aa=i.split('=')
		with open('%s.ico'%aa[0],'wb+') as ff:
			ff.write(base64.b64decode(eval('icon.%s'%aa[0])))