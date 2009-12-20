#!/usr/bin/env python
#-*- coding:utf-8 -*-

import libmeelu


import gtk
gtk.gdk.threads_init()
import gtk.glade
import sys
import webkit
import thread
class MeeluGUIWebkit:
    def __init__(self):
        """
        Funzione d'iniziale.
        """
        self.widgets = gtk.glade.XML("gui.glade")
        self.window = self.widgets.get_widget("window")
        
        self.about_window = self.widgets.get_widget("about")
        
        self.window_show = False
        self.about_window_show = False
        
        signalDic = { 
                        "quit_event" : self.quit,
                        "new_meme" : self.new_meme,
                        "home_page" : self.home_page,
                        "refresh_page": self.refresh,
                        "get_wf" : self.get_wf,
                        "about_close": self.__about,
                        "about_info" : self.__about_info,
                        "about_help" : self.__about_help,
                        "close_window": self.__show
                    }
                    
        self.widgets.signal_autoconnect(signalDic)

        self.webkit = webkit.WebView()
        
        self.widgets.get_widget("scrolledwindow1").add(self.webkit)
        self.webkit.connect('title-changed', self.title_changed)

        self.about_webkit = webkit.WebView()
        self.widgets.get_widget("aboutscrolled").add(self.about_webkit)
        self.about_webkit.show()
        self.about_webkit.load_html_string("<h1>Info</h1>","meelu://newmeme")
        

        self.__status_icon()

        self.HtmlBuilder = libmeelu.HtmlBuilder()
        self.connection = libmeelu.MeemiConnect()

    def __status_icon(self):
        
        self.Icon = gtk.StatusIcon()
        self.Icon_Menu = gtk.Menu()

        self.Icon.set_from_stock(gtk.STOCK_HOME)
        self.Icon.set_tooltip("Meelu - Meemi Client")
        
        self.Icon.connect('activate', self.__show)
        self.Icon.connect('popup-menu', self.__status_icon_popup, self.Icon_Menu)

        self.Icon_Menu_Home = gtk.ImageMenuItem(gtk.STOCK_HOME)        
        self.Icon_Menu_About = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
        self.Icon_Menu_Quit = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        
        self.Icon_Menu_Quit.connect('activate', self.quit, self.Icon)
        self.Icon_Menu_Home.connect('activate', self.__show)
        self.Icon_Menu_About.connect('activate', self.__about)
                
        self.Icon_Menu.append(self.Icon_Menu_Home)
        self.Icon_Menu.append(self.Icon_Menu_About)
        self.Icon_Menu.append(self.Icon_Menu_Quit)        
        
        self.Icon.set_visible(True)
        
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

    def __about_info(self, widget=True, button=True, time=True, data=None):
        self.about_webkit.load_html_string("<h1>Info</h1>","meelu://newmeme")

    def __about_help(self, widget=True, button=True, time=True, data=None):
        self.about_webkit.load_html_string("<h1>Help</h1>","meelu://newmeme")
    def __about(self, widget=True, button=True, time=True, data=None):
        if self.about_window_show:
            self.about_window.hide()
            self.about_window_show = False
        else:
            self.about_window.show()
            self.about_window_show = True

    def login(self, widget):
        if not self.connection.logged:
            html, status = self.HtmlBuilder.login()
            self.webkit.load_html_string(html,"meelu://")
            
    def new_meme(self, widget):
        if self.connection.logged:
            html, status = self.HtmlBuilder.get_new_meme_form()
            self.webkit.load_html_string(html,"meelu://newmeme")
        else:
            self.login(True)
            
    def get_wf(self, widget):
        if self.connection.logged:
            xml = self.connection.get_wf()
            html, status = self.HtmlBuilder.wf_from_xml(xml)
            self.webkit.load_html_string(html,"meelu://wf")
        else:
            self.login(True)
                    
    def refresh(self, widget):
        print "TODO"
        pass
    
    def home_page(self, widget):
        if self.connection.logged:
            html, status = self.HtmlBuilder.home_page()
            self.webkit.load_html_string(html,"meelu://")
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
                
                xml = self.connection.get_wf()
                html, status = self.HtmlBuilder.wf_from_xml(xml)
                self.webkit.load_html_string(html,"meelu://wf")
                
            if "show_newmeme" in msg:
                html, status = self.HtmlBuilder.get_new_meme_form()
                self.webkit.load_html_string(html,"meelu://")
                
        elif "#login#" in msg:
            msg = msg.replace("#login#","")
            accesslist = msg.split("#")
            self.connection.set_access(accesslist[0],accesslist[1]) # Salvo username e password
            
            xml = self.connection.check_username_exists()
            html, status = self.HtmlBuilder.login_from_xml(xml)
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
        html, status = self.HtmlBuilder.login()
        self.webkit.load_html_string(html,"meelu://")
        
        self.webkit.show()
        self.__show()
        
        
        gtk.main()
        
    def quit(self, widget=True, other=True, one=True):
        """
        Quesa funzione chiude il programma.
        """
        sys.exit(0)


if __name__ == "__main__":
    gui = MeeluGUIWebkit()
    gui.show_window()
