import urllib, urllib2
import simplejson
import sys
import re
from operator import itemgetter, attrgetter

# insert your VT api key below
APIKEY = ''

class VirusTotal:

    def __init__(self, sha1, data = None):
        self.content = data
        self.sha1 = sha1

    def fetch(self):
        url = "https://www.virustotal.com/vtapi/v2/file/report"
        parameters = {"resource": self.sha1,
                      "key": APIKEY}
        data = urllib.urlencode(parameters)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        json = response.read()
        try:
            report = simplejson.loads(json)
        except:
            return False

        # tokenize the threat names
        try:
            token_lst = []
            for scan in report['scans']:
                item = report.get("scans",{}).get(scan, {}).get("result")
                try:
                    tokens = re.split('\.|-|!|:|_|/', item)
                    for token in tokens:
                        token_lst.append(token.lower()) 
                except:
                    pass

            d = {}

            # filtering vars
            ignore = ['win32','trojan','troj','generic','adware',
                      'virus','agent','variant']
            min_score = 2
            min_len = 4

            for i in set(token_lst):
                d[i] = token_lst.count(i)

            tags = []
            for key,val in sorted(d.items(), key=itemgetter(1), reverse=True):
                #print '%s,%s' % (key,val)
                
                # token filtering
                if val > min_score and len(key) >= min_len and key[0].isalpha() and not key in ignore:
                        tags.append(key)

            return tags
        except Exception, e:
            return False

if __name__ == '__main__':
    if not APIKEY:
        sys.exit("Ops! You forgot to fill the APIKEY variable.")

    try:
        sample = VirusTotal(sys.argv[1])
        tags = sample.fetch()

        for tag in tags:
            print '%s,%s' % (sys.argv[1],tag)
    except:
        pass
