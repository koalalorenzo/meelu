#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys

import os
import urllib
import urllib2
import xml.dom.minidom
from xml.dom.minidom import Node
        
class Meme:
    def __init__ (self,dict):
        self.id = dict["id"]
        self.screen_name = dict["screen_name"]
        self.content = dict["content"]
        self.avatar_small = dict["avatar_small"]
        self.location = dict["location"]
        
class XmlString:
    def __init__(self,string):
        self.xml = xml.dom.minidom.parseString(string)
        self.mapping = dict()
        
    def parse_meme(self):
        for node in self.xml.getElementsByTagName("meme"):
            id = node.getAttribute("id")
            for avatars in node.getElementsByTagName("avatars"):
                avatar_small = avatars.getAttribute("small")
            content = ""
            original_link = ""
            location = ""
            source = ""
            for node2 in node.getElementsByTagName("content"):
                for node3 in node2.childNodes:
                    content = node3.data
            for node2 in node.getElementsByTagName("original_link"):
                for node3 in node2.childNodes:
                    original_link = node3.data
            for node2 in node.getElementsByTagName("location"):
                for node3 in node2.childNodes:
                    location = node3.data
            for node2 in node.getElementsByTagName("source"):
                for node3 in node2.childNodes:
                    source = node3.data
                    
            memedict = {
                            "id": id,
                            "favourite": node.getAttribute("favourite"),
                            "screen_name": node.getAttribute("screen_name"),
                            "data_time": node.getAttribute("data_time"),
                            "qta_replies": node.getAttribute("qta_replies"),
                            "type": node.getAttribute("type"),
                            "avatar_small": avatars.getAttribute("small"),
                            "content": content,
                            "original_link": original_link,
                            "location": location,
                            "source": source
                        }
                        
            self.mapping[id] = memedict

    def parse_profile(self):
        for node in self.xml.getElementsByTagName("meemi"):
            avatar_small = ""
            avatar_medium = ""
            avatar_normal = ""
            for avatars in node.getElementsByTagName("avatars"):
                avatar_small = avatars.getAttribute("small")
                avatar_medium = avatars.getAttribute("medium")
                avatar_normal = avatars.getAttribute("normal")
            profile = ""
            for node2 in node.getElementsByTagName("profile"):
                for node3 in node2.childNodes:
                    profile = node3.data
        self.mapping = {
                            "avatar_small": avatar_small,
                            "avatar_medium": avatar_medium,
                            "avatar_normal": avatar_normal,
                            "profile": profile
                       }
            
class MeemiConnect:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.app_key = "0cf8795780cf09ef50f70783c4c0d755fff50b01"
        self.logged = False
        
    def set_access(self,username,password,nohash=False):
        self.username = username
        if not nohash:
            import hashlib
            OSha512 = hashlib.sha256()
            OSha512.update(password)
            self.password = OSha512.hexdigest()
            OSha512 = ""
        else:
            self.password = password
        
    def api_ask(self, address, dicto={}):
        data = urllib.urlencode(dicto)
        conn = urllib2.urlopen(address, data)
        return conn.read()
        
    def check_username_exists(self):
        dicto = {
                    "meemi_id": self.username,
                    "pwd": self.password,
                    "app_key": self.app_key
                 }
        log = self.api_ask("http://meemi.com/api/p/exists",dicto)
        if 'code="0"' in log:
            self.logged = True
        else:
            self.logged = False
        return log
    def reply_meme(self,user,meme,text):
        dicto = {
                    "meemi_id": self.username,
                    "pwd": self.password,
                    "app_key": self.app_key,
                    "meme_type": "text",
                    "reply_screen_name": user,
                    "reply_meme_id": meme,
                    "text_content": text
                 }
        return self.api_ask("http://meemi.com/api/%s/reply" % self.username,dicto)

    def new_text_meme(self,text):
        dicto = {
                    "meemi_id": self.username,
                    "pwd": self.password,
                    "app_key": self.app_key,
                    "meme_type": "text",
                    "text_content": text
                 }
        return self.api_ask("http://meemi.com/api/%s/save" % self.username,dicto)
        
    def mark_as_read_new_memes(self):
        dicto = {
                    "meemi_id": self.username,
                    "pwd": self.password,
                    "app_key": self.app_key,
                 }
        return self.api_ask("http://meemi.com/api/%s/wf/mark/only_new_memes" % self.username,dicto)
        
    def mark_as_read_replies(self):
        dicto = {
                    "meemi_id": self.username,
                    "pwd": self.password,
                    "app_key": self.app_key,
                 }
        return self.api_ask("http://meemi.com/api/%s/wf/mark/only_new_replies" % self.username,dicto)
        
    def get_wf(self,limit=20,nr=True,ot=False):
        if nr and ot:
            return self.api_ask("http://meemi.com/api/%s/wf/text/nr" % self.username, {})
        elif nr and not ot:
            return self.api_ask("http://meemi.com/api/%s/wf/nr" % self.username, {})
        elif ot and not nr:
            return self.api_ask("http://meemi.com/api/%s/wf/text" % self.username, {})
        else:
            return self.api_ask("http://meemi.com/api/%s/wf" % self.username, {})

    def get_wf_new(self,limit=20,nr=True):
        dicto = {
                    "meemi_id": self.username,
                    "pwd": self.password,
                    "app_key": self.app_key,
                 }
        if nr:
            return self.api_ask("http://meemi.com/api/%s/wf/only_new_memes/text/nr" % self.username, dicto)
        else:
            return self.api_ask("http://meemi.com/api/%s/wf/only_new_memes/text" % self.username, dicto)


    def get_memesfera(self,limit=20,nr=True):
        if nr:
            return self.api_ask("http://meemi.com/api/p/meme-sfera/text/nr", {})
        else:
            return self.api_ask("http://meemi.com/api/p/meme-sfera/text", {})
    
    def get_single_meme(self,user,mid):
        return self.api_ask("http://meemi.com/api/%s/%s" % (user,mid), {})

    def get_profile(self,username):
        return self.api_ask("http://meemi.com/api/%s/profile" % username,{})

class HtmlBuilder:
    def __init__(self):
        self.set_default_values()
        
    def load_css(self, path):
        if os.path.isfile(path):
            opened = open(path,"r")
            self.css = opened.read()
            opened.close()
            self.header = """<head><style type="text/css">%s</style>
%s
</head>""" % (self.css, self.javascript)
        else:
            print "%s not found!" % path
    def set_default_values(self):
        self.css = """
#meme {
    border: 1px solid #3465a4;
    -moz-border-radius: 10px;
    -webkit-border-radius: 10px;
    padding: 10px;
}

#screenavatar {
    float: right;
}
#meme:hover {
    border: 1px solid #cc0000;
    -moz-border-radius: 10px;
    -webkit-border-radius: 10px;
}
#screenname {
    font-weight: bold;
}
#screenname:hover {
    color: #204a87;
}

#replyform {
    border: 1px solid #3465a4;
    text-align: center;
}

#replyform:hover {
    border: 1px solid #204a87;
}
"""
        self.javascript = """<script type="text/javascript">
function newmeme(content) {
    document.title = "#NewMeme#" + content;
}
function menu(content) {
    document.title = "#menu#" + content;
}
function login(username,password) {
    document.title = "#login#" + username + "#" + password;
}
function openmeme(username,id) {
    document.title = "#OpenMeme#" + username + "#" + id;
}
function replymeme(username,id,meme) {
    document.title = "#ReplyMeme#" + username + "#" + id + "#" + meme;
}

function openuser(username) {
    document.title = "#OpenUsername#" + username;
}
</script>
"""
        self.login_form = """<form name="form" align="center">
Username: <br>
<input type="textarea" name="modulo" value="Username" size="20"><br>
Password: <br>
<input type="password" name="password" value="Password" size="20"><br>
<input type="button" onclick="login(this.form.modulo.value,this.form.password.value);" value="Enter">
</form>"""
        self.new_meme_form = """<form name="form" align="center">
Meme:<br>
<textarea name='content' cols='25' rows='5' >
</textarea><br>
<input type="button" onclick="newmeme(this.form.content.value);" value="Enter">
</form>"""
        self.header = """<head><style type="text/css">%s</style>
%s
</head>""" % (self.css, self.javascript)
        self.menu_form = """
        <input type="button" onclick="menu('show_wf');" value="Get New Memes">
        <input type="button" onclick="menu('show_newmeme');" value="NewMeme">
        """
    def __code_html(self,str):
        str = str.replace("[i]","<i>")
        str = str.replace("[/i]","</i>")
        
        str = str.replace("[b]","<b>")
        str = str.replace("[/b]","</b>")
        
        str = str.replace("[u]","<u>")
        str = str.replace("[/u]","</u>")
        
        str = str.replace("[del]","<del>")
        str = str.replace("[/del]","</del>")
            
        str = str.replace(":)","<img src='http://meemi.com/stc/i/emo/smile.png'>")
        str = str.replace(":-)","<img src='http://meemi.com/stc/i/emo/smile.png'>")
        
        str = str.replace(":o)","<img src='http://meemi.com/stc/i/emo/smile_clown.png'>")
        
        str = str.replace(";)","<img src='http://meemi.com/stc/i/emo/wink.png'>")
        str = str.replace(";-)","<img src='http://meemi.com/stc/i/emo/wink.png'>")
        
        str = str.replace(":'(","<img src='http://meemi.com/stc/i/emo/cry.png'>")
        str = str.replace(":-(","<img src='http://meemi.com/stc/i/emo/cry.png'>")
        str = str.replace(":(","<img src='http://meemi.com/stc/i/emo/cry.png'>")
        
        str = str.replace(":-o","<img src='http://meemi.com/stc/i/emo/surprised.png'>")
        str = str.replace(":-O","<img src='http://meemi.com/stc/i/emo/surprised.png'>")
        str = str.replace(":O","<img src='http://meemi.com/stc/i/emo/surprised.png'>")
        str = str.replace(":o","<img src='http://meemi.com/stc/i/emo/surprised.png'>")

        str = str.replace(":D","<img src='http://meemi.com/stc/i/emo/grin.png'>")
        str = str.replace(":-D","<img src='http://meemi.com/stc/i/emo/grin.png'>")
        str = str.replace(":d","<img src='http://meemi.com/stc/i/emo/grin.png'>")
        str = str.replace(":-d","<img src='http://meemi.com/stc/i/emo/grin.png'>")
        
        str = str.replace(":s","<img src='http://meemi.com/stc/i/emo/confused.png'>")
        str = str.replace(":S","<img src='http://meemi.com/stc/i/emo/confused.png'>")
        str = str.replace(":-s","<img src='http://meemi.com/stc/i/emo/confused.png'>")
        str = str.replace(":-S","<img src='http://meemi.com/stc/i/emo/confused.png'>")
        
        
        str = str.replace(":P","<img src='http://meemi.com/stc/i/emo/tongue.png'>")
        str = str.replace(":-P","<img src='http://meemi.com/stc/i/emo/tongue.png'>")
        str = str.replace(":p","<img src='http://meemi.com/stc/i/emo/tongue.png'>")
        str = str.replace(":-p","<img src='http://meemi.com/stc/i/emo/tongue.png'>")
        
        str = str.replace(":-@","<img src='http://meemi.com/stc/i/emo/angry.png'>")
        str = str.replace(":@","<img src='http://meemi.com/stc/i/emo/angry.png'>")
        
        str = str.replace(":*","<img src='http://meemi.com/stc/i/emo/kiss.png'>")
        str = str.replace(":-*","<img src='http://meemi.com/stc/i/emo/kiss.png'>")
        str = str.replace("(k)","<img src='http://meemi.com/stc/i/emo/kiss.png'>")
        
        str = str.replace(":$","<img src='http://meemi.com/stc/i/emo/embara.png'>")
        str = str.replace(":-$","<img src='http://meemi.com/stc/i/emo/embara.png'>")
                
        if "[l:" in str and "|" in str and "]" in str:
            str = str.replace("[l:","<a href='")
            str = str.replace("|","'>")
            str = str.replace("]","</a>")
            
        return str
        
    def login(self, log=False):
        """
        Questa funzione ritorna la pagina html per il login.
        """
        return "<html>%s<body>%s</body>" % ( self.header, self.login_form), True
        
    def login_from_xml(self, log):
        if 'code="0"' in log:
            return "<html>%s<body>%s</body>" % ( self.header,"<h1 id='meme' align='center'>Benvenuto!</h1>"), True
        else:
            return "<html>%s<body><h1>Failed!</h1><br>%s</body>" % ( self.header, self.login_form), False        
    
    def get_new_meme_form(self):
        return "<html>%s<body>%s</body>" % ( self.header, self.new_meme_form), True
        
    def new_meme(self, xml):
        if 'code="7"' in xml:
            return "<html>%s<body>%s</body>" % ( self.header,"<h1 id='meme' align='center'>Meme Inviato!</h1>"), True
        else:
            return "<html>%s<body>%s%s</body>" % ( self.header,"<h1 id='meme' align='center'>Errore! Meme non inviato!</h1>", self.new_meme_form), False
                
    def wf_from_xml(self, xml):
        parser = XmlString(xml)
        parser.parse_meme()
        dicto = parser.mapping
        chiavi = dicto.keys()
        chiavi.sort()
        chiavi.reverse()
        html = "<html>%s<body>" % self.header
        for meme in chiavi:
            str = self.__code_html(dicto[meme]["content"])
            html += """\n<div id='meme'><div id='screenname' onclick='openuser("%s");'><div id="screenavatar"><img src="%s" /></div>%s:</div><div onclick='openmeme("%s","%s");'>%s</div></div><br>""" % (dicto[meme]["screen_name"],dicto[meme]["avatar_small"],dicto[meme]["screen_name"],dicto[meme]["screen_name"],dicto[meme]["id"],str)
        html += "</body>"
        return html, True
        
    def single_meme_from_xml(self, xml, username, numero):
        parser = XmlString(xml)
        parser.parse_meme()
        dicto = parser.mapping
        chiavi = dicto.keys()
        chiavi.sort()
        html = "<html>%s<body>" % self.header
        for meme in chiavi:
            str = self.__code_html(dicto[meme]["content"])
            html += """\n<div id='meme'><div id='screenname' onclick='openuser("%s");'><div id="screenavatar"><img src="%s" /></div>%s:</div><div onclick='openmeme("%s","%s");'>%s</div></div><br>""" % (dicto[meme]["screen_name"],dicto[meme]["avatar_small"],dicto[meme]["screen_name"],dicto[meme]["screen_name"],dicto[meme]["id"],str)
        html += """<div id="replyform"><from name="form">
Rispondi:<br>
<textarea id='content' name="content" cols='25' rows='5' ></textarea><br>
<input type="button" onclick="replymeme('%s','%s',content.value);" value="Enter">
</form></div>""" % (username, numero)

        html += "</body>"
        return html, True
        
    def profile_from_xml(self, xml, username):
        parser = XmlString(xml)
        parser.parse_profile()
        html = "<html>%s<body>" % self.header
        str = self.__code_html(parser.mapping["profile"])
        html += """<div id="screen_name>%s</div><div id="screen_avatar"><img src="%s" /></div><div id="screen_profile">%s</div>""" % ( username, parser.mapping["avatar_medium"], str) 
        html += "</body>"
        return html, True
        
    def reply_meme_from_xml(self, xml):
        if 'code="7"' in xml:
            return "<html>%s<body>%s</body>" % ( self.header,"<h1 id='meme' align='center'>Meme Inviato!</h1>"), True
        else:
            return "<html>%s<body>%s%s</body>" % ( self.header,"<h1 id='meme' align='center'>Meme Non Inviato! :(</h1>", self.menu_form), False

    def home_page(self):
        return "<html>%s<body>%s%s</body>" % ( self.header,"<h1 id='meme'>Benvenuto!</h1>", self.menu_form), True

class ConfigParser:
    def __init__(self):
        self.path_home = os.path.expanduser("~")
        self.path_config = os.path.join(self.path_home,".config/meelu/")
        if not os.path.exists(self.path_config):
            os.mkdir(self.path_config)
        self.path_file = os.path.join(self.path_config,"config.lst")
        self.path_log_file = os.path.join(self.path_config,"axex.log")
        
        self.__touch(self.path_file)
        self.__touch(self.path_log_file)
        
        self.data = dict()
        self.data["cssfile"] = None
        self.data["refreshtime"] = 120
        self.data["username"] = None
        self.data["password"] = None
        
        self.load_files()
        
    def get_username(self):
        return self.data["username"].decode("base64")
        
    def get_password(self):
        return self.data["password"].decode("base64")

    def get_access(self):
        return self.get_username, self.get_password
 
    def load_files(self):
        lines = self.__read_lines(self.path_file)
        for line in lines:
            list = line.split(":")
            if "username" in list[0]: # username
                self.data["username"] = list[1]
            elif "password" in list[0]: # hash
                self.data["password"] = list[1]
            elif "refreshtime" in list[0]: # tempo di caricamento
                self.data["refreshtime"] = int(list[1])
            elif "cssfile" in list[0]: # path del css
                self.data["cssfile"] = list[1]
    
    def set_access(self, username, hash):
        self.data["username"] = str(username).encode("base64")
        self.data["password"] = str(hash).encode("base64")
        self.data["username"] = self.data["username"].replace("\n","")
        self.data["password"] = self.data["password"].replace("\n","")

    def set_cssfile(self, path):
        if os.path.exists(path):
            self.data["cssfile"] = path
            
    def set_refreshtime(self, time):
        self.data["refreshtime"] = int(time)

    def save_files(self):    
        datafile = ""
        for key in self.data.keys():
            datafile += "\n%s:%s" % ( str(key), str(self.data[key]) )
        configfile = open(self.path_file,"w")
        configfile.write(datafile)
        configfile.close()
        
    def __touch(self,path):
        if not os.path.exists(path):
            fileopen = open(path,"w")
            fileopen.write("")
            fileopen.close()
            
    def __read_lines(self, path):
        if not os.path.exists(path):
            return []
        fileopen = open(path)
        lines = fileopen.readlines()
        fileopen.close()
        for line in lines:
            if not line or line == "" or line == "\n" or line == " " or ":" not in line:
                try:
                    lines.pop(lines.index(line))
                except:
                    pass
        newlines = []
        for line in lines:
            line = line.replace("\n","")
            newlines.append(line)
        return newlines
