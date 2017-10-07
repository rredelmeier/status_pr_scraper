# status_pr_scraper
Scrapes <a href=status.pr>StatusPR</a> for full details on the Puerto Rico recovery

<b>Summary</b>

This python module provide a function that returns most data from the StatusPR dashboard. Given that 
<a href="https://www.theatlantic.com/politics/archive/2017/10/why-did-fema-remove-stats-about-puerto-ricos-recovery/542343/">FEMA took  down some of its statistics</a> (although <a href="https://twitter.com/wpjenna/status/916364778502803456">they are now available once more</a>,
statusPR is the best site available for the stats on Puerto Rico's recovery from Hurricane Maria, but it lacks an easy-access API to collect that information.
I therefore created a script that scrapes and cleans the data on the dashboard to make this great resource more accessible.

<b>Data Format</b>

Currently, the data is returned as a python dictionary. This almost certainly isn't the best format for it, and it might be updated soon.
Still, this should work on a short-term basis.
Each of the 21 cards (for the moment, not including water and commercial flights) is a key for the dictionary, and corresponds to another dictionary (again, probably sub-optimal).

The Dictionary keys and the data they correspond to:

Key | Card
--- | ---
gas | Gas stations that have received fuel at least once since Hurricane Maria.
supermarket | Active supermarkets*
AEE | Electrical Energy Authority clients with access to electricity
telecommunication | Clients with access to telecommunication services*
antenna | Active cell phone antennas
tower | Active cell phone towers
shelter | Operational shelters
refugee | Shelterees
pet | Displaced Pets
hospital | Active assisted hospitals (including those without power)
dialysis | Active assisted dialysis centers
pharmacy | Active online processing pharmacies
port | Open ports
container | Containers*
bank | Active bank branches
cooperatives | Active cooperatives
ATMs | Active ATMs
barrel | Barrels of diesel and gasoline supplied
bread | Active buisenesses processing bread
ama | Active Metropolitan Bus Authority routes
federal_mail | Active post offices (USPS)

\*: Cards where I am particularly unsure of the specifics of what the metric is precisely measuring.

The data dictionaries all have the same format. Every value is a string, for now:

Key | Data | Notes
--- | --- | --- |
Reported Value | The main value, printed in large on statusPR. Often, this is the only data available. It can be a percentage or raw number. | Weird for barrels of diesel and gasoline, see below.
Current | If the reported value is a percentage, then if statusPR reports the raw number (numerator), it'll be stored here. | Not all percentages also provide the raw number.
Total | If the reported value is a percentage, then if statusPR reports the total (denominator), it'll be stored here. | Not all percentages also provide the raw number.
Last Update | The date, formatted in the style of "06/oct/2017" | Hopefully changed to an easier-to-work-with format soon.
Source | StatusPR's source for the data |
Note | If StatusPR included a note with the data card, it'll be stored here. | Most cards don't include notes.

As mentioned, the data for barrels of diesel and gasoline is formatted strangely. Key 'Reported Value' 
instead returns a dictionary, where key 'Diesel' will get the number of diesel barrels supplied, and key 'Gasoline' will get the number of 
gasoline barrels supplied. This will hopefully be fixed/changed soon. 


<b>How-To</b>

This module requires the packages <a href="http://docs.python-requests.org/en/master/">requests</a> and
<a href="https://www.crummy.com/software/BeautifulSoup/">Beautiful Soup</a>. Make sure those are installed before running this.

In whatever piece of python you want to get this dictionary into, import status_pr_scraper, and call the function get_data().
The function returns the dictionary.

<b>TO-DO</b>

(In no particular order)

1. Return data in a better-to-use format than a dictionary, for heaven's sake.

2. Make a function that will just output the data into a csv/tsv, as a stop-gap for the above.

3. Split barrels of diesel/gas into two different pieces of data, one for each type.

4. Format the dates as python dates.

5. Store the numbers as numbers, not strings.

6. Add more data from other places on statusPR

<b>Thanks to</b>

Philip Bump at the Washington Post, whose <a href="https://www.washingtonpost.com/news/politics/wp/2017/10/06/fema-buried-updates-on-puerto-rico-here-they-are/?utm_term=.701ef12a9d67">October 6 article</a> inspired this work. Also, just a solid journalist, and that deserves thanks just as well.
