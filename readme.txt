# Mookey
mookey is a python script which uses Asterisk ARI to connect to asterisk and records the voice of caller during talking and stops during silent .




installation :
pip install ari
edit ari-py.py file and configure Asterisk ARI credentials
run it : python ari-py.py


add this to extentions.conf

[Mookey]
exten => 1,1,NoOp()
 same =>     n,Stasis(Mookey,${EXTEN})
 same =>     n,Hangup()


dial 1 in context Mookey to get to stasis application Mookey
call will be answered
listens to you , if you talk it will record , if you stop talking it will playback the recorded message , if you talk again , it will start a new recording


