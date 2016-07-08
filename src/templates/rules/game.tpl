<style>
  #tracks td { text-align:center; vertical-align:top; }
  #tracks tr:nth-child(3) td { padding:10px 20px; }
  #instr { font-size:12px; margin-left:50px; }
</style>

<h1>Le jeu</h1>

<h2>Les instructions</h2>

<p>
Chaque vaisseau est capable d'exécuter un certain nombre d'instructions. La
liste de ces instructions est finie. Leur détail est
donné sur la page <a class="racename" href="/rules/instructions">INSTRUCTIONS</a>.<br/>
</p>


<table id="instr">
  <tr> <td>and</td> <td>ET logique registre à registre</td>                      <td>or</td> <td>OU logique registre à registre</td> </tr>
  <tr> <td>xor</td> <td>OU exclusif registre à registre</td>                     <td>not</td> <td>Négation binaire de registre à registre</td> </tr>
  <tr> <td>rol</td> <td>Rotation à gauche d'un registre</td>                     <td>asr</td> <td>Décalage arithmétique à droite d'un registre</td> </tr>
  <tr> <td>add</td> <td>Addition registre à registre</td>                        <td>sub</td> <td>Soustraction registre à registre</td> </tr>
  <tr> <td>cmp</td> <td>Comparaison registre à registre</td>                     <td>addi</td> <td>Addition immédiate à registre</td> </tr>
  <tr> <td>cmpi</td> <td>Comparaison immédiate à registre</td>                   <td>neg</td> <td>Calcul de l'opposé de registre à registre</td> </tr>
  <tr> <td>mov</td> <td>Déplacement de données registre à registre</td>          <td>swp</td> <td>Échange de contenu de registre</td> </tr>
  <tr> <td>lc</td> <td>Chargement de données immédiates courtes à registre</td>  <td>ll</td> <td>Chargement de données immédiates longues à registre</td> </tr>
  <tr> <td>ldr</td> <td>Chargement de données mémoire à registre</td>            <td>str</td> <td>Stockage de données registre à mémoire</td> </tr>
  <tr> <td>ldb</td> <td>Chargement du tampon</td>                                <td>stb</td> <td>Écriture du tampon</td> </tr>
  <tr> <td>b</td> <td>Saut inconditionnel</td>                                   <td>bz</td> <td>Saut conditionnel (si Z posé)</td> </tr>
  <tr> <td>bnz</td> <td>Saut conditionnel (si Z non posé)</td>                   <td>bs</td> <td>Saut conditionnel (si S posé)</td> </tr>
  <tr> <td>write</td> <td>Affichage d'un registre sur la sortie standard</td>    <td>stat</td> <td>Chargement de statistique dans un registre spécial</td> </tr>
  <tr> <td>check</td> <td>Validation d'une étape</td>                            <td>mode</td> <td>Changement de mode</td> </tr>
  <tr> <td>fork</td> <td>Demande d'entrée en duplication</td>                    <td>crash</td> <td>Destruction</td> </tr>
  <tr> <td>nop</td> <td>Pas d'opération</td>                                    </tr>
</table>


<h2>C'est quoi un vaisseau ?</h2>

  Un vaisseau est une suite d'instructions.
  La liste des instructions est finie, et à chaque instruction est associé :
  <ul>
    <li>Une syntaxe : un nom et un nombre variable d'arguments</li>
    <li>Une représentation textuelle : une pseudo-langage assembleur appelé
        <a class="racename" href="/rules/language">F6100</a>
    <li>Une représentation binaire : qui sera lue et exécutée par la <a class="racename" href="/rules/language">VM</a>
  </ul>
</br>


<h2>Comment faire un vaisseau ?</h2>

  <p>
  Pour créer son vaisseau, le pilote se présente aux <a class="racename" href="/pit">STANDS</a>.
  La bas, il pourra donner les plans de son vaisseau (en langage <a class="racename" href="/rules/language">F6100</a>).
  Les plans y seront vérifiés et transformés en binaire. Le pilote n'a plus qu'a se présenter à la <a class="racename" href="/league">COMPÉTITION</a> de son choix<br/>
  <ul>
    <li>Le détails du langage est présenté sur la page F6100 <a class="racename" href="/rules/language">F6100</a>.</li>
  </ul>
  </p>
</br>



<h2>C'est quoi le circuit ?</h2>

<p>
  Le circuit est une machine virtuelle initialisée au démarrage avec le code des vaisseaux en compétition. La VM va ensuite lire cette mémoire séquenciellement, et exécuter chaque instruction décodée.</br>
  <ul>
    <li>Les caractéristiques détaillées de la VM sont présentée sur la page <a class="racename" href="/rules/vm">VM</a>.</li>
    <li>La liste complète des instructions est disponible sur la page  <a class="racename" href="/rules/isntructions">INSTRUCTIONS</a>.</li>
  </ul>
</p>
<br/>


<h2>Comment faire avancer son vaisseau ?</h2>

<p>
  Pour avancer, un vaisseau doit copier tout ou une partie de lui même (son code)
  un peu plus loin dans la mémoire puis sauter vers cette zone mémoire.
  L'exécution du bloc copié provoquera une nouvelle copie encore un peu plus loin
  et le saut vers ce bloc. Et ainsi de suite jusqu'à la fin de la course.
</p>

<table id="tracks">
  <tr>
    <td>1.</td>
    <td>2.</td>
    <td>3.</td>
    <td>4.</td>
  </tr>
  <tr>
    <td><img width="190" src="/img/track_1.png"/></td>
    <td><img width="190"  src="/img/track_2.png"/></td>
    <td><img width="190"  src="/img/track_3.png"/></td>
    <td><img width="190"  src="/img/track_4.png"/></td>
  </tr>
  <tr>
    <td>
      État initial du vaisseau dans la mémoire.
    </td>
    <td>
      Le vaisseau s'est répliqué plus loin.
    </td>
    <td>
      Le vaisseau "saute" jusqu'au bloc copié.
    </td>
    <td>
      L'exécution du code copié provoque une nouvelle réplication.
    </td>
  </tr>
</table>
