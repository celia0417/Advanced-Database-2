import json
import urllib
import re

def part2(input):
    if len(input) < 1 or input is None:                     # check input file
        print "\n Wrong Question! \n"
    elif len(input) == 1:                                   # single question
        print "\n Query-Question: " + input[0] + "\n"
        result = get_one(input[0])
        if result is not None and result is not False:
            result.sort()
            count = 1
            for res in result:
                print str(count) + ". " + res
                count += 1
        elif result is False:
            print "\n Wrong Question! \n"
        else:
            print "It seems no one created [" + input[0] + "]"  # no matched result

    elif len(input) > 1:                                       # multiple questions
        for i in input:
            print "\n Query-Question: " + i + "\n"
            result = get_one(i)
            count = 1
            if result is not None and result is not False:
                result.sort()
                for res in result:
                    print str(count) + ". "+res
                    count += 1
            elif result is False:
                print "\n Wrong Question! \n"
            else:
                print "It seems no one created [" + i + "]"  # no matched result


def get_one(one_input):
    p = re.compile("who created (.*) ?")                    # extract pattern match "who created"
    question = p.findall(one_input.lower())
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

    if business_person['result'] and author['result']:        # for both author and businees person
        bp = get_bus_per(business_person['result'])
        author = get_author(author['result'])
        result = bp + author
        return result

    elif business_person['result']:                           # only ofr businees person
        bp = get_bus_per(business_person['result'])
        return bp

    elif author['result']:                                    # only for author
        author = get_author(author['result'])
        return author

    else:
        return None


# for getting business person
def get_bus_per(bp):
    res = []
    for i in range(0,len(bp)):
        output = bp[i]['name'] +' (as BusinessPerson) created'
        founder = bp[i]['/organization/organization_founder/organizations_founded']
        size = len(founder)

        output += ' <' + founder[0]['a:name']+'>'
        for j in range(1,size-1):
            output += ', <' + founder[j]['a:name']+'>'
        if size != 1:
            output += ' and <' + founder[size-1]['a:name']+'>'
        res.append(output)

    return res


# for getting author
def get_author(input):
    res = []
    for i in range(0,len(input)):
        output = input[i]['name'] +' (as Author) created'
        author = input[i]['/book/author/works_written']
        size = len(author)
        output += ' <' + author[0]['a:name']+'>'

        for j in range(1,size-1):
            output += ', <' + author[j]['a:name']+'>'
        if size != 1:
            output += ' and <' + author[size-1]['a:name']+'>'

        res.append(output)
    return res

#part2 (["Who created Google?","Who created Lord of the Rings?","Who created Microsoft?","Who created Romeo and Juliet?"])
# part2(["Who created the zzzzzzii?","Who created microsoft?","ho created the lord of the rings?",""])
# part2 ([])
# part2(["ho created the lord of the rings?","Who created microsoft?"])
# part2(["Who created Google?",""])    # check invalid
