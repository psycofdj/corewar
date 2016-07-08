<h2>News</h2>
<p>
  Vous trouverez dans cette section toute l'actualité du jeu, en particulier
  d'éventuelles modifications des règles, des spécificités de la machine
  virtuelle ou de buxfix de l'implémentation.
</p>


<h3>29-09-2015</h3>
<p>
  Ajout d'une interface graphique de visualisation de la course. Très pratique pour
  debugger vos vaisseaux ! L'interface est disponible en cliquant sur le lien <a href="#" class="racename">visualiser</a>
  dans les stands.
</p>

<div style="text-align:center;">
  <h4><u>Demo</u></h4><br/>
  <video controls  width="800"  src="/img/demo.ogv">Ici la description alternative</video>
</div>


<h3>19-08-2013</h3>
<p>
	Correction de l'instruction mode qui ne prenait pas en compte la constante <b>assegai</b>.
</p>

<h3>18-08-2013</h3>
<p>
  <ul>
    <li> Fix d'un bug dans la gestion de la base de données du site web produisant un <span style="color:red;">Error HTTP 500: Sql serveur gone</span> au bout d'un certain
         moment d'inactivité.</li>
    <li> Coloration des lignes au survol de la souris dans les tableaux de la page <a href="/rules/instructions">instructions</a>.</li>
    <li> Ajout d'un loader lors de la compilation et la sauvegarde d'un vaisseau dans les <a href="/pit">stands</a>.</li>
    <li> Ajout de la possibilité d'activer/désactiver l'éditeur de code dans les  <a href="/pit">stands</a>.</li>
    <li> Augmentation de la limite de taille de stockage du code de vaisseau dans la base de données.</li>
  </ul>
</p>


<h3>14-08-2013</h3>
<p>
  Pas mal de bugfix dans la vm :
  <ul>
    <li>Gestion du flag S du processus qui ne fonctionnait tout simplement pas jusque ici.</li>
    <li>Correction de l'instruction Cmpi qui faisait planter le processus de compilation (message "erreur").</li>
    <li>Correction des logs d'exécution de toutes les instructions (beaucoup ne logeaient pas leur nom).</li>
    <li>Correction de l'instruction Add qui était confondue par la VM avec un "and".</li>
    <li>Impression de la valeur des registres dans le log d'exécution des instructions.</li>
    <li>Correction de la syntaxe des instructions asr et rol dans la doc et l'éditeur de code (elles prennent rx, n au lieu de ry, ry).</li>
    <li>Ajout des warnings de dépassement de constante lors de l'assemblage du vaisseau.</li>
  </ul>
</p>
