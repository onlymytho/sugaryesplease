import json
import io
import requests

class JsonHandler(dict):
    ### This is JsonHandler for easy Json handling. ###


    def URLParserJson(url) :
        r = requests.get(url)
        return r

    def URLParserJsonDict(url) :
        r = requests.get(url)
        datadict = r.json()
        return datadict

    def OpenFile(filepath) :
        f = open(filepath, 'r')
        f = f.read()
        return f

    def OpenJsonFileConvertToDict(filepath) :
        f = open(filepath, 'r')
        JsonDict = json.loads(f.read())
        f.close()
        return JsonDict

    def getValue(self, path, default = None):
        keys = path.split("/")
        val = None
        for key in keys:
            if val:
                if isinstance(val, list):
                    val = [ v.get(key, default) if v else None for v in val]
                else:
                    val = val.get(key, default)
            else:
                val = dict.get(self, key, default)
            if not val:
                break;
        return val
        # Example :
        # print (JsonHandler(JsonDict).getValue('results/description')
