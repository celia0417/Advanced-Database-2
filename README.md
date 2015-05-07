# Advanced-Database-2

1. How to run
python infobox.py -key <Freebase API key> -q <query> -t <infobox|question>
or python infobox.py -key <Freebase API key> -f <file of queries> -t <infobox|question> or python infobox.py -key <Freebase API key>

The first command returns a infobox/question result of a query (it can be quoted or not).
The second command use a file input (each line as a query), and output the result sequentialy.
After typing in the third command, you can input a query and the program will judge if it is a infobox query or a question and show the result. Type in “quit” to exit.


2. Program Internal Design
(1) Part 1: Infobox Creation
The process of creating an infobox is as following:
<1>. Use Freebase search API to get the topics of the query.
<2>. Parse the “type/object/type” tag and add the types of our interest (the six
types of entities). An entity cannot be both a person and a league or sports team, so if it has been parsed as a person, then we don’t add the “League” or “Sports_team” type. Similarly if we already have league or sports team.
<3>. We used a ordered dictionary to correspond each tag to the property we care about. Like there’s key-value pair “Name, /type/object/name”; for the compound value type, the value is a sub-level dictionary. We use this ordered dictionary to parse the topic object returned from freebase topic API and store the information in another ordered dictionary called “infobox”.
<4>. We designed a function to format the output of the infobox, the width output is 100. So it is similar to the output of reference implementation.

(2) Part 2: Question Answering
<1>. Check if input file or question is empty, if so return warnings.
<2>. For every single question, check if question is valid, if so do next steps; otherwise, return warnings.
<3>. Call MQL Freebase API, search for both author and business person. As long as we have result from any of these two, construct every output according to the required format. If return results for both author and business person, combine the results. Return the results sorted by first letter. Otherwise, if no match result for both, return warnings.
<4>. Print out all the result according to required format.

3. Freebase API Key AIzaSyCSr5ZDDE-XCrc6xTPML7CaRqHbAAsHXDM
