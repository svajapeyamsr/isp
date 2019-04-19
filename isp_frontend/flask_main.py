from flask import *


app=Flask(__name__)


##Flask pages

#Index
@app.route('/',methods=['GET','POST'])
def index():
    bodytext=Markup("<p> Welcome to the home page. Please select an option:- <p><a href='/Topology' target='127.0.0.1:80'>Topology</a></p> <p><a href='/Link_State' target='127.0.0.1:80'>Link State</a></p><p><a href='/Current_Traffic' target='127.0.0.1:80'>Current Traffic</a></p> <p><a href='/Top_Talkers' target='127.0.0.1:80'>Top Talkers</a></p>")
    return(bodytext)



#Topology
@app.route('/Topology',methods=['GET','POST'])
def Topology():
    if request.method=='GET':
        response="This is Topology page, babe"
        return(response)

#Link_State
@app.route('/Link_State',methods=['GET','POST'])
def Link_State():
    if request.method=='GET':
        response="This is Link_State page, babe"
        return(response)

#Current_Traffic
@app.route('/Current_Traffic',methods=['GET','POST'])
def Current_Traffic():
    if request.method=='GET':
        response="This is Current_Traffic page, babe"
        return(response)


#Top Talkers
@app.route('/Top_Talkers',methods=['GET','POST'])
def Top_Talkers():
    if request.method=='GET':
        response="This is Top_Talkers page, babe"
        return(response)




##MAIN
if __name__=='__main__':
    app.debug=True
    app.run(host='127.0.0.1',port=80,threaded=True)
