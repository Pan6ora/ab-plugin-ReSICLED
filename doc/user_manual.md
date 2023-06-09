---
title: "Manuel Utilisateur de ReSICLED"
author: "Rémy Le Calloch, Brice Notario Bourgade, Elysée Tchassem Noukimi"
date : "29 Juillet 2022"
output:
    pdf_document :
        toc: true
header-includes:
    \usepackage{graphicx}
---

\maketitle
\begin{center}
\includegraphics{images/logo_resicled_transparent.png}
\end{center}
\thispagestyle{empty}
\clearpage
\tableofcontents
\pagenumbering{roman}
\clearpage
\pagenumbering{arabic}
\setcounter{page}{1}


## Présentation de ReSICLED 

Le document que vous êtes en train de lire est le manuel d'utilisation du plugin ReSICLED pour Activity Browser. 
ReSICLED est un logiciel d'analyse environnementale visant à étudier les différents scénarios de recyclage et les taux de recyclabilité de produits composés de différents composants. L'objectif de ce logiciel est de construire un scénario de recyclage qui respecte la directive européenne associé au produit, et ce en donnant à l'utilisateur des informations pour créer le scénario.


## Importer le plugin ReSICLED

Pour importer le lpugin ReSICLED, on clique sur le bouton import dans la catégorie Plugin du panel gauche, puis on sélectionne le plugin nommé ReSICLED.plugin.
Une fois cette opération faite, on valide, et le plugin est importé !

## Comment le plugin fonctionne-t-il ?

Le fonctionnement général du plugin est assez simple : on entre les données du produit dans l'onglet Input, on sélectionne une directive dans les onglets Dismantling, Shredding et Mixed, et on construit un scénario viable en utilisant les HotSpots et en changeant le scénario de chaque pièce dans Mixed. Pour avoir des pistes d'aide à la conception des composants, le plugin met également à disposition un système de sélection de guidelines.

### Création d'un nouveau produit

La toute première étape lorsqu'on veut analyser un produit est de créer un produit (pour l'ajouter à la base de données). Pour ce faire, on se place dans l'onglet Input, puis on clique sur "Add product". Ensuite, dans la fenêtre qui vient de s'ouvrir, on remplit le nom du produit et de l'utilisateur.

![](images/inputTab.png)  
*Onglet Input*  

![](images/add_product_form.png)  
*Création d'un nouveau produit*  

### Ajout d'un nouveau composant

Pour ajouter un nouveau composant, on clique sur le bouton "Add component" : une fenêtre s'ouvre. Dans cette fenêtre, on doit :
 - Sélectionner le produit auquel ajouter un composant
 - Donner le nom du composant
 - Donner la masse d'une pièce du composant (si vous avez 6 vis de 0.25 grammes chacune, mettez 0.25)
 - Donner le nombre de pièces
 - Mettre un commentaire sur le composant (facultatif)
 - Choisir le matériau : On ne peut choisir qu'un seul matériau, et on peut également créer des matériaux, à condition d'avoir les taux de recyclage et de récupération des scénarios)
 - Ensuite on valide et le nouveau composant est rajouté.

![](images/component_add_form.png)  
*Ajout d'un composant*  

Pour ajouter tous les composants, on répète cette opération autant de fois que nécéssaire.

### Premiers scénarii

Une fois que l'on a ajouté nos composants, on peut commencer à étudier les différents scénarii. Avant de construire notre propre scénario, on va regarder les deux scénarii extrêmes : celui avec le meilleur taux de recyclage possible, Dismantling, et le scénario avec le pire taux de recyclage possible, Shredding.

#### Scénario Dismantling 

Le scénario Dismantling est le scénario idéal (avec le meilleur taux de récupération, de recyclage). Dans ce scénario, toutes les composants du produit vont être démontés. Si on sélectionne la directive correspondant au bon produit (en cliquant sur le bouton "Apply directive"), on peut donc comparer le meilleur scénario possible à la directive européenne : si la directive est plus élevée que le scénario Dismantling, alors il est impossible de pouvoir respecter la directive (et donc que le produit est mal conçu).

![](images/dismantlingtab.png)  
*Onglet Dismantling*  

#### Scénario Shredding

A l'inverse du scénario Dismantling, le scénario Shredding est le pire scénario possible en terems de taux de récupération. Dans ce scénario, on va broyer tous les composants (à l'exception des composants de matériaux polluants, qui doivent nécessairement être démontés selon une autre directive européenne). Dans cet onglet aussi, on peut également comparer le taux de recyclage et de récupération du produit par rapport à la directive choisie (il faut la resélectionner). Dans le cas de figur où l'on a que la directive est plus faible et taux de récupération que le scénario Shredding, ceci signifie que n'importe lequel des scénarii choisis pour le produit satisfera la directive européenne.

![](images/shreddingTab.png)  
*Onglet Shredding*  

### Scénario Personnalisé

Une fois qu'on étudié les deux scénarii limites (Dismantling et Shredding), on peut alors créer un scénario personnalisé. On le crée alors dans l'onglet Mixed. Dans ce tableau, à la différence des tableaux précédents, on a d'autres informations :  
 - le gain 1 : Représente le gain en taux de recyclage quand on passe du scénario shredding au scénario dismantling. Ce gain est nul si le matériau constituant le composant est polluant.  
 - le gain 2 : Représente le gain en taux de récupération quand on passe du scénario shredding au scénario dismantling. Ce gain est nul si le matériau constituant le composant est polluant.  
 - Relative weight : donne le poids relatif d'une unité du composant dans le produit complet  
 - Scenario : Indique le scénario appliqué sur le composant (et donc quels seront les taux de recyclage/récupération énergétique/déchets résiduels on utilisera dans le calcul du taux global). Par défaut, les scénarii de chaque composants sont ceux du scénario Mixed, à savoir que les composants en matérieux polluants sont démontés, et les composants en matériaux non polluants sont broyés.  
Lorsqu'on double-clique sur la case "Scénario" d'un composant du produit, on peut changer son scénario, pour changer de Shredding à Dismantling (et inversement). Cependant, de même que pour Shredding, la directive européenne impose que les composants en matériaux polluants soient nécessairement démontés et non broyés. Ainsi, si on double clique sur un composant fait avec un matériau composant, on a une alerte nous disant qu'on ne peut pas changer le scénario. Sinon, une fenêtre s'affiche, et l'on doit sélectionner la raison pour laquelle on choisit de changer le scénario de fin de vie.

![](images/mixed_before.png)  
*Onglet Mixed*  

### Hotspots

Une fois qu'on a pu voir qu'on pouvait créer un scénario personnalisé de fin de vie pour le produit, l'idée est alors de faire en sorte que le scénario qu'on construit va respecter la directive sélectionnée. C'est alors qu'on introduit l'onglet Hotspots, qui va nous permettre de choisir les composants à changer pour respecter la directive.

L'onglet Hotspots est constitué de deux tableaux : le premier présente les composants qui ont le meilleur potentiel pour le scénario de démontage (à savoir quelles sont les composants qui feront gagner le plus de pourcents aux taux globaux lorsqu'on change leur scénario), et le second classe les composants en fonction de la masse de déchets résiduels qu'ils genèrent.

Ainsi, pour choisir les meilleurs composants dont on changera le scénario, on va prendre les composants qui apparaissent le plus haut dans les tableaux : d'abord, on regarde les valeurs les plus hautes du tableau 1, et on choisit avec le 2e tableau si jamais il y a des composants qui sont à égalité.

Ensuite, on change le scénario des composants dans Mixed, et on continue à changer les scénarii de composants tant qu'on respecte pas la directive.

Exemple : Ici, on est dans le scénario Mixed, et on a de recyclabilité  
![](images/mixed_before.png)  
*Onglet Mixed avant changement*  
On va voir dans Hotspots pour choisir le composant le plus intéressant à changer : 

![](images/hotspots.png)  
*Onglet Hotspots*  

On repère alors que le composant le plus intéressant à changer est le composant n°2 : on retourne donc dans Mixed et on double-clique sur le scénario de ce composant pour le changer : on remarque alors que le taux de recyclage est passé de 47% à 59%, soit une évolution de environ 11.84%

![](images/mixed_after.png)  
*Onglet Mixed après le changement*  

### Visualisation des données

Si l'on veut avoir accès aux bases de données du plugin, on peut alors regarder dans l'onglet Database pour visualiser les entrées de la base de donnée :
Pour visualiser une base de données, on la sélectionne dans le menu déroulant, et le tableau nous montre les éléments contenus dans cette base de données. On peut également, dans cette base de données, ajouter de nouvelles entrées, c'est-à-dire un nouveau produit, matériau, composant ou directive, en cliquant sur le bouton "Add new database entry".

![](images/databasetab.png)  
*Visaualisation d'une base de donnée*  

### Guidelines 

Enfin, ReSICLED propose à l'utilisateur d'avoir des guidelines afin d'aider à la conception des composants : tout se passe dans l'onglet Guidelines du plugin. Dans cet onglet, nous avons 4 menus défilants, qui permettent de sélectionner la stratégie de récupération, les paramètres de design, la position du composant dans l'architecture du produit et le type de composant. Quand on sélectionne des critères dans ces menus déroulants, le plugin va automatiquement enlever les guidelines qui ne sont pas concernées par les paramètres sélectionnés.

![](images/guidelines.png)  
*Exemple sélection de guidelines*  