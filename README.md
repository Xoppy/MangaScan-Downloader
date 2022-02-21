# MangaScan-Downloader
Bienvenue sur la page du projet open-source MangaScan-Downloader. 
Cet outil permet de télécharger les différentes pages ou chapitres de scans à partir des sites de scan français les plus connus, pour ensuite les convertir en un fichier PDF facile à lire.

Voici la page pour télécharger le programme executable sur windows : [Télécharger](https://github.com/Xoppy/MangaScan-Downloader/releases)


# M'offrir un café
Si cet outil vous a permis de gagner du temps ou de vous rendre la vie plus facile n'hésitez pas à m'offir un café en faisant une donation, je suis encore en études et dans ma situation chaque petit don compte énormement.

### http://paypal.me/xoppyad
### BTC : bc1q6g63n8xerchkukn70x2mvfjjjfajpj4605vgn5
### ETH : 0xB4a96EdC2e83385379DFe62BA528FC38D6DA4d09

# Comment ça marche
Si vous souhaitez télécharger le code source pour bidouiller avec, il vous faudra télécharger plusieurs librairies à l'aide de la commande "pip install", voici la liste des librairies nécessaires :
- requests
- bs4
- Pillow
- tkinter (n'est pas toujours présent par défaut dans les environnements virtuels)

Pour ce qui est du fonctionnement dans les grandes lignes, cet outil va scraper les liens sources des images disponibles dans les differents sites pour les télécharger et les comprimer dans un fichier PDF.

L'intérface graphique du logiciel est assez rudimentaire mais elle est assez explicite. Pour chaque téléchargement, il faudra indiquer le nom du manga / webtoon, le lien de la première page du chapitre à télécharger et le nombre de chapitres ou de pages que vous voulez dans votre PDF.

![alt text](https://github.com/Xoppy/MangaScan-Downloader/blob/main/MangaScan-Downloader-GUI.png)

Il faut savoir que lors de la création du PDF le logiciel demande une bonne capacité de RAM, je vous conseille de ne pas dépasser les 2000 pages par PDF si vous avez moins de 16Go de RAM.

# Quels sites sont pris en compte
Pour l'instant on peut utiliser cet outil sur trois sites différents : 
- https://scansmangas.xyz/
- https://www.frscan.cc/
- https://lelscans.net/

Attention, pour frscan.cc la fonction pour télécharger directement par chapitres n'est pas disponible pour l'instant. Il faut donc indiquer le nombre de pages précises que l'on souhaite télécharger.

# Disclaimer légal
Cet outil n'est aucunement rattaché aux sites cités ci-dessus et n'a pas été conçu pour une utilisation illégale. L'outil a été crée à la base pour l'utiliser sur des scans non licensés en Europe et des webtoons libres de droits. Toute utilisation à des fins illégaux sera à charge de l'utilisateur.

# Remerciements et disclaimer finaux
Merci beaucoup d'avoir consulté ce projet, c'est mon tout premier projet en Python et je suis particulièrement fier du résultat jusqu'à maintenant. 

Je tiens tout de même à remercier les personnes (qui se reconnaîtront) qui m'ont donné des inspirations sur les différents sites à scraper. Et j'aimerai terminer en vous indiquant que la qualité du code qui est utilisé dans ce projet n'est surement pas parfaite (je dirais même qu'elle est médiocre), mais pour un premier projet et pour une première version je suis assez content du résultat. 

Encore une fois merci, et bon scraping!
