import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
import re
import sqlite3
import os

class Series():
    
    def __init__(self):
        self.connection = sqlite3.connect(os.getcwd() + "\\Series_reminder.db")
        self.cursor = self.connection.cursor()
        self._createTable()
        
    def _createTable(self):
        query = 'CREATE TABLE IF NOT EXISTS Series (Name TEXT,Link TEXT,Season TEXT,Episode TEXT)'
        self.cursor.execute(query)
        self.connection.commit()
    
    def _seriesRollCall(self, name):
        self.cursor.execute("SELECT * FROM Series where name=?",(name,))
        incoming_data = self.cursor.fetchall()
        
        return incoming_data

    def seriesAdd(self, name, link, season, episode):
        incoming_data = self._seriesRollCall(name)
        
        if incoming_data:
            return 'Bu adda dizi vardı!'
        
        else:
            x = Series.searchEpisode(link, season, episode)
            if x == 0:
                return 'Link və ya bölüm sırası səhvdi!'

            elif x == -1:
                return 'İnternet yoxdu!'
            
            else:
                self.cursor.execute("INSERT INTO Series VALUES(?,?,?,?)", (name, link, season, episode))
                self.connection.commit()
                return 1
    
    def allSearchSeries(self):
        self.cursor.execute("SELECT * FROM Series")
        incoming_data = self.cursor.fetchall()
        l = []

        for i in incoming_data:
            x = Series.searchEpisode(i[1], i[2], i[3])
            if x > 1:
                l.append(f'<font size = 4><br>{i[0]} dizisinin {x - 1} ədəd izlənməyən bölümü var<br>İzlənilən son bölüm: sezon-{i[2]} bölüm-{i[3]}</font><hr>')

            elif x == -1:
                return 'İnternet yoxdu!'
            
        return l
            
    def allSeriesShow(self):
        self.cursor.execute("SELECT * FROM Series")
        incoming_data = self.cursor.fetchall()
        l = []
        
        for i in incoming_data:
            l.append(f'<font size = 4><br>Ad: {i[0]}<br>Link: {i[1]}<br>Sezon: {i[2]}<br>Bölüm: {i[3]}</font><hr>')

        return l
        
    def seriesUpdate(self, name, name_new, link, season, episode):
        incoming_data = self._seriesRollCall(name)

        name_new = name_new if name_new else incoming_data[0][0]
        link = link if link else incoming_data[0][1]
        season = season if season else incoming_data[0][2]
        episode = episode if episode else incoming_data[0][3]
        
        x = Series.searchEpisode(link, season, episode)
        if x == 0:
            return 'Link və ya bölüm sırası səhvdi!'
        
        elif x == -1:
            return 'İnternet yoxdu!'
        
        else:
            self.cursor.execute("UPDATE Series SET Name = ? WHERE Name = ?", (name_new, name))
            self.cursor.execute("UPDATE Series SET Link = ? WHERE Name = ?", (link, name))
            self.cursor.execute("UPDATE Series SET Season = ? WHERE Name = ?", (season, name))
            self.cursor.execute("UPDATE Series SET Episode = ? WHERE Name = ?", (episode, name))
            self.connection.commit()
            return f'<font size = 4><b>Dizi güncəlləndi</b><br><hr>Ad: {name_new}<br>Link: {link}<br>Sezon: {season}<br>Bölüm: {episode}</font>'
            
    def seriesDelete (self, name):
        self.cursor.execute("DELETE FROM Series where Name = ?",(name,))
        self.connection.commit()
    
    def allSeriesDelete(self):
        self.cursor.execute("DELETE FROM Series")
        self.connection.commit()
        self._createTable()

    @staticmethod
    def searchEpisode(url, season, episode):
        
        season_copy = season
        season_url =  url[:url.find('?')] + 'episodes' + '?' + 'season='
        date_now = datetime.strptime(datetime.strftime(datetime.now(),'%d %b %Y'), '%d %b %Y')
        cnt = 0
        
        while 1:
            input_season_url_copy = season_url + season

            try:
                response = requests.get(input_season_url_copy)
                html = response.content

                soup = bs(html,"html.parser")
                find_episode = soup.find_all('div',{'class':'hover-over-image zero-z-index'})
                find_date = soup.find_all('div',{'class':'airdate'})
            
            #except x:
                #return 0
            
            except:
                return -1

            for i, j in zip(find_episode, find_date):
                i = i.text
                j = j.text
                
                i = i.strip()
                i = i.replace('\n','')

                j = j.strip()
                j = j.replace('\n','')
                j = j.replace('.','')

                if i == '' or j == '' or len(j) == 4:
                    break

                x = re.search("([0-9]+)\D+([0-9]+)", i)
                if "https://www.imdb.com/title/tt10795658/?ref_=ttep_ep_tt" == url:
                    print(x)
                if x.group(1) == season_copy:

                    if int(x.group(2)) >= int(episode) and (datetime.strptime(j, '%d %b %Y') - date_now).days < 0:
                        cnt += 1

                else:
                    try:
                        if (datetime.strptime(j, '%d %b %Y') - date_now).days < 0:
                            cnt += 1
                    
                    except ValueError:
                        break
                        
            next_episode = soup.find_all('a',{'id':'load_next_episodes'})
            if not next_episode or cnt == 0:
                break 
            
            try:
                if next_episode[0].text == 'Unknown Season':
                    break
            
            except:
                pass
            
            season = str(int(season) + 1)

        return cnt
