# Plan global

 - Conception générale d'un plugin pour Activity Browser
 - Exemple : conception du plugin ReSICLED

# Points à aborder

- necéssité de séparer API (partie calculs) de l'UIG
- Manipulation des données via Brightway
- Stockage des données préexistantes via les bdd bw2package
- Intérêt de préconcevoir une API moche en python pour faciliter l'implémentation
- Intégration graphique dans AB
- Pyside, Qt et les Widgets
- Signaux
- Nécessité de conserver à la fois le layout global de AB et celui du logiciel pré existant (dans le cas de ReSICLED, faire des onglets pour garder le concept de feuilles Excel du logiciel natif)


# Conception d'un plugin pour Brightway/Activity Browser :

## 


# Exemple : conception du plugin ReSICLED 

## Description de ReSICLED

ReSICLED est un logiciel d'analyse environnementale axé sur l'étude des scénarii de recyclage de composants. Ce logiciel a d'abord été conçu sur Excel (avec des macros Visual Basic), puis a été adapté en une version Web. ReSICLED a également fait l'objet d'un protage sous forme de plugin pour Activity Browser, en tant que démonstrateur pour le système de plugins développé, dans l'optique d'une uniformaisation des moyens informatiques du laboratoire.

## Création et manipulation des données :

L'un des aspects principaux de ReSICLED est le fait de constamment interroger la base de données, afin d'accéder aux caractéristiques principales des matériaux composant chacun des composants du produit. Il nous faut alors concevoir un modèle de données, qu'on implémente par la suite via un système de classes Python.

### Modèle de données :

On réalise une analyse complète des interactions qui existent entre les différentes entités impliquées (Produits, composants, matériaux), puis on en déduit le modèle physique de données qui sera, par la suite, modélisé via le système de bases de données de Brightway.
On implémente alors le modèles de données dans le sous dossier databases du plugin, de la manière suivante :
 - Pour chaque base de données, on lui crée une classe spécifique, avec l'initialisation (si nécessaire), les accès aux données, écriture et suppression d'entrées.
 - On crée également une classe qui réunit toutes ces classes bases de données (qui permet donc d'accéder à toutes les données via 1 seul objet)

### Manipulation des données :

La manipulation des données (et donc la partie principale de l'API) se fait dans le dossier models, et notamment dans la classe Datamodel. Pour chaque onglet, on a besoin de formatter les données de différentes manières. Par exemple, dnas l'onglet Dismantling, on doit manipuler les données afin de pouvoir afficher le tableau voulu.
On a donc, pour chaque tableau à afficher, une méthode dans la classe Datamodel qui va faire les calculs nécessaires, puis formatter les valeurs pour qu'on puisse les présenter correctement dans les tableaux

### Présentation des données :

Une fois qu'on a effectué le traitement des données, on peut s'o



Plan de la doc de conception :

 - Arborescence du plugin ReSICLED (et explications des classes dans l'arbo)
 - Roadmap de conception du plugin

# Arborescence du plugin ReSICLED

Le plugin ReSICLED a été structuré de la manière suivante : (insérer image)


Dans cette arborescence, on remarque 2 choses principales : tout d'abord, on a séparé les documents du code en lui même, car les documents ne servent à rien en termes de focntionnalité (cependant, on les laisse dans le plugin car ils sont liés à ce plugin). Ensuite, on a séparé les fichiers python par thématique : le sous-dossier databases contient uniquement les classes qui permettent de manipuler les bases de données qu'on utilise, là ou views ne contient que les classes qui gèrent l'affichage des onglets du plugin.

## Bases de données

Dans le sous-dossier databases, on implémente un modèle physique de données implémentéà la suite d'une analyse du logiciel préexistant. (insérer image du MPD). Par la suite, pour chacune des bases de données présentes dans le MPD, on implémente une classe qui va permettre de manipuler une base de donnée Brightway (création, initialisation, ajouts et suppressions). On obtient alors 6 classes (ProductDatabase, ComponentDatabase, MaterialDatabase, ComposeDatabase, DirectiveDatabase et GuidelinesDatabase). Pour manipuler ces 6 bases de données d'une manière plus simple, et permettre des interactions entre les bases de données, on crée une classe DatabaseManager, qui va servir de point d'accès à l'entièreté des bases de données du plugin.



## Ajouts de données externes

Dans le cadre du plugin ReSICLED, on est amenés à devoir initialiser des bases de données lorsuq'on importe le plugin pour la première fois : ces données doivent donc être stockées dans le plugin. On utilise alors le format bw2package (inhérent à Brightway) pour stocker les données initiales. Dans notre cas, nous initialisons les bases de données Materials, Directives et Guidelines.
On stocke alors ces bases de données dans le sous-dossier includes.

## Formattage des données 

Le formattage des données est effectué par une unique classe Datamodel, qui va s'occuper de récupérer les données dont on a besoin, puis les formatter afin de les afficher correctement dans le tableau correspondant. Cette classe est donc munie 


## Intégration graphique dans Activity Browser

Pour la partie interface graphique du plugin, on doit nécessairement se baser sur la mmanière dont a été conçue le logiciel de base (Activity Browser), et comment le système de plugins développé integre ces derniers.
Nous avons donc utilisé la bibliothèque graphique PySide, qui est en fait un portage Python de la bibliothèque graphique Qt (développée pour du C++). D'une manière similaire à ce qui est fait dans Activity Browser, nous disposons d'un onglet ReSICLED qui est généré à l'import du plugin, dans lequel nous allons pouvoir afficher tous les éléments du plugin.

### Layout Principal de l'application 

    En ce qui concerne le layout principal du plugin, à savoir comment organiser les éléments principaux du plugin, nous avons opté pour une
solution qui consiste en la reproduction de la strucuture principale de ReSICLED. La version originale du logiciel étant un fichier Excel, nous avons alors décidé de reproduire le système de feuilles, en utilisant des onglets. Chacun de ces onglets possède ses propres fonctions, et peut interragir avec les autres via l'intérmédiaire de signaux (fonctionnalité de PySide/Qt). Pour chacun des onglets, mais également le layout général du plugin, nous avons implémenté une classe, qui va à la fois gérer l'affichage des éléments qui se trouvent dans l'onglet, mais aussi gérer les interactions entre l'utilisateur et le plugin (via les widgets). Par exemple, la classe MixedTab, qui s'occupe d'afficher l'onglet Mixed, va s'occuper de générer le tableau du scénario Mixed, la grille des 


0) Présentation du plugin
0.5) Arborescence du plugin
1) Gestion des données 
2) Calculs et formattage données
3) Affichage dans Activity Browser
3.1) Affichage des onglets
3.2) Les fenêtres contextuelles
4) Annexes
 - MPD
 - Strucutr

0) Présentation du plugin

ReSICLED est historiquement un logiciel d'analyse environnementale axé sur l'étude des scénarios de recyclage dans le cadre de la conception d'un produit. Ce logiciel, à partir des informations rentrées par l'utilisateur, c'est-à-dire les différentes caractéristiques (poids, matériau, nombre) des composants contenus dans le produit, va produire différents scénarios de recyclage qui vont permettre de dire si le scénario personalisé conçu par l'utilisateur respecte la Directive Européenne, et donc si le produit a correctement été conçu. 

Dans notre cas, cette documentation technique est axée sur le portage de ce logiciel sous la forme d'un plugin pour un autre logiciel d'analyse environnementale, Activity Browser. Ainsi, nous allons voir comment ont été implémentés les principales fonctionnalités du plugin, à savoir la gestion des données, les calculs effectués sur les données, et l'implémentation graphique au sein de Activity Browser.

0.5) Architecture du plugin 

Le plugin a été conçu de manière a séparer les différentes grandes parties du code : d'un côté, nous avons tout ce qui touche à l'API, c'est à dire la gestion des bases de données, calcul et formattage des données. Toutes les classes python concernant l'API se trouvent dans les sous-dossiers databases et models du plugin. De l'autre côté, pour ce qui touche à la partie interface graphique et interactions entre le plugin et l'utilisateur, les classes correspondantes sont situées dans les sous-dossiers views et layouts. Enfin, on retrouve les dossiers contenant des classes et des données utilitaires : dans notre cas, les données sont situées dans le dossier Include, et les classes utilitaires dans le sous-dossier tools.


1) Gestion des données

La partie analyse environnementale de Activity Browser, et notamment la partie API, est permise par la bibliothèque Python dénommée Brightway. Cette bibliothèque permet de créer des projets, dans lesquels on peut créer différentes bases de données et effectuer des calculs sur ces différentes données (Activity Browser n'est en fait que l'interface graphique de Brightway). De ce fait, on utilisera ce système de stockage de données pour réaliser le stockage des données propres à ReSICLED.

Le système de gestion de données de Brightway possède plusieurs avantages :
    - Les données sont stockées en dur, sous la forme de fichiers JSON ou BW2Package. Ceci nous permet alors de pouvoir permettre une conservation des données du plugin en permanence, sans avoir à implémenter une fonction d'écriture en dur.
    - On peut accéder aux données très facilement, du fait que le stockage des données peut s'identifier à celui d'un dictionnaire python. On peut alors créer des entrées personnalisées dans les bases de données qu'on crée, et donc dépasser le simple cadre de l'ACV de Brightway.
    - L'import de bases de données pré-existantes est très simple : à condition que le fichier soit bien formatté ou dans la bonne extenstion, il est possible de créer une base de donnée contenant déjà des entrées de manière très simple (ce qui permet de pouvoir initialiser des données d'une manière très simple).

A la suite d'une analyse approfondie du logiciel pré existant, on aboutit à un modèle physique de données (MPD), qu'on implémente par la suite via un système de classes Python manipulant des bases de donnée Brightway. [Voir annexe 1 pour le MPD, annexe 2 pour la structure des bdd bw].
Pour certaines des classes, nous avons dû initialiser les bases de données avec certaines informations à l'intérieur, notamment les matériaux, afin de permettre le bon fonctionnement du plugin. Nous avons alors tiré partie de la fonctionnalité d'import de bases de données préexistantes, en créant 3 fichiers bw2package contenant les 3 bases de données à initialiser lors de l'import du plugin.
De plus, chaque classe est munie de méthodes permettant de faciliter l'accès et la manipulation de ces données (méthodes d'accès à 1 entrée ou à toutes les entrées, méthode d'ajout ou de suppression).

[mettre photo json structure d'une base de donnée]

2) Calculs et formattage des données : 

L'une des autres grandes parties du plugin consiste en la réalisation des différents calculs nécessaires à l'établissement des scénarii. Dans le cadre de ReSICLED, les calculs et  résultats sont affichés sous forme de tableaux : nosu avons donc besoin de faire les calculs, puis de formatter les données pour rendre l'affichage des tableaux et leur utilisation beaucoup plus facile. Nous avons alors implémenté une classe appelée Datamodel, qui va faire les deux étapes. Cette classe implémente alors des méthodes pour obtenir les données dont nous avons besoin, effectuer les calculs nécéssaires, puis formatter les données pour qu'ensuite leur affichage soit le plus simple possible. Pour chaque tableau présent dans le plugin, nous avons implémenté sa propre méthode de formattage dans la classe Datamodel. Si l'on prend l'exemple du tableau du scénario Dismantling, la méthode associée va alors faire ce qui suit :
 - Récupérer les informations des composants du produit sélectionné;
 - Identifier les données intéressantes (ici le nom du composant, son identifiant, son poids, et les taux de recyclage du scénario correspondant)
 - Pour chacun des composants, on effectue les calculs nécéssaires (ici calcul des masses recyclées, de récupération énergétique et de déchets résiduels), puis on ajoute les données à la liste des données formattées les données (sour la forme d'un tuple)
 - Une fois tous les composants ajoutés, on trie la liste selon le numéro d'identifiant, afin de conserver l'ordre d'ajout des composants et de permettre d'aider l'utilisateur à identifier les pièces.
 - On retourne la liste des tuples (contenant les calculs effectués et les données formattées)

Une fois ceci fait, tout ce qui a trait à la manipulation des données en elles-mêmes est terminé, il ne nous reste plus qu'à rendre les données formattées lisibles et faciles à comprendre.

[Mettre tableau dismantling]

3) Affichage dans Activity Browser

Comme évoqué brièvement précédemment, le système de plugins développé pour Activity Browser permet l'ajout d'onglets pour permettre aux plugins de disposer d'une interface graphique. C'est donc dans l'onglet généré par Activity Browser que nous allons générer l'interface graphique du plugin.
Activity Browser étant développé sur la base de la bibliothèque graphique PySide2 (portage de la bibliothèque graphique Qt de C++ en Python), il nous faut alors développer l'interface du plugin en utilisant cette bibliothèque.
Tout d'abord, pour ce qui est de l'aspect principal du plugin, nous avons décidé de garder une présentation similaire à celle que proposait la version originelle de ReSICLED, c'est-à-dire utiliser un système d'onglets pour garder le côté feuilles de Excel. De même, dans chacun de ces onglets, nous remettons les mêmes éléments contenus dans les feuilles du Excel : on implémente  les tableaux, boutons, menus déroulants, panneaux de présentation dans les onglets correspondants.

Cette implémentation passe alors par des classes, chacune se chargeant de gérer un onglet et ses interactions. Par exemple, pour l'onglet Dismantling :
La classe qui gère l'affichage de l'onglet va s'occuper d'afficher les éléments de changement de produit (menu déroulant), le panel de comparaison des taux de récupération à la directive sélectionnée, ainsi que le tableau. La classe implémente également les méthodes qui mettent à jour les éléments qui sont appelées lorsqu'on récupère les interactions entre l'application et l'utilisateur via les signaux PySide.


De même, le plugin fait appel à des fenêtres contextuelles afin d'ajouter des données ou de faire choisir à l'utilisateur des données (directives notamment). Pour ce faire, on fait appel à des fenêtres contextuelles qui vont permettre à l'utilisateur depouvoir interragir avec le plugin (pour créer un nouveau produit/composant/matériau, choisir la directive). Toutes ces fenêtres contextuelles sont gérées de la même façon, via une classe qui génère la fenêtre, et se charge de gérer les interactions avec l'utilisateur (notamment la sauvegarde des données quand on valide). Toutes les classes gérant les fenêtres de dialogue sont situées dans le même fichier ```form.py``` situé dans le sous-dossier views du plugin.

Enfin, la gestion globale des onglets du plugin est confiée au sous-dossier layouts, qui va contenir les classes qui implémentent le design des onglets de Activity Browser attribués au plugin et la gestion globale des onglets du plugin (par exemple, la classe rightTab va appeler ResicledTab, classe qui permet de mettre en place les différents onglets nécessaires).


