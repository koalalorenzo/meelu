#!/usr/bin/env python
#-*- coding:utf-8 -*-

import libmeelu


import gtk
gtk.gdk.threads_init()
import gtk.glade
import sys
import webkit
import thread
import os
import pynotify
from time import sleep

class MeeluGUIWebkit:
    def __init__(self,maindir=''):
        """
        Funzione d'iniziale.
        """
        self.maindir = maindir
        
        ######################
        print "Loading environment:",
        self.path_icon = os.path.join(self.maindir, "meelu.png")
        self.HtmlBuilder = libmeelu.HtmlBuilder()
        self.connection = libmeelu.MeemiConnect()
        self.config = libmeelu.ConfigParser()
        pynotify.init("Meelu")
        print "done"
        pynotify.Notification("Meelu", "Loading... Please Wait...").show() 
        ######################
        print "Loading GUI:",
        self.widgets = gtk.glade.XML(os.path.join(self.maindir, "gui.glade"))
        self.window = self.widgets.get_widget("window")
        self.window.set_title("Meelu")

        self.window.set_icon_from_file(self.path_icon)
        self.window_show = False
        
        signalDic = { 
                        "quit_event" : self.quit,
                        "new_meme" : self.new_meme,
                        "home_page" : self.home_page,
                        "get_wf" : self.get_wf,
                        "get_new" : self.get_new,
                        "close_window": self.__show,
                        "show_settings": self.show_settings
                    }
                    
        self.widgets.signal_autoconnect(signalDic)

        self.webkit = webkit.WebView()
        
        self.widgets.get_widget("scrolledwindow1").add(self.webkit)
        self.webkit.connect('title-changed', self.title_changed)

        self.__status_icon()
        print "done"
        ###################
        self.cache_get_wf_xml = ""
        self.__ntf_read = []
        if not self.config.data["cssfile"] == "None":
            self.HtmlBuilder.load_css(self.config.data["cssfile"])
            
    def __status_icon(self):
        
        self.Icon = gtk.StatusIcon()
        self.Icon.set_from_file(self.path_icon)
        self.Icon_Menu = gtk.Menu()
        self.Icon.set_tooltip("Meelu - Meemi Client")
        
        self.Icon.connect('activate', self.__show)
        self.Icon.connect('popup-menu', self.__status_icon_popup, self.Icon_Menu)

        self.Icon_Menu_Home = gtk.ImageMenuItem(gtk.STOCK_HOME)        
        self.Icon_Menu_About = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
        self.Icon_Menu_Quit = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        
        self.Icon_Menu_Quit.connect('activate', self.quit, self.Icon)
        self.Icon_Menu_Home.connect('activate', self.__show)
        self.Icon_Menu_About.connect('activate', self.__show_info)
                
        self.Icon_Menu.append(self.Icon_Menu_Home)
        self.Icon_Menu.append(self.Icon_Menu_About)
        self.Icon_Menu.append(self.Icon_Menu_Quit)        
        
        self.Icon.set_visible(True)
        
    def __show_info(self, widget=True, button=True, time=True, data=None):
        self.window.show()
        self.window_show = True
        self.show_info()
        
    def __status_icon_popup(self, widget=True, button=True, time=True, data=None):
        if button == 3:
            if data:
                data.show_all()
                data.popup(None, None, None, 3, time)
        pass
        
    def __show(self, widget=True, button=True, time=True, data=None):
        if self.window_show:
            self.window.hide()
            self.window_show = False
        else:
            self.window.show()
            self.window_show = True
            
    def show_settings(self,widget=True, button=True, time=True, data=None):
        html = self.HtmlBuilder.settings_page(self.config.data)
        self.webkit.load_html_string(html,"meelu://settings")

    def show_info(self, widget=True, button=True, time=True, data=None):
        self.webkit.load_html_string("<h1>In costruzione</h1><hr>Perfavore visita <a href='http://www.meelu.org'>http://www.meelu.org</a>!","meelu://Info")

    def login(self, widget=True):
        if not self.connection.logged:
            html, status = self.HtmlBuilder.login()
            self.webkit.load_html_string(html,"meelu://")
        else:
            self.get_wf()
            
    def new_meme(self, widget):
        if self.connection.logged:
            html, status = self.HtmlBuilder.get_new_meme_form()
            self.webkit.load_html_string(html,"meelu://newmeme")
        else:
            self.login(True)
            
    def get_wf(self, widget=True):
        if self.connection.logged:
            if self.cache_get_wf_xml:
                xml = self.cache_get_wf_xml
            else:
                self.cache_get_wf_xml = self.connection.get_wf()
                xml = self.cache_get_wf_xml
            html, status = self.HtmlBuilder.wf_from_xml(xml)
            self.webkit.load_html_string(html,"meelu://wf")
        else:
            self.login(True)

    def get_new(self, widget=True):
        xml = self.connection.get_wf_new(limit=self.config.data["limit"], ot=self.config.data["only_txt"])
        html, status = self.HtmlBuilder.wf_from_xml(xml)
        self.webkit.load_html_string(html,"meelu://newwf")
        
    def home_page(self, widget):
        if self.connection.logged:
            self.get_wf()
        else:
            self.login(True)
            
    def title_changed(self, widget, frame, msg):
        """
        Questa funzione viene richiamata quando viene cambiato il titolo
        della pagina in Webkit. Questo ci permette di interagire con il
        codice mediante la GUI scritta in HTML.
        """
        self.webkit.load_html_string("<h1>Loading...</h1>","meelu://")
        if "#menu#" in msg:
            msg = msg.replace("#menu#","")
            if "show_wf" in msg:
                self.get_wf()
                
            elif "show_newmeme" in msg:
                self.new_meme()
                
        elif "#settings#" in msg:
            self.show_settings()
            msg = msg.replace("#settings#","")
            list = msg.split("#")
            if "force_get_wf" in list[0]:
                self.cache_get_wf_xml = self.connection.get_wf(limit=self.config.data["limit"], ot=self.config.data["only_txt"])
            elif "refreshtime" in list[0]:
                self.config.set_refreshtime(list[1])
            elif "limit" in list[0]:
                self.config.set_limit(list[1])
            elif "notifylimit" in list[0]:
                self.config.set_notify_limit(list[1])
            elif "cssfile" in list[0]:
                self.config.set_cssfile(list[1])
                if self.config.data["cssfile"]:
                    self.HtmlBuilder.load_css(self.config.data["cssfile"])
            elif "only_txt" in list[0]:
                self.config.change_only_text_value()
            elif "mark_as_read" in list[0]:
                self.connection.mark_as_read_new_memes()
                self.connection.mark_as_read_replies()
            elif "info" in list[0]:
                self.show_about_info()
            elif "notify" in list[0]:
                self.config.change_notify_value()
            else:
                print "Error: What is it? :S » ", msg
            self.config.save_files()
            
                
        elif "#login#" in msg:
            msg = msg.replace("#login#","")
            accesslist = msg.split("#")
            self.connection.set_access(accesslist[0],accesslist[1])
            
            xml = self.connection.check_username_exists()
            html, status = self.HtmlBuilder.login_from_xml(xml)
            
            if status:
                import hashlib
                OSha512 = hashlib.sha256()
                OSha512.update(accesslist[1])
                newhash = OSha512.hexdigest()
                OSha512 = ""
                self.config.set_access(accesslist[0],newhash)
                self.config.save_files()
                
            self.webkit.load_html_string(html,"meelu://")
            
        elif "#NewMeme#" in msg:
            msg = msg.replace("#NewMeme#","")
            
            xml = self.connection.new_text_meme(msg)
            html, status = self.HtmlBuilder.new_meme(xml)
            self.webkit.load_html_string(html,"meelu://")
            
        elif "#OpenMeme#" in msg:
            msg = msg.replace("#OpenMeme#","")
            lista = msg.split("#")
            username = lista[0]
            mid = lista[1]
            
            xml = self.connection.get_single_meme(username,mid)
            html, status = self.HtmlBuilder.single_meme_from_xml(xml,username,mid)
            self.webkit.load_html_string(html,"meelu://")

        elif "#OpenUsername#" in msg:
            username = msg.replace("#OpenUsername#","")
            
            xml = self.connection.get_profile(username)
            html, status = self.HtmlBuilder.profile_from_xml(xml,username)
            self.webkit.load_html_string(html,"meelu://")

        elif "#ReplyMeme#" in msg:
            msg = msg.replace("#ReplyMeme#","")
            lista = msg.split("#")
            username = lista[0]
            mid = lista[1]
            content = lista[2]
            
            xml = self.connection.reply_meme(username,mid,content)
            html, status = self.HtmlBuilder.reply_meme_from_xml(xml)
            self.webkit.load_html_string(html,"meelu://")
            
            if status:
                xml = self.connection.get_single_meme(username,mid)
                html, status = self.HtmlBuilder.single_meme_from_xml(xml,username,mid)
                self.webkit.load_html_string(html,"meelu://")

        else:
            html, status = self.HtmlBuilder.home_page()
            self.webkit.load_html_string(html,"meelu://")
        
    def show_window(self):
        """
        Mostra la finestra e carica la pagina di Login.
        """
        print "Loading connections:",
        username =  self.config.get_username()
        hash = self.config.get_password()
        if username and hash:
            self.connection.set_access(username,hash,nohash=True)
            xml = self.connection.check_username_exists()
        print "done"
        print "Starting threads:",
        thread.start_new_thread(self.loop_get_wf, ())
        print "done... please wait..."
        
        print "Making pages and GUI:",
        self.login()
        
        self.webkit.show()
        self.__show()
        print "done"
        print "Load Complete"
        gtk.main()

    def loop_get_wf(self):
        while 1:
            if self.connection.logged:
                self.cache_get_wf_xml = self.connection.get_wf(limit=self.config.data["limit"], ot=self.config.data["only_txt"])
                #self.cache_get_wf_xml = self.connection.get_wf(ot=self.config.data["only_txt"]) # Non sembra funzionare
                if self.config.data["notify"]:
                    thread.start_new_thread(self.__ntf_new_meme, ())
            else:
                self.cache_get_wf_xml = ""
            sleep(int(self.config.data["refreshtime"]))

    def __ntf_new_meme(self):
        parser = libmeelu.XmlString(self.cache_get_wf_xml)
        parser.parse_meme()
        dicto = parser.mapping
        chiavi = dicto.keys()
        chiavi.sort()
        chiavi.reverse()
        time = True
        count = 0
        for meme in chiavi:
            if not dicto[meme]["id"] in self.__ntf_read:
                self.__ntf_read.append(dicto[meme]["id"])
                if not dicto[meme]["content"]:
                    continue
                if len(dicto[meme]["content"]) >= 253:
                    text = dicto[meme]["content"][:253] + "..."
                else:
                    text = dicto[meme]["content"]
                if time:
                    sleep(0.1)
                    pynotify.Notification("Meelu: %s" % dicto[meme]["screen_name"], text).show()
                    count += 1
                else:
                    continue
                if self.config.data["notify_limit"] == count:
                    time = False
                    
    def quit(self, widget=True, other=True, one=True):
        """
        Quesa funzione chiude il programma.
        """
        sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        gui = MeeluGUIWebkit(sys.argv[1])
    else:
        gui = MeeluGUIWebkit()
    gui.show_window()
