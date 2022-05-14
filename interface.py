from PyQt6 import QtGui, QtWidgets, QtCore
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QWidget
from MainWindow import Ui_MainWindow
import sys
import main as mn
from Form import Ui_Form
from UpdateSeriesWindow import Ui_updateSeriesWindow
import webbrowser
import rc_icons

class Window3(QWidget):
        
    def __init__(self):
        super().__init__()
        
        self.series = mn.Series()
        self.y = Ui_updateSeriesWindow()
        self.y.setupUi(self)
        self.name = ''
        
        self.y.pushButton.clicked.connect(self.textPull)
        self.y.lineEdit_3.setValidator(QtGui.QIntValidator(0, 1000, self))
        self.y.lineEdit_4.setValidator(QtGui.QIntValidator(0, 1000, self))
        
    def textPull(self):
        name = self.y.lineEdit.text()
        link = self.y.lineEdit_2.text()
        season = self.y.lineEdit_3.text()
        episode = self.y.lineEdit_4.text()

        x = self.series.seriesUpdate(self.name, name, link, season, episode)
        
        if x == 'Link və ya bölüm sırası səhvdi!':
            QMessageBox.warning(self, 'Səhvlik var', f'<font size = 4>Link və ya bölüm sırası səhvdi!</font>')
        
        elif x == 'İnternet yoxdu!':
            QMessageBox.warning(self, 'Səhvlik var', f'<font size = 4>İnternet yoxdu!</font>')
        
        else:
            self.name = name if name else self.name
            QMessageBox.information(self, 'Dizi güncəlləndi', x)
        
        
class Window2(QWidget):
    def __init__(self):
        super().__init__()
        
        self.x = Ui_Form()
        self.x.setupUi(self)
        

class Window(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.fr = Window2()
        self.usw = Window3()
        
        self.series = mn.Series()
        
        rx = QtCore.QRegularExpression('\d*')
        self.ui.lineEdit_3.setValidator(QtGui.QRegularExpressionValidator(rx, self))
        self.ui.lineEdit_4.setValidator(QtGui.QRegularExpressionValidator(rx, self))
        
        self.ui.pushButton.clicked.connect(self.allNewSeries)
        self.ui.pushButton_2.clicked.connect(self.showAllSeries)
        self.ui.pushButton_3.clicked.connect(self.deleteAllSeries)
        self.ui.pushButton_4.clicked.connect(self.addSeries)
        self.ui.pushButton_5.clicked.connect(self.searchSeries)
        self.ui.pushButton_6.clicked.connect(self.seriesUpdate)
        self.ui.pushButton_7.clicked.connect(self.showSeries)
        self.ui.pushButton_8.clicked.connect(self.deleteSeries)
        
        self.ui.actionGitHub.triggered.connect(lambda : webbrowser.open("https://github.com/Ayxan-z/SeriesRobot"))
        self.ui.actionHaqq_nda.triggered.connect(self.about)
    
    
    def about(self):
        text = '''<font size = 4><b>Ayxan Şahsuvarov</b> tərəfindən hazırlandı.
    <br><br>
    Bütün boğuşdurma haqları sərbəstdi.
    <br><br>
    <br><br>
    </font>
    <font size = 2>© Hüquqları qorunmur</font>
    '''
        QMessageBox.about(self, 'Haqqında', text)
    
    def allNewSeries(self):
        x = self.series.allSearchSeries()
        
        if x == 'İnternet yoxdu!':
            QMessageBox.warning(self, 'Səhvlik var', f'<font size = 4>İnternet yoxdu!</font>')
        
        else:
            if len(x) > 0:
                self.fr.show()
                self.fr.setWindowIcon(QtGui.QIcon(":/icons/icons/Custom-Icon-Design-Flatastic-1-Information.ico"))
                x.insert(0, f'<font size = 5>{len(x)} ədəd yeni bölümü olan dizi var</font><br>')
                self.fr.x.textBrowser.setText(('').join(x))

            else:
                QMessageBox.information(self, 'Yeni bölüm tapılmadı', '<font size = 4>Heç bir dizinin yeni bölümü yoxdu :(</font>')
        
    def showAllSeries(self):
        x = self.series.allSeriesShow()
        
        if len(x) > 0:
            self.fr.show()
            self.fr.setWindowIcon(QtGui.QIcon(":/icons/icons/Custom-Icon-Design-Flatastic-1-Information.ico"))
            x.insert(0, f'<font size = 5>{len(x)} ədəd dizi var</font><br>')
            self.fr.x.textBrowser.setText(('').join(x))
            
        else:
            icon = ":/icons/icons/Custom-Icon-Design-Flatastic-1-Information.ico"
            text = '''<font size = 4>Dizi tapılmadı.<br><br>
            Dizi əlavə etmək istəyirsiniz?</font>'''
        
            result = self.notificationScreen(icon, 'Dizi tapılmadı', text, 'Yox', 'Hə')

            if result == 16384:
                self.ui.tabWidget.setCurrentIndex(1)
    
    def deleteAllSeries(self):
        icon = ":/icons/icons/Google-Noto-Emoji-Symbols-73028-warning.ico"
        text = '<font size = 4>Bütün diziləri silmək istədiyinizdən əminsiniz?</font>'
    
        result = self.notificationScreen(icon, 'Dizilər silinir!', text, 'Yox', 'Hə')
        
        if result == 16384:
            self.series.allSeriesDelete()
            QMessageBox.information(self, 'Dizilər silindi', '<font size = 4>Bütün dizilər silindi</font>')
    
    def addSeries(self):
        name = self.ui.lineEdit.text()
        link = self.ui.lineEdit_2.text()
        season = self.ui.lineEdit_3.text()
        episode = self.ui.lineEdit_4.text()
        
        prt = []
        if not name:
            prt.append(' adını')
        if not link:
            prt.append(' linkini')
        if not season:
            prt.append(' son izlədiyiniz sezonunu')
        if not episode:
            prt.append(' son izlədiyiniz bölümünü')

        if len(prt) == 1:
            QMessageBox.warning(self, 'Daxil etməmisiniz', f'<font size = 4>Dizinin{prt[0]} daxil etməmisiniz!</font>')
        
        elif len(prt) > 1:
            QMessageBox.warning(self, 'Daxil etməmisiniz', f'<font size = 4>Dizinin{",".join(prt)} daxil etməmisiniz!</font>')

        else:
            link = link if '?ref_=ttep_ep_tt' in link else link + '?ref_=ttep_ep_tt'
            x = self.series.seriesAdd(name, link, season, episode)
            
            if x == 1:
                QMessageBox.information(self, 'Dizi əlavə olundu', f'<font size = 4>{name} dizisi əlavə olundu</font>')

            elif x == 'İnternet yoxdu!':
                QMessageBox.warning(self, 'Səhvlik var', f'<font size = 4>İnternet yoxdu!</font>')
            
            else:
                QMessageBox.warning(self, 'Dizi əlavə olunanmadı', f'<font size = 4>{x}</font>')
    
    def searchSeries(self):
        name = self.ui.lineEdit_5.text()
        
        if name:
            i = self.series._seriesRollCall(name)
            
            if not i:
                QMessageBox.warning(self, 'Dizi yoxdu', f'<font size = 4>Bu adda dizi yoxdu!</font>')

            else:
                x = self.series.searchEpisode(i[0][1], i[0][2], i[0][3])
                
                if x == 1:
                    QMessageBox.information(self, 'Dizi tapıldı', f'<font size = 4>{name} dizisinin izlənməyən bölümü yoxdu</font>')

                elif x == -1:
                    QMessageBox.warning(self, 'Səhvlik var', f'<font size = 4>İnternet yoxdu!</font>')
                
                else:
                    QMessageBox.information(self, 'Dizi tapıldı', f'<font size = 4>{name} dizisinin {x - 1} ədəd izlənməyən bölümü vardı.<br><br>İzlənilən son bölüm: <b>sezon-{i[0][2]} bölüm-{i[0][3]}</b></font>')
        
        else:
            QMessageBox.warning(self, 'Ad daxil etməlisiniz', f'<font size = 4>Axtarmaq istədiyiniz dizinin adını daxil etməlisiniz!</font>')
    
    def seriesUpdate(self):
        name, i = self.copyPaste('Güncəlləmək')

        if name != 1:
            self.usw.name = name
            self.usw.show()
            self.usw.setWindowIcon(QtGui.QIcon(":/icons/icons/film-editing.png"))

    def showSeries(self):
        name, i = self.copyPaste('Görmək')
        
        if name != 1:
            QMessageBox.information(self, 'Dizi tapıldı', f'<font size = 4><br>Ad: {i[0][0]}<br>Link: {i[0][1]}<br>Sezon: {i[0][2]}<br>Bölüm: {i[0][3]}</font>')

    def copyPaste(self, word):
        name = self.ui.lineEdit_5.text()
        
        if name:
            i = self.series._seriesRollCall(name)

            if not i:
                QMessageBox.warning(self, 'Dizi yoxdu', f'<font size = 4>Bu adda dizi yoxdu!</font>')
                return 1, 1
                
            else:
                return name, i

        else:
            QMessageBox.warning(self, 'Ad daxil etməlisiniz', f'<font size = 4>{word} istədiyiniz dizinin adını daxil etməlisiniz!</font>')
            return 1, 1
            
    def deleteSeries(self):
        name, i = self.copyPaste('Silmək')
        
        if name != 1:
            self.series.seriesDelete(name)
            QMessageBox.information(self, 'Dizi silindi', f'<font size = 4>{name} dizisi silindi</font>')

    def notificationScreen(self, icon, windowtitle, text, btn_no_text, btn_yes_text):
        mb = QMessageBox()
        mb.setWindowIcon(QtGui.QIcon(icon))
        mb.setWindowTitle(windowtitle)
        mb.setText(text)
        mb.setStandardButtons(QMessageBox.StandardButton.Yes |
                          QMessageBox.StandardButton.No)
        mb.setEscapeButton(QMessageBox.StandardButton.No)
            
        btn_no = mb.button(QMessageBox.StandardButton.No)
        btn_no.setText(btn_no_text)
        btn_yes = mb.button(QMessageBox.StandardButton.Yes)
        btn_yes.setText(btn_yes_text)
        
        result = mb.exec()
        
        return result
        
    

app = QtWidgets.QApplication(sys.argv)
wnd = Window()
wnd.show()
sys.exit(app.exec())