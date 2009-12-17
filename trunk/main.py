#!/usr/bin/env python
#-*- coding:utf-8 -*-

import libmeelu


import gtk
import gtk.glade
import sys
import webkit

class MeeluGUIWebkit:
    def __init__(self):
        """
        Funzione d'iniziale.
        """
        self.widgets = gtk.glade.XML("gui.glade")
        self.window = self.widgets.get_widget("window")
        
        signalDic = { 
                        "quit_event" : self.quit,
                        "new_meme" : self.new_meme,
                        "home_page" : self.home_page,
                        "refresh_page": self.refresh,
                        "get_wf" : self.get_wf
                    }
                    
        self.widgets.signal_autoconnect(signalDic)

        self.webkit = webkit.WebView()
        self.widgets.get_widget("scrolledwindow1").add(self.webkit)
        self.webkit.connect('title-changed', self.title_changed)
        
        self.HtmlBuilder = libmeelu.HtmlBuilder()
        self.connection = libmeelu.MeemiConnect()

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
        self.window.show()
        
        gtk.main()
        
    def quit(self, widget=True):
        """
        Quesa funzione chiude il programma.
        """
        sys.exit(0)


if __name__ == "__main__":
    gui = MeeluGUIWebkit()
    gui.show_window()
