# Onderweg naar een betere doorstroming op de weg

Dit is onze repo voor een school project die we voor Vialis hebben uitgevoerd. 
Deze repo bevat de code van de visualisatie en de simulatie, de testcode, het adviesrapport en de resultaten van ons onderzoek. 


## Visualisatie en simulatie 
De code van het programma kan je in `Programma` vinden. De resultaten van de onderzoek kan terug vinden in `map_naam\bestandnaam.ipynb` 
Voor volledige uitleg van de onderzoek zie `map_naam\adviesrapport.pdf`

## Installatie

Clone de repository naar een map naar keuze op je eigen pc.
*voor meer informatie zie https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository

De software heeft een paar benodigde libraries deze kun je makkelijk installeren met pip. Hiervoor kan het volgende commando uitgevoerd worden:
```bash
    pip install -r requirements.txt
``` 

Als je de standaard visualisatie wil afspelen moet `kruispunt_data(unziphere).zip` en `wachtrij_data(unziphere).zip` worden uitgepakt.
Om de visualisatie te runnen ga naar `Main_Program\` en run het bestand `main.py` via een IDE naar keuze, of de terminal.

Er zou een pygame omgeving geopend moeten worden. In deze omgeving kan er een tijd ingevoerd worden om de visualisatie te runnen.

### Optionele feature, maar nog niet geheel gebruiksvriendelijk

Ook kun je een afbeelding van een kaart "uitknippen" en deze toevoegen voordat je een simulatie uitvoerd. Bijvoorkeur in png format
Noteer hiervan de latitude en longitude van links-boven hoek en rechts-onder hoek, deze zijn nodig om de simulatie op deze locatie weer tegeven.
Deze afbeelding grote moet exact overeenkomen met de resolutie, aangezien hieroverheen de data punten worden geprojecteerd.**
Verander als je dit wil doen in main.py de p0 en p1 variable aan naar respectievele top left en bottom right coordinaten.
Noem de afbeelding "bg.png" zodat het programma het kan vinden



** Dit hebben we binnen deze tijd helaas niet kunnen oplossen omdat de afbeelding dan "gescaled" zou moeten worden, met verhoudingen niet alleen aan de resolutie, maar ook met de longitude en latitude van de wereld.


## Uitleg van de Visualisatie zelf

De cyaan gekleurde vierkanten zijn lussen, deze lichten op in een oranje kleur als deze geactiveerd word.
Druk knoppen zijn paarse vierkantjes, en veranderen ook naar oranje wanneer geactiveerd.
Als je de externe data bekijkt heeft de externe gps data een zwart vierkantje om de auto te visualiseren
Stoplichten worden weergegeven in de kleur die ze op dat moment weergeven en zijn gevormd naar een rondje met een streepje er doorheen.


**Een voorbeeld** 


![Visualisatie](https://github.com/mickers13/Vialis-1-Verkeersimulatie/tree/main/Main_Program/overig/visualisatie.PNG)

## Test code

In dit project hebben voor zover het mogelijk is de TDD en BDD principes werkwijze gehanteerd.
Daarvoor kijk in de commits en de versiebeheer. 
Om de test code te runnen ga naar `Main_Program\tests\` en run het bestand `main_test.py`. 
Helaas zijn er meerdere functies binnen de visualisatie die niet getest kunnen zijn.


## Hergebruiken van de code 
Zodra je `main.py` hebt uitgevoerd kun je de tijd aanpassen, en hier naar bepaalde data kijken. 

## Validatie
Wij zelf hebben een experiment opgezet om de heatmap te controleren met extern vergaarde data, dit hebben we gedaan met extern vergaarde gps data.
Deze data hebben we over onze simulatie heen gemapped om te kijken of de sensoren, verkeerslichten en onze algoritmes correct zijn. 
Als je zelf ook wil kijken naar onze data kun je tussen `14:54` en `15:25` op 10/01/2021 zelf verschillende tijden bekijken en zien waar wij hebben gereden over het voorbeeld kruispunt.


Zo kun je zien dat een groot deel van onze simulatie erg goed overeenkomt, maar helaas door het interpoleren rijd de auto soms erg langzaam door rood. Dit is natuurlijk niet in het echt gebeurd, en is een probleem waar we helaas niet aantoegekomen zijn binnen de tijd van dit project.
Ook is er een kleine delay met het "afkoelen" van de heatmap, onstaan door ongeveer hetzelfde probleem met het interpoleren. Dit zou ook een van de volgende features zijn die we kunnen toevoegen. Maar de simulatie werkt ook erg goed zonder.


> Groep 1 vialis casus 2021
