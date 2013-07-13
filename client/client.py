import urlparse
import urllib
import urllib2
import json
import pdb

#---------------------------------------------
# bandit api client
# --------------------------------------------

#TODO: algo_get, bandit_arm_update
class BanditClient():

    def __init__(self, host="localhost:5000", api_version="1.0"):
        self.host = host
        self.api_version = api_version
    
    #-------------------------- API METHODS WRAPPERS--------------------------------------#
        
    # create a new bandit experiment    
    def bandit_create(self, name=None, arm_count=None, algo_type="egreedy", budget_type="trials", \
                    budget=1000, epsilon=0.1, reward_type="click"):    
        ''' create a new bandit experiment '''
        params = {
            "name" : name,
            "arm_count" : arm_count,
            "algo_type" : algo_type,
            "budget_type" : budget_type,
            "budget" : budget,
            "epsilon" : epsilon,
            "reward_type" : reward_type
        }

        return self._do_post_request(resource="bandits", param_dict=params)

    # list status of a running bandit
    def bandit_get(self, bandit_id):
        resource = "bandits/%d" % (bandit_id)
        return self._do_get_request(resource=resource, param_dict={})
        
    # list bandit algorithms
    def algo_get(self):
       pass
        
    # status of an arm within a bandit (arm ids are unique)
    def arm_get(self, bandit_id, arm_id):
        resource = "bandits/%d/arms/%d" % (bandit_id, arm_id)
        return self._do_get_request(resource=resource, param_dict={})
        
    def arm_get_current(self, bandit_id):
        resource = "bandits/%d/arms/current" % bandit_id
        return self._do_get_request(resource=resource, param_dict={})
   
    def bandit_update(self, bandit_id=None, exp_name=None, n_arms=None, algo=None, horizon_type=None, \
                     horizon_value=None, epsilon=None, reward_type=None):
        resource = "bandits/%d" % bandit_id
        params = {
            "exp_name": exp_name,
            "n_arms":n_arms
        }
        return self._do_put_request(resource=resource, param_dict=params)
        
       
        
    #-------------------- LOW LEVEL REQUEST METHODS -----------------------------------#
    
    def _do_get_request(self, resource, param_dict):
        # build query string from param dictionary
        param_str = "&".join(["%s=%s" % (k,v) for k,v in param_dict.iteritems()])
        req_url = urlparse.urlunparse(["http", self.host, "api/v%s/%s" % (self.api_version,resource), "", param_str, ""])
        
        try:
            return eval(urllib2.urlopen(req_url).read())
        except urllib2.HTTPError, err:
            return parse_errors(err)
            
    def _do_post_request(self, resource, param_dict):
        req_url = urlparse.urlunparse(["http", self.host, "api/v%s/%s" % (self.api_version, resource), "", "", ""]) 
        print "req_url=%s" % (req_url)
                
        opener = urllib2.build_opener(urllib2.HTTPHandler)
                       
        req = urllib2.Request(req_url, data=json.dumps(param_dict))
        req.add_header('Content-Type', 'application/json')

        try:
            return eval(opener.open(req).read())
        except urllib2.HTTPError, err:
            return parse_errors(err)
    
    def _do_put_request(self, resource, param_dict):
        req_url = urlparse.urlunparse(["http", self.host, "api/v%s/%s" % (self.api_version, resource), "", "", ""]) 
        print "req_url=%s" % (req_url)
                
        opener = urllib2.build_opener(urllib2.HTTPHandler)
                       
        req = urllib2.Request(req_url, data=json.dumps(param_dict))
        req.add_header('Content-Type', 'application/json')
        req.get_method= lambda: 'PUT'
        
        try:
            return eval(opener.open(req).read())
        except urllib2.HTTPError, err:
            return parse_errors(err)

#---------------------------------------------
# error parsing
# --------------------------------------------

def parse_errors(err):
    if err.code == 404:
        return 'HTTPError: 404'
    if err.code == 401:
        return 'HTTPError: 401'
        

        