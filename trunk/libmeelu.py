#!/usr/bin/env python
#-*- coding:utf-8 -*-
import gtk
import webkit
import os
import thread
import sys
import urllib
import urllib2
import xml.dom.minidom
from xml.dom.minidom import Node


class MeeluConfig:
    def __init__(self):
        self.config_dir = os.path.expanduser("~") + "/.Meelu"
        self.config_file = self.config_dir + "/config.xml"
        self.xml = ""        
        self.xmldata = dict()
        if not os.path.exists(self.config_dir):
            os.mkdir(self.config_dir)
        if not os.path.isfile(self.config_file):
            self.xmldata = {"username": "","location": "","hash": "","css": ""}
            self.save_xml_config()
    def set_username(self,username):
        self.xmldata["username"] = username

    def set_password(self,password):
        import hashlib
        OSha512 = hashlib.sha256()
        OSha512.update(password)
        self.xmldata["hash"] = OSha512.hexdigest()
        OSha512 = ""

    def parse_xml_config(self):
        self.xml = xml.dom.minidom.parse(self.config_file)
        for node in self.xml.getElementsByTagName("meeluconfig"):
            username = ""
            hash_password = ""
            location = ""
            css = ""        
            for node2 in node.getElementsByTagName("username"):
                for node3 in node2.childNodes:
                    username = node3.data
            for node2 in node.getElementsByTagName("hash"):
                for node3 in node2.childNodes:
                    hash_password = node3.data
            for node2 in node.getElementsByTagName("location"):
                for node3 in node2.childNodes:
                    location = node3.data
            for node2 in node.getElementsByTagName("css"):
                for node3 in node2.childNodes:
                    css = node3.data     
            self.xmldata = {
                            "username": username,
                            "location": location,
                            "hash": hash_password,
                            "css": css
                        }
        
    def save_xml_config(self):
        self.__xmlfile = open(self.config_file,"w")
        self.__xmlcode = """<meeluconfig>
    <username>%s</username>
    <hash>%s</hash>
    <location>%s</location>
    <css>%s</css>
</meeluconfig>""" % (self.xmldata["username"],self.xmldata["hash"],self.xmldata["location"],self.xmldata["css"])
        self.__xmlfile.write(self.__xmlcode)
        self.__xmlfile.close()

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

class MeemiConnect:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.app_key = "0cf8795780cf09ef50f70783c4c0d755fff50b01"
        
        
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
        return self.api_ask("http://meemi.com/api/p/exists",dicto)
        
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
        
    def get_wf(self):
        return self.api_ask("http://meemi.com/api/%s/wf" % self.username, {})

    def get_memesfera(self):
        return self.api_ask("http://meemi.com/api/p/meme-sfera", {})
        
    def get_single_meme(self,user,mid):
        return self.api_ask("http://meemi.com/api/%s/%s" % (user,mid), {})

class MeeluWindow:
    def __init__(self):
        self.toolbar_code = '<toolbar name="toolbar_format"><toolitem action="Memes" /><toolitem action="MemeSfera" /><toolitem action="NewMeme" /><toolitem action="Replies" /></toolbar>'
        self.actions = [
                        ("Memes", gtk.STOCK_HOME, "Memes", None , "Memes", self.show_memes),
                        ("MemeSfera", gtk.STOCK_HOME, "MemeSfera", None , "MemeSfera", self.show_meme_sfera),
                        ("NewMeme", gtk.STOCK_HOME, "NewMeme", None , "NewMeme", self.new_meme),
                        ("Replies", gtk.STOCK_HOME, "Replies", None , "Replies", self.show_replies),
                        ]
        self.connection = MeemiConnect()
        self.config = MeeluConfig()
        self.config.parse_xml_config()
        self.html = dict()
        if self.config.xmldata["css"] == "":
            self.html["css"] = """<style type="text/css">
#meme {
    border: 1px solid #3465a4;
    -moz-border-radius: 5px 5px 5px 0;
    -webkit-border-radius: 5px 5px 5px 0; 
}
#meme:hover {
    border: 1px solid #cc0000;
    -moz-border-radius: 5px 5px 5px 0;
    -webkit-border-radius: 5px 5px 5px 0;
}
#screenname:hover {
    color: #204a87;
}

#replyform {
    border: 1px solid #3465a4;
}

#replyform:hover {
    border: 1px solid #204a87;
}
</style>"""
        else:
            self.html["css"] == """ <style type="text/css">
""" + self.config.xmldata["css"] + "\n</style>"
        self.html["header"] = self.html["css"] +"""<script type="text/javascript">
function newmeme(content) {
    document.title = "#NewMeme#" + content;
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

</script>
"""
        self.html["Login"] = """<form name="form" align="center">
Username: <br>
<input type="textarea" name="modulo" value="Username" size="20"><br>
Password: <br>
<input type="password" name="password" value="Password" size="20"><br>
<input type="button" onclick="login(this.form.modulo.value,this.form.password.value);" value="Enter">
</form>"""
        self.html["NewMeme"] = """<form name="form" align="center">
Meme:<br>
<textarea name='content' cols='25' rows='5' >
</textarea>
<input type="button" onclick="newmeme(this.form.content.value);" value="Enter">
</form>"""
        
    def title_changed(self, widget, frame, msg):
        
        if "#login#" in msg:
            msg = msg.replace("#login#","")
            accesslist = msg.split("#")
            self.connection.set_access(accesslist[0],accesslist[1]) # Salvo username e password
            if 'code="0"' in self.connection.check_username_exists():
                self.config.set_username(accesslist[0])
                self.config.set_password(accesslist[1])
                self.config.save_xml_config()
                self.show_memes("")
            else:
                self.webkit.load_html_string(self.html["header"] + self.html["Login"] + "<h1>Errore! Dati d'accesso non validi!</h1>", "meelu://Memes")

        elif "#NewMeme#" in msg:
            msg = msg.replace("#NewMeme#","")
            if 'code="7"' in self.connection.new_text_meme(msg):
                self.webkit.load_html_string(self.html["header"] + "<h2>Meme inviato!</h2>" + self.html["NewMeme"], "meelu://NewMeme")
            else:
                self.webkit.load_html_string(self.html["header"] + "<h2>Errore! Meme non inviato!</h2>" + self.html["NewMeme"], "meelu://NewMeme")

        elif "#OpenMeme#" in msg:
            msg = msg.replace("#OpenMeme#","")
            lista = msg.split("#")
            username = lista[0]
            mid = lista[1]
            self.show_meme(username,mid)

        elif "#ReplyMeme#" in msg:
            msg = msg.replace("#ReplyMeme#","")
            lista = msg.split("#")
            username = lista[0]
            mid = lista[1]
            content = lista[2]
            if 'code="7"' in self.connection.reply_meme(username,mid,content):
                self.show_meme(username,mid)
            else:
                self.webkit.load_html_string(self.html["header"] + "<h2>Errore! Meme non inviato!</h2>" + self.html["NewMeme"], "meelu://NewMeme")

    def show_memes(self,action):
        self.webkit.set_name("Memes")
        self.update("Memes")
        self.webkit.load_html_string(self.html["header"] + self.html["Memes"], "meelu://Memes")
        
    def show_meme_sfera(self,action):
        self.webkit.set_name("MemeSfera")
        self.update("MemeSfera")
        self.webkit.load_html_string(self.html["header"] + self.html["MemeSfera"], "meelu://MemeSfera")

    def show_replies(self,action):
        self.webkit.set_name("Replies")
        self.update("Replies")
        self.webkit.load_html_string(self.html["header"] + self.html["Replies"] , "meelu://Replies")
        
    def show_meme(self,username,numero):
        self.webkit.set_name("Meme")
        self.update("Meme",username,numero)
        self.__html = """<div id="replyform"><from name="form">
Risposta:
<textarea id='content' name="content" cols='25' rows='5' ></textarea>
<input type="button" onclick="replymeme('%s','%s',content.value);" value="Enter">
</form></div>""" % (username, numero)

        self.webkit.load_html_string(self.html["header"] + self.html["Meme"] + self.__html, "meelu://Meme/%s/%s" % (username,numero))
        
    def new_meme(self,action):
        self.webkit.set_name("NewMeme")
        self.update("NewMeme")
        self.webkit.load_html_string(self.html["header"] + self.html["NewMeme"], "meelu://NewMeme")

    def update(self,what,username="",numero=""):
        if what == "NewMeme":
            pass
        elif what == "Replies":
            self.html["Replies"] = "<h1>TODO2</h1>"
        elif what == "Memes":
            self.html["Memes"] = self.get_html_Memes()
        elif what == "MemeSfera":
            self.html["MemeSfera"] = self.get_html_MemeSfera()
        elif what == "Meme":
            self.html["Meme"] = self.get_html_meme(username,numero)

    def get_html_Memes(self):
        html = ""
        xml = self.connection.get_wf()
        parser = XmlString(xml)
        parser.parse_meme()
        dicto = parser.mapping
        chiavi = self.ordina(dicto.keys(),dicto)
        for meme in chiavi:
            if dicto[meme]["type"] == "text":
                html += """\n<div id='meme' onclick='openmeme("%s","%s"); '><div id='screenname'>%s:</div>%s<br>%s</div><br>""" % (dicto[meme]["screen_name"],dicto[meme]["id"],dicto[meme]["screen_name"],dicto[meme]["content"], dicto[meme]["data_time"])
        return html

    def get_html_MemeSfera(self):
        html = ""
        xml = self.connection.get_memesfera()
        parser = XmlString(xml)
        parser.parse_meme()
        dicto = parser.mapping
        chiavi = self.ordina(dicto.keys(),dicto)
        for meme in chiavi:
            if dicto[meme]["type"] == "text":
                html += """\n<div id='meme' onclick='openmeme("%s","%s");' ><div id='screenname' >%s:</div>%s<br>%s</div><br>""" % (dicto[meme]["screen_name"],dicto[meme]["id"],dicto[meme]["screen_name"],dicto[meme]["content"], dicto[meme]["data_time"])
        return html

    def get_html_meme(self,username,numero):
        html = ""
        xml = self.connection.get_single_meme(username,numero)
        parser = XmlString(xml)
        parser.parse_meme()
        dicto = parser.mapping
        chiavi = self.ordina(dicto.keys(),dicto,reverse=False)
        for meme in chiavi:
            if dicto[meme]["type"] == "text":
                html += """\n<div id='meme' onclick='openmeme("%s","%s");' ><div id='screenname' >%s:</div>%s<br>%s</div><br>""" % (dicto[meme]["screen_name"],dicto[meme]["id"],dicto[meme]["screen_name"],dicto[meme]["content"], dicto[meme]["data_time"])
        return html

    def ordina(self,chiavi,dicto,reverse=True):
        ordine = []
        ultimo = 0
        for meme in chiavi:
            if ultimo < int(dicto[meme]["id"]):
                ultimo = int(dicto[meme]["id"])
                ordine.append(meme)
            elif ultimo > int(dicto[meme]["id"]):
                ordine.reverse()
                ordine.append(meme)
                ordine.reverse()
            else:
                ultimo = int(dicto[meme]["id"])
                ordine.append(meme)
        if reverse:
            ordine.reverse()
        return ordine
        
    def quit(self,args):
        gtk.main_quit(args)

    def make_window(self):
        self.window = gtk.Window()
        self.window.set_title("Meelu - Meemi Client!")
        self.window.set_size_request(300,400)
        self.window.connect("destroy", self.quit)

    def make_webkit(self):
        self.webkit = webkit.WebView()
        if not self.config.xmldata["username"] == "" and not self.config.xmldata["hash"] == "":
            self.connection.set_access(self.config.xmldata["username"],self.config.xmldata["hash"],nohash=True)
            if 'code="0"' in self.connection.check_username_exists():
                self.show_memes("")
            else:
                self.webkit.load_html_string(self.html["header"] + self.html["Login"] + "<h1>Errore! Dati d'accesso non validi!</h1>", "meelu://Memes")
        else:
            self.webkit.load_html_string(self.html["header"] + self.html["Login"], "meelu://Memes")
        self.webkit.connect('title-changed', self.title_changed)
           
    def load_toolbar(self):
        self.gtk_actions = gtk.ActionGroup("Actions")
        self.gtk_actions.add_actions(self.actions)
        
        self.ui = gtk.UIManager()
        self.ui.insert_action_group(self.gtk_actions)
        self.ui.add_ui_from_string(self.toolbar_code)
        
        self.vbox = gtk.VBox()
        self.vbox.pack_start(self.ui.get_widget("/toolbar_format"), False)
        self.vbox.pack_start(self.webkit, True)
        self.window.add(self.vbox)
        
    def show_window(self):
        self.window.show_all()
        gtk.main()
