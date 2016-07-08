<style>
  .op tr td:last-child { text-align:left; padding-left: 15px}
  .opcode tr:nth-child(n+2) td:first-child { text-align:left; padding-left:10px; }
  .img { display:block; margin:0px auto; }
</style>





<h1>La machine virtuelle</h1>


<ul>
  <li>
    <a href="#structure">I. Structure</a>
    <ul>
      <li>
        <a href="#struct_mem">I.1 Le circuit</a>
      </li>
      <li>
        <a href="#struct_proc">I.2 Les processus</a>
        <ul>
          <li> <a href="#struct_registres">I.2.1 Les registres de calcul rx</a></li>
          <li> <a href="#struct_z">I.2.2 Le registre Z</a></li>
          <li> <a href="#struct_s">I.2.3 Le registre S</a></li>
          <li> <a href="#struct_tampon">I.2.4 Le tampon</a></li>
          <li> <a href="#struct_fetch">I.2.5 La file de récupération</a></li>
          <li> <a href="#struct_pc">I.2.6 Le pointeur d'exécution</a></li>
          <li> <a href="#struct_wo">I.2.7 Le compteur de distance</a></li>
          <li> <a href="#struct_mode">I.2.8 Le mode</a></li>
          <li> <a href="#struct_sight">I.2.8 Le rayon d'action</a></li>
        </ul>
      </li>
    </ul>
  </li>

  <li>
    <a href="#init">II. Initialisation</a>
    <ul>
      <li> <a href="#init_mem">II.2 Initialisation du circuit</a></li>
      <li> <a href="#init_proc">II.1 Initialisation des processus</a></li>
    </ul>
  </li>

  <li>
    <a href="#exec">III. Exécution d'un cycle</a>
    <ul>
      <li>
        <a href="#exec_dead">III.1 Conditions de survit</a>
      </li>
      <li>
        <a href="#exec_instr">III.2 Exécution d'une instruction</a>
        <ul>
          <li> <a href="#exec_extraction">III.2.1 Phase d'extraction</a></li>
          <li> <a href="#exec_decodage">III.2.2 Phase de décodage</a></li>
          <li> <a href="#exec_execution">III.2.3 Phase d'exécution</a></li>
        </ul>
      </li>
      <li> <a href="#exec_fork">III.3 Duplications</a> </li>
      <li> <a href="#exec_write">III.4 Écritures simultanées</a> </li>
      <li> <a href="#exec_recap">III.5 Ordre d'exécution global</a> </li>
    </ul>
  </li>

  <li>
    <a href="#rules">IV. Règles complémentaires</a>
    <ul>
      <li>
        <a href="#rules_accel">VI.1 Les plages accélérées</a>
        <ul>
          <li> <a href="#rules_blue">VI.1.1 Les flèches bleue</a></li>
          <li> <a href="#rules_rail">VI.1.2 Le rail</a></li>
        </ul>
      </li>
      <li>
        <a href="#rules_lock">VI.2 Le verrouillage</a>
        <ul>
          <li> <a href="#rules_locked">IV.2.1 Target locked</a></li>
          <li> <a href="#rules_fail">IV.2.1 Échec du verrouillage</a></li>
        </ul>
      </li>
    </ul>
  </li>

  <li> <a href="#exemple">V. Exemple</a> </li>
</ul>






<h2 id="structure">I. Structure</h2>
<p>
  La machine virtuelle est responsable du déroulement de la partie.
  Elle est composée d'une mémoire circulaire qui fait office de piste de course et
  d'une liste de processus qu'elle fait évoluer cycle par cycle.
<p>


<h3 id="struct_mem">I.1 Le circuit</h3>
<p>
  Le circuit est une mémoire circulaire de taille fixe de 65336 quartets. Comme tout circuit qui se
  respecte, il est circulaire. Cela signifie que le quartets suivant le quartet d'adresse 65535 est
  le quartet d'adresse 0. Symétriquement, le quartet précédant le quartet d'adresse 0 est le quartet
  d'adresse 65535.
</p>

<h3 id="struct_proc">I.2 Les processus</h3>

Un processus de la VM travaille toujours sur des quartets. Chaque processus est composé de :
<ul>
  <li>16 registres de calculs de 16 bits chacun notés <b>r0</b> à <b>r15</b></li>
  <li>Un registre de 1 bit noté <b>Z</b></li>
  <li>Un registre de 1 bit noté <b>S</b></li>
  <li>Un tampon d'instructions de 64 quartets</li>
  <li>Une file de récupération</li>
  <li>Un pointeur d'exécution de programme sur 16 bits noté <b>PC</b></li>
  <li>Un compteur de distance sur 32 bits noté <b>W'O''</b></li>
  <li>Un <b>mode</b> de fonctionnement et un rayon d'action associé appelé <b>SIGHT</b></li>
</ul>

<h4 id="struct_registres">I.2.1 Les registres de calcul rx</h4>
<p>
Notés r0 à r15, ces registres de 16 bits à utilisation générale servent à effectuer
des calculs arithmétiques (addition, soustraction, etc.), des calculs logiques
(``ET'', ``OU'', etc.) ou des lectures/écritures sur la mémoire.
</p>


<h4 id="struct_z">I.2.2 Le registre Z</h4>
<p>
  Z est un registre dédié. Il est essentiellement affecté par les instructions de
  calcul. Après un calcul, Z vaut 1 si le résultat est nul, sinon il prend la valeur 0.
  La mise à jour du registre Z est spécifié dans le détail de chaque instruction.
</p>


<h4 id="struct_s">I.2.3 Le registre S</h4>
<p>
  S est un registre dédié. Il est essentiellement affecté par les instructions de
  calcul. Après un calcul, S vaut 1 si le signe du résultat est négatif, sinon il prend
  la valeur 0. La mise à jour du registre S est spécifié dans le détail de chaque instruction.
</p>


<h4 id="struct_tampon">I.2.4 Le tampon</h4>
<p>
  Le tampon est un espace de stockage de donnée de taille fixe de 64 quartets.
  Un processus peut écrire dans son tampon des quartets qu'il lit sur le circuit (instruction <a href="/rules/instructions#ldb">ldb</a>), ou bien
  écrire sur le circuit des quartets lus dans son tampon (instruction <a href="/rules/instructions#stb">stb</a>).
</p>


<h4 id="struct_fetch">I.2.5 La file de récupération</h4>
<p>
  Plus connue sous le nom de fetchqueue, cette file permet au processus de
  stocker les quartets déjà lus de l'instruction en cours de décodage. Elle n'est en aucun cas
  manipulable directement par les instructions mais est indispensable au fonctionnement de la
  VM (et à votre compréhension du déroulement des cycles).
</p>


<h4 id="struct_pc">I.2.6 Le pointeur d'éxécution</h4>
<p>
  Noté PC, ce registre de 16 bits contient l'adresse mémoire de la prochaine
  instruction à exécuter.

  Comme la mémoire est circulaire, lorsque le PC atteint une limite de la mémoire, il cycle.
  Pour un espace mémoire de 1000 quartets, si un PC vaut 990 et que le processus
  saute de 20 quartets en avant, le PC vaudra 10 et non 1010.
  Pour une même taille de mémoire, si un PC vaut 10 et que le processus saute de 20
  quartets en arrière, le PC vaudra 990 et non -10.
</p>


<h4 id="struct_wo">I.2.7 Le compteur de distance</h4>
<p>
  Chaque processus conserve dans un registre W'O'' la distance mémoire parcourue,
  calculée par cumul des déplacements relatifs de son PC (incrémentation
  automatique et sauts); contrairement au pointeur de programme PC, le W'O'' ne
  cycle pas. En outre, contrairement au PC, le W'O'' commence toujours à zéro.
  Pour un espace mémoire de 1000 quartets, si un W'O'' vaut 990 et que le
  processus saute de 20 quartets en avant, le W'O'' vaudra 1010 ; si un W'O''
  vaut 10 et que le processus saute de 20 quartets en arrière, le W'O'' vaudra -10.
  Ce compteur de distance permet, par de simples divisons entières, de connaître
  le nombre de tours parcourus et le nombre d'étapes passées.
</p>


<h4 id="struct_mode">I.2.8 Le mode</h4>
<p>
  Les processus de la machine virtuelle peuvent fonctionner en un certain
  nombre de modes. La seule différence entre les différents modes réside dans
  les temps des instructions et la valeur de SIGHT (voir ci-dessous) qui sont
  différents pour chaque mode. Chaque processus peut passer d'un mode à l'autre
  au moyen de l'instruction <a href="/rules/instructions#mode">mode</a>.
  Chaque mode de fonctionnement est caractérisé par le temps que lui prend
  chaque instruction. Vous pourrez trouver ces temps dans le <a href="/rules/instructions#data">tableau des instructions</a>.
</p>


<h4 id="struct_sight">I.2.8 Le rayon d'action</h4>
<p>
  Le processus fonctionne entièrement en relatif. Chaque accès mémoire ou saut
  se fait d'une certaine distance en avant ou en arrière par
  rapport à l'adresse contenue dans le PC. Toute instruction demandant un accès
  mémoire <b>indique non une valeur absolue, mais un offset par rapport au PC</b>.
  Le processus n'a aucun moyen de sauter à une adresse mémoire constante.
</p>
<p>
  A chaque mode de fonctionnement est associée une valeur, appelée SIGHT,
  qui détermine la distance maximale auquel le processus peut accéder de chaque
  côté de son PC. Ainsi, l'adresse la plus petite accessible pour le processus est PC
  - SIGHT, et la plus haute est PC + SIGHT - 1. Pour le processus, tout
  se passe comme si l'espace de 2 * SIGHT autour de lui était circulaire, donc
  le quartet qui suit PC + SIGHT - 1 est le quartet d'adresse PC - SIGHT.
</p>




<h2 id="init">II. Initialisation</h2>


<h3 id="init_mem">II.1 Initialisation du circuit</h3>
<p>
  L'espace mémoire va être entièrement initialisé à 0x0 et le code des différents
  vaisseaux va être copié en mémoire de manière équitable.
</p>
<p>
  Plus précisément, chaque vaisseau sera placé à l'adresse équivalente à i/n
  ('i' étant le numéro du vaisseau courant, 'n' le nombre total de vaisseaux)
  de la taille de la mémoire. Le PC de chaque processus démarre à l'adresse ainsi calculée, et les vaisseaux
  sont espacés régulièrement.
</p>
<p>
  Si un champion est trop gros pour tenir dans la zone
  qui lui est impartie, la machine refuse de le placer sur la grille de départ : il est
  disqualifié.
</p>

<h3 id="init_proc">II.2 Initialisation des processus</h3>
<p>
  Dans chaque course, plusieurs programmes s'affrontent. Pour chacun de ces programmes
  est créé un processus, dont chaque registre est initialisé à zéro, exceptés les PC,
  qui reçoivent l'adresse du début du programme à exécuter (voir section ci-dessous);
  notez que le W'O'' est initialisé à zéro comme les autres.
  Le tampon est initialisé plein de zéros, et chaque vaisseau commence avec le type feisar.
</p>





<h2 id="exec">III. Exécution d'un cycle</h2>

<p>
</p>


<h3 id="exec_dead">III.1 Conditions de survit</h3>
<p>
  Il s'agit de simuler une course de vitesse. Les processus doivent donc être
  suffisamment rapides et justifier de ce fait. Ainsi, ils doivent prouver au circuit
  périodiquement qu'ils ont suffisamment avancé. Afin de représenter ceci,
  chacun des vaisseaux doit valider un certain nombre de checkpoints, espacés
  régulièrement sur le circuit. Pour cela, ils disposent de l'instruction <a href="/rules/instructions#check">check</a>.
</p>
<%
   from corewar.core.data import const
%>
<p>
  Au démarrage, on considère que chaque processus vient tout juste d'appeler
  l'instruction check pour valider la première zone : il n'a donc pas à le
  refaire pour la zone située entre 0 et ${const.CHECKPOINT_SIZE}. Par la suite, il doit appeler
  cette instruction pendant que son W'O'' se situe entre ${const.CHECKPOINT_SIZE}
  et 2 * ${const.CHECKPOINT_SIZE} afin de valider la deuxième zone.
</p>
<p>
  Tout appel à l'instruction check en dehors de cette zone est ignoré.
  S'il valide au-delà de 2 * ${const.CHECKPOINT_SIZE}, c'est trop loin : la deuxième zone
  n'est pas validée, et le check est ignoré par la machine virtuelle. Si par la suite il
  revient en arrière et valide la deuxième zone, il survivra, mais devra malgré tout valider
  la troisième zone à nouveau.
</p>
<p>
  Bien entendu, un processus dispose d'un certain temps pour valider la zone
  suivante. Ce temps est spécifié en cycles par la valeur ${const.CHECKPOINT_DELAY}.
  Lorsqu'un processus valide une zone, il a de nouveau ${const.CHECKPOINT_DELAY} cycles
  pour valider une nouvelle étape, et ainsi de suite. Tout processus qui n'a pas validé
  l'étape suivante dans le temps imparti est détruit par la VM.
</p>
<p>
  Le premier processus à avoir réalisé ${const.LAPS_NUMBER * const.CHECKPOINTS_PER_LAP}
  checks gagne la course. En cas d'égalité due au parallélisme, les processus sont
  déclarés ex-aequo.
</p>


<h3 id="exec_instr">III.2 Exécution d'une instruction</h3>

L'exécution de chaque instruction se déroule en trois étapes :
<ol>
  <li>la phase d'extraction</li>
  <li>la phase de décodage</li>
  <li>la phase d'exécution</li>
</ol>


<h4 id="exec_extraction">III.2.1 Phase d'extraction</h4>
<p>
  Elle consiste à lire le quartet de mémoire à l'adresse contenue dans le registre PC, en
  avançant le registre PC à raison d'un quartet par cycle après chaque lecture,
  jusqu'à extraire une instruction.
<p>
<p>
  Le quartet lu à chaque cycle va dans la file de récupération. Ainsi, la mémoire peut changer
  pendant la lecture de l'instruction, mais ce qui a déjà été lu est inviolable.
  La file de récupération sera remise à zéro avant la prochaine phase d'extraction afin de ne pas
  influencer la prochaine instruction.
</p>



<h4 id="exec_decodage">III.2.2 Phase de décodage</h4>
<p>
  La phase de délai simule le temps que met un processus réel à décoder une instruction.
  Extérieurement, tout se passe comme s'il ne faisait rien pendant un certain temps.
  La phase de décodage dure un temps fixe qui dépend du mode du processus et de l'instruction
  à décoder. Ce temps est précisé dans le <a href="/rules/instructions#data">tableau des instructions</a>.<br/>
</p>
<p>
  Nous attirons votre attention sur le fait que le délai n'est pas forcément non
  nul. Si le délai de décodage est nul, la phase de décodage dure bien zéro cycles,
  donc au cycle qui suit le dernier cycle de la phase d'extraction le processus est
  bien en phase d'exécution.
</p>


<h4 id="exec_execution">III.2.3 Phase d'exécution</h4>

<p>
  C'est pendant cette phase que le processus met à jour les registres ou les
  quartets de mémoire affectés par l'instruction. L'exécution prend un temps fixe qui dépend de l'instruction. Pendant ce
  délai, l'instruction est exécutée, c'est-à-dire que le processus effectue les opérations,
  et cela lui prend un certain temps.
</p>
<p>
  Le temps d'exécution est fortement dépendant de l'instruction elle-même.
  Par exemple, l'instruction ldr va lire les quartets dans la mémoire à la vitesse
  de n cycles par quartet lu. Consultez la documentation de chaque instruction
  pour savoir comment est utilisé chaque délai d'exécution.
</p>



<h3 id="exec_fork">III.3 Duplications</h3>
<p>
  Un processus peut se dupliquer grâce à l'instruction <a href="/rules/instructions#fork">fork</a>.
  A l'issue d'un fork, un nouveau processus est introduit en course par la machine virtuelle,
  entièrement identique à celui qui a exécuté le fork. La seule différence entre
  les deux est l'état du registre Z qui vaut 1 dans le nouveau processus et 0
  dans son initiateur, ce qui permet de les différencier. En dehors de ceci, ils sont
  complètement indifférenciables.
</p>
<p>
  Si le nombre maximal de processus est atteint, le fork échoue, c'est-à-dire
  qu'aucun nouveau processus n'est crée. Il renvoie 0 dans Z, et ne prend pas
  moins de temps que s'il réussit. Le fork échoue si le nombre total de processus
  créé depuis le départ de la course dépasse 10 000 (dix mille).
</p>


<h3 id="exec_write">III.4 Écritures simultanées</h3>
<p>
  Pour ne pas favoriser de pilote en fonction de l'ordre de traitement des processus
  par la machine virtuelle, elle est tenue se simuler un système entièrement
  parallèle.
  Le problème est simple : que se passe-t-il lorsque plusieurs processus tentent
  d'écrire en mémoire au même endroit, au même moment ?
  La ligue F6100 se doit d'être parfaitement égalitaire pour ses concurrents.
</p>
<p>
  Si plusieurs processus tentent d'écrire au même quartet au même cycle, la machine
  virtuelle considère chaque écriture comme un <b>vote</b>. A la fin du cycle,
  chaque bit du quartet aura la valeur pour laquelle il y a eu le plus de votes. En
  cas d'égalité des votes, le bit n'est pas modifié.
</p>

Exemple :

<pre class="code">
-- Le processus 1 essaie d'écrire :      D (%1101)
-- Le processus 2 essaie d'écrire :      B (%1011)
-- Le processus 3 essaie d'écrire :      1 (%0001)
-------------------------------------------------
-> Au final, le quartet aura la valeur : 9 (%1001)
</pre>

<p>
  Les premier et quatrième bits ont reçu une majorité de votes pour le 1,
  alors que les deuxième et troisième bits ont reçu une majorité de votes pour le 0.
  Si seuls deux processus tentent d'écrire simultanément, l'un la valeur 3 (%0011) et l'autre 5 (%0101),
  le quartet valant à l'origine F (%1111), la valeur résultant est 7 (%0111), puisque les bits ayant
  reçu un vote pour 0 et un vote pour 1 se voient inchangés.
</p>



<h3 id="exec_recap">III.5 Ordre d'exécution global</h3>
  Chaque cycle est résolu par la machine virtuelle en suivant l'ordre est étapes ci-dessous :
<ol>
  <li>test de destruction des processeurs qui n'ont pas passé de checkpoints depuis trop longtemps ;</li>
  <li>exécution du cycle pour chaque processeur (lecture ou délai, ou bien exécution si ce n'est pas ni un accès mémoire, ni un check ni un fork qui sont résolus séparément) ;</li>
  <li>lectures en mémoire ;</li>
  <li>écritures en mémoire, selon le système de parallélisme décrit à la section <a href="#exec_write">III.4 Écritures simultanées</a>;</li>
  <li>résolution des fork ;</li>
  <li>résolution des check.</li>
</ol>
<p>
  On remarquera que les lectures ont lieu avant les écritures et que la résolution
  des check a lieu après lecture des compteurs. Naturellement, le premier cycle
  qu'exécutera la machine sera le cycle 0, et il sera incrémenté entre deux cycles.
</p>






<h2 id="rules">IV. Règles complémentaires</h2>

<h3 id="rules_accel">VI.1 Les plages accélérées</h3>
<p>
  Certains emplacements mémoire peuvent avoir un effet bénéfique sur la vitesse d'un processus.
  On distingue deux caractéristiques vérifiant ce principe :
  <ul>
    <li>les <b>flèches bleues</b></li>
    <li>le <b>rail</b></li>
  </ul>
</p>

<h4 id="rules_blue">VI.1.1 Les flèches bleue</h4>
<p>
  Toute instruction qui se trouve à une adresse multiple de ${const.BLUE_ARROW_SPACING}
  ne prend que la moitié du temps réglementaire. Ainsi, un fork se trouvant à l'adresse
  absolue ${3*const.BLUE_ARROW_SPACING} prendra deux fois moins
  de temps qu'habituellement pour s'exécuter. Le temps de décodage et le temps
  d'exécution sont à diviser par deux tous les deux, arrondis au cycle inférieur.
</p>
<p>
  Les arrondis sont calculés en divisions entières, c'est à dire qu'une instruction qui
  métrerait normalement 1 cycle à décoder, sur une flèche bleue, cette instruction n'aura pas
  de délai de décodage et passera directement en phase d'exécution.
</p>


<h4 id="rules_rail">VI.1.2 Le rail</h4>
<p>
  Pour un processus donné, s'il y a eu une écriture à la valeur du PC au cycle
  précédent la lecture de l'opcode, le programme prend le rail, c'est-à-dire que
  le temps de l'instruction qu'exécute le processus qui l'exécute sont divisés par
  deux (division entière, arrondi inférieur). Cela concerne le temps de décodage
  comme le temps d'exécution.
  Pour les instructions dont l'opcode est sur deux quartets, il suffit qu'il y ait eu une écriture
  au cycle précédant la lecture de n'importe lequel des deux ; ce n'est cependant pas cumulatif.
</p>
<p>
  Par exemple, si le processus 1 écrit à l'adresse n au cycle 10, et qu'au cycle
  11 le processus 2 lit un opcode, alors les temps de l'instruction du processus 2
  seront deux fois moindres que la normale. Notez que ces deux processus peuvent tout à
  fait appartenir au même joueur ;)
</p>


<h3 id="rules_lock">VI.2 Le vérouillage</h3>
<p>
  Comme vous l'avez déjà compris, pour vaincre ses adversaires, le moyen le
  plus simple est de les surclasser en termes de vitesse. Mais il est aussi possible
  de s'en débarrasser, c'est-à-dire de s'arranger pour qu'ils exécutent l'instruction
  crash. C'est la guerre après tout !
</p>
<p>
  Ainsi, les vaisseaux sont capables de verrouiller le vaisseau qui les précède
  immédiatement en mémoire. Au moment où l'instruction <a href="/rules/instructions#mode">mode</a>
  est exécutée, la machine virtuelle détermine le vaisseau qui précède immédiatement celui qui
  exécute l'instruction mode.
</p>
<p>
  Par la suite, il sera possible au vaisseau de demander, via l'appel <a href="/rules/instructions#stat">stat</a>,
  la position relative du vaisseau verrouillé. Le vaisseau verrouillé ne change pas tant que le processeur
  n'exécute pas l'instruction mode et que la cible est vivante. Une fois que la cible est verrouillée,
  à vous les missiles à tête chercheuse.
</p>


<h4 id="rules_locked">IV.2.1 Target locked</h4>
<p>
  L'appel stat, avec le paramètre 13, permet de connaître la position relative
  du vaisseau verrouillé. Il retourne dans le registre spécifié la différence entre
  le PC du vaisseau qui l'exécute et le PC de sa cible. Naturellement, comme la
  mémoire est circulaire, cette distance a deux valeurs possibles : une positive et
  une négative. stat 13 retournera celle dont la valeur absolue est la plus petite.
  Avec le paramètre 14, l'appel stat retourne le mode du processeur verrouillé.
</p>
<p>
  Autrement dit, on vous dit dans quel sens il faut aller pour faire le moins de chemin
  possible : s'il est tout près devant, on aura une valeur positive, s'il est tout près derrière, une
  valeur négative. Au cas ou c'est pareil, on prend la valeur positive. Attention, on retourne
  la distance dont la valeur absolue est la plus petite, on ne retourne pas la plus petite valeur
  absolue. Autrement dit, si les valeurs sont -50 et +25, on retourne +25, mais si c'est -25 et
  +50, on retourne -25 et non +25.
</p>

<h4 id="rules_fail">IV.2.1 Échec du verrouillage</h4>
<p>
  Dans certains cas, le verrouillage peut échouer. C'est le cas si le vaisseau
  qui change de mode est seul sur la piste. C'est le cas aussi si au moment du
  changement de mode, deux processeurs ont leur PC à la même adresse, rendant
  impossible le choix entre l'un et l'autre. Dans ce cas, le verrouillage échoue,
  et stat 13 et stat 14 renverront 0. Bien sûr on peut verrouiller un nouveau
  vaisseau en exécutant l'instruction mode, y compris si c'est pour rester dans le
  même mode. Attention toutefois au délai !
  Dans le cas où la cible s'est crashée depuis le verrouillage, stat 13 et stat
  14 renverront 0.
</p>



<h2 id="exemple">V. Exemple</h2>
<p>

Dans cette section, on va détaillé les étapes d'exécution du vaisseau zorg, présenté
dans la section <a href="/rules/language#exemple">IV.3 Exemple : Vaisseau complet</a>
de la page de description du langage F6100.

<pre class="code">
.name "Zork"
.comment "This is the first ship ever."

  ll r0, 0x2ecf       # Load simple code
  ll r1, 0x13e0       #   into two registers
  ll r2, to -from1    # Load offsets for
  ll r3, to -from2 +4 #   the two str
  str [r2], r0        # Write code just
from1:
  str [r3], r1        # before PC
from2:
to:                   # When the PC reaches here , a `check '
                      # instruction has been written
</pre>


<p>
  Ci-dessous, le log d'éxécution du vaisseau zork sur la VM avec quelques éxplications
  ce ce qu'il se passe.
</p>

<pre class="code">
[init]           adding ship #0: ../ships/zorg.s
[init]           initializing machine
  # Pendant la phase d'initialisation, la mémoire est initialisée avec des quartets à %0000,
  # un processus est crée, tous ses attributs sont initialisés à 0 (registres, tampon...etc).

[init]           ship #0 start pos is 0
[init]           dumping ship initial code
[init]           chunk #0 : wrote=(-1), data=[1,1,1,1], votes=()
[init]           chunk #1 : wrote=(-1), data=[0,0,1,1], votes=()
[init]           chunk #2 : wrote=(-1), data=[0,0,0,0], votes=()
[init]           chunk #3 : wrote=(-1), data=[1,1,1,1], votes=()
[init]           chunk #4 : wrote=(-1), data=[1,1,0,0], votes=()
[init]           chunk #5 : wrote=(-1), data=[1,1,1,0], votes=()
[init]           chunk #6 : wrote=(-1), data=[0,0,1,0], votes=()
[init]           chunk #7 : wrote=(-1), data=[1,1,1,1], votes=()
[init]           chunk #8 : wrote=(-1), data=[0,0,1,1], votes=()
[init]           chunk #9 : wrote=(-1), data=[0,0,0,1], votes=()
[init]           chunk #10 : wrote=(-1), data=[0,0,0,0], votes=()
[init]           chunk #11 : wrote=(-1), data=[1,1,1,0], votes=()
[init]           chunk #12 : wrote=(-1), data=[0,0,1,1], votes=()
[init]           chunk #13 : wrote=(-1), data=[0,0,0,1], votes=()
[init]           chunk #14 : wrote=(-1), data=[1,1,1,1], votes=()
[init]           chunk #15 : wrote=(-1), data=[0,0,1,1], votes=()
[init]           chunk #16 : wrote=(-1), data=[0,0,1,0], votes=()
[init]           chunk #17 : wrote=(-1), data=[0,0,1,1], votes=()
[init]           chunk #18 : wrote=(-1), data=[0,0,0,0], votes=()
[init]           chunk #19 : wrote=(-1), data=[0,0,0,0], votes=()
[init]           chunk #20 : wrote=(-1), data=[0,0,0,0], votes=()
[init]           chunk #21 : wrote=(-1), data=[1,1,1,1], votes=()
[init]           chunk #22 : wrote=(-1), data=[0,0,1,1], votes=()
[init]           chunk #23 : wrote=(-1), data=[0,0,1,1], votes=()
[init]           chunk #24 : wrote=(-1), data=[0,1,0,0], votes=()
[init]           chunk #25 : wrote=(-1), data=[0,0,0,0], votes=()
[init]           chunk #26 : wrote=(-1), data=[0,0,0,0], votes=()
[init]           chunk #27 : wrote=(-1), data=[0,0,0,0], votes=()
[init]           chunk #28 : wrote=(-1), data=[1,1,1,0], votes=()
[init]           chunk #29 : wrote=(-1), data=[0,0,1,0], votes=()
[init]           chunk #30 : wrote=(-1), data=[0,0,0,0], votes=()
[init]           chunk #31 : wrote=(-1), data=[1,1,1,0], votes=()
[init]           chunk #32 : wrote=(-1), data=[0,0,1,1], votes=()
[init]           chunk #33 : wrote=(-1), data=[0,0,0,1], votes=()
  # Ensuite, le PC du processus est calculé : seul sur la piste, il prend la valeur 0.
  # Et le code d'initialisation du processus est placé à partir du PC.
  # On se souvient que le code binaire du vaisseau zork était : F3 0F CE 2F 31 0E 31 F3 23 00 0F 33 40 00 E2 0E 31

[run]            starting race
[run]            begin cycle #0
[resolve ships]  processing ship #0 (pc = 0, wo = 0)
[resolve ships]    reading : chunk #0 : wrote=(-1), data=[1,1,1,1], votes=()
  # On commence l'exécution du processus #0. Là, la fetchqueue est vide, on est donc dans une
  # phase d'extraction. On lit le quartet #0 du circuit et on le place dans la fetchqueue.


[run]            begin cycle #1
[resolve ships]  processing ship #0 (pc = 1, wo = 1)
[resolve ships]    reading : chunk #1 : wrote=(-1), data=[0,0,1,1], votes=()
  # Au cycle suivant, la même chose. La fetchqueue n'est pas vide mais l'optcode lu (%1111)
  # indique qu'il faut lire un autre quartet pour décoder la mnémonique de l'instruction. On
  # reste donc en phase d'extraction.

[run]            begin cycle #2
[resolve ships]  processing ship #0 (pc = 2, wo = 2)
[resolve ships]    reading : chunk #2 : wrote=(-1), data=[0,0,0,0], votes=()
  # Au début du cycle #2, la fetchqueue permet de décoder la mnémonique : il s'agit de l'opcode de l'instruction ll.
  # Par définition, cette instruction prend 2 arguments respectivement codés sur 1 et 4 quartets. Il faut
  # lire encore 5 quartets pour avoir l'instruction complète. On reste donc en phase de décodage.
  # Ainsi de suite jusqu'au cycle #6.


[run]            begin cycle #3
[resolve ships]  processing ship #0 (pc = 3, wo = 3)
[resolve ships]    reading : chunk #3 : wrote=(-1), data=[1,1,1,1], votes=()
[run]            begin cycle #4
[resolve ships]  processing ship #0 (pc = 4, wo = 4)
[resolve ships]    reading : chunk #4 : wrote=(-1), data=[1,1,0,0], votes=()
[run]            begin cycle #5
[resolve ships]  processing ship #0 (pc = 5, wo = 5)
[resolve ships]    reading : chunk #5 : wrote=(-1), data=[1,1,1,0], votes=()
[run]            begin cycle #6
[resolve ships]  processing ship #0 (pc = 6, wo = 6)
[resolve ships]    reading : chunk #6 : wrote=(-1), data=[0,0,1,0], votes=()
[resolve ships]    fecthed : ll r0, [1,1,1,1][1,1,0,0][1,1,1,0][0,0,1,0](11983) : blue = True, rail = False
  # Au cycle #6, on a extrait tous les quartets de l'instruction ll, ses arguments sont décodés
  # et le processus passe en phase de décodage. La durée de décodage de l'instruction ll en mode feisar (mode
  # par défaut) est de 3. Cependant, comme l'un des deux optcode de cette instruction à été lu sur
  # une adresse multiple de 64, on est sur une "flèche bleue". A ce titre, le temps de décodage
  # de l'instruction est divisé par 2 (division entière). On part donc pour 3/2=1 cycle de décodage.

[run]            begin cycle #7
[resolve ships]  processing ship #0 (pc = 7, wo = 7)
[resolve ships]    decoding wait : 1
[resolve ships]    decode
  # Le vaisseau est en phase de décodage pour une durée de 1 cycle, on décode (on décrémente le
  # compteur d'attente. Le compteur est à 0, le vaisseau passe donc en phase d'exécution.
  # Le délai d'exécution est de 4 cycle pour cette instruction dans ce mode. L'instruction ayant
  # été lue sur une flèche bleue, ce temps est divisé par deux. On par pour 2 cycles de temps
  # d'exécution.

[run]            begin cycle #8
[resolve ships]  processing ship #0 (pc = 7, wo = 7)
[resolve ships]    executing wait : 2
  # Le vaisseau est en phase d'exécution, le délai est non-null, on décrémente le délai.

[run]            begin cycle #9
[resolve ships]  processing ship #0 (pc = 7, wo = 7)
[resolve ships]    executing wait : 1
[resolve ships]    execute
  # Le vaisseau est en phase d'exécution, on décrémente le délai, il devient nul, on exécute effectivement l'instruction.
  # A la fin de ce cycle, le registre r0 du processus #0 contient la constante [1,1,1,1][1,1,0,0][1,1,1,0][0,0,1,0]
  # Le vaisseau repasse en phase d'extraction en quête d'une nouvelle instruction et sa fetchque est vidée.

[run]            begin cycle #10
[resolve ships]  processing ship #0 (pc = 7, wo = 7)
[resolve ships]    reading : chunk #7 : wrote=(-1), data=[1,1,1,1], votes=()
[run]            begin cycle #11
[resolve ships]  processing ship #0 (pc = 8, wo = 8)
[resolve ships]    reading : chunk #8 : wrote=(-1), data=[0,0,1,1], votes=()
[run]            begin cycle #12
[resolve ships]  processing ship #0 (pc = 9, wo = 9)
[resolve ships]    reading : chunk #9 : wrote=(-1), data=[0,0,0,1], votes=()
[run]            begin cycle #13
[resolve ships]  processing ship #0 (pc = 10, wo = 10)
[resolve ships]    reading : chunk #10 : wrote=(-1), data=[0,0,0,0], votes=()
[run]            begin cycle #14
[resolve ships]  processing ship #0 (pc = 11, wo = 11)
[resolve ships]    reading : chunk #11 : wrote=(-1), data=[1,1,1,0], votes=()
[run]            begin cycle #15
[resolve ships]  processing ship #0 (pc = 12, wo = 12)
[resolve ships]    reading : chunk #12 : wrote=(-1), data=[0,0,1,1], votes=()
[run]            begin cycle #16
[resolve ships]  processing ship #0 (pc = 13, wo = 13)
[resolve ships]    reading : chunk #13 : wrote=(-1), data=[0,0,0,1], votes=()
[resolve ships]    fecthed : ll r1, [0,0,0,0][1,1,1,0][0,0,1,1][0,0,0,1](5088) : blue = False, rail = False
  # Même chose jusqu'à avoir lu assez de quartets pour décoder une nouvelle instruction.
  # On passe en phase de décodage mais cette fois on est pas sur une flèche bleue.
  # Rendez vous au cycle 23

[run]            begin cycle #17
[resolve ships]  processing ship #0 (pc = 14, wo = 14)
[resolve ships]    decoding wait : 3
[run]            begin cycle #18
[resolve ships]  processing ship #0 (pc = 14, wo = 14)
[resolve ships]    decoding wait : 2
[run]            begin cycle #19
[resolve ships]  processing ship #0 (pc = 14, wo = 14)
[resolve ships]    decoding wait : 1
[resolve ships]    decode
[run]            begin cycle #20
[resolve ships]  processing ship #0 (pc = 14, wo = 14)
[resolve ships]    executing wait : 4
[run]            begin cycle #21
[resolve ships]  processing ship #0 (pc = 14, wo = 14)
[resolve ships]    executing wait : 3
[run]            begin cycle #22
[resolve ships]  processing ship #0 (pc = 14, wo = 14)
[resolve ships]    executing wait : 2
[run]            begin cycle #23
[resolve ships]  processing ship #0 (pc = 14, wo = 14)
[resolve ships]    executing wait : 1
[resolve ships]    execute
  # A la fin de ce cycle, le registre r1 du processus #0 contient la constante [0,0,0,0][1,1,1,0][0,0,1,1][0,0,0,1]
  # Rendez vous à l'exécution de la première instruction str au cycle 56

[run]            begin cycle #24
[resolve ships]  processing ship #0 (pc = 14, wo = 14)
[resolve ships]    reading : chunk #14 : wrote=(-1), data=[1,1,1,1], votes=()
[run]            begin cycle #25
[resolve ships]  processing ship #0 (pc = 15, wo = 15)
[resolve ships]    reading : chunk #15 : wrote=(-1), data=[0,0,1,1], votes=()
[run]            begin cycle #26
[resolve ships]  processing ship #0 (pc = 16, wo = 16)
[resolve ships]    reading : chunk #16 : wrote=(-1), data=[0,0,1,0], votes=()
[run]            begin cycle #27
[resolve ships]  processing ship #0 (pc = 17, wo = 17)
[resolve ships]    reading : chunk #17 : wrote=(-1), data=[0,0,1,1], votes=()
[run]            begin cycle #28
[resolve ships]  processing ship #0 (pc = 18, wo = 18)
[resolve ships]    reading : chunk #18 : wrote=(-1), data=[0,0,0,0], votes=()
[run]            begin cycle #29
[resolve ships]  processing ship #0 (pc = 19, wo = 19)
[resolve ships]    reading : chunk #19 : wrote=(-1), data=[0,0,0,0], votes=()
[run]            begin cycle #30
[resolve ships]  processing ship #0 (pc = 20, wo = 20)
[resolve ships]    reading : chunk #20 : wrote=(-1), data=[0,0,0,0], votes=()
[resolve ships]    fecthed : ll r2, [0,0,1,1][0,0,0,0][0,0,0,0][0,0,0,0](3) : blue = False, rail = False
[run]            begin cycle #31
[resolve ships]  processing ship #0 (pc = 21, wo = 21)
[resolve ships]    decoding wait : 3
[run]            begin cycle #32
[resolve ships]  processing ship #0 (pc = 21, wo = 21)
[resolve ships]    decoding wait : 2
[run]            begin cycle #33
[resolve ships]  processing ship #0 (pc = 21, wo = 21)
[resolve ships]    decoding wait : 1
[resolve ships]    decode
[run]            begin cycle #34
[resolve ships]  processing ship #0 (pc = 21, wo = 21)
[resolve ships]    executing wait : 4
[run]            begin cycle #35
[resolve ships]  processing ship #0 (pc = 21, wo = 21)
[resolve ships]    executing wait : 3
[run]            begin cycle #36
[resolve ships]  processing ship #0 (pc = 21, wo = 21)
[resolve ships]    executing wait : 2
[run]            begin cycle #37
[resolve ships]  processing ship #0 (pc = 21, wo = 21)
[resolve ships]    executing wait : 1
[resolve ships]    execute
[run]            begin cycle #38
[resolve ships]  processing ship #0 (pc = 21, wo = 21)
[resolve ships]    reading : chunk #21 : wrote=(-1), data=[1,1,1,1], votes=()
[run]            begin cycle #39
[resolve ships]  processing ship #0 (pc = 22, wo = 22)
[resolve ships]    reading : chunk #22 : wrote=(-1), data=[0,0,1,1], votes=()
[run]            begin cycle #40
[resolve ships]  processing ship #0 (pc = 23, wo = 23)
[resolve ships]    reading : chunk #23 : wrote=(-1), data=[0,0,1,1], votes=()
[run]            begin cycle #41
[resolve ships]  processing ship #0 (pc = 24, wo = 24)
[resolve ships]    reading : chunk #24 : wrote=(-1), data=[0,1,0,0], votes=()
[run]            begin cycle #42
[resolve ships]  processing ship #0 (pc = 25, wo = 25)
[resolve ships]    reading : chunk #25 : wrote=(-1), data=[0,0,0,0], votes=()
[run]            begin cycle #43
[resolve ships]  processing ship #0 (pc = 26, wo = 26)
[resolve ships]    reading : chunk #26 : wrote=(-1), data=[0,0,0,0], votes=()
[run]            begin cycle #44
[resolve ships]  processing ship #0 (pc = 27, wo = 27)
[resolve ships]    reading : chunk #27 : wrote=(-1), data=[0,0,0,0], votes=()
[resolve ships]    fecthed : ll r3, [0,1,0,0][0,0,0,0][0,0,0,0][0,0,0,0](4) : blue = False, rail = False
[run]            begin cycle #45
[resolve ships]  processing ship #0 (pc = 28, wo = 28)
[resolve ships]    decoding wait : 3
[run]            begin cycle #46
[resolve ships]  processing ship #0 (pc = 28, wo = 28)
[resolve ships]    decoding wait : 2
[run]            begin cycle #47
[resolve ships]  processing ship #0 (pc = 28, wo = 28)
[resolve ships]    decoding wait : 1
[resolve ships]    decode
[run]            begin cycle #48
[resolve ships]  processing ship #0 (pc = 28, wo = 28)
[resolve ships]    executing wait : 4
[run]            begin cycle #49
[resolve ships]  processing ship #0 (pc = 28, wo = 28)
[resolve ships]    executing wait : 3
[run]            begin cycle #50
[resolve ships]  processing ship #0 (pc = 28, wo = 28)
[resolve ships]    executing wait : 2
[run]            begin cycle #51
[resolve ships]  processing ship #0 (pc = 28, wo = 28)
[resolve ships]    executing wait : 1
[resolve ships]    execute
[run]            begin cycle #52
[resolve ships]  processing ship #0 (pc = 28, wo = 28)
[resolve ships]    reading : chunk #28 : wrote=(-1), data=[1,1,1,0], votes=()
[run]            begin cycle #53
[resolve ships]  processing ship #0 (pc = 29, wo = 29)
[resolve ships]    reading : chunk #29 : wrote=(-1), data=[0,0,1,0], votes=()
[run]            begin cycle #54
[resolve ships]  processing ship #0 (pc = 30, wo = 30)
[resolve ships]    reading : chunk #30 : wrote=(-1), data=[0,0,0,0], votes=()
[resolve ships]    fecthed : str [r2], r0 -> str (11983) ([0,0,0,0],[1,1,1,0],[0,0,1,1],[0,0,0,1])
[run]            begin cycle #55
[resolve ships]  processing ship #0 (pc = 31, wo = 31)
[resolve ships]    decoding wait : 2
[run]            begin cycle #56
[resolve ships]  processing ship #0 (pc = 31, wo = 31)
[resolve ships]    decoding wait : 1
[resolve ships]    decode
  # A ce stade, la première instruction str a été lue et finie de décodé. Le vaisseau
  # passe en phase d'exécution. L'instruction stipule que le temps d'exécution
  # est en fonction du nombre de quartets à écrire (ici 4 quartets).
  # On part donc pour une attente d'exécution de 2 cycle entre chaque écritures.

[run]            begin cycle #57
[resolve ships]  processing ship #0 (pc = 31, wo = 31)
[resolve ships]    executing wait : 2
[run]            begin cycle #58
[resolve ships]  processing ship #0 (pc = 31, wo = 31)
[resolve ships]    executing wait : 1
[resolve ships]    execute
[resolve writes] chunk : chunk #34 : wrote=(-1), data=[0,0,0,0], votes=([1,1,1,1])
  # Ca y est, le premier a été écrit. La valeur [1,1,1,1] a été écrit dans l'adresse #34
  # On remarque la phase [resolve writes]. En réalité, l'exécution de l'instruction
  # n'a pas directement écrit sur la mémoire mais à seulement crée un vote.
  # A la fin de chaque cycle, les votes sont résolus et la mémoire est modifiée en conséquence.
  # Après l'écriture, on repart pour une attente d'exécution.

[run]            begin cycle #59
[resolve ships]  processing ship #0 (pc = 31, wo = 31)
[resolve ships]    executing wait : 2
[run]            begin cycle #60
[resolve ships]  processing ship #0 (pc = 31, wo = 31)
[resolve ships]    executing wait : 1
[resolve ships]    execute
[resolve writes] chunk : chunk #35 : wrote=(-1), data=[0,0,0,0], votes=([1,1,0,0])
  # Le second quartet a été écrit. La valeur [1,1,0,0] a été écrit dans l'adresse #35

[run]            begin cycle #61
[resolve ships]  processing ship #0 (pc = 31, wo = 31)
[resolve ships]    executing wait : 2
[run]            begin cycle #62
[resolve ships]  processing ship #0 (pc = 31, wo = 31)
[resolve ships]    executing wait : 1
[resolve ships]    execute
[resolve writes] chunk : chunk #36 : wrote=(-1), data=[0,0,0,0], votes=([1,1,1,0])
  # Le troisième quartet a été écrit. La valeur [1,1,1,0] a été écrit dans l'adresse #36

[run]            begin cycle #63
[resolve ships]  processing ship #0 (pc = 31, wo = 31)
[resolve ships]    executing wait : 2
[run]            begin cycle #64
[resolve ships]  processing ship #0 (pc = 31, wo = 31)
[resolve ships]    executing wait : 1
[resolve ships]    execute
[resolve writes] chunk : chunk #37 : wrote=(-1), data=[0,0,0,0], votes=([0,0,1,0])
  # Le troisième quartet a été écrit. La valeur [0,0,1,0] a été écrit dans l'adresse #37
  # L'exécution de l'instruction str est terminée, on repasse en phase d'extraction.
  # Rendez-vous au cycle 77

[run]            begin cycle #65
[resolve ships]  processing ship #0 (pc = 31, wo = 31)
[resolve ships]    reading : chunk #31 : wrote=(-1), data=[1,1,1,0], votes=()
[run]            begin cycle #66
[resolve ships]  processing ship #0 (pc = 32, wo = 32)
[resolve ships]    reading : chunk #32 : wrote=(-1), data=[0,0,1,1], votes=()
[run]            begin cycle #67
[resolve ships]  processing ship #0 (pc = 33, wo = 33)
[resolve ships]    reading : chunk #33 : wrote=(-1), data=[0,0,0,1], votes=()
[resolve ships]    fecthed : str [r3], r1 -> str (11983) ([0,0,0,0],[1,1,1,0],[0,0,1,1],[0,0,0,1])
[run]            begin cycle #68
[resolve ships]  processing ship #0 (pc = 34, wo = 34)
[resolve ships]    decoding wait : 2
[run]            begin cycle #69
[resolve ships]  processing ship #0 (pc = 34, wo = 34)
[resolve ships]    decoding wait : 1
[resolve ships]    decode
[run]            begin cycle #70
[resolve ships]  processing ship #0 (pc = 34, wo = 34)
[resolve ships]    executing wait : 2
[run]            begin cycle #71
[resolve ships]  processing ship #0 (pc = 34, wo = 34)
[resolve ships]    executing wait : 1
[resolve ships]    execute
[resolve writes] chunk : chunk #38 : wrote=(-1), data=[0,0,0,0], votes=([0,0,0,0])
[run]            begin cycle #72
[resolve ships]  processing ship #0 (pc = 34, wo = 34)
[resolve ships]    executing wait : 2
[run]            begin cycle #73
[resolve ships]  processing ship #0 (pc = 34, wo = 34)
[resolve ships]    executing wait : 1
[resolve ships]    execute
[resolve writes] chunk : chunk #39 : wrote=(-1), data=[0,0,0,0], votes=([1,1,1,0])
[run]            begin cycle #74
[resolve ships]  processing ship #0 (pc = 34, wo = 34)
[resolve ships]    executing wait : 2
[run]            begin cycle #75
[resolve ships]  processing ship #0 (pc = 34, wo = 34)
[resolve ships]    executing wait : 1
[resolve ships]    execute
[resolve writes] chunk : chunk #40 : wrote=(-1), data=[0,0,0,0], votes=([0,0,1,1])
[run]            begin cycle #76
[resolve ships]  processing ship #0 (pc = 34, wo = 34)
[resolve ships]    executing wait : 2
[run]            begin cycle #77
[resolve ships]  processing ship #0 (pc = 34, wo = 34)
[resolve ships]    executing wait : 1
[resolve ships]    execute
[resolve writes] chunk : chunk #41 : wrote=(-1), data=[0,0,0,0], votes=([0,0,0,1])
  # Ici, l'éxécution de la deuxième instruction str est terminée. Les valeurs suivantes ont
  # été écrites sur le circuit :
  # [0,0,0,0] en #38
  # [1,1,1,0] en #39
  # [0,0,1,1] en #40
  # [0,0,0,1] en #41
  # Ce qui est intéressant, c'est la valeur du PC. A force de lire des instructions, le pointeur
  # d'exécution arrive maintenant à la valeur #34. Soit le premier quartet de mémoire qui n'ait pas
  # été initialisé avec le code du vaisseau pendant la phase d'init.
  # Si on avait rien fait, le prochain quartet lu serait [0,0,0,0] (valeur par défaut de la mémoire)
  # qui code pour l'instruction crash.
  # Fort heureusement, l'instruction str exécutée plus haut à écrasé cette valeur en mémoire avec le
  # contenu du registre r0, lui même initialise avec la première instruction ll.
  # Mais que va-t-on lire alors ? :)

[run]            begin cycle #78
[resolve ships]  processing ship #0 (pc = 34, wo = 34)
[resolve ships]    reading : chunk #34 : wrote=(58), data=[1,1,1,1], votes=()
[run]            begin cycle #79
[resolve ships]  processing ship #0 (pc = 35, wo = 35)
[resolve ships]    reading : chunk #35 : wrote=(60), data=[1,1,0,0], votes=()
[resolve ships]    fecthed : check : blue = False, rail = False
  # Et oui ! La valeur du registre savamment chargé contenait les quartets [1,1,1,1][1,1,0,0]
  # qui codent pour l'instruction check.
  # Bon, le fait est que le PC est à la position 35, soit toujours dans la première des 8 sections
  # composant un tour de mémoire. L'instruction ne servira donc à rien puisque cette section
  # est validée au démarrage.
  #
  # Plus intéressant :
  # A elles deux, les instructions str ont écrit 8 quartets sur la mémoire, nous n'en avons lu que deux.
  # Que contiennent les autres ? Je vous le donne dans le mille : les deux mêmes instructions str.
  # On comprend donc le principe de fonctionnement de zork : écrire juste devant lui 8 quartets. Deux d'entre
  # eux codent pour un check, et les six autres codent pour l'écriture des 8 quartets. En procédant
  # ainsi de suite, le PC de zork va avancer case par case jusqu'à la fin.
  #
  # En réalité, ce vaisseau ne termine pas la course. Ci-dessous les dernières lignes de log. Commencer
  # par comprendre pourquoi le processus à été éliminé. Quand vous aurez trouvé, faire votre tout premier
  # vaisseau en modifiant celui de zork, c'est un excellent moyen de commencer votre carrière de pilote !

...
...
[run]            begin cycle #33552
[resolve deads]  ship #0 last cycle (0) ******************* killing
[resolve ships]  processing ship #0 (pc = 6122, wo = 6122)
[resolve ships]    decoding wait : 2
[run]            begin cycle #33553
[resolve wins]   no more running ships, stopping race
[run]            finishing race
+--------------------------------------------------------------+
|    name :  Zork                                              |
|  status : Dead                                               |
| comment :  This is the first ship ever.                      |
| ship id : #0                                                 |
|  cycles : 33553                                              |
|    mode : Feisar                                             |
|      pc : 6122                                               |
|      wo : 6122                                               |
+--------------------------------------------------------------+
</pre>

