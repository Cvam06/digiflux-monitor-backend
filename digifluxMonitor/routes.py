from flask import request, jsonify
from digifluxMonitor.models import Website, Pinghistory
from digifluxMonitor import ma, app, db
from sqlalchemy.sql.expression import func
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
from datetime import datetime
import requests
from digifluxMonitor.scheduler import start_scheduler, stop_scheduler

# Website Schema
class WebsiteSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'hostname', 'env')

# Pinghistory Scema
class HistorySchema(ma.Schema):
    class Meta:
        fields = ('id','batch_no','date_time', 'status', 'website_id')

# Init Schema
website_schema = WebsiteSchema()
websites_schema = WebsiteSchema(many=True)
history_schema = HistorySchema()
historys_schema  =HistorySchema(many= True)

@app.route('/',methods=['GET'])
def get():
    return jsonify({ 'msg' : 'Hello World'})


# This will get all websites from website
@app.route('/websites',methods=['GET'])
def get_all():
    all_websites = Website.query.all()
    result = websites_schema.dump(all_websites)
    return jsonify(result)

# This will add new website in Websites table with given data
@app.route('/addwebsite', methods=['POST'])
def add_website():
    name = request.json['name'] 
    hostname = request.json['hostname']
    env = request.json['env']

    new_website = Website(name, hostname, env)
    
    websites = Website.query.all()
    result = websites_schema.dump(websites)
    if(len(result) > 0):
        for website in result:
            if(name == website['name']):
                return jsonify({'msg':'Same name already exists. Please enter another name.'})
            elif(hostname == website['hostname']):
                return jsonify({'msg':'Same hostname already exists. Please enter another hostname.'})
            elif(env == website['env']):
                return jsonify({'msg':'Same env already exists. Please enter another env.'})
            else:
                db.session.add(new_website)
                db.session.commit()
                return website_schema.jsonify(new_website)
    else:
        db.session.add(new_website)
        db.session.commit()
        return website_schema.jsonify(new_website)

# This will ping only onw website and send current status of website
@app.route('/pingone/<id>', methods=['GET'])
def pingOneWebsite(id):
    website = Website.query.get(id)

    hostname = website.hostname
    status = pingHttpHost(hostname)

    return jsonify({'status':status})

# This will ping all website from websites table and 
@app.route('/pingall', methods=['GET'])
def ping_all():
    websites = Website.query.all()
    all_websites = websites_schema.dump(websites)
    if(len(all_websites) > 0):
        data = []
        maxBatch = getMaxBatch()
        if maxBatch is None : 
            batch_to_be = 1
        else :
            batch_to_be = maxBatch + 1
        for website in all_websites:
            website_id = website['id']
            host = website['hostname'] # host='www.digiflux.io'
            batch_no = batch_to_be
            date_time = datetime.utcnow()
            status = pingHttpHost(host)
            ping_website = Pinghistory(batch_no, date_time,status,website_id)
            db.session.add(ping_website)
            data.append(ping_website)
        result = historys_schema.dump(data)
        db.session.commit()
        print("result = ",result)
        # return jsonify(result)
    else:
        return jsonify({'msg':'No websites to ping.'})

# This will get all ping data on one website from website_id
@app.route('/dataofone/<id>', methods=['GET'])
def dataOfOneFromPingHistory(id):
    allPingData = Pinghistory.query.filter(Pinghistory.website_id == id)
    result = historys_schema.dump(allPingData)
    return jsonify(result)

# This will delete one website from Websites Table
@app.route('/deletewebsite/<id>', methods=['DELETE'])
def deleteOneWebsite(id):
    website = Website.query.get(id)
    allPingData = Pinghistory.query.filter(Pinghistory.website_id == id)

    db.session.delete(allPingData)
    db.session.delete(website)
    db.session.commit()

    return website_schema.jsonify(website)

@app.route('/startscheduler', methods = ['GET'])
def startScheler():
    start_scheduler(ping_all, app)
    return jsonify({'msg':'Scheduler Started'})

@app.route('/stopscheduler', methods = ['GET'])
def stopScheler():
    stop_scheduler()
    return jsonify({'msg':'Scheduler Stopped'})

def getMaxBatch():
    qry = db.session.query(func.max(Pinghistory.batch_no).label("max_batch"))
    res = qry.one()
    max = res.max_batch
    return max

def pingHost(host):
    
    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'
            
    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]
    res = subprocess.call(command)
    return res

def pingHttpHost(host):
    r = requests.get(host, verify=False)
    return r.status_code
