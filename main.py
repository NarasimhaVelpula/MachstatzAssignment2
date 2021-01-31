from flask import Flask,request,jsonify
import json
import requests
import time
from operator import itemgetter
from datetime import datetime
app=Flask(__name__)
def createDateTime(obj):
    obj["time"]=datetime.strptime(obj["time"],"%Y-%m-%d %H:%M:%S")
    return obj
def createDateTime2(obj):
    obj["time"]=datetime.strptime(obj["time"],"%Y-%m-%d %H:%M:%S")
    obj["id"]=int(obj["id"][2:])
    return obj
data1=list(map(createDateTime,requests.get('https://gitlab.com/-/snippets/2067888/raw/master/sample_json_1.json').json()))
data2=list(map(createDateTime,requests.get('https://gitlab.com/-/snippets/2067888/raw/master/sample_json_2.json').json()))
data3=list(map(createDateTime2,requests.get('https://gitlab.com/-/snippets/2067888/raw/master/sample_json_3.json').json()))

#print(data1)
@app.route('/',methods=['GET'])
def func():
    return "Provide proper APIs"
@app.route('/question1',methods=['GET'])
def home():
    date1=datetime.strptime(request.args.get('start_time'),"%Y-%m-%dT%H:%M:%SZ")
    date2=datetime.strptime(request.args.get('end_time'),"%Y-%m-%dT%H:%M:%SZ")
    output={
        "shiftA" :{ "production_A_count" :0, "production_B_count" :0},
	"shiftB" :{ "production_A_count" :0, "production_B_count" :0},
	"shiftC" :{ "production_A_count" :0, "production_B_count" :0},

    }
    for obj in data1:
        if(date1<=obj["time"] and date2>=obj["time"]):
            if(int(obj["time"].strftime("%H"))>=6 and int(obj["time"].strftime("%H"))<14):
                if(obj["production_A"]==True):
                    output["shiftA"]["production_A_count"]=output["shiftA"]["production_A_count"]+1
                if (obj["production_B"] == True):
                    output["shiftA"]["production_B_count"] = output["shiftA"]["production_B_count"] + 1
            if (int(obj["time"].strftime("%H")) >= 14 and int(obj["time"].strftime("%H")) < 20):
                if (obj["production_A"] == True):
                    output["shiftB"]["production_A_count"] = output["shiftB"]["production_A_count"] + 1
                if (obj["production_B"] == True):
                    output["shiftB"]["production_B_count"] = output["shiftB"]["production_B_count"] + 1
            if (int(obj["time"].strftime("%H")) >=20 or int(obj["time"].strftime("%H")) < 6):
                if (obj["production_A"] == True):
                    output["shiftC"]["production_A_count"] = output["shiftC"]["production_A_count"] + 1
                if (obj["production_B"] == True):
                    output["shiftC"]["production_B_count"] = output["shiftC"]["production_B_count"] + 1
    return output
@app.route('/question2',methods=['GET'])
def utilisation():
    output={
        "runtime":0,
        "downtime":0,
        "utilisation":0
    }
    date1 = datetime.strptime(request.args.get('start_time'),"%Y-%m-%dT%H:%M:%SZ")
    date2 = datetime.strptime(request.args.get('end_time'),"%Y-%m-%dT%H:%M:%SZ")
    for obj in data2:
        if(obj["time"]>=date1 and obj["time"]<=date2):
            if(obj["runtime"]<1021):
                output["runtime"]=output["runtime"]+obj["runtime"]
                output["downtime"]=output["downtime"]+obj["downtime"]
            else:
                output["runtime"] = output["runtime"] + 1021
                output["downtime"] = output["downtime"] + obj["runtime"]-1021
    output["utilisation"]=(output["runtime"]/(output["runtime"]+output["downtime"]))*100
    output["downtime"] = time.strftime("%Hh:%Mm:%Ss", time.gmtime(output["downtime"]))
    output["runtime"]=time.strftime("%Hh:%Mm:%Ss", time.gmtime(output["runtime"]))
    return output
@app.route('/question3',methods=['GET'])
def avgBelt():

    #date1=datetime.strftime(request.args.get["start_time"],"%Y-%m-%dT%H"
    date1 = datetime.strptime(request.args.get('start_time'), "%Y-%m-%dT%H:%M:%SZ")
    date2 = datetime.strptime(request.args.get('end_time'), "%Y-%m-%dT%H:%M:%SZ")
    output=[]
    count={}
    for obj in data3:
        if (obj["time"] >= date1 and obj["time"] <= date2):
            temp=0
            for k in output:
                if(k["id"]==obj["id"]):
                    temp = 1
                    count[obj["id"]] = count[obj["id"]]+1
                    if(obj["state"]==True):
                     k["avg_belt1"]=k["avg_belt1"]+obj["belt1"]
                    else:
                        k["avg_belt2"] = k["avg_belt2"]+obj["belt2"]
                    break
            if(temp==0):
                var={"id":"","avg_belt1":0,"avg_belt2":0}
                count[obj["id"]]=1
                if(obj["state"]==True):
                    var["id"]=obj["id"]
                    var["avg_belt1"]= obj["belt1"]
                else:
                    var["id"] = obj["id"]
                    var["avg_belt2"] = obj["belt2"]
                output.append(var)
            #print(count)
            for k in output:
                k["avg_belt1"]=round(k["avg_belt1"]/count[k["id"]])
                k["avg_belt2"] = round(k["avg_belt2"] / count[k["id"]])
            output.sort(key=itemgetter('id'))
    return jsonify(output)



app.run()
