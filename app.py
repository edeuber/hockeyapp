import os
import time



from flask import Flask, request, render_template, url_for, redirect, send_from_directory, session
#from flask_mail import Mail, Message
from hockeyFinal import runAnalysis, expectedValue, getProbs




app = Flask(__name__)
#app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")

@app.route('/getProbs', methods=["POST"])
def getProb():
    scenario = str(request.form["scenario"])

    result = getProbs(scenario)

    probs1 = "{:.2%}".format(float(result[1]))
    probs2 = "{:.2%}".format(float(result[3]))
    probs3 = "{:.2%}".format(float(result[5]))
    probs4 = "{:.2%}".format(float(result[7]))
    probs5 = "{:.2%}".format(float(result[9]))

    displayScen = ""    

    if scenario == "2H": 
        displayScen = "Home leading by 2 goals (2H)"
        
    if scenario == "2A": 
        displayScen = "Away leading by 2 goals (2A)"
    
    if scenario == "3H": 
        displayScen = "Home leading by 3 goals (3H)"
        
    if scenario == "3A": 
        displayScen = "Away leading by 3 goals (3A)"
    
    if scenario == "4H": 
        displayScen = "Home leading by 4+ goals (4H)"
    
    if scenario == "4A": 
        displayScen = "Away leading by 4+ goals (4H)"
        
    session['probs1'] = float(result[1])
    session['probs2'] = float(result[3])
    session['probs3'] = float(result[5])
    session['probs4'] = float(result[7])
    session['probs5'] = float(result[9])
    
    session['score1'] = result[0]
    session['score2'] = result[2]
    session['score3'] = result[4]
    session['score4'] = result[6]
    session['score5'] = result[8]
    
    session['displayScen'] = displayScen
    session['scenario'] = scenario
    
    return render_template("index.html", scenario=scenario, displayScen=displayScen, score1=result[0], probs1=probs1, 
                           score2=result[2], probs2=probs2, score3=result[4], probs3=probs3, score4=result[6], 
                           probs4=probs4, score5=result[8], probs5=probs5)

@app.route('/getAnalysis', methods=["POST"])
def getResults():
    probs1num = session.get('probs1')
    probs1 = "{:.2%}".format(probs1num)
    
    probs2num = session.get('probs2')
    probs2 = "{:.2%}".format(probs2num)
    
    probs3num = session.get('probs3')
    probs3 = "{:.2%}".format(probs3num)
    
    probs4num = session.get('probs4')
    probs4 = "{:.2%}".format(probs4num)
    
    probs5num = session.get('probs5')
    probs5 = "{:.2%}".format(probs5num)
    
    
    score1 = session.get('score1')
    score2 = session.get('score2')
    score3 = session.get('score3')
    score4 = session.get('score4')
    score5 = session.get('score5')
    
    displayScen = session.get('displayScen')
    scenario = session.get('scenario')
    
    
    odds1 = float(request.form["odds1"])
    odds2 = float(request.form["odds2"])
    odds3 = float(request.form["odds3"])
    odds4 = float(request.form["odds4"])
    odds5 = float(request.form["odds5"])
    bet = int(request.form["bet"])


    result = runAnalysis(odds1, odds2, odds3, odds4, odds5, scenario, bet)

    wins1 = float(result[0])
    wins2 = float(result[1])
    wins3 = float(result[2])
    wins4 = float(result[3])
    wins5 = float(result[4])
    
    percent1 = float(result[5])
    percent2 = float(result[6])
    percent3 = float(result[7])
    percent4 = float(result[8])
    percent5 = float(result[9])
    
    ev1 = float(result[10])
    ev2 = float(result[11])
    ev3 = float(result[12])
    ev4 = float(result[13])
    ev5 = float(result[14])
    
    totalScore1 = probs1num
    totalScore1 = "{:.2%}".format(totalScore1) 
    
    totalScore2 = probs1num + probs2num
    totalScore2 = "{:.2%}".format(totalScore2)

    totalScore3 = probs1num + probs2num + probs3num
    totalScore3 = "{:.2%}".format(totalScore3)
 
    totalScore4 = probs1num + probs2num + probs3num + probs4num
    totalScore4 = "{:.2%}".format(totalScore4)

    totalScore5 = probs1num + probs2num + probs3num + probs4num + probs5num
    totalScore5 = "{:.2%}".format(totalScore5)


    return render_template("index.html", probs1=probs1, probs2=probs2, probs3=probs3, probs4=probs4, probs5=probs5,
                           score1=score1, score2=score2, score3=score3, score4=score4, score5=score5,
                           scenario=scenario, displayScen = displayScen,
                           wins1=wins1, wins2=wins2, wins3=wins3, wins4=wins4, wins5=wins5,
                           percent1=percent1, percent2=percent2, percent3=percent3, percent4=percent4, percent5=percent5, 
                           ev1=ev1, ev2=ev2, ev3=ev3, ev4=ev4, ev5=ev5,
                           odds1=odds1, odds2=odds2, odds3=odds3, odds4=odds4, odds5=odds5,
                           totalScore1=totalScore1, totalScore2=totalScore2, totalScore3=totalScore3, totalScore4=totalScore4,
                           totalScore5=totalScore5)



#@app.route('/', methods=["POST"])
#def postHiLo():
    #iterations = int(request.form["iterations"])
    #counting = int(request.form["counting"])
    #leniency = int(request.form["leniency"])
    #riskiness = int(request.form["riskiness"])
    #result = runAnalysis(iterations,counting,leniency,riskiness)
    #percent = "{:.2%}".format(result[3])
    #bestper = "{:.2%}".format(result[7])
    #worstper = "{:.2%}".format(result[11])
    #rnag = result[7] - result[11]
    #rnag = "{:.2%}".format(rnag)
    #return render_template("index.html", right=result[0], wrong=result[1], percent=percent, ballsies=result[2], avgright = result[4], avgwrong=result[5],avgballs=result[6],bestper=bestper,ballsright=result[8],ballswrong=result[9],worstper=worstper,rnag=rnag)

#app.run(host='0.0.0.0', port=80)


# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


#netstat -ano | findstr :80
#taskkill /PID <PID> /F