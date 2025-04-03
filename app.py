from flask import Flask, jsonify, request
from flask_cors import CORS 
from datetime import datetime

import random
import os

app = Flask(__name__)
CORS(app)

# Sample players
players = {
    "batsmen": ["Player1", "Player2", "Player3", "Player4", "Player5", "Player6"],
    "bowlers": ["Bowler1", "Bowler2", "Bowler3", "Bowler4", "Bowler5", "Bowler6"]
}


match_data = [
    {
        "id": "208d68e5-3fab-4f3b-88e9-29ec4a02d3e2",
        "name": "Chennai Super Kings vs Mumbai Indians, 3rd Match",
        "matchType": "t20",
        "status": "Chennai Super Kings won by 4 wkts",
        "venue": "MA Chidambaram Stadium, Chennai",
        "date": "2025-03-23",
        "dateTimeGMT": "2025-03-23T14:00:00",
        "teams": [
            "Chennai Super Kings",
            "Mumbai Indians"
        ],
        "fantasyEnabled": True,
        "bbbEnabled": True,
        "hasSquad": True,
        "matchStarted": True,
        "matchEnded": True
    },
    {
        "id": "83d70527-5fc4-4fad-8dd2-b88b385f379e",
        "name": "Gujarat Titans vs Punjab Kings, 5th Match",
        "matchType": "t20",
        "status": "Punjab Kings won by 11 runs",
        "venue": "Narendra Modi Stadium, Ahmedabad",
        "date": "2025-03-25",
        "dateTimeGMT": "2025-03-25T14:00:00",
        "teams": [
            "Gujarat Titans",
            "Punjab Kings"
        ],
        "fantasyEnabled": True,
        "bbbEnabled": True,
        "hasSquad": True,
        "matchStarted": True,
        "matchEnded": True
    },
    {
        "id": "d5915da0-c08b-4122-bcb0-2c2e1e6e168a",
        "name": "Kolkata Knight Riders vs Sunrisers Hyderabad, 15th Match",
        "matchType": "t20",
        "status": "Match not started",
        "venue": "Eden Gardens, Kolkata",
        "date": "2025-04-03",
        "dateTimeGMT": "2025-04-03T14:00:00",
        "teams": [
            "Kolkata Knight Riders",
            "Sunrisers Hyderabad"
        ],
        "fantasyEnabled": False,
        "bbbEnabled": False,
        "hasSquad": True,
        "matchStarted": False,
        "matchEnded": False
    },
    {
    "id": "5dc7a22f-5057-4895-bb98-965d9a1f004e",
    "name": "Lucknow Super Giants vs Mumbai Indians, 16th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow",
    "date": "2025-04-04",
    "dateTimeGMT": "2025-04-04T14:00:00",
    "teams": [
        "Lucknow Super Giants",
        "Mumbai Indians"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "f5dabb5b-a934-4666-a368-7134e991f569",
    "name": "Chennai Super Kings vs Delhi Capitals, 17th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "MA Chidambaram Stadium, Chennai",
    "date": "2025-04-05",
    "dateTimeGMT": "2025-04-05T10:00:00",
    "teams": [
        "Chennai Super Kings",
        "Delhi Capitals"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "b2e603ab-96f7-4711-ac9f-6a78e742237d",
    "name": "Punjab Kings vs Rajasthan Royals, 18th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Maharaja Yadavindra Singh International Cricket Stadium, Mullanpur, Chandigarh",
    "date": "2025-04-05",
    "dateTimeGMT": "2025-04-05T14:00:00",
    "teams": [
        "Punjab Kings",
        "Rajasthan Royals"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "2ac97990-6265-40e4-b93e-fcd24e89026c",
    "name": "Kolkata Knight Riders vs Lucknow Super Giants, 21st Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Eden Gardens, Kolkata",
    "date": "2025-04-06",
    "dateTimeGMT": "2025-04-06T10:00:00",
    "teams": [
        "Kolkata Knight Riders",
        "Lucknow Super Giants"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "3027ad1a-e7d8-4891-8ea0-1a56f81e8700",
    "name": "Sunrisers Hyderabad vs Gujarat Titans, 19th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Rajiv Gandhi International Stadium, Hyderabad",
    "date": "2025-04-06",
    "dateTimeGMT": "2025-04-06T14:00:00",
    "teams": [
        "Sunrisers Hyderabad",
        "Gujarat Titans"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "0a5ebe67-67a3-41d2-bbc8-5fc94aef0529",
    "name": "Mumbai Indians vs Royal Challengers Bengaluru, 20th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Wankhede Stadium, Mumbai",
    "date": "2025-04-07",
    "dateTimeGMT": "2025-04-07T14:00:00",
    "teams": [
        "Mumbai Indians",
        "Royal Challengers Bengaluru"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "56a88e0e-e844-41bd-ba65-3c905e36ba0d",
    "name": "Punjab Kings vs Chennai Super Kings, 22nd Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Maharaja Yadavindra Singh International Cricket Stadium, Mullanpur, Chandigarh",
    "date": "2025-04-08",
    "dateTimeGMT": "2025-04-08T14:00:00",
    "teams": [
        "Punjab Kings",
        "Chennai Super Kings"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "71213f27-c274-48b0-97f7-ec74e895dcbe",
    "name": "Gujarat Titans vs Rajasthan Royals, 23rd Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Narendra Modi Stadium, Ahmedabad",
    "date": "2025-04-09",
    "dateTimeGMT": "2025-04-09T14:00:00",
    "teams": [
        "Gujarat Titans",
        "Rajasthan Royals"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "3f309c2d-75dd-48bc-9d9f-e3979e252949",
    "name": "Royal Challengers Bengaluru vs Delhi Capitals, 24th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "M.Chinnaswamy Stadium, Bengaluru",
    "date": "2025-04-10",
    "dateTimeGMT": "2025-04-10T14:00:00",
    "teams": [
        "Royal Challengers Bengaluru",
        "Delhi Capitals"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "b39bbd39-c67f-4892-9a48-02e958946718",
    "name": "Chennai Super Kings vs Kolkata Knight Riders, 25th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "MA Chidambaram Stadium, Chennai",
    "date": "2025-04-11",
    "dateTimeGMT": "2025-04-11T14:00:00",
    "teams": [
        "Chennai Super Kings",
        "Kolkata Knight Riders"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "35938151-73ee-4969-8153-db8aabee3b90",
    "name": "Lucknow Super Giants vs Gujarat Titans, 26th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow",
    "date": "2025-04-12",
    "dateTimeGMT": "2025-04-12T10:00:00",
    "teams": [
        "Lucknow Super Giants",
        "Gujarat Titans"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "b13f129b-2596-429d-ad49-a1b0d102809b",
    "name": "Sunrisers Hyderabad vs Punjab Kings, 27th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Rajiv Gandhi International Stadium, Hyderabad",
    "date": "2025-04-12",
    "dateTimeGMT": "2025-04-12T14:00:00",
    "teams": [
        "Sunrisers Hyderabad",
        "Punjab Kings"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "953420f4-982c-4dcb-b8f7-bbda5acd438d",
    "name": "Rajasthan Royals vs Royal Challengers Bengaluru, 28th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Sawai Mansingh Stadium, Jaipur",
    "date": "2025-04-13",
    "dateTimeGMT": "2025-04-13T10:00:00",
    "teams": [
        "Rajasthan Royals",
        "Royal Challengers Bengaluru"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "3683354f-3c17-4346-9236-8d2bc474e7a5",
    "name": "Kolkata Knight Riders vs Punjab Kings, 44th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Eden Gardens, Kolkata",
    "date": "2025-04-26",
    "dateTimeGMT": "2025-04-26T14:00:00",
    "teams": [
        "Kolkata Knight Riders",
        "Punjab Kings"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "cacf2d34-41b8-41dd-91ed-5183d880084c",
    "name": "Kolkata Knight Riders vs Royal Challengers Bengaluru, 1st Match",
    "matchType": "t20",
    "status": "Royal Challengers Bengaluru won by 7 wkts",
    "venue": "Eden Gardens, Kolkata",
    "date": "2025-03-22",
    "dateTimeGMT": "2025-03-22T14:00:00",
    "teams": [
        "Kolkata Knight Riders",
        "Royal Challengers Bengaluru"
    ],
    "fantasyEnabled": True,
    "bbbEnabled": True,
    "hasSquad": True,
    "matchStarted": True,
    "matchEnded": True
    },
    {
    "id": "16cd14fd-9a69-49fc-b310-585a03e1d2b2",
    "name": "Gujarat Titans vs Chennai Super Kings, 69th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Narendra Modi Stadium, Ahmedabad",
    "date": "2025-05-18",
    "dateTimeGMT": "2025-05-18T10:00:00",
    "teams": [
        "Gujarat Titans",
        "Chennai Super Kings"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "91b007f3-c0af-493f-808a-3f4ae2d66e33",
    "name": "Sunrisers Hyderabad vs Rajasthan Royals, 2nd Match",
    "matchType": "t20",
    "status": "Sunrisers Hyderabad won by 44 runs",
    "venue": "Rajiv Gandhi International Stadium, Hyderabad",
    "date": "2025-03-23",
    "dateTimeGMT": "2025-03-23T10:00:00",
    "teams": [
        "Sunrisers Hyderabad",
        "Rajasthan Royals"
    ],
    "fantasyEnabled": True,
    "bbbEnabled": True,
    "hasSquad": True,
    "matchStarted": True,
    "matchEnded": True
    },
    {
    "id": "c6e97609-d9c1-46eb-805a-e282b34f3bb1",
    "name": "Delhi Capitals vs Lucknow Super Giants, 4th Match",
    "matchType": "t20",
    "status": "Delhi Capitals won by 1 wkt",
    "venue": "Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium, Visakhapatnam",
    "date": "2025-03-24",
    "dateTimeGMT": "2025-03-24T14:00:00",
    "teams": [
        "Delhi Capitals",
        "Lucknow Super Giants"
    ],
    "fantasyEnabled": True,
    "bbbEnabled": True,
    "hasSquad": True,
    "matchStarted": True,
    "matchEnded": True
    },
    {
    "id": "fd459f45-6e79-42c5-84e4-d046f291cacf",
    "name": "Rajasthan Royals vs Kolkata Knight Riders, 6th Match",
    "matchType": "t20",
    "status": "Kolkata Knight Riders won by 8 wkts",
    "venue": "Barsapara Cricket Stadium, Guwahati",
    "date": "2025-03-26",
    "dateTimeGMT": "2025-03-26T14:00:00",
    "teams": [
        "Rajasthan Royals",
        "Kolkata Knight Riders"
    ],
    "fantasyEnabled": True,
    "bbbEnabled": True,
    "hasSquad": True,
    "matchStarted": True,
    "matchEnded": True
    },
    {
    "id": "f5ed540f-15c7-4189-a5d4-e54be746a522",
    "name": "Gujarat Titans vs Mumbai Indians, 9th Match",
    "matchType": "t20",
    "status": "Gujarat Titans won by 36 runs",
    "venue": "Narendra Modi Stadium, Ahmedabad",
    "date": "2025-03-29",
    "dateTimeGMT": "2025-03-29T14:00:00",
    "teams": [
        "Gujarat Titans",
        "Mumbai Indians"
    ],
    "fantasyEnabled": True,
    "bbbEnabled": True,
    "hasSquad": True,
    "matchStarted": True,
    "matchEnded": True
    },
    {
    "id": "af5cf1dd-b3d4-4e8d-8660-e5e27cd5202e",
    "name": "Delhi Capitals vs Sunrisers Hyderabad, 10th Match",
    "matchType": "t20",
    "status": "Delhi Capitals won by 7 wkts",
    "venue": "Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium, Visakhapatnam",
    "date": "2025-03-30",
    "dateTimeGMT": "2025-03-30T10:00:00",
    "teams": [
        "Delhi Capitals",
        "Sunrisers Hyderabad"
    ],
    "fantasyEnabled": True,
    "bbbEnabled": True,
    "hasSquad": True,
    "matchStarted": True,
    "matchEnded": True
    },
    {
    "id": "057ce3fb-8117-47fe-bf25-be0ed8a56dd0",
    "name": "Rajasthan Royals vs Chennai Super Kings, 11th Match",
    "matchType": "t20",
    "status": "Rajasthan Royals won by 6 runs",
    "venue": "Barsapara Cricket Stadium, Guwahati",
    "date": "2025-03-30",
    "dateTimeGMT": "2025-03-30T14:00:00",
    "teams": [
        "Rajasthan Royals",
        "Chennai Super Kings"
    ],
    "fantasyEnabled": True,
    "bbbEnabled": True,
    "hasSquad": True,
    "matchStarted": True,
    "matchEnded": True
    },
    {
    "id": "075649ef-6ca8-4f50-8143-87814b828ea0",
    "name": "Mumbai Indians vs Kolkata Knight Riders, 12th Match",
    "matchType": "t20",
    "status": "Mumbai Indians won by 8 wkts",
    "venue": "Wankhede Stadium, Mumbai",
    "date": "2025-03-31",
    "dateTimeGMT": "2025-03-31T14:00:00",
    "teams": [
        "Mumbai Indians",
        "Kolkata Knight Riders"
    ],
    "fantasyEnabled": True,
    "bbbEnabled": True,
    "hasSquad": True,
    "matchStarted": True,
    "matchEnded": True
    },
    {
    "id": "7896feec-8fd6-44ef-aee3-eabb679e6305",
    "name": "Lucknow Super Giants vs Punjab Kings, 13th Match",
    "matchType": "t20",
    "status": "Punjab Kings won by 8 wkts",
    "venue": "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow",
    "date": "2025-04-01",
    "dateTimeGMT": "2025-04-01T14:00:00",
    "teams": [
        "Lucknow Super Giants",
        "Punjab Kings"
    ],
    "fantasyEnabled": True,
    "bbbEnabled": True,
    "hasSquad": True,
    "matchStarted": True,
    "matchEnded": True
    },
    {
    "id": "64e88ffc-606f-4d4f-b848-310f1ec7a98a",
    "name": "Royal Challengers Bengaluru vs Gujarat Titans, 14th Match",
    "matchType": "t20",
    "status": "Gujarat Titans won by 8 wkts",
    "venue": "M.Chinnaswamy Stadium, Bengaluru",
    "date": "2025-04-02",
    "dateTimeGMT": "2025-04-02T14:00:00",
    "teams": [
        "Royal Challengers Bengaluru",
        "Gujarat Titans"
    ],
    "fantasyEnabled": True,
    "bbbEnabled": True,
    "hasSquad": True,
    "matchStarted": True,
    "matchEnded": True
    },
    {
    "id": "7ab847ee-a1ee-47a9-82bd-ce923b23984f",
    "name": "Punjab Kings vs Mumbai Indians, 61st Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Himachal Pradesh Cricket Association Stadium, Dharamsala",
    "date": "2025-05-11",
    "dateTimeGMT": "2025-05-11T10:00:00",
    "teams": [
        "Punjab Kings",
        "Mumbai Indians"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "1ead6330-fb0b-48b4-ac7c-cec61b0b7063",
    "name": "Delhi Capitals vs Gujarat Titans, 62nd Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Arun Jaitley Stadium, Delhi",
    "date": "2025-05-11",
    "dateTimeGMT": "2025-05-11T14:00:00",
    "teams": [
        "Delhi Capitals",
        "Gujarat Titans"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "940a01f0-f893-4bd9-9e1b-352d561f7ee1",
    "name": "Chennai Super Kings vs Rajasthan Royals, 63rd Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "MA Chidambaram Stadium, Chennai",
    "date": "2025-05-12",
    "dateTimeGMT": "2025-05-12T14:00:00",
    "teams": [
        "Chennai Super Kings",
        "Rajasthan Royals"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "305c7d58-c26f-487d-8404-d30c6ad29f99",
    "name": "Royal Challengers Bengaluru vs Sunrisers Hyderabad, 64th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "M.Chinnaswamy Stadium, Bengaluru",
    "date": "2025-05-13",
    "dateTimeGMT": "2025-05-13T14:00:00",
    "teams": [
        "Royal Challengers Bengaluru",
        "Sunrisers Hyderabad"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "0a54b5bd-c4f5-48c6-b8aa-db27fa890b73",
    "name": "Gujarat Titans vs Lucknow Super Giants, 65th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Narendra Modi Stadium, Ahmedabad",
    "date": "2025-05-14",
    "dateTimeGMT": "2025-05-14T14:00:00",
    "teams": [
        "Gujarat Titans",
        "Lucknow Super Giants"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "469c4673-1449-4e20-9bc9-b358ec604fcf",
    "name": "Mumbai Indians vs Delhi Capitals, 66th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Wankhede Stadium, Mumbai",
    "date": "2025-05-15",
    "dateTimeGMT": "2025-05-15T14:00:00",
    "teams": [
        "Mumbai Indians",
        "Delhi Capitals"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "a860a259-b9a4-42cd-acf7-f9a650e24292",
    "name": "Rajasthan Royals vs Punjab Kings, 67th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Sawai Mansingh Stadium, Jaipur",
    "date": "2025-05-16",
    "dateTimeGMT": "2025-05-16T14:00:00",
    "teams": [
        "Rajasthan Royals",
        "Punjab Kings"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "1c3424f1-400a-4122-bc01-fb5ab52aa2ee",
    "name": "Royal Challengers Bengaluru vs Kolkata Knight Riders, 68th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "M.Chinnaswamy Stadium, Bengaluru",
    "date": "2025-05-17",
    "dateTimeGMT": "2025-05-17T14:00:00",
    "teams": [
        "Royal Challengers Bengaluru",
        "Kolkata Knight Riders"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "99c52578-1257-4834-9848-88cfec556836",
    "name": "Delhi Capitals vs Mumbai Indians, 29th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Arun Jaitley Stadium, Delhi",
    "date": "2025-04-13",
    "dateTimeGMT": "2025-04-13T14:00:00",
    "teams": [
        "Delhi Capitals",
        "Mumbai Indians"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "263c1103-33c0-4c05-864f-5dbcd29ead9b",
    "name": "Lucknow Super Giants vs Chennai Super Kings, 30th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow",
    "date": "2025-04-14",
    "dateTimeGMT": "2025-04-14T14:00:00",
    "teams": [
        "Lucknow Super Giants",
        "Chennai Super Kings"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "23f60d1b-2641-4a84-bb73-54d3aadfb294",
    "name": "Punjab Kings vs Kolkata Knight Riders, 31st Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Maharaja Yadavindra Singh International Cricket Stadium, Mullanpur, Chandigarh",
    "date": "2025-04-15",
    "dateTimeGMT": "2025-04-15T14:00:00",
    "teams": [
        "Punjab Kings",
        "Kolkata Knight Riders"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "3659022a-de1d-48fe-b68a-c62197297408",
    "name": "Delhi Capitals vs Rajasthan Royals, 32nd Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Arun Jaitley Stadium, Delhi",
    "date": "2025-04-16",
    "dateTimeGMT": "2025-04-16T14:00:00",
    "teams": [
        "Delhi Capitals",
        "Rajasthan Royals"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "71756de6-bdef-4b23-801f-c6bec9604e07",
    "name": "Mumbai Indians vs Sunrisers Hyderabad, 33rd Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Wankhede Stadium, Mumbai",
    "date": "2025-04-17",
    "dateTimeGMT": "2025-04-17T14:00:00",
    "teams": [
        "Mumbai Indians",
        "Sunrisers Hyderabad"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "ebce77ae-63e1-46eb-8ff4-360ba8dc9bf2",
    "name": "Royal Challengers Bengaluru vs Punjab Kings, 34th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "M.Chinnaswamy Stadium, Bengaluru",
    "date": "2025-04-18",
    "dateTimeGMT": "2025-04-18T14:00:00",
    "teams": [
        "Royal Challengers Bengaluru",
        "Punjab Kings"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "71666b6c-a6f9-4e09-a9d9-7f3ddca832d6",
    "name": "Gujarat Titans vs Delhi Capitals, 35th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Narendra Modi Stadium, Ahmedabad",
    "date": "2025-04-19",
    "dateTimeGMT": "2025-04-19T10:00:00",
    "teams": [
        "Gujarat Titans",
        "Delhi Capitals"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "a007a070-6120-4e37-8bf9-c9582801a20b",
    "name": "Rajasthan Royals vs Lucknow Super Giants, 36th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Sawai Mansingh Stadium, Jaipur",
    "date": "2025-04-19",
    "dateTimeGMT": "2025-04-19T14:00:00",
    "teams": [
        "Rajasthan Royals",
        "Lucknow Super Giants"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "4ace6d56-2e54-473e-a3c1-8bfcd06da6e2",
    "name": "Punjab Kings vs Royal Challengers Bengaluru, 37th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Maharaja Yadavindra Singh International Cricket Stadium, Mullanpur, Chandigarh",
    "date": "2025-04-20",
    "dateTimeGMT": "2025-04-20T10:00:00",
    "teams": [
        "Punjab Kings",
        "Royal Challengers Bengaluru"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "01244c3f-ce16-42a7-bcee-31d75fcdfb4e",
    "name": "Mumbai Indians vs Chennai Super Kings, 38th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Wankhede Stadium, Mumbai",
    "date": "2025-04-20",
    "dateTimeGMT": "2025-04-20T14:00:00",
    "teams": [
        "Mumbai Indians",
        "Chennai Super Kings"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "a62d133e-9370-4575-b649-9415fea63aab",
    "name": "Kolkata Knight Riders vs Gujarat Titans, 39th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Eden Gardens, Kolkata",
    "date": "2025-04-21",
    "dateTimeGMT": "2025-04-21T14:00:00",
    "teams": [
        "Kolkata Knight Riders",
        "Gujarat Titans"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "47fd62f1-ca48-4c9c-9ded-0d2fcb5a64df",
    "name": "Lucknow Super Giants vs Delhi Capitals, 40th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow",
    "date": "2025-04-22",
    "dateTimeGMT": "2025-04-22T14:00:00",
    "teams": [
        "Lucknow Super Giants",
        "Delhi Capitals"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "cec210ca-9184-43d3-9664-5ff0cbce7cd0",
    "name": "Sunrisers Hyderabad vs Mumbai Indians, 41st Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Rajiv Gandhi International Stadium, Hyderabad",
    "date": "2025-04-23",
    "dateTimeGMT": "2025-04-23T14:00:00",
    "teams": [
        "Sunrisers Hyderabad",
        "Mumbai Indians"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "9c1e5e4c-b72e-4db2-b2be-df9b4d27f539",
    "name": "Royal Challengers Bengaluru vs Rajasthan Royals, 42nd Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "M.Chinnaswamy Stadium, Bengaluru",
    "date": "2025-04-24",
    "dateTimeGMT": "2025-04-24T14:00:00",
    "teams": [
        "Royal Challengers Bengaluru",
        "Rajasthan Royals"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "92d38459-52b6-40a9-8508-f3dd2692a0bf",
    "name": "Chennai Super Kings vs Sunrisers Hyderabad, 43rd Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "MA Chidambaram Stadium, Chennai",
    "date": "2025-04-25",
    "dateTimeGMT": "2025-04-25T14:00:00",
    "teams": [
        "Chennai Super Kings",
        "Sunrisers Hyderabad"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "eae7163d-b06c-41df-95fb-835fd5b9798b",
    "name": "Mumbai Indians vs Lucknow Super Giants, 45th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Wankhede Stadium, Mumbai",
    "date": "2025-04-27",
    "dateTimeGMT": "2025-04-27T10:00:00",
    "teams": [
        "Mumbai Indians",
        "Lucknow Super Giants"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "04e8d307-7acd-4c3d-8117-b92ced6c583a",
    "name": "Delhi Capitals vs Royal Challengers Bengaluru, 46th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Arun Jaitley Stadium, Delhi",
    "date": "2025-04-27",
    "dateTimeGMT": "2025-04-27T14:00:00",
    "teams": [
        "Delhi Capitals",
        "Royal Challengers Bengaluru"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "32450f41-24d3-463a-9d37-e6df114b43df",
    "name": "Rajasthan Royals vs Gujarat Titans, 47th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Sawai Mansingh Stadium, Jaipur",
    "date": "2025-04-28",
    "dateTimeGMT": "2025-04-28T14:00:00",
    "teams": [
        "Rajasthan Royals",
        "Gujarat Titans"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "fa06c479-3015-4e58-b37c-9c6c076fab14",
    "name": "Delhi Capitals vs Kolkata Knight Riders, 48th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Arun Jaitley Stadium, Delhi",
    "date": "2025-04-29",
    "dateTimeGMT": "2025-04-29T14:00:00",
    "teams": [
        "Delhi Capitals",
        "Kolkata Knight Riders"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "9b3be8ba-8302-4051-87a8-9022037b9a84",
    "name": "Chennai Super Kings vs Punjab Kings, 49th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "MA Chidambaram Stadium, Chennai",
    "date": "2025-04-30",
    "dateTimeGMT": "2025-04-30T14:00:00",
    "teams": [
        "Chennai Super Kings",
        "Punjab Kings"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "d0b375d6-eb90-48f9-b8a3-37647a418ea2",
    "name": "Rajasthan Royals vs Mumbai Indians, 50th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Sawai Mansingh Stadium, Jaipur",
    "date": "2025-05-01",
    "dateTimeGMT": "2025-05-01T14:00:00",
    "teams": [
        "Rajasthan Royals",
        "Mumbai Indians"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "1a4b354c-8692-44d0-9b52-562da45bcce9",
    "name": "Gujarat Titans vs Sunrisers Hyderabad, 51st Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Narendra Modi Stadium, Ahmedabad",
    "date": "2025-05-02",
    "dateTimeGMT": "2025-05-02T14:00:00",
    "teams": [
        "Gujarat Titans",
        "Sunrisers Hyderabad"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "48e77e32-3016-4f17-9c99-a5663c5eb3e6",
    "name": "Royal Challengers Bengaluru vs Chennai Super Kings, 52nd Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "M.Chinnaswamy Stadium, Bengaluru",
    "date": "2025-05-03",
    "dateTimeGMT": "2025-05-03T14:00:00",
    "teams": [
        "Royal Challengers Bengaluru",
        "Chennai Super Kings"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "aeb65c00-9359-4bc0-827a-9d0365364d1b",
    "name": "Kolkata Knight Riders vs Rajasthan Royals, 53rd Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Eden Gardens, Kolkata",
    "date": "2025-05-04",
    "dateTimeGMT": "2025-05-04T10:00:00",
    "teams": [
        "Kolkata Knight Riders",
        "Rajasthan Royals"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "df44cff0-d889-44a2-a63c-415c93b9d022",
    "name": "Punjab Kings vs Lucknow Super Giants, 54th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Himachal Pradesh Cricket Association Stadium, Dharamsala",
    "date": "2025-05-04",
    "dateTimeGMT": "2025-05-04T14:00:00",
    "teams": [
        "Punjab Kings",
        "Lucknow Super Giants"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "4e4b259f-19b6-4405-9df7-b94ce3b0a2c9",
    "name": "Sunrisers Hyderabad vs Delhi Capitals, 55th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Rajiv Gandhi International Stadium, Hyderabad",
    "date": "2025-05-05",
    "dateTimeGMT": "2025-05-05T14:00:00",
    "teams": [
        "Sunrisers Hyderabad",
        "Delhi Capitals"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "a97077e7-466a-46e8-b6e7-2b74731b1d42",
    "name": "Mumbai Indians vs Gujarat Titans, 56th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Wankhede Stadium, Mumbai",
    "date": "2025-05-06",
    "dateTimeGMT": "2025-05-06T14:00:00",
    "teams": [
        "Mumbai Indians",
        "Gujarat Titans"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "96324bfb-686e-44b6-a48e-5bd71188d1b2",
    "name": "Kolkata Knight Riders vs Chennai Super Kings, 57th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Eden Gardens, Kolkata",
    "date": "2025-05-07",
    "dateTimeGMT": "2025-05-07T14:00:00",
    "teams": [
        "Kolkata Knight Riders",
        "Chennai Super Kings"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "c0de6e70-b66d-4d1e-9915-599bb417f8f4",
    "name": "Punjab Kings vs Delhi Capitals, 58th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Himachal Pradesh Cricket Association Stadium, Dharamsala",
    "date": "2025-05-08",
    "dateTimeGMT": "2025-05-08T14:00:00",
    "teams": [
        "Punjab Kings",
        "Delhi Capitals"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "fe6cfcc7-5018-4673-b864-020cba29b470",
    "name": "Lucknow Super Giants vs Royal Challengers Bengaluru, 59th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow",
    "date": "2025-05-09",
    "dateTimeGMT": "2025-05-09T14:00:00",
    "teams": [
        "Lucknow Super Giants",
        "Royal Challengers Bengaluru"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "1c2f9a38-4c3a-407b-90c1-9b78dee63cb8",
    "name": "Tbc vs Tbc, Qualifier 1",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Rajiv Gandhi International Stadium, Hyderabad",
    "date": "2025-05-20",
    "dateTimeGMT": "2025-05-20T14:00:00",
    "teams": [
        "Tbc",
        "Tbc"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": False,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "40596379-a096-4513-8b6f-41df069ca70c",
    "name": "Tbc vs Tbc, Eliminator",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Rajiv Gandhi International Stadium, Hyderabad",
    "date": "2025-05-21",
    "dateTimeGMT": "2025-05-21T14:00:00",
    "teams": [
        "Tbc",
        "Tbc"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": False,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "08b32e61-9c96-4f37-8f76-0b3439a80567",
    "name": "Tbc vs Tbc, Qualifier 2",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Eden Gardens, Kolkata",
    "date": "2025-05-23",
    "dateTimeGMT": "2025-05-23T14:00:00",
    "teams": [
        "Tbc",
        "Tbc"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": False,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "b70371b1-6528-4af6-992c-e880ed585183",
    "name": "Tbc vs Tbc, Final",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Eden Gardens, Kolkata",
    "date": "2025-05-25",
    "dateTimeGMT": "2025-05-25T14:00:00",
    "teams": [
        "Tbc",
        "Tbc"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": False,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "d3edeb1d-61f4-417d-ba88-85b608c2ba7e",
    "name": "Lucknow Super Giants vs Sunrisers Hyderabad, 70th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow",
    "date": "2025-05-18",
    "dateTimeGMT": "2025-05-18T14:00:00",
    "teams": [
        "Lucknow Super Giants",
        "Sunrisers Hyderabad"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    },
    {
    "id": "ab4e0813-1e78-467e-aca0-d80c5cfe7dbd",
    "name": "Sunrisers Hyderabad vs Lucknow Super Giants, 7th Match",
    "matchType": "t20",
    "status": "Lucknow Super Giants won by 5 wkts",
    "venue": "Rajiv Gandhi International Stadium, Hyderabad",
    "date": "2025-03-27",
    "dateTimeGMT": "2025-03-27T14:00:00",
    "teams": [
        "Sunrisers Hyderabad",
        "Lucknow Super Giants"
    ],
    "fantasyEnabled": True,
    "bbbEnabled": True,
    "hasSquad": True,
    "matchStarted": True,
    "matchEnded": True
    },
    {
    "id": "7431523f-7ccb-4a4a-aed7-5c42fc08464c",
    "name": "Chennai Super Kings vs Royal Challengers Bengaluru, 8th Match",
    "matchType": "t20",
    "status": "Royal Challengers Bengaluru won by 50 runs",
    "venue": "MA Chidambaram Stadium, Chennai",
    "date": "2025-03-28",
    "dateTimeGMT": "2025-03-28T14:00:00",
    "teams": [
        "Chennai Super Kings",
        "Royal Challengers Bengaluru"
    ],
    "fantasyEnabled": True,
    "bbbEnabled": True,
    "hasSquad": True,
    "matchStarted": True,
    "matchEnded": True
    },
    {
    "id": "aa75cb4c-36c7-4ade-a6b6-a6eaf61a33e8",
    "name": "Sunrisers Hyderabad vs Kolkata Knight Riders, 60th Match",
    "matchType": "t20",
    "status": "Match not started",
    "venue": "Rajiv Gandhi International Stadium, Hyderabad",
    "date": "2025-05-10",
    "dateTimeGMT": "2025-05-10T14:00:00",
    "teams": [
        "Sunrisers Hyderabad",
        "Kolkata Knight Riders"
    ],
    "fantasyEnabled": False,
    "bbbEnabled": False,
    "hasSquad": True,
    "matchStarted": False,
    "matchEnded": False
    }
]

# Points System
RUN_POINTS = 10
WICKET_POINTS = 100

class Player:
    def __init__(self, name):
        self.name = name
        self.runs = 0
        self.wickets = 0
        self.points = 0

    def update_runs(self, runs):
        self.runs += runs
        self.points += runs * RUN_POINTS

    def update_wickets(self, wickets):
        self.wickets += wickets
        self.points += wickets * WICKET_POINTS

class Team:
    def __init__(self, name):
        self.name = name
        self.batsmen = []
        self.bowlers = []
        self.total_points = 0

    def add_batsman(self, batsman):
        self.batsmen.append(batsman)

    def add_bowler(self, bowler):
        self.bowlers.append(bowler)

    def update_points(self):
        self.total_points = sum(p.points for p in self.batsmen + self.bowlers)

# Function to select players
def select_players():
    selected_batsmen = random.sample(players["batsmen"], 3)
    selected_bowlers = random.sample(players["bowlers"], 3)
    return selected_batsmen, selected_bowlers

@app.route("/start-game", methods=["GET"])
def start_game():
    team1 = Team("Team 1")
    team2 = Team("Team 2")

    for team in [team1, team2]:
        batsmen, bowlers = select_players()
        for name in batsmen:
            team.add_batsman(Player(name))
        for name in bowlers:
            team.add_bowler(Player(name))

    return jsonify({
        "team1": {
            "batsmen": [p.name for p in team1.batsmen],
            "bowlers": [p.name for p in team1.bowlers]
        },
        "team2": {
            "batsmen": [p.name for p in team2.batsmen],
            "bowlers": [p.name for p in team2.bowlers]
        }
    })

@app.route("/simulate-game", methods=["GET"])
def simulate_game():
    team1 = Team("Team 1")
    team2 = Team("Team 2")
    
    # Simulate the game for both teams
    for team in [team1, team2]:
        # Update runs for each batsman
        for player in team.batsmen:
            player.update_runs(random.randint(0, 100))
        # Update wickets for each bowler
        for player in team.bowlers:
            player.update_wickets(random.randint(0, 5))
        # Update team points based on the players' performance
        team.update_points()
    
    # Prepare the response data
    response_data = {
        "team1": {
            "total_points": team1.total_points
        },
        "team2": {
            "total_points": team2.total_points
        },
        "difference": abs(team1.total_points - team2.total_points)
    }

    # Print the response data to the console
    print("Response Data:", response_data)

    # Return the response as JSON
    return jsonify(response_data)


@app.route("/todays-match", methods=["GET"])
def todays_match():
    # Get today's date in the same format as the match data
    today_date = datetime.now().strftime("%Y-%m-%d")

    # Filter out matches that are happening today
    todays_matches = [
        {
            "teams": match["teams"],
            "venue": match["venue"]
        }
        for match in match_data if match["date"] == today_date
    ]

    # If there is a match today, return it
    if todays_matches:
        return jsonify(todays_matches), 200
    else:
        return jsonify({"message": "No match scheduled for today"}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Use Render's default port
    app.run(host="0.0.0.0", port=port)
