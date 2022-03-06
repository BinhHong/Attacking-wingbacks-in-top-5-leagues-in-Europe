import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

base_url='https://understat.com/league'
leagues=['EPL','La_liga','Bundesliga','Serie_A','Ligue_1']  
seasons=['2014','2015','2016','2017','2018','2019','2020','2021'] 


allteams={} # keys are id's of all teams and values are their names

full_data=dict() # keys are leagues and values are their dataframes  


for league in leagues:
    
    season_data=dict() # keys are seasons and values are their dataframes
    
    for season in seasons:
        
        url=base_url+'/'+league+'/'+season
        res=requests.get(url)
        soup=BeautifulSoup(res.content,'lxml')
        scripts=soup.find_all('script') # is a list, containing info

        match_id_string=''
        teams_string=''

        for x in scripts:
            if 'datesData' in x.text:
                match_id_string=x.text.strip()
            if 'teamsData' in x.text:
                teams_string=x.text.strip()
                
        
        # remove unnecessary characters
        match_id_string_first=match_id_string.index("('")+2
        match_id_string_end=match_id_string.index("')")
        match_id_string=match_id_string[match_id_string_first:match_id_string_end]

        teams_string_first=teams_string.index("('")+2
        teams_string_end=teams_string.index("')")
        teams_string=teams_string[teams_string_first:teams_string_end]
        
        
        # extract info
        match_id_data=match_id_string.encode('utf8').decode('unicode_escape')
        match_id_data=json.loads(match_id_data)               # is a list

        teams_data=teams_string.encode('utf8').decode('unicode_escape')
        teams_data=json.loads(teams_data)                 # is a dictionary        
        
        
        
        # collect all match ids in this season
        match_id_list=[]
        for i in match_id_data:
            if i['isResult']==True:
                match_id_list.append(i['id'])
                
        
                
        
        # collect all teams (id + names) and add to the dictionaries 'allteams' and 'teams'
        teams=dict() # temporary dictionary used only in this season
        for id in teams_data.keys():
            allteams[id]=teams_data[id]['title']
            teams[id]=teams_data[id]['title']
            
               
        
        # make a ranking based on points
        teams_frames={} # a dictionary where keys are names of teams and values are their dataframes
        
        cols=list(teams_data[list(teams_data.keys())[0]]['history'][0].keys())
        for id,team in teams.items():
            team_data=[]
            for row in teams_data[id]['history']:
                team_data.append(list(row.values()))

            df=pd.DataFrame(team_data,columns=cols)
            teams_frames[team]=df
            
        cols_to_sum = ['scored','pts','xG']    
        rank_frames=[]
        for team,df in teams_frames.items():
            data_sum=pd.DataFrame(df[cols_to_sum].sum()).T
            final_data=data_sum
            final_data['team']=team
            rank_frames.append(final_data)

        rank_stat=pd.concat(rank_frames)
        rank_stat=rank_stat[['team','pts','scored','xG']]
        rank_stat.sort_values('pts',ascending=False,inplace=True)
        rank_stat.reset_index(inplace=True, drop=True)
        rank_stat['position'] = range(1,len(rank_stat)+1)

        
        # filter out top 5
        top5=list(rank_stat['team'])[:5]
        
               
        # start scraping all matches in this season
        A=[]
        for i in match_id_list:
            try:
                url='https://understat.com/match/'+i
                res=requests.get(url)
                soup=BeautifulSoup(res.content,'lxml')
                scripts=soup.find_all('script')# is a list, containing info

                roster_string='' # gives match data
                shots_string=''

                for x in scripts:
                    if 'rostersData' in x.text:
                        roster_string=x.text.strip()
                    if 'shotsData' in x.text:
                        shots_string=x.text.strip()


                first_roster_string=roster_string.index("('")+2
                end_roster_string=roster_string.index("')")
                match_string=roster_string[first_roster_string:end_roster_string]

                first_shots_string=shots_string.index("('")+2
                end_shots_string=shots_string.index("')")
                shotsdata_string=shots_string[first_shots_string:end_shots_string]

                match_json=match_string.encode('utf8').decode('unicode_escape')
                shots_json=shotsdata_string.encode('utf8').decode('unicode_escape')
                match_data=json.loads(match_json)
                shots_data=json.loads(shots_json)
            except:
                print('Cannot access match',i,'!')
            


            # collect stats for wingbacks
            role_team=['h','a']
            for a in role_team:
                if shots_data[a]!=[]:
                    if shots_data[a][0][a+'_team'] in top5:
                        for x in match_data[a].values(): # x is a dict
                            if x['position'] in ['DL','DR','DML','DMR']:
                                A.append(list(x.values()))
            

            cols=list(match_data['h'].values())[0].keys()
        
        
        # make a dataframe for this season, consisting of stats of all wingbacks this season       
        df=pd.DataFrame(A,columns=cols)
        
        
        # modify df, turn some columns into integer and float values
        new_cols=['player', 'team_id','position','goals','assists','key_passes','xG','xA', 'time','shots', 'player_id','xGChain', 'xGBuildup']
        df=df[new_cols]
        cols_to_int = ['goals','shots','assists','time','key_passes']

        df.loc[:,cols_to_int]=df[cols_to_int].astype(int)
        cols_to_float=['xG','xA','xGChain', 'xGBuildup']
        df.loc[:,cols_to_float] = df[cols_to_float].astype(float)

        pd.options.display.float_format = '{:,.2f}'.format      
        

        # add df, dataframe of this season, to season_data
        season_data[season] = df
        
        
        
    # make df_seasons, a dataframe for this league, by concatenating all seasons   
    df_seasons = pd.concat(season_data)
    
    # add df_seasons to full_data
    full_data[league] = df_seasons
    

# concatenate all dataframes into one    
data = pd.concat(full_data)

data.to_csv('wingbacks_topteams.csv')