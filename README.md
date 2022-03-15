[<img src="https://deepnote.com/buttons/launch-in-deepnote.svg">](https://deepnote.com/@binh-hong-ngoc-a131/Attacking-wingbacks-in-top-5-leagues-in-Europe-9_-oWE4uQsO_bbB4WdC6Jw)

# Attacking wingbacks in top 5 leagues in Europe

## Introduction
In football, **wingbacks** are the outside defenders in a team's defense, with much more emphasis on attack. They are typically used in a formation with 3 centre-backs and are called by the names left wingbacks and right wingbacks. In a formation with 2 center-backs like 4-3-3, they play very high to add more width in attack. 

In this project I will focus on **attacking aspects** of the wingbacks of top teams in 5 European Leagues: Premier League, La Liga, Bundesliga, Serie A and League 1. The main purposes are to check if there is a trend of using wingbacks in attack and to evaluate how well wingbacks take part in bulding up their team's play.

## Methodologies
1. Scrape the data from https://understat.com/.
2. Cleanse the data.
4. Analyze and visualize the data. One of the main terms used for analysis is `xGChain90`-the **expected goal chain per 90 minutes**. Basically, this stat measures the involvement of a player in attacking by assigning to him a number, which is deduced from the expected goal of all possessions he joins (only possesions which lead to a shot are counted), detailed explanation at https://statsbomb.com/2018/08/introducing-xgchain-and-xgbuildup/. 
5. Rank the best wingbacks and visualize by radar charts.

## Findings
1. Actually there is a trend of using wingbacks in attack, indicated by the graph

![](plot1.png?raw=true)

2. The best wingback is **Alphonso Davies** from FC Bayern Munich with leading `xGChain90` and `xGBuildup90`.

![](Davies.png?raw=true)

3. **Trent Alexander-Arnold** from Liverpool FC is the best wingback in terms of stats directly related to goals, e.g `key passes`, `expected assists`.

![](Arnold.png?raw=true)
