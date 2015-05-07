import json
import urllib
import re

def part2_table(input):
    p = re.compile("who created (.*) ?")                    # extract pattern match "who created"
    question = p.findall(input.lower())
    if not question:
        return False                                        # invalid input
    else:
        question = question[0]                              # use valid question to query

    api_key = "AIzaSyCSr5ZDDE-XCrc6xTPML7CaRqHbAAsHXDM"
    service_url = 'https://www.googleapis.com/freebase/v1/mqlread'

    # query for organization
    query = [{"/organization/organization_founder/organizations_founded": [{"a:name": None,"name~=": question}],"id": None,"name": None, "type": "/organization/organization_founder"}]
    # query for book
    query2 = [{"/book/author/works_written": [{"a:name": None, "name~=": question}], "id": None, "name": None, "type": "/book/author"}]

    params = {
            'query': json.dumps(query),
            'key': api_key
    }
    params2 = {
            'query': json.dumps(query2),
            'key': api_key
    }

    url = service_url + '?' + urllib.urlencode(params)
    business_person = json.loads(urllib.urlopen(url).read())

    url2 = service_url + '?' + urllib.urlencode(params2)
    author = json.loads(urllib.urlopen(url2).read())

    plot_table(business_person['result'], author['result'], input)


def plot_table(bp, author, input):
    result = []                                             # for both author and business person
    for i in range(0,len(bp)):                              # creat json for business person
        bper = bp[i]['name']
        bper= []
        bper.append(bp[i]['name'])
        bper.append('Business Person')
        founder = bp[i]['/organization/organization_founder/organizations_founded']
        size = len(founder)

        bper.append(founder[0]['a:name'])

        for j in range(1,size):
            bper.append(founder[j]['a:name'])

        result.append(bper)

    result.sort()

    for i in range(0,len(author)):                          # creat json for author 
        auth = author[i]['name']
        auth = []
        auth.append(author[i]['name'])
        auth.append('Author')
        founder = author[i]['/book/author/works_written']
        size = len(founder)

        auth.append(founder[0]['a:name'])

        for j in range(1,size):
            auth.append(founder[j]['a:name'])

        result.append(auth)

    result.sort()

    print "".ljust(100,'-')
    print "|"+input.center(98)+"|"
    print "".ljust(100,'-')

    # plot table
    for i in range(0,len(result)):
        print "| " + result[i][0]+ "".ljust(25-len(str(result[i][0]))-1,' ') + "| As"+"".ljust(30,' ') + "| Creation" + "".ljust(29,' ')+"|"
        print "|" + "".ljust(25,' ') +"".ljust(74,'-')
        if len(result[i][2]) > 33:                          # construct table
            print "|" + "".ljust(25,' ') + "|" ,
            print result[i][1],
            print "".ljust(31-len(result[i][1]), ' ') + "|",
            print result[i][2][:33],
            print "..."+"".ljust(33-len(result[i][2]),' ')+"|"
        else:
            print "|" + "".ljust(25,' ') + "|" ,
            print result[i][1],
            print "".ljust(31-len(result[i][1]), ' ') + "|",
            print str(result[i][2]),
            print "   "+"".ljust(33-len(result[i][2]),' ')+"|"
        for j in range(3,len(result[i])):
            if len(result[i][j]) > 33:
                print '|' + "".ljust(25,' ') + "|" "".ljust(34,' ')+ "|",
                print result[i][j][:33],
                print"..."+"".ljust(33-len(result[i][j]),' ')+"|"
            else:
                print '|' + "".ljust(25,' ') + "|" "".ljust(34,' ')+ "|" ,
                print result[i][j],
                print "   "+"".ljust(33-len(result[i][j]),' ')+"|"
        print "".ljust(100,'-')




