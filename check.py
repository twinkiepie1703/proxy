import urllib2, socket, re, threading, sys, getopt

# read from txt file proxy.txt / gives good requests 

_file="proxy.txt"
_threads=10
_urls=False
_out=""
_file_out=0
_timeout=80
proxyList=[]

class Proxy:
   def __init__(self, time_out=80, check_url="http://www.google.com", inside_text="<title>Google</title>"):
       self._sock=socket
       self._sock.setdefaulttimeout(time_out)
       self._check_url=check_url
       self._inside_text=inside_text
       self._proxy_buf=[]
       self._proxy_list=[]
       self._thread_count=0

   def check(self, proxy):
       try:
           proxy_handler = urllib2.ProxyHandler({'http': proxy})
           opener = urllib2.build_opener(proxy_handler)

           opener.addheaders = [('User-agent', 'Mozilla/5.0')]
           urllib2.install_opener(opener)
           req=urllib2.Request(self._check_url)
           self._sock=urllib2.urlopen(req)
           if (self._sock.read().index(self._inside_text))>=0:
               return True
       except:
           return False
       return True

   def check_all(self, proxy_list=[], thread_count=10):
       if type([])==type(proxy_list) and len(proxy_list)>0:
           self._proxy_list=[]
           self._proxy_buf=proxy_list
           self._thread_count=thread_count
           for i in range(thread_count):
               thr=threading.Thread(target=self._thread_check, name=str(i))
               thr.start();
           while (self._thread_count>0):
               pass
           return self._proxy_list

   def _thread_check(self):
       while (len(self._proxy_buf)>0):
           try:
               item=self._proxy_buf.pop()
               if self.check(item):
                   self._proxy_list.append(item)
           except:
               pass
       self._thread_count-=1
   sys.exit(1)

def _add_to_list(text):
   global proxyList
   for _tmp in text:
       try:
           while True:
               buf=re.search("([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\:[0-9]{1,5})", _tmp)
               try:
                   proxyList.index(proxyList)
               except ValueError:
                   proxyList.append(buf.group(0))
               _tmp=_tmp[len(buf.group(0)):]
       except:
           pass

try:
   opts, args=getopt.getopt(sys.argv[1:], "uf:c:o:t:", ["urls","file=","count=","out=","timeout="])
except getopt.GetoptError:
   _usage()
for opt, arg in opts:
   if opt in ("-f","--file"):
       _file=arg
   elif opt in ("-u","--urls"):
       _urls=True
   elif opt in ("-c","--count"):
       _threads=int(arg)
   elif opt in ("-o","--out"):
       _out=arg
   elif opt in ("-t","--timeout"):
       _timeout=int(arg)
try:
   f=open(_file,'r')
except IOError:
   print "Error. File './%s' not found!" % (_file)
   sys.exit(1)
pr_list=f.readlines()
f.close()
if _urls==False:
   _add_to_list(pr_list)
else:
   for url in pr_list:
       try:
           _sock=socket
           _sock=urllib2.urlopen(urllib2.Request(url))
           _add_to_list(_sock.read().split('\n'))
       except:
           pass
p_check=Proxy(time_out=_timeout)
if len(_out)>1:
   _file_out=open(_out,'w')
if _threads>len(proxyList):
   _threads=len(proxyList)
for i in p_check.check_all(proxyList,_threads):
   if len(_out)>1:
       _file_out.write(i)
   else:
       print i
if len(_out)>1:
   _file_out.close()
