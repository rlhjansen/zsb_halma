
halmavisuals-3.py
het programma werkt in python versie 2.7.13.
Zorg ervoor dat de volgende libraries geinstalleerd zijn.

__future__
random
copy
time
visual

Onderaan in de file "halmavisuals-3.py" staan parameters om het spel te runnen.
Om een succesvolle run te kunnen hebben vul je de volgende parameters in.


boardsize
rows
playerlist

Boardsize is de grootte van het bord, rows het aantal rijen pionnen en playerlist een lijst met het type spelers dat speelt.
Playerlist heeft als mogelijke variabelen in de list de volgende strings:

'h' voor human, 
'ab' voor Alfa-Beta
'mc' voor Monte Carlo

Als voorbeeld kan playerlist = ['h', 'h'] gebruikt worden wanneer je tegen iemand anders of jezelf wil spelen.
Daarnaast is het van belang dat het aantal rows kleiner is dan de boardsize, maar dit spreekt voor zich.
Ook is aan te raden dat de boardsize altijd 4 of meer groter is dan het aantal rows, zodat het spel gespeeld kan worden zoals bedoelt.
Veel gebruikte instellingen zijn:
boardsize = 16
rows = 5 

Het Monte Carlo algoritme heeft geoefend met de instellingen:
boardsize = 10
rows = 5

Dus tenzij je wil spelen tegen een zeer slechte Monte Carlo, zijn dat de instellingen voor het spelen tegen Monte Carlo.
