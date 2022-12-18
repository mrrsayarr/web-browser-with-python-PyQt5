#WebSurf Yenilikler
"""
Not dosyası için harici bir uygulamaya gerek kalmadan txt dosyası yazıp kaydedebilme
Hesap Makinesi tuşun basıp Hesap makinesini açma (online)
Home, ileri, geri, yenile ve diğer tuşlara icon koyuldu
Pencere içinde ayrıca icon koyuldu
Navbar  çubuğu istebildiği zaman istenildiği kenara taşınabilir
Yeni sekme açma ve kapatma özelliği getilirdi***
Varsayılan tarayıcı olarak google otomatik olarak açılıyor
Aramayı durdurmak için Dur tuşu konuldu(Çarpı işareti şeklinde)
Sınırsız Yeni sekme açıldığı halde az RAM tüketimi (optimize edildi)
Kapatma tuşuna basınca "Emin misniz?" şeklinde bir pencere çıkarıldı

"""
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import * #Herhangi bir sayfayı yazdırmak**

import os
import sys
import subprocess

class MainWindow(QMainWindow):
    # Navbar için Dark modu
    app = QApplication([])
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # sekme widget'ı oluşturma
        self.tabs = QTabWidget()

        #Websurf Maximum boyutla açılır.
        self.showMaximized()

        # belge modunu aktif etme
        self.tabs.setDocumentMode(True)

        # çift tıklandığında aksiyon alma
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)

        #  sekme değiştirildiğinde aksiyon alma
        self.tabs.currentChanged.connect(self.current_tab_changed)

        # sekmeleri kapatılabilir yapmak
        self.tabs.setTabsClosable(True)

        # sekme kapatma istendiğinde cevap alma
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        # sekmeleri merkezi widget olarak yapma
        self.setCentralWidget(self.tabs)

        # durum çubuğu oluşturma
        self.status = QStatusBar()

        # durum çubuğunu ana pencereye ayarlama
        self.setStatusBar(self.status)

        # gezinme için bir araç çubuğu oluşturma
        navtb = QToolBar("Navigation")

        # ana pencereye araç çubuğu ekleme
        self.addToolBar(navtb)

        self.setWindowIcon(QIcon('web.png'))

        # Geri eylemi oluşturma
        geri_btn = QAction("Geri", self)
        geri_btn.setStatusTip("Önceki sayfaya geri dön")    # durum ipucu ayarlama
        geri_btn.setIcon(QIcon('geri.png'))   # geri düğmesine eylem ekleme
        geri_btn.triggered.connect(lambda: self.tabs.currentWidget().back())    # geçerli sekmeyi geri gitmek için
        navtb.addAction(geri_btn)# tool bar kısmına ekleme

        # ileri butonunu ekleme
        ileri_btn = QAction("İleri", self)
        ileri_btn.setStatusTip("Sonraki sayfaya git")
        ileri_btn.setIcon(QIcon('ileri.png'))
        ileri_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(ileri_btn)

        # Yenileme düğmesi oluşturma
        yenile_btn = QAction("Yenile", self)
        yenile_btn.setStatusTip("Sayfayı yenile")
        yenile_btn.setIcon(QIcon('yenile.png'))
        yenile_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(yenile_btn)

        # Ana sayfa butonu oluşturma
        anasayfa_btn = QAction("Ana sayfa", self)
        anasayfa_btn.setStatusTip("ana Sayfaya git")
        anasayfa_btn.setIcon(QIcon('Home.png'))
        #  Ana sayfa butonuna eylem ekleme
        anasayfa_btn.triggered.connect(self.navigate_home)
        navtb.addAction(anasayfa_btn)

        # ayırıcı ekleme
        navtb.addSeparator()

        # URL için bir satır düzenleme widget'ı oluşturma
        self.urlbar = QLineEdit()

        # dönüş tuşuna basıldığında satır düzenlemeye eylem ekleme
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        # araç çubuğuna satır düzenleme ekleme
        navtb.addWidget(self.urlbar)

        linked = QAction("Linkedin", self)
        linked.setStatusTip("Linkedin")
        linked.setIcon(QIcon('linkedin.png'))
        linked.triggered.connect(self.linkedin)
        navtb.addAction(linked)

        hmakine = QAction("Hesap Makinesi", self)
        hmakine.setStatusTip("Hesap Makinesi")
        hmakine.setIcon(QIcon('hm.png'))
        hmakine.triggered.connect(self.siteye_yonlendir)
        navtb.addAction(hmakine)

        txteditor = QAction("Metin Editörü", self)
        txteditor.setStatusTip("Metin Editör")
        txteditor.setIcon(QIcon('txt.png'))
        txteditor.triggered.connect(self.txt_editor)
        navtb.addAction(txteditor)

        cam_btn = QAction("Kamera", self)
        cam_btn.setStatusTip("Kamera uygulamasını aç")
        cam_btn.setIcon(QIcon('camera.png'))
        cam_btn.triggered.connect(self.kamera_ac)
        navtb.addAction(cam_btn)

        # durdurma düğmesi oluşturma
        dur_btn = QAction("Durdur", self)
        dur_btn.setStatusTip("Mevcut sayfayı durdur")
        dur_btn.setIcon(QIcon('durdur.png'))
        dur_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navtb.addAction(dur_btn)

        # ilk sekmeyi oluşturma
        self.add_new_tab(QUrl('http://www.google.com'), 'Ana Sayfa')

        # tüm bileşenleri göster
        self.show()

        # pencere başlığını ayarlama
        self.setWindowTitle("WebSurf")

    # yeni sekme ekleme methodu
    def add_new_tab(self, qurl = None, label = "Yeni Sekme"):

        # url boş ise google'a gönderir
        if qurl is None:
            # google url oluşturma
            qurl = QUrl('http://www.google.com')

        # bir QWebEngineView nesnesi oluşturma
        browser = QWebEngineView()

        # url'yi tarayıcıya ayarlama
        browser.setUrl(qurl)

        # sekme dizini ayarlama
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        # url değiştirildiğinde tarayıcıya eylem ekleme
        # url'yi güncelle
        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))

        # yükleme bittiğinde tarayıcıya eylem ekleme
        # sekme başlığını ayarla
        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))

    def cikis_bttn(self):
        self.setGeometry(500, 300, 700, 700)

        self.setWindowTitle("Çıkış")

        quit = QAction("Çıkış", self)
        quit.triggered.connect(self.closeEvent)

    def closeEvent(self, event):
        close = QMessageBox()
        close.setText("Emin misiniz?")
        close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        close = close.exec()

        if close == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # sekmelerde çift tıklandığında
    def tab_open_doubleclick(self, i):

        # indeks kontrolü
        # Tıklamanın altında sekme yok
        if i == -1:
            # Yeni sekme oluştur
            self.add_new_tab()

    #  sekme değiştirildiğinde
    def current_tab_changed(self, i):

        # qurl ü al
        qurl = self.tabs.currentWidget().url()

        # url yi yenile
        self.update_urlbar(qurl, self.tabs.currentWidget())

        #Başlığı günceller
        self.update_title(self.tabs.currentWidget())

    #Sekme kapatıldığında
    def close_current_tab(self, i):

        #Sadece bir sekme varsa
        if self.tabs.count() < 2:
            #Hiçbirşey yapmaz
            return #Yani Bir sekme hiçbir zaman kapanmaz

        # yoksa sekmeyi kaldır
        self.tabs.removeTab(i)

    # başlığı güncelleme fonk
    def update_title(self, browser):

        # sinyal mevcut sekmeden değilse
        if browser != self.tabs.currentWidget():
            # hiçbirşey yapmaz
            return

        # sayfa başlığını alma
        title = self.tabs.currentWidget().page().title()

        # pencere başlığını ayarlama
        self.setWindowTitle("%s WebSurf" % title)

    #  Ana sayfaya  gitme eylemi
    def navigate_home(self):

        # googl a git
        self.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))

    def siteye_yonlendir(self):
        self.tabs.currentWidget().setUrl(QUrl("https://www.calculator.net/"))

    def txt_editor(self):
        self.tabs.currentWidget().setUrl(QUrl("https://write-box.appspot.com/"))

    def kamera_ac(self):
        pass
        #os.startfile("C:\Users\denem\Desktop\exedosyaları\kamera\kamera.exe")
        #subprocess.Popen(['C:/Users/denem/Desktop/WarGods Cheat Defender Win8.exe'])
        #subprocess.call(['C:\\Users\\denem\\Desktop\\WarGods Cheat Defender Win8.exe'])
        #os.system('kamera.exe')
        #open()


    def linkedin(self):
        self.tabs.currentWidget().setUrl(QUrl("https://www.linkedin.com/"))

    # url'ye gitme yöntemi
    def navigate_to_url(self):

        # satır düzenleme metnini al
        # onu Qurl nesnesine dönüştür
        q = QUrl(self.urlbar.text())

        # şema boş ise
        if q.scheme() == "":
            # şemayı ayarla
            q.setScheme("http")

        # url'yi ayarla
        self.tabs.currentWidget().setUrl(q)

    #  url'yi güncelleme yöntemi
    def update_urlbar(self, q, browser=None):

        # Bu sinyal mevcut sekmeden değilse yoksayar
        if browser != self.tabs.currentWidget():
            return

        # metni url çubuğuna ayarla
        self.urlbar.setText(q.toString())

        # imleç konumunu ayarla
        self.urlbar.setCursorPosition(0)


# PyQt5 uygulaması oluşturma
app = QApplication(sys.argv)

# uygulamaya isim ayarlama
app.setApplicationName("WebSurf")

# MainWindow nesnesi oluşturma
window = MainWindow()

# döngü
app.exec_()

def Main():
   app = QApplication(sys.argv)
   ex = MainWindow()
   ex.show()
   sys.exit(app.exec_())
