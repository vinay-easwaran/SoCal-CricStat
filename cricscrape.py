import requests
from bs4 import BeautifulSoup

# player_query = input("SoCal CricStat: ")

class CricScrape:

    def __init__(self, player_query):
        STARTER_URL_EPL = 'https://cricclubs.com/SandsCricketAssociation/playerRankings.do?clubId=5917'
        STARTER_URL_OCCA = 'https://cricclubs.com/OCCA/playerRankings.do?clubId=1231'
        self.PLAYER_PROFILE_BASE_URL_EPL = 'https://cricclubs.com/SandsCricketAssociation/'
        self.PLAYER_PROFILE_BASE_URL_OCCA = 'https://cricclubs.com/OCCA/'
        self.PLAYER_URL = ''
        self.player_query = player_query
        self.player_found = False

        EPL_TALLY = self.find_player(STARTER_URL_EPL)
        OCCA_TALLY = self.find_player(STARTER_URL_OCCA)

        if self.player_found:
            self.output_stats(EPL_TALLY, OCCA_TALLY)

        else:
            print("Player Not Found")

    def find_player(self, url):
        if url[22] == self.PLAYER_PROFILE_BASE_URL_EPL[22]:
            self.WHICH_URL = self.PLAYER_PROFILE_BASE_URL_EPL
        else:
            self.WHICH_URL = self.PLAYER_PROFILE_BASE_URL_OCCA
            
        response = requests.get(url).text
        soup = BeautifulSoup(response,'lxml')
        player_table = soup.find('table',{'id':'sortableTableId'})
        links = player_table.findAll('a')
        num_players = int(len(links)/3)

        i = 1
        while i <= num_players:
            conversion = (i-1)*3
            player = links[conversion].text.strip()
            if self.player_query == player:
                self.PLAYER_URL = links[conversion]['href']
                self.player_found = True
                break
            i += 1


        if self.player_found:
            return self.return_stats()

        else:
            return (self.player_query, 0, 0)

    def return_stats(self):
        url = self.WHICH_URL + self.PLAYER_URL
        response = requests.get(url).text
        soup = BeautifulSoup(response, 'lxml')

        batting_table = soup.find('table',{'id':'myTable'})
        bowling_table = soup.find_all('table',{'id':'myTable'})[1]

        intro = soup.find_all('h3', {'class': 'col-title'})[0].text.strip()
        name = intro.split('\n')[0]

        batting_links = batting_table.findAll('a')
        bowling_links = bowling_table.findAll('a')
        runs = 0
        wickets = 0

        for innings in batting_links:
            runs += int(innings.text)
            
        for innings in bowling_links:
            wickets += int(innings.text)

        return (name, runs, wickets)

        # print(name)
        # print("SoCal Runs: " + str(runs))
        # print("SoCal Wickets: " + str(wickets))

    def output_stats(self, stat1, stat2):
        print(stat1[0])
        if (stat1[1] == stat2[1]) and (stat1[2] == stat2[2]):
            print("SoCal Runs: " + str(stat1[1]))
            print("Socal Wickets: " + str(stat1[2]))

        else:
            print("SoCal Runs: " + str(stat1[1] + stat2[1]))
            print("Socal Wickets: " + str(stat1[2] + stat2[2]))

            



