# status_pr_scraper
Scrapes <a href=status.pr>StatusPR</a> for full details on the Puerto Rico recovery

## Summary

This python module provide a function that returns most data from the StatusPR dashboard. Given that 
<a href="https://www.theatlantic.com/politics/archive/2017/10/why-did-fema-remove-stats-about-puerto-ricos-recovery/542343/">FEMA took  down some of its statistics</a> (although <a href="https://twitter.com/wpjenna/status/916364778502803456">they are now available once more</a>,
statusPR is the best site available for the stats on Puerto Rico's recovery from Hurricane Maria, but it lacks an easy-access API to collect that information.
I therefore created a script that scrapes and cleans the data on the dashboard to make this great resource more accessible.

There are two functions. The first, get_data(), returns statusPR's data as a dictionary. The second, get_data_as_tsv(file_path), prints statusPR's data to a file (defaulting to tab-seperated). Details can be found below.

## Data Format

**get_data_as_tsv(out_path,sep='\t')**
Returns the data as a tsv (or otherwise-seperated value file, if you change sep).  Relies on get_data.
The header row is organized as: Key, Reported Value, Current, Total, Last Update, Source, Note.

**get_data**

Returns the data as a python dictionary. This almost certainly isn't the best format for it, and it might be updated soon.
Still, this should work on a short-term basis.
Each of the 21 statusPR cards (for the moment, this is not including water or commercial flights cards) is a key for the dictionary, and corresponds to another dictionary (again, probably sub-optimal).

The Dictionary keys and the data they correspond to:

Key | Card
--- | ---
gas | Gas stations that have received fuel at least once since Hurricane Maria.
supermarket | Active supermarkets\*
AEE | Electrical Energy Authority clients with access to electricity
telecommunication | Clients with access to telecommunication services\*
antenna | Active cell phone antennas
tower | Active cell phone towers
shelter | Operational shelters
refugee | Shelterees
pet | Displaced Pets
hospital | Active assisted hospitals (including those without power)
dialysis | Active assisted dialysis centers
pharmacy | Active online processing pharmacies
port | Open ports
container | Containers\*
bank | Active bank branches
cooperatives | Active cooperatives
ATMs | Active ATMs
barrel_diesel | Barrels of diesel supplied\*\*
barrel_gasoline | Barrels of gasoline supplied\*\*
bread | Active buisenesses processing bread
ama | Active Metropolitan Bus Authority routes
federal_mail | Active post offices (USPS)

\*: Cards where I am particularly unsure of the specifics of what the metric is precisely measuring.
\*\*: Last Update and Note values are the same for these two keys, only the Reported Value field differs.

The data dictionaries all have the same format. Every value is a string, for now:

Key | Data | Notes
--- | --- | --- |
Reported Value | The main value, printed in large on statusPR. Often, this is the only data available. It can be a percentage or raw number. |
Current | If the reported value is a percentage, then if statusPR reports the raw number (numerator), it'll be stored here. | Not all percentages also provide the raw number.
Total | If the reported value is a percentage, then if statusPR reports the total (denominator), it'll be stored here. | Not all percentages also provide the raw number.
Last Update | Last update date | Stored as datatime.date.
Source | StatusPR's source for the data |
Note | If StatusPR included a note with the data card, it'll be stored here. | Most cards don't include notes.

## How-To

This module requires the packages <a href="http://docs.python-requests.org/en/master/">requests</a> and
<a href="https://www.crummy.com/software/BeautifulSoup/">Beautiful Soup</a>.

In whatever piece of python you want to get this dictionary into, import status_pr_scraper, and call the function get_data().
The function returns the dictionary.

Alternatively, call get_data_as_tsv(file_path). The function will write the data at the file path you provide.

## To-do

(In no particular order)

1. Return data in a better-to-use format than a dictionary, for heaven's sake.

2. ~~Make a function that will just output the data into a csv/tsv, as a stop-gap for the above.~~ Done!

3. ~~Split barrels of diesel/gas into two different pieces of data, one for each type.~~ Done!

4. ~~Format the dates as python dates~~. Done!

5. ~~Store the numbers as numbers, not strings.~~ Done! Stored as floats/None.

6. Add more data from other places on statusPR

## Thanks to

Philip Bump at the Washington Post, whose <a href="https://www.washingtonpost.com/news/politics/wp/2017/10/06/fema-buried-updates-on-puerto-rico-here-they-are/?utm_term=.701ef12a9d67">October 6 article</a> inspired this work. Also, he's a solid journalist, and that deserves appreciation just as well.
