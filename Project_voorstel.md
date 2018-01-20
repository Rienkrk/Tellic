## Projectvoorstel IK15
#### Rienk Koenders, Nigel Goossens en Stijn van Geene

### Samenvatting
We bouwen een webapplicatie waar gebruikers kunnen vragen naar aanbevelingen voor nieuwe een telefoon. Op een soort forum kunnen gebruikers een vraag posten en andere gebruikers kunnen daar op reageren met één of meer suggesties uit de database van telefoons. Gebruikers kunnen telefoons toevoegen aan hun favorieten. Op de profielpagina zijn alle posts van de gebruiker te zien.<br> 

### Schetsen
![Imgur](https://i.imgur.com/M9iGh67.jpg)<br>

### Features
**MVP**<br>
Vraag stellen + antwoorden:<br>
Gebruikers hebben de mogelijkheid om een post te maken, waarin ze vragen kunnen stellen aan andere gebruikers door middel van een forum. Andere gebruikers kunnen hierop antwoorden en via een hyperlink een telefoon aanbevelen.<br>
Zoekfunctie:<br>
Gebruikers kunnen zoeken naar telefoons op basis van de naam.<br>
Account aanmaken:<br>
Gebruikers kunnen een account aanmaken en natuurlijk inloggen en uitloggen.<br>
Persoonlijk profiel + favoriete telefoon:<br>
Gebruikers hebben een persoonlijk profiel waar ze hun favoriete telefoons kunnen laten zien.<br>


**Overige**<br>
Telefoon Pagina:<br>
Gebruikers kunnen een telefoon pagina bekijken waar alle telefoons, in onze database, te vinden zijn en waar gebruikers bepaalde telefoons kunnen vinden door te filteren op specificaties.<br>


### Afhankelijkheden
**Databronnen:**<br> https://fonoapi.freshpixl.com/<br>
**Externe componenten:**<br> Bootstrap, Flask, Jinja, SQLAlchemy, SASS<br> 
**Concurrenten:**<br>
Gsmarena: Redelijk onoverzichtelijk, enkel telefoons vergelijken niet extra functionaliteiten.<br>
Tweakers: Het vergelijk panel aan de linkerkant is ingewikkeld. Het sorteren op meest bekeken is interessant.<br>
Phonearena: Het “discussions” gedeelte is interessant, het zorgt ervoor dat mensen sneller duidelijkheid krijgen over het product.<br>
**Moeilijkste delen:**<br> Code collaboration, Beveleiliging eigen database voor account<br>


