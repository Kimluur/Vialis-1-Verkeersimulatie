# Onderweg naar een betere doorstroming op de weg

Dit is onze repo voor een school project die we voor Vialis hebben uitgevoerd. 
Deze repo bevat de code van de visualisatie en de simulatie, de testcode, het adviesrapport en de resultaten van ons onderzoek. 


## Visualisatie en simulatie 
De code van het programma kan je in `Programma` vinden. De resultaten van de onderzoek kan terug vinden in `map_naam\bestandnaam.ipynb` 
Voor volledige uitleg van de onderzoek zie `map_naam\adviesrapport.pdf`

## Installatie

Als allereerst moet `kruispunt_data(unziphere).zip` en `wachtrij_data(unziphere).zip` worden uitgepakt.
Om de visualisatie te runnen ga naar `Main_Program\` en run het bestand `main.py`.

Er zou een pygame omgeving geopend moeten worden. In deze omgeving kan er een tijd ingevoerd worden om de visualisatie te runnen.

**Een voorbeeld** 
Hier komt een foto van de visualisatie te staan

Het is aanbevolen om de benodigde libraries te installeren. Hiervoor kan het volgende commando uitgevoerd worden:
```bash
    pip install -r requirements.txt
``` 
Let op: eerst moet de repo gecloned worden om de code te kunnen runnen.
voor meer informatie zie https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository

## Test code

In dit project hebben voor zover het mogelijk is de TDD en BDD principes werkwijze gehanteerd.
Daarvoor kijk in de commits en de versiebeheer. 
Om de test code te runnen ga naar `Main_Program\tests\` en run het bestand `main_test.py`. 
Helaas zijn er meerdere functies binnen de visualisatie die niet getest kunnen zijn.


## Hergebruiken van de code 
Zodra je `main.py` hebt gerund dan kan je de tijd aanpassen TODO: Voeg nog het experiment toe

> Groep 1 vialis casus 2021
