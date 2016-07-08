<style>
  .op tr td:last-child { text-align:left; padding-left: 15px}
  .opcode tr:nth-child(n+2) td:first-child { text-align:left; padding-left:10px; }
  .img { display:block; margin:0px auto; }
</style>

<h1>Language F6100</h1>
<p>
  Pour représenter ces instructions, le langage bénéficie d'une syntaxe relativement simple présentée ici.
</p>
<ul>
  <li><a href="#sep">I. Séparateur et commentaires</a></li>
  <li>
    <a href="#instructions">II. Instructions</a>
    <ul>
      <li><a href="#mnemonique">II.1 Mnémonique</a></li>
      <li>
        <a href="#arguments">II.2 Arguments</a>
        <ul>
          <li><a href="#registres">     II.2.1 Type : registres</a></li>
          <li><a href="#register_deref">II.2.2 Type : registres déréférencés</a></li>
          <li><a href="#mode">          II.2.3 Type : mode</a></li>
          <li><a href="#const">         II.2.4 Type : constante</a></li>

        </ul>
      </li>
    </ul>
  </li>
  <li><a href="#directives">III. Directives</a></li>
  <li>
    <a href="#binaire">IV. Représentation binaire</a>
    <ul>
      <li><a href="#binaire_mnemonique">IV.1 Mnémoniques</a></li>
      <li>
        <a href="#binaire_arguments"> IV.2 Arguments</a>
        <ul>
          <li><a href="#binaire_constantes">IV.2.3 Constantes</a></li>
          <li><a href="#binaire_modes">IV.2.2 Modes</a></li>
          <li><a href="#binaire_registres"> IV.2.1 Registres</a></li>
        </ul>
      </li>
      <li> <a href="#exemple">IV.3 Exemple complet</a>  </li>
    </ul>
  </li>
</ul>



<h2 id="sep">I. Séparateur et commentaires</h2>
<p>
Pour qu'un vaisseau soit assemblable, les différents éléments qui le composent
doivent être séparés par des séparateurs. Un séparateur sera juste un groupe
de caractères formé d'espaces, de '\t', de '\r' et de '\n'. Cela signifie qu'il peut
y avoir une instruction étalée sur plusieurs lignes, ou plusieurs instructions sur
une ligne.
</p>
<p>
  L'assembleur supporte les commentaires. Le caractère '#' marque le début
  d'un commentaire, et celui-ci se terminera à la fin de la ligne ('\n' suivant).
  Tous les caractères appartenant à un commentaire sont ignorés par l'assembleur.
</p>
Exemple :
<pre class="code">
mov r0 , r1 # Ceci est un commentaire
</pre>




<h2 id="instructions">II. Instructions</h2>
<p>
Les instructions sont le coeur de métier de l'assembleur. Une instruction est
composée d'exactement une <a href="#mnemonique">mnémonique</a> et éventuellement d'un ou plusieurs
arguments, séparés par des virgules.
</p>
Exemple :
<pre class="code">
mov r0 , r1   # Opcode mov , argument r0 , argument r1
mov , r0 , r1 # Erreur de syntaxe
mov r0 r1     # Erreur de syntaxe , pas de virgule
mov , r0 r1   # Erreur de syntaxe
mov r0 , , r1 # Erreur de syntaxe
</pre>



<h3 id="mnemonique">II.1 Mnémonique</h3>
<p>
La mnémonique identifie l'instruction. Dans sa représentation textuelle, la mnémonique
est le "nom" de l'instruction - par exemple "mov" ou "add".
C'est elle qui renseigne l'assembleur sur le nombre et le type des arguments de l'instruction.
</p>
Exemple
<pre class="code">
mov r0, r1, r2 # Erreur. Syntaxiquement correct, mais mov ne prend que 2 paramètres
mov 3, 5       # Erreur. Syntaxiquement correct, mais mov prend des paramètres de types registre
mov r0, r1     # Correct
</pre>



<h3 id="arguments">II.2 Arguments</h3>
<h4 id="registres">II.2.1 Type : registres</h4>
<p>
Les registres sont nommés r0 à r15.
</p>



<h4 id="register_deref">II.2.2 Type : registres dé-référencés</h4>
<p>
Certaines instructions prennent en argument un registre dé-référencé. Cela
signifie que la machine n'utilisera pas la valeur du registre, mais la valeur de la
mémoire dont l'adresse est la valeur du registre. Un registre dé-référencé s'écrit
[rx], où x est le numéro du registre.
</p>


<h4 id="mode">II.2.3 Type : mode</h4>
<p>
Dans sa représentation textuelle, l'instruction mode prend une chaîne de caractères en argument.
Le tableau suivant présente les chaînes de caractères acceptables.
</p>
<table class="tab" style="width:150px;">
  <tr><th>Nom</th></tr>
  <tr><td>feisar</td></tr>
  <tr><td>goteki45</td></tr>
  <tr><td>agsystems</td></tr>
  <tr><td>auricom</td></tr>
  <tr><td>assegai</td></tr>
  <tr><td>piranha</td></tr>
  <tr><td>qirex</td></tr>
  <tr><td>icaras</td></tr>
  <tr><td>rocket</td></tr>
  <tr><td>missile</td></tr>
  <tr><td>mine</td></tr>
  <tr><td>plasma</td></tr>
</table>
<p>
  Toute autre chaîne de caractères est considérée comme une erreur. Notez
  que l'assembleur ne tient pas compte de la casse. La chaîne <b>PlaSmA</b> est valide.
</p>




<h4 id="const">II.2.4 Type : constante</h4>
<p>
Certaines instructions prennent des constantes en argument. Dans ce cas,
l'assembleur reconnaîtra une expression et enregistrera dans le binaire résultant
la valeur à laquelle s'évalue l'expression. C'est la mnémonique qui détermine le
nombre de quartets qu'occupera la constante. L'évaluation des expressions est
sujette à un certain nombre de règles. Si l'expression s'évalue à un nombre trop grand pour tenir dans le nombre de
quartets spécifié par l'instruction, l'assembleur émettra un warning.
Les constantes peuvent être exprimée en hexadécimal, en décimal, en octal et en binaire.
L'assembleur interprète la constante selon le préfixe donné à l'expression :
</p>
<table class="tab">
  <tr><th>Base</th><th>Préfixe</th><th>Exemple</th></tr>
  <tr><td>Hexadécimal</td><td>0x</td><td>0xA8</td></tr>
  <tr><td>Décimal</td><td></td><td>95</td></tr>
  <tr><td>Octal</td><td>0</td><td>074</td></tr>
  <tr><td>Binaire</td><td>%</td><td>%011110011</td></tr>
</table>
</p>
<p>
L'assembleur ignore les underscores donné dans la partie descriptive des constantes (après le préfix).
</p>
Exemple
<pre class="code">
  ll r1, 2097       # valide
  ll r1, 2_097      # valide
  ll r1, _2097      # invalide
  ll r1, %0110_1100 # valide
</pre>
<p>
  Les constantes peuvent également être exprimées sous forme d'expression :
  une formule mathématique qui fournit une valeur en résultat.
  Les expressions peuvent contenir des parenthèses, des opérateurs binaires,
  des opérateurs unaires, des labels (voir plus loin),
  ainsi que des constantes. Le tableau suivant liste les opérateurs supportés.
</p>
<table class="tab op">
  <tr><th>Opérateur</th><th>Description</th><th>Exemple</th></tr>
  <tr><td>+</td><td>Plus unaire</td><td>+50</td></tr>
  <tr><td>-</td><td>Moins unaire</td><td>-50</td></tr>
  <tr><td>+</td><td>Plus binaire</td><td>10 + 50</td></tr>
  <tr><td>-</td><td>Moins binaire</td><td>50 - 50</td></tr>
  <tr><td>*</td><td>Multiplication</td><td>5 * 10</td></tr>
  <tr><td>/</td><td>Division</td><td>50 / 10</td></tr>
  <tr><td>%</td><td>Modulo*</td><td>%1110010 % 2</td></tr>
</table>
<br/>
*Note : Le modulo des nombres négatif à le même comportement que GCC
<p>
Un label est un identifiant qui sert à indiquer une position dans le code.
Ils sont utiles pour calculer automatiquement les distances des sauts et des accès
mémoire. Un label peut être constitué de lettres, de chiffres et d'underscores,
mais il doit commencer par une lettre et se terminer par une lettre ou un chiffre.
Les labels seront utilisés dans les expressions pour faire des calculs, même plus
haut que leur déclaration. Il est interdit de déclarer plusieurs fois le même label,
l'assembleur génère une erreur dans ce cas.
Un label indique l'emplacement de début de l'instruction qui suit sa déclaration.
Plus précisément, la valeur d'un label est le nombre de quartets qui sépare le
début du vaisseau du début de l'instruction qui suit le label.
Les labels sont déclarés par leur identifiant immédiatement suivi du caractère
':' (pas de séparateur). Ils peuvent se trouver n'importe où entre deux instructions.
</p>

Exemples
<pre class="code">
foo:               # Le label `foo' vaut 0
  mov r0, r1
bar:               # Le label `bar' vaut 3, car l'instruction `mov' occupe 3 quartets
  nop
  nop
  nop
qux:               # Le label `qux' vaut 6, car l'instruction `nop' occupe 1 quartets.
to42:              # Déclaration valide
3com:              # Label invalide, ne doit pas commencer par une chiffre
a--a:              # Label invalide, ne doit pas contenir de tiret
to42:              # Label invalide, le label to42 à déjà été déclaré
</pre>




<h2 id="directives">III. Directives</h2>
<p>
  L'assembleur reconnaît des directives. Les directives ne sont pas des instructions
  au sens où elles ne laissent aucune trace directe dans le code généré. Elles
  servent en fait à transmettre des requêtes ou des informations à l'assembleur,
  celles-ci pouvant modifier son comportement.
<p>
<p>
  Chaque directive est un mot commençant par un '.' et constitué de lettres (voire de chiffres).
  L'assembleur reconnaît seulement 2 directives : <b>.name</b> et <b>.comment</b>. Elles
  sont toutes les deux suivies d'une chaîne de caractères délimitée par des '"',
  et permettent de fournir à l'assembleur le nom et la description du pilote.
  Ces chaînes apparaîtront dans les pages de classement, c'est l'occasion pour vous de chambrer le voisin.
  Les chaînes de caractères pourront contenir n'importe quels caractères à l'exception du '"'.
</p>
Exemple
<pre class="code">
.name "Arial Tetsuo"
.comment "I will destroy Arian Tetsuo"
</pre>
<p>
  La taille des chaînes que peuvent prendre les directives '.name' et '.comment'
  sont respectivement 64 et 256. Chacune des directives peut apparaître au plus
  une fois dans le code du vaisseau ; une violation de cette règle provoque une erreur.
</p>




<h2 id="binaire">IV. Représentation binaire</h2>
<p>
La représentation binaire d'un vaisseau est simple. Elle est composée des représentations
binaire mise bout à bout de chacune des instructions du vaisseau.
</p>
<img width="40%" class="img" src="/img/vaisseau_binaire.png"/>

<p>
Une instruction est elle même représenté en binaire en mettant bout à bout la représentation
de sa mnémonique et des ses éventuels arguments pris dans l'ordre donné par la syntaxe.
</p>
<img width="25%" class="img" src="/img/instruction_binaire.png"/>


<p>
  Le nombre d'argument, leur représentation binaire, et le nombre de quartet codant pour l'opcode
  de l'instruction pouvant varier, toutes les instructions n'ont pas la même taille en binaire.
  Ainsi, les instructions les plus courte s'encodent sur 1 quartet (<a href="/rules/instructions#crash">crash</a>
  et <a href="/rules/instructions#nop">nop</a>), alors que les instructions les plus longues s'encodent sur
  7 quartets (<a href="/rules/instructions#stb">stb</a>, <a href="/rules/instructions#ldb">ldb</a> et
  <a href="/rules/instructions#ll">ll</a>).
</p>



<h3 id="binaire_mnemonique">IV.1 Mnémoniques</h3>
<p>
  Chaque instruction est identifié par sa mnémonique et chaque mnémonique à une
  représentation binaire unique : son opcode.<br/>

  Selon la mnémonique, l'opcode occupera 1 ou 2 quartets.
  Pour permettre à la machine virtuelle de décoder les opcodes sans ambiguïté, les
  mnémonique à deux quartets ont systématiquement un opcode de poids fort à %1111,
  et tout opcode commençant par quelque chose de différent s'encode sur un unique quartet.
  Le tableau ci-dessous liste les opcodes de toutes les instructions :
</p>

<table class="tab opcode">
  <tr>
    <th>Syntaxe</th>
    <th>q0</th>
    <th>q1</th>
  </tr>
  <tr>
    <td><a href="#crash">crash</a></td>
    <td class="op">0000</td>
  </tr>
  <tr>
    <td><a href="#nop">nop</a></td>
    <td class="op">0001</td>
  </tr>
  <tr>
    <td><a href="#and">and</a> rx, ry</td>
    <td class="op">0010</td>
  </tr>
  <tr>
    <td><a href="#or">or</a> rx, ry</td>
    <td class="op">0011</td>
  </tr>
  <tr>
    <td><a href="#xor">xor</a> rx, ry</td>
    <td class="op">0100</td>
  </tr>
  <tr>
    <td><a href="#not">not</a> rx, ry</td>
    <td class="op">0101</td>
  </tr>
  <tr>
    <td><a href="#rol">rol</a> rx, ry</td>
    <td class="op">0110</td>
  </tr>
  <tr>
    <td><a href="#asr">asr</a> rx, ry</td>
    <td class="op">0111</td>
  </tr>
  <tr>
    <td><a href="#add">add</a> rx, ry</td>
    <td class="op">1000</td>
  </tr>
  <tr>
    <td><a href="#sub">sub</a> rx, ry</td>
    <td class="op">1001</td>
  </tr>
  <tr>
    <td><a href="#cmp">cmp</a> rx, ry</td>
    <td class="op">1010</td>
  </tr>
  <tr>
    <td><a href="#neg">neg</a> rx, ry</td>
    <td class="op">1011</td>
  </tr>
  <tr>
    <td><a href="#mov">mov</a> rx, ry</td>
    <td class="op">1100</td>
  </tr>
  <tr>
    <td><a href="#ldr">ldr</a> rx, [ry]</td>
    <td class="op">1101</td>
  </tr>
  <tr>
    <td><a href="#str">str</a> [rx], ry</td>
    <td class="op">1110</td>
  </tr>
  <tr>
    <td><a href="#ldb">ldb</a> [rx], n, m</td>
    <td class="op">1111</td>
    <td class="op">0000</td>
  </tr>
  <tr>
    <td><a href="#stb">stb</a> [rx], n, m</td>
    <td class="op">1111</td>
    <td class="op">0001</td>
  </tr>
  <tr>
    <td><a href="#lc">lc</a> rx, n</td>
    <td class="op">1111</td>
    <td class="op">0010</td>
  </tr>
  <tr>
    <td><a href="#ll">ll</a> rx, n</td>
    <td class="op">1111</td>
    <td class="op">0011</td>
  </tr>
  <tr>
    <td><a href="#swp">swp</a> rx, ry</td>
    <td class="op">1111</td>
    <td class="op">0100</td>
  </tr>
  <tr>
    <td><a href="#addi">addi</a> rx, n</td>
    <td class="op">1111</td>
    <td class="op">0101</td>
  </tr>
  <tr>
    <td><a href="#cmpi">cmpi</a> rx, n</td>
    <td class="op">1111</td>
    <td class="op">0110</td>
  </tr>
  <tr>
    <td><a href="#b">b</a> rx</td>
    <td class="op">1111</td>
    <td class="op">0111</td>
  </tr>
  <tr>
    <td><a href="#bz">bz</a> rx</td>
    <td class="op">1111</td>
    <td class="op">1000</td>
  </tr>
  <tr>
    <td><a href="#bnz">bnz</a> rx</td>
    <td class="op">1111</td>
    <td class="op">1001</td>
  </tr>
  <tr>
    <td><a href="#bs">bs</a> rx</td>
    <td class="op">1111</td>
    <td class="op">1010</td>
  </tr>
  <tr>
    <td><a href="#stat">stat</a> rx, n</td>
    <td class="op">1111</td>
    <td class="op">1011</td>
  </tr>
  <tr>
    <td><a href="#check">check</a></td>
    <td class="op">1111</td>
    <td class="op">1100</td>
  </tr>
  <tr>
    <td><a href="#mode">mode</a> m</td>
    <td class="op">1111</td>
    <td class="op">1101</td>
  </tr>
  <tr>
    <td><a href="#fork">fork</a></td>
    <td class="op">1111</td>
    <td class="op">1110</td>
  </tr>
  <tr>
    <td><a href="#write">write</a> rx</td>
    <td class="op">1111</td>
    <td class="op">1111</td>
  </tr>
</table>
<br/>
<br/>


<p>
</p>

<h3 id="binaire_arguments"> IV.2 Arguments</h3>


<h4 id="binaire_registres"> IV.2.1 Registres</h4>
<p>
Leur représentation binaire est simplement leur numéro codé sur un quartet,
c'est-à-dire que le registre r5 se verra représenté par un seul quartet de
valeur 5. Idem pour les registres dé-référencés, il sont encodés comme un registre normal,
seul l'interprétation de l'argument par la VM sera différente.
</p>

<h4 id="binaire_modes">IV.2.2 Modes</h4>
<p>
  Dans sa représentation binaire, l'instruction mode prendra un quartet
  en argument : le tableau suivant indique quelle valeur représente chaque mode.
</p>
<table class="tab">
  <tr><th>Nom</th><th>Valeur</th></tr>
  <tr><td>feisar</td><td>0</td></tr>
  <tr><td>goteki45</td><td>1</td></tr>
  <tr><td>agsystems</td><td>2</td></tr>
  <tr><td>auricom</td><td>3</td></tr>
  <tr><td>assegai</td><td>4</td></tr>
  <tr><td>piranha</td><td>5</td></tr>
  <tr><td>qirex</td><td>6</td></tr>
  <tr><td>icaras</td><td>7</td></tr>
  <tr><td>rocket</td><td>8</td></tr>
  <tr><td>missile</td><td>9</td></tr>
  <tr><td>mine</td><td>10</td></tr>
  <tr><td>plasma</td><td>11</td></tr>
</table>

<h4 id="binaire_constantes">IV.2.3 Constantes</h4>

<p>
  Les constantes sont encodés sur 1, 2 ou 4 quartet selon les spécifications d'encodage d'argument de chaque instruction.
  Pour les constants de 1 quartet, celui ci prend simplement la valeur de la constante.
  Pour les constantes s'encodant sur plusieurs quartet, le premier quartet encode le poids faible.
  La spécification complète de l'encodage des arguments des différentes instructions est disponible
  sur la page <a class="racename" href="/rules/instructions#instr">INSTRUCTIONS</a>.
</p>

Exemples
<pre class="code">
  # encodage de 5     sur un quartet      => 0101
  # encodage de 35    sur deux quartets   => 0011 0010
  # encodage de 11983 sur quatre quartets => 1111 1100 1110 0010
  # encodage de 5     sur deux quartets   => 0101 0000
</pre>

<p>Notez que les labels ne s'encodent pas. Ils ne sont jamais présents dans la représentation binaire du vaisseau, ils servent
uniquement pour effectuer des calculs de constante dans une expression au moment
de l'assemblage.</p>

<h3 id="exemple">IV.3 Exemple : Vaisseau complet</h3>

<p>Dans cette section, on va décortiquer la représentation binaire d'un vaisseau complet.
Le même vaisseau sera décortiqué dans le détail de la VM. Allons y, soit le vaisseau suivant :
</p>


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
  On commence par encoder la première instruction, "ll r0, 0x2ecf".
  Le tableau récapitulatif des encodages présenter <a href="/rules/instructions#instr">ici</a> nous dit :
</p>
<pre class="code">
  - syntaxe : ll rx, n
  - quartet d'opcode : 1111 0011 (2 quartets d'opcode)
  - codage des arguments : rx n0 n1 n2 n3 (1 quartet pour le registre plus 4 quartets pour la constante)
</pre>

L'instruction se code donc sur 2+1+4 = 7 quartets.

<pre class="code">
  q0   q1   q2   q3   q4   q5   q6
+----+----+----+----+----+----+----+
|    |    |    |    |    |    |    |
+----+----+----+----+----+----+----+
</pre>

On commence par écrire les opcode : 1111 0011, ça c'est facile.

<pre class="code">
  q0   q1   q2   q3   q4   q5   q6
+----+----+----+----+----+----+----+
|1111|0011|    |    |    |    |    |
+----+----+----+----+----+----+----+
 op1  op2
</pre>

On ajoute ensuite le quartet d'encodage du paramètre r0 :

<pre class="code">
  q0   q1   q2   q3   q4   q5   q6
+----+----+----+----+----+----+----+
|1111|0011|0000|    |    |    |    |
+----+----+----+----+----+----+----+
 op1  op2   r0
</pre>

On décompose 0x2ecf en 4 quartet, et on rempli notre instruction en commencant par le poids faible :

<pre class="code">
2ecf => 0010 1110 1100 1111
         2    e    c    f

  q0   q1   q2   q3   q4   q5   q6
+----+----+----+----+----+----+----+
|1111|0011|0000|1111|1100|1110|0010|
+----+----+----+----+----+----+----+
 op1  op2  r0    f    c    e    2
</pre>

Et voila, une jolie petite instruction encodée comme il se doit.
Au final on obtient la séquence F3 0F CE 2.

<pre class="code">
  q0   q1   q2   q3   q4   q5   q6
+----+----+----+----+----+----+----+
|1111|0011|0000|1111|1100|1110|0010|
+----+----+----+----+----+----+----+
  F    3    0    F    C    E     2
</pre>


De la même façon, l'instruction suivante : ll r1, 0x13e0 s'encode F3 10 E3 1

<pre class="code">
0x13e0 => 0001 0011 1110 0000
            1   3    e    0

  q0   q1   q2   q3   q4   q5   q6
+----+----+----+----+----+----+----+
|1111|0011|0001|0000|1110|0011|0001|
+----+----+----+----+----+----+----+
 op1   op2  r1   0    e    3    1
 F     3    1    0    E    3    1
</pre>

<p>
Pour la prochaine instruction, "ll r2, to - from1", il faut résoudre l'expression
to - from1 et pour calculer la valeur de chacun d'entre eux.
</p>

<p>
Le from1 est placé après les 4 instructions "ll" et la première instruction "str". On sait
déjà que l'instruction "ll" s'encode sur 7 quartets, et le tableau donnée <a href="/rules/instructions#instr">ici</a>
nous dit que str s'encode sur 3 quartets (1 quartet pour la mnémonique et 1 quartet pour chacun des deux arguments).
La valeur du label from1 est donc de 7*4 + 3 = 31.
Pour to, c'est là même chose, il faut compter les 4 instructions "ll" et les deux instructions "str" donc 7*4 + 3*2 = 34.
</p>
<p>L'expression to-from1 est donc égale à 34-31 = 3. Ça tombe bien, c'est justement la taille de l'instruction "str" qui sépare les deux labels.
</p>
On veut donc l'instruction ll r2, 3. Ce qui donne : F3 23 00 0
<pre class="code">
0x0003 => 0000 0000 0000 0011
            0   0    0    3

  q0   q1   q2   q3   q4   q5   q6
+----+----+----+----+----+----+----+
|1111|0011|0002|0003|0000|0000|0000|
+----+----+----+----+----+----+----+
 op1   op2  r2   3    0    0    0
 F     3    2    3    0    0    0
</pre>

<p>
De la même façon l'instruction suivante, "ll r3, to-from2+4", se simplifie en "ll r3, 4". Et cette dernière s'encode F3 34 00 0
En encodant les instructions, "str [r2], r0" et "str [r3], r1", on arrive respectivement a E2 0 et E3 1.
</p>


Si on récapitule :


<pre class="code">
ll r0, 0x2ecf     # F3 0F CE 2
ll r1, 0x13e0     # F3 10 E3 1
ll r2, to-from1   # F3 23 00 0
ll r3, to-from2+4 # F3 34 00 0
str [r2], r0      # E2 0
str [r3], r1      # E3 1

Code final du vaisseau : F3 0F CE 2F 31 0E 31 F3 23 00 0F 33 40 00 E2 0E 31
</pre>


Bonus :
<p>
Nous verrons dans la présentation de la VM comment va s'exécuter ce code, mais on peut faire un petit teaser.
On a chargé deux constantes en mémoire : 0x2ECF ET 0x13E0.
Les instructions str vont avoir pour effet d'écrire ces deux constantes dans la mémoire du circuit,
on va se retrouver avec les quartets consécutifs suivants : FC E2 0E 31.
Si je réécris cette liste de la façon suivante : <b>FC E20 E31</b>, cela ne vous dit rien ? (aidez-vous du tableau d'instruction).
</p>
