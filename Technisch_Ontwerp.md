## Technisch ontwerp IK15 (Tellic)
Zie de afbeelding onderaan dit bestand voor een overzichtstekening
### Views
**Index.html**<br>
GET en POST, Forum + zoekbalk<br>
**Post.html**<br>
GET en POST, pagina om post te presenteren en erop reageren<br>
**Display.html** <br> 
GET en POST, pagina om gevonden telefoon te presenteren en toe te voegen aan favorieten<br>
**Login.html**<br>
GET en POST, inlogpagina <br>
**Register.html**<br>
GET en POST, Registreerpagina<br>
**Profile.html** <br>
GET, Profielpagina met alle posts en userdata<br>
**CreatePost.html** <br>
GET en POST, Pagina om post te schrijven daarbij te zoeken in telefoondatabase <br>
**Layout.html** <br>
GET, Standaard menu dat op iedere pagina zichtbaar is<br>

### Models
**tellicdatabase**<br>
users: id, username, password, timestamp<br>
favoirtes: id, user_id, phone_id<br>
posts: id, user_id, timestamp, text, title<br>
replies: id, user_id, post_id, text, phone_id<br>
**phonedatabase**<br>
phones: API

### Controllers
Logout.py: Logt de gebruiker uit<br>
addFavorites.py: Zorgt ervoor dat een gebruiker zijn favoriete telefoons kan toevoegen aan zijn profiel.<br>
getPhone.py: functie die telefoon opzoekt in database en alle data ervan returnt<br>
createPost.py: Zorgt ervoor dat de gebruiker een post kan maken<br>
getUserData.py: Haalt alle gebruikersdata uit de database<br>
Reply.py: Zorgt ervoor dat de gebruiker kan reageren op een post<br>
getReplies.py: Haalt alle antwoorden op een post op.<br>
getPost.py: Haalt de post op van een gebruiker om het te openen. <br>
Register.py: Registreert de gebruiker.<br>
getFavorites.py: Haalt de favoriete telefoons op van een gebruiker.<br>

### Hulpfuncties
Error.py: Zorgt ervoor dat de gebruiker een error bericht krijgt als er iets fout is.<br>
Login_required.py: Zorgt ervoor dat je voor sommige functies van de site ingelogd moet zijn om het te kunnen gebruiken. ( Voor het maken van een nieuwe post bijvoorbeeld )
( wss nog meer later )<br>
hash: Iets om het wachtwoord mee te encrypten

### Overzicht
![Imgur](https://i.imgur.com/M9iGh67.jpg)

### Schetsen
**Profiel.html**<br>
![Imgur](https://i.imgur.com/0TZenH2.jpg)
**Login.html**<br>
![Imgur](https://i.imgur.com/58gcoog.jpg)
**Register.html**<br>
![Imgur](https://i.imgur.com/Z9dCnop.jpg)
**Index.html**<br>
![Imgur](https://i.imgur.com/sTPOQqa.jpg)
**createPost.html**<br>
![Imgur](https://i.imgur.com/OL70O7O.jpg)
**Post.html**<br>
![Imgur](https://i.imgur.com/PAWerLy.jpg)
**Display.html**<br>
![Imgur](https://i.imgur.com/iOOzioZ.jpg)
