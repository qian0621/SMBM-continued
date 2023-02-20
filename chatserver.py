from flask_socketio import SocketIO,send,emit
from flask import request,session
from app import app
import shelve
import datetime 


socketio=SocketIO(app,cors_allowed_origins='*')


@socketio.on('message')
def handle_message(message):
    if message['mes'] != 'connected':
        if message['mes'] !='' and message['customerId'] !='0':
            print("do")
            db = shelve.open('storage/charserver.db', 'c')
            try:
                
                messages=db[message['customerId']] 
                messages.append(message)
                db[message['customerId']]=messages
                
                send(message,broadcast=True)
                # for staff people list 
                peoples=db['peoples']
                tosend=[]
                customerName=''
                for people in peoples:
                    
                    if people['customerId']!=message['customerId']:
                        tosend.append(people)
                    else:
                        customerName=people['customerName']
                message['customerName']=customerName
                tosend.insert(0,message)
                db['peoples']=tosend
                send(tosend,broadcast=True)
                db.close()
            except:
                db[message['customerId']]=[message]
                try:
                    peoples=[message]+db['peoples']
                    db['peoples']=peoples
                    send(peoples,broadcast=True)
                except:
                    db['peoples']=[message]
                    send([message],broadcast=True)
                db.close()
                send(message,broadcast=True)
                print("Error in creating Feedbacks in chatserver.db.")   
    else:  
        if message['customerId'] == 'all':
            try:
                db = shelve.open('storage/charserver.db', 'r')
                peoples=db['peoples']
                send(peoples,broadcast=True)
            except:
                   print("No user")
        try:
            db = shelve.open('storage/charserver.db', 'r')
            messages=db[message['customerId']] 
            db.close() 
            for mes in messages:
                send(mes,room=request.sid, broadcast=True)
        except:
            print("No message for this user!")




@socketio.on('forgetmessage') 
def toGet(customerId):
    try:
        db = shelve.open('storage/charserver.db', 'r')
        messages=db[str(customerId)]
        emit('oldmessage',messages)
    except:
        print("No message for this user!")
    


@socketio.on('deletemessage') 
def delete():
    current_user=session['userInfo']
    user_id=current_user.count 
    try:
        db = shelve.open('storage/charserver.db')
        db[str(user_id)]=[]
        emit('newmessage',[])
    except:
        print("No message for this user!")
