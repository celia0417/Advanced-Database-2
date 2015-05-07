import json
import urllib
import re
import collections
import sys
from Part2 import part2
from part2_table import part2_table

def getTopic(api_key, query):
    #Get search result from freebase
    service_url = 'https://www.googleapis.com/freebase/v1/search'
    params = {
            'query': query,
            'key': api_key
    }
    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())

    #Get topic from freebase
    service_url = 'https://www.googleapis.com/freebase/v1/topic'
    params = {
      'key': api_key
    }
    topic=[]
    topictypes=[]
    for i in range(5):
        if i+1 > len(response['result']):
            break
        topic_id = response['result'][0]['mid']
        url = service_url + topic_id + '?' + urllib.urlencode(params)
        topic = json.loads(urllib.urlopen(url).read())

        sixtopics=collections.OrderedDict([('/people/person','Person'), ('/sports/sports_league','League'),
                   ('/sports/sports_team','Sports_Team'),('/sports/professional_sports_team','Sports_Team'),
                   ('/book/author','Author'), ('/film/actor','Actor'),('/tv/tv_actor','Actor'),
                   ('/organization/organization_founder','Business_Person'),('/business/board_member','Business_Person')])

        if topic['property'].has_key('/type/object/type'):
            for stk in sixtopics.keys():
                for value in topic['property']['/type/object/type']['values']:
                    if value['id'] == stk:
                        tpctype=sixtopics[value['id']]
                        if 'Person' in topictypes and (tpctype=='League' or tpctype=='Sports_Team'):
                            continue
                        elif 'League' in topictypes or 'Sports_Team' in topictypes:
                            continue
                        if not tpctype in topictypes:
                            topictypes.append(tpctype)
        if len(topictypes)>0:
            break
                        
    #print topictypes
    infobox=getInfobox(topictypes, topic)
    return (topictypes,infobox)
                    
def getInfobox(topictypes, topic):
    infobox=collections.OrderedDict()

    tags=collections.OrderedDict([('Person',collections.OrderedDict([("Name","/type/object/name"),
                    ("Birthdate","/people/person/date_of_birth"),
                    ("Place of Birth","/people/person/place_of_birth"),
                    ("Cause of Death","/people/deceased_person/cause_of_death"),
                    ("Date of Death","/people/deceased_person/date_of_death"),
                    ("Place of Death","/people/deceased_person/place_of_death"),
                    ("Siblings",["/people/person/sibling_s","/people/sibling_relationship/sibling"]),
                    ("Spouses",["/people/person/spouse_s",("Spouse","/people/marriage/spouse"),
                               ("From","/people/marriage/from"),
                               ("Location","/people/marriage/location_of_ceremony"),
                               ("To","/people/marriage/to")]),
                    ("Description","/common/topic/description")])),
          ('Author',collections.OrderedDict([("Books","/book/author/works_written"),
                    ("Books about","/book/book_subject/works"),
                    ("Influenced","/influence/influence_node/influenced"),
                    ("Influenced by","/influence/influence_node/influenced_by")])),
          ('Actor',{"Films":["/film/actor/film",("Character","/film/performance/character"),
                            ("Film name","/film/performance/film")]}),
          ('Business_Person',collections.OrderedDict([("Leadership",["/business/board_member/leader_of",
                                          ("Organization","/organization/leadership/organization"),
                                          ("Role","/organization/leadership/role"),
                                          ("Title","/organization/leadership/title"),
                                          ("From","/organization/leadership/from"),
                                          ("To","/organization/leadership/to")]),
                            ("Board member",["/business/board_member/organization_board_memberships",
                                            ("Organization","/organization/organization_board_membership/organization"),
                                            ("Role","/organization/organization_board_membership/role"),
                                            ("Title","/organization/organization_board_membership/title"),
                                            ("From","/organization/organization_board_membership/from"),
                                            ("To","/organization/organization_board_membership/to")]),
                            ("Founded","/organization/organization_founder/organizations_founded")])),
          ('League',collections.OrderedDict([("Name","/type/object/name"),
                    ("Championship","/sports/sports_league/championship"),
                    ("Sports","/sports/sports_league/sport"),
                    ("Slogan","/organization/organization/slogan"),
                    ("Official Websites","/common/topic/official_website"),
                    ("Teams",["/sports/sports_league/teams","/sports/sports_league_participation/team"]),
                    ("Description","/common/topic/description")])),
          ('Sports_Team',collections.OrderedDict([("Name","/type/object/name"),
                        ("Sport","/sports/sports_team/sport"),
                        ("Arena","/sports/sports_team/arena_stadium"),
                        ("Founded","/sports/sports_team/founded"),
                        ("Leagues",["/sports/sports_team/league","/sports/sports_league_participation/league"]),
                        ("Location","/sports/sports_team/location"),
                        ("Description","/common/topic/description"),
                        ("Coaches",["/sports/sports_team/coaches",
                                   ("Name","/sports/sports_team_coach_tenure/coach"),
                                   ("Position","/sports/sports_team_coach_tenure/position"),
                                   ("From","/sports/sports_team_coach_tenure/from"),
                                   ("To","/sports/sports_team_coach_tenure/to")]),
                        ("PlayersRoster",["/sports/sports_team/roster",
                                         ("Name","/sports/sports_team_roster/player"),
                                         ("Position","/sports/sports_team_roster/position"),
                                         ("Number","/sports/sports_team_roster/number"),
                                         ("From","/sports/sports_team_roster/from"),
                                         ("To","/sports/sports_team_roster/to")]),
                        ("Championships","/sports/sports_team/championships")])
                        )])

    for tt in topictypes:
        for k, v in tags[tt].iteritems():
            #Compound valuetype
            if type(v)==list:
                if topic['property'].has_key(v[0]):
                    valuelist=[]
                    for subtopic in topic['property'][v[0]]['values']:
                        subvaluedict=collections.OrderedDict()
                        fr=""
                        to="now"
                        for i in range(1,len(v)):
                            if type(v[i])==tuple:
                                tagname=v[i][0]
                                tag=v[i][1]
                                if tagname!="From" and tagname!="To":
                                    subvaluedict[tagname]=""
                            #dont have a specific description of subtype, like 'siblings', then just one property
                            else:
                                tagname="value"
                                tag=v[i]
                            #put each property into the sub-dictionary
                            if subtopic['property'].has_key(tag):
                                for value in subtopic['property'][tag]['values']:
                                    if tagname=="From":
                                        fr=value['text']
                                        subvaluedict["From-To"]="("+fr+" / "+to+")"
                                    elif tagname=="To":
                                        to=value['text']
                                        subvaluedict["From-To"]="("+fr+" / "+to+")"
                                    else:
                                        subvaluedict[tagname]=value['text']
                        valuelist.append(subvaluedict)
                    infobox[k]=valuelist
            #Other valuetype
            else:
                if topic['property'].has_key(v):
                    valuelist=[]
                    for value in topic['property'][v]['values']:
                        if k=="Description":
                            valuelist.append(value['value'])
                        else:
                            valuelist.append(value['text'])
                    infobox[k]=valuelist
    return infobox


def printinfobox(topictypes,infobox):
    print " ".ljust(98,'-')
    infotitle=query+'('
    for tt in topictypes:
        if tt!='Person':
            infotitle=infotitle+tt.upper()+', '
    infotitle=infotitle[:-2]+')'
    print "|"+infotitle.center(98)+"|"
    print " ".ljust(98,'-')
    for k,v in infobox.iteritems():
        nlines=len(v)
        if nlines==0:
            continue
        if type(v[0])!=collections.OrderedDict:
            if k=='Description':
                v[0]=re.sub('\n',' ',v[0])
                len_d=len(v[0])
                if len_d<=80:
                    print "| "+(k+':').ljust(17,' ')+v[0].ljust(80,' ')+"|"
                else:
                    print "| "+(k+':').ljust(17,' ')+v[0][0:80]+"|"
                    for i in range(1,len_d/80):
                        print "|".ljust(18,' '),
                        if len_d>(i+1)*80:
                            print v[0][80*i:80*(i+1)]+"|"
                        else:
                            print v[0][80*i:].ljust(80,' ')+"|"
            else:
                for i in range(len(v)):
                    if i==0:
                        if(len(k)>16):
                            print "| "+(k[:12]+'...:'),
                        else:
                            print "| "+(k+':').ljust(16,' '),
                    else:
                        print "|".ljust(18,' '),
                    if len(v[i])>80:
                        print v[i][:77]+"...|"
                    else:
                        print v[i].ljust(80,' ')+"|"
        elif v[0].keys()[0]=='value':
            for i in range(len(v)):
                if i==0:
                    print "| "+(k+':').ljust(16,' '),
                else:
                    print "|".ljust(18,' '),
                if len(v[i].values()[0])>80:
                    print v[i].values()[0][:77]+"...|"
                else:
                    print v[i].values()[0].ljust(80,' ')+"|"
        #Compound valuetype
        else:
            nspace=80
            for subkey in v[0].keys():
                nspace-=len(subkey)
            eachspace=nspace/(len(v[0]))
            spaces=[]
            nspace=80
            for i in range(len(v[0].keys())):
                if i!=len(v[0].keys())-1:
                    space=len(v[0].keys()[i])+eachspace-2
                    spaces.append(space)
                    nspace=nspace-space-2
                else:
                    spaces.append(nspace-1)
            #print titles
            print "| "+(k+':').ljust(15,' '),
            for i in range(len(v[0].keys())):
                print "|"+(v[0].keys()[i]+':').ljust(spaces[i],' '),
            print "|"
            
            print "|".ljust(18,' ')+"".ljust(80,'-')
            #print values
            for i in range(len(v)):
                print "|".ljust(17,' '),
                for j in range(len(v[i].values())):
                    if len(v[i].values()[j])>spaces[j]:
                        print "|"+(v[i].values()[j][:spaces[j]-3]+"..."),
                    else:
                        print "|"+(v[i].values()[j]).ljust(spaces[j],' '),
                print "|"
        print " ".ljust(98,'-')

def usage():
    sys.stderr.write("""
    Usage: python infobox.py -key <Freebase API key> -q <query> -t <infobox|question>
        or python infobox.py -key <Freebase API key> -f <file of queries> -t <infobox|question>
        or python infobox.py -key <Freebase API key>\n""")

if __name__ == "__main__":
    if len(sys.argv)==3:
        if sys.argv[1]!='-key':
            usage()
            sys.exit(1)
        
    elif len(sys.argv)>6:
        if sys.argv[1]!='-key' or (sys.argv[3]!='-q' and sys.argv[3]!='-f') or sys.argv[-2]!='-t' or (sys.argv[-1]!='infobox' and sys.argv[-1]!='question'):
            usage()
            sys.exit(1)
    else:
        usage()
        sys.exit(1)

    api_key = sys.argv[2]

    if len(sys.argv)==3:
        while True:
            query=raw_input("Start exploring...\n")
            if query.lower()=="quit":
                break
            query=query.strip('\'')
            if query.lower().startswith('who created'):
                part2_table(query)
            else:
                (topictypes,infobox)=getTopic(api_key,query)
                printinfobox(topictypes,infobox)
        
    elif sys.argv[-1]=='infobox':
        if sys.argv[3]=='-q':
            query = sys.argv[4]
            for i in range(5, len(sys.argv)-2):
                query=query+' '+sys.argv[i]

            (topictypes,infobox)=getTopic(api_key,query)
            printinfobox(topictypes,infobox)
        else:
        #Read from file
            f=open(sys.argv[4],"r")
            lines=f.readlines()
            for query in lines:
                query=query.strip()
                (topictypes,infobox)=getTopic(api_key,query)
                printinfobox(topictypes,infobox)
        
    elif sys.argv[-1]=='question':
        if sys.argv[3]=='-q':
            query = sys.argv[4]
            for i in range(5, len(sys.argv)-2):
                query=query+' '+sys.argv[i]

            part2([query])
        else:
        #Read from file
            f=open(sys.argv[4],"r")
            lines=f.readlines()
            for query in lines:
                query=query.strip()
                part2([query])




