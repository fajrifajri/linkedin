#!/usr/bin/python

from http.server import BaseHTTPRequestHandler, HTTPServer
from prometheus_client import Gauge,MetricsHandler,CollectorRegistry,multiprocess,start_http_server
import prometheus_client
from pymongo import MongoClient

### Database Connection
client = MongoClient('172.18.0.1:27017',
                      username='jobs',
                      password='jobs',
                      authSource='jobs',
                      authMechanism='SCRAM-SHA-1')

db = client["jobs"]
jobs = db["jobs"]


class HTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        #curl "http://localhost:8110/jobs?location=San%20Francisco%20Bay%20Area"
        self.registry = prometheus_client.CollectorRegistry()
        function  = self.path.split('?')[0]
        param  = self.path.split('?')[1]
        input_name = dict(pair.split('=') for pair in param.split('&'))
        if function=='/jobs':
            loc = input_name.get('location').replace("%20"," ").replace("%2C",",")
            self.job = Gauge('jobs', 'jobs',['keyword','location'],registry=self.registry)
            if(loc=="all"):
                data_query = {}
            else:
                data_query = {"loc":loc}
            data_result = jobs.find(data_query)
            for res in enumerate(data_result):
                keyword = res[1]["keyword"]
                loc = res[1]["loc"]
                total = res[1]["total"]
                self.job.labels(keyword=keyword, location=loc).set(total)
            return MetricsHandler.do_GET(self)
        else:
            print("function not defined")

if __name__ == "__main__":
    daemon = HTTPServer(('0.0.0.0', 8110), HTTPHandler)
    try:
        daemon.serve_forever()
    except KeyboardInterrupt:
        pass
    daemon.server_close()