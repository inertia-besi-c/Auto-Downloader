import time as t
from csvtools import *

cg_folder = "Caregiver/"
pt_folder = "Patient/"

roles = ["PT1","PT2","CG1","CG2"]
mf = ["_Pain_EMA_Results.csv","_EndOfDay_EMA_Activity.csv"]
inputdateformat = "%Y/%m/%d %H:%M:%S"
outputdateformat ="%m/%d/%Y %I:%M;%S %p"
dic = {}

delay = 20

def datestr_to_date(datestr):
    return t.strptime(datestr,inputdateformat)

def date_to_datestr(date):
    return t.strftime(outputdateformat,date)

tbt = datestr_to_date("2000/06/16 00:16:00")

while True:
    for role in roles:
        try:
            if "PT" in role:
                _Pain_Data = read(pt_folder+role+mf[0])
            else:
                _Pain_Data = read(cg_folder+role+mf[0])
            for i in range(5):
                val = _Pain_Data[-1-i]
                if "null" not in str.lower(val[-1]):
                    dic[role+"pain"] = datestr_to_date(val[0])
                    break
                else:
                    dic[role+"pain"] = tbt
        except Exception as e:
            print(e)
            dic[role+"pain"] = tbt
        
        try:
            if "PT" in role:
                _Pain_Data = read(pt_folder+role+mf[0])
            else:
                _Pain_Data = read(cg_folder+role+mf[0])
            for i in range(5):
                val = _Pain_Data[-1-i]
                if "null" not in str.lower(val[-1]):
                    dic[role+"eod"] = datestr_to_date(val[0])
                    break
                else:
                    dic[role+"eod"] = tbt
        except Exception as e:
            dic[role+"eod"] = tbt
    
    
    LastPTP = tbt
    LastCGP = tbt
    LastPTE = tbt
    LastCGE = tbt

    if dic["PT1pain"] > dic["PT2pain"]:
        LastPTP = dic["PT1pain"]
    else:
        LastPTP = dic["PT2pain"]

    if dic["CG1pain"] > dic["CG2pain"]:
        LastCGP = dic["CG1pain"]
    else:
        LastCGP = dic["CG2pain"]

    if dic["PT1eod"] > dic["PT2eod"]:
        LastPTE = dic["PT1oed"]
    else:
        LastPTE = dic["PT2eod"]
    
    if dic["CG1eod"] > dic["CG2eod"]:
        LastCGE = dic["CG1oed"]
    else:
        LastCGE = dic["CG2eod"]

    print("Last Patient Pain Event | " + date_to_datestr(LastPTP))
    print("Last Caregiver Pain Event | " + date_to_datestr(LastCGP))
    print("\n")
    print("Last Patient Daily EMA | " + date_to_datestr(LastPTE))
    print("Last Caregiver Daily EMA | " + date_to_datestr(LastPTE))

    t.sleep(delay)
