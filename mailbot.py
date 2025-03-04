
import urllib
import urllib.request
import re
import asyncio
import argparse
from alive_progress import alive_bar
import sys

async def ExtractURLs(myUrl):
    try:
        t=[]
        regex="(?P<url>https?://[^\\s'\"]+)"
        t=re.findall(regex, myUrl)
    except:
        pass
    finally:
        return t

async def ExtractMails(myUrl):
    try:
        q=[]
        regex='[\\w\\.-]+@[\\w\\.-]+\\.\\w+'
        u=re.findall(regex, myUrl)
    except:
        pass
    finally:
        return u

try:
    parser=argparse.ArgumentParser()
    parser.add_argument("url", help="Url to analyze", type=str)
    parser.add_argument("output", help="Output file", type=str)
    parser.add_argument("-r", "--recursive", help="Recursive search", action="store_true")
    args=parser.parse_args()

    response = urllib.request.urlopen(args.url)
    webContent = response.read().decode('UTF-8') 

    z=asyncio.run(ExtractMails(webContent))

    if(args.recursive==True):
        v=asyncio.run(ExtractURLs(webContent))
        with alive_bar(len(v)) as bar:
            for i in range(len(v)):
                k=asyncio.run(ExtractMails(v[i]))
                if(len(k)!=0):
                    z.extend(k)
                bar()

    if(len(z)>0):
        z[-1] = z[-1] + ";" 
        with open(args.output, "w") as f:
            print(*z, sep="; ", file=f)
        print("Found " + str(len(z)) + " mail addresses.")
    else:
        print("No mail addresses were found.")
except Exception as e:
    print(e)