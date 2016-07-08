<style>
  #instr {
    font-size:12px;
  }

  #instr tr td:nth-child(n+3) { text-align:center; }
  #instr tr:first-child td { font-weight:bold; font-size:16px; padding-bottom:20px; }

  #instr td.op { background-color:d0d0d0 !important; }

  .instrd { font-size: 14px; }
  .instrd td:nth-child(2n+1) { font-weight:bold; width: 200px; vertical-align:top; text-align:right; padding-right:10px; }
  .instrd td pre { padding-top:5px; font-size: 12px; font-family:Consolas,Monaco,Lucida Console,Liberation Mono,DejaVu Sans Mono,Bitstream Vera Sans Mono,Courier New, monospace; }

  #data { font-size:12px; }
  #data tr td:nth-child(1) { width:100px; }
  #data td { border-top:1px #d6d6d6 solid; border-left:1px #d6d6d6 solid;width:4%; }
  #data td:last-child { border-right:1px #d6d6d6 solid; }
  #data tr:last-child td { border-bottom:1px #d6d6d6 solid; }
  #data tr td:nth-child(n+2) { text-align:center; }
  #data tr:nth-child(n+2) td:nth-child(n+2) { font-size:12px; }
  #data tr:first-child td { font-weight:bold; }
  #data tr td:first-child { font-weight:bold; }
  #data td.min { background-color:#D9FFB3 !important; }
  #data td.max { background-color:#FF9999 !important; }

  #instr > tbody > tr:hover > td,
  #data > tbody > tr:hover > td {
    background-color: rgba(102, 179, 255, 0.5);
  }

</style>


<h1>Instructions</h2>

<h2>Récapitulatif des instructions</h2>

<p>
Ci-dessous une vue d'ensemble de toutes les instructions disponibles, leur syntaxe respective ainsi que leur
représentation binaire (comprenant entre un et deux quartets d'optcode et entre zéro et cinq quartets d'argument).
Vous pouvez consulter le descriptif détaillé de chaque instruction en suivant le lien sur leur
</p>
<table id="instr">
  <tr>
    <td>Syntaxe</td>
    <td>Description</td>
    <td>q0</td>
    <td>q1</td>
    <td>q2</td>
    <td>q3</td>
    <td>q4</td>
    <td>q5</td>
    <td>q6</td>
  </tr>
  <tr>
    <td><a href="#crash">crash</a></td>
    <td>Destruction</td>
    <td class="op">0000</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td><a href="#nop">nop</a></td>
    <td>No operation</td>
    <td class="op">0001</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td><a href="#and">and</a> rx, ry</td>
    <td>ET logique registre à registre</td>
    <td class="op">0010</td>
    <td>rx</td>
    <td>ry</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td><a href="#or">or</a> rx, ry</td>
    <td>OU logique registre à registre</td>
    <td class="op">0011</td>
    <td>rx</td>
    <td>ry</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td><a href="#xor">xor</a> rx, ry</td>
    <td>OU exclusif registre à registre</td>
    <td class="op">0100</td>
    <td>rx</td>
    <td>ry</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td><a href="#not">not</a> rx, ry</td>
    <td>Négation binaire de registre à registre</td>
    <td class="op">0101</td>
    <td>rx</td>
    <td>ry</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td><a href="#rol">rol</a> rx, n</td>
    <td>Rotation à gauche d'un registre</td>
    <td class="op">0110</td>
    <td>rx</td>
    <td>n</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td><a href="#asr">asr</a> rx, n</td>
    <td>Décalage arithmétique à droite d'un registre</td>
    <td class="op">0111</td>
    <td>rx</td>
    <td>n</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td><a href="#add">add</a> rx, ry</td>
    <td>Addition registre à registre</td>
    <td class="op">1000</td>
    <td>rx</td>
    <td>ry</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td><a href="#sub">sub</a> rx, ry</td>
    <td>Soustraction registre à registre</td>
    <td class="op">1001</td>
    <td>rx</td>
    <td>ry</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td><a href="#cmp">cmp</a> rx, ry</td>
    <td>Comparaison registre à registre</td>
    <td class="op">1010</td>
    <td>rx</td>
    <td>ry</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td><a href="#neg">neg</a> rx, ry</td>
    <td>Calcul de l'opposé de registre à registre</td>
    <td class="op">1011</td>
    <td>rx</td>
    <td>ry</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td><a href="#mov">mov</a> rx, ry</td>
    <td>Déplacement de données registre à registre</td>
    <td class="op">1100</td>
    <td>rx</td>
    <td>ry</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td><a href="#ldr">ldr</a> rx, [ry]</td>
    <td>Chargement de données mémoire à registre</td>
    <td class="op">1101</td>
    <td>rx</td>
    <td>ry</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td><a href="#str">str</a> [rx], ry</td>
    <td>Stockage de données registre à mémoire</td>
    <td class="op">1110</td>
    <td>rx</td>
    <td>ry</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td><a href="#ldb">ldb</a> [rx], n, m</td>
    <td>Chargement du tampon</td>
    <td class="op">1111</td>
    <td class="op">0000</td>
    <td>rx</td>
    <td>n0</td>
    <td>n1</td>
    <td>m0</td>
    <td>m1</td>
  </tr>
  <tr>
    <td><a href="#stb">stb</a> [rx], n, m</td>
    <td>Écriture du tampon</td>
    <td class="op">1111</td>
    <td class="op">0001</td>
    <td>rx</td>
    <td>n0</td>
    <td>n1</td>
    <td>m0</td>
    <td>m1</td>
  </tr>
  <tr>
    <td><a href="#lc">lc</a> rx, n</td>
    <td>Chargement de données immédiates courtes à registre</td>
    <td class="op">1111</td>
    <td class="op">0010</td>
    <td>rx</td>
    <td>n0</td>
    <td>n1</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td><a href="#ll">ll</a> rx, n</td>
    <td>Chargement de données immédiates longues à registre</td>
    <td class="op">1111</td>
    <td class="op">0011</td>
    <td>rx</td>
    <td>n0</td>
    <td>n1</td>
    <td>n2</td>
    <td>n3</td>
  </tr>
  <tr>
    <td><a href="#swp">swp</a> rx, ry</td>
    <td>Echange de contenu de registre</td>
    <td class="op">1111</td>
    <td class="op">0100</td>
    <td>rx</td>
    <td>ry</td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td><a href="#addi">addi</a> rx, n</td>
    <td>Addition immédiate à registre</td>
    <td class="op">1111</td>
    <td class="op">0101</td>
    <td>rx</td>
    <td>n</td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td><a href="#cmpi">cmpi</a> rx, n</td>
    <td>Comparaison immédiate à registre</td>
    <td class="op">1111</td>
    <td class="op">0110</td>
    <td>rx</td>
    <td>n</td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td><a href="#b">b</a> rx</td>
    <td>Saut inconditionnel</td>
    <td class="op">1111</td>
    <td class="op">0111</td>
    <td>rx</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td><a href="#bz">bz</a> rx</td>
    <td>Saut conditionnel (si Z posé)</td>
    <td class="op">1111</td>
    <td class="op">1000</td>
    <td>rx</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td><a href="#bnz">bnz</a> rx</td>
    <td>Saut conditionnel (si Z non posé)</td>
    <td class="op">1111</td>
    <td class="op">1001</td>
    <td>rx</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td><a href="#bs">bs</a> rx</td>
    <td>Saut conditionnel (si S posé)</td>
    <td class="op">1111</td>
    <td class="op">1010</td>
    <td>rx</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td><a href="#stat">stat</a> rx, n</td>
    <td>Chargement de statistique dans un registre spécial</td>
    <td class="op">1111</td>
    <td class="op">1011</td>
    <td>rx</td>
    <td>n</td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td><a href="#check">check</a></td>
    <td>Validation d'une étape</td>
    <td class="op">1111</td>
    <td class="op">1100</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td><a href="#mode">mode</a> m</td>
    <td>Changement de mode</td>
    <td class="op">1111</td>
    <td class="op">1101</td>
    <td>m</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td><a href="#fork">fork</a></td>
    <td>Demande d'entrée en duplication</td>
    <td class="op">1111</td>
    <td class="op">1110</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td><a href="#write">write</a> rx</td>
    <td>Affichage d'un registre sur la sortie standard</td>
    <td class="op">1111</td>
    <td class="op">1111</td>
    <td>rx</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
</table>
<br/>
<br/>



<h2>Coût des instructions</h2>
<p>
Tel qu'éxpliqué dans la section dédié au fonctionnement de la <a class="racename" href="/rules/vm">VM</a>, chaque instruction
à un coût de décodage et un coût d'exécution. Ce coût s'exprime en nombre de cycle et dépend du mode
dans lequel se trouve le vaisseau. Le tableau ci-dessous regroupe les coûts de décodage (Dec) et exécution de toutes
les instructions en fonction des différents mode possibles. De plus, ce tableau récapitule les différentes valeurs de
portées (expliqué dans la section <a href="/rules/vm#shight">monde du relatif</a>) en fonction du mode.
</p>

<%
import corewar.core.data.modes as modes
l_modeList  = [(x,getattr(modes.Modes, x)) for x in dir(modes.Modes) if x != "Instr" and not "__" in x]
l_instrList = [(x.lower(), getattr(modes.Modes.Instr, x)) for x in dir(modes.Modes.Instr) if not "__" in x]
%>

<table id="data">
  <tr>
    <td></td>
% for c_modeName, c_modeVal in l_modeList:
    <td colspan="2">${c_modeName}</td>
% endfor
  </tr>

  <tr>
    <td></td>
    % for c_modeName, c_modeVal in l_modeList:
      <td>Dec</td><td>Exe</td>
    % endfor
  </tr>

% for c_instName, c_instrVal in l_instrList:
  <tr>
   <%
      l_minDecode = min([ y.Decode[c_instrVal] for x,y in l_modeList ])
      l_maxDecode = max([ y.Decode[c_instrVal] for x,y in l_modeList ])
      l_minExecute = min([ y.Execute[c_instrVal] for x,y in l_modeList ])
      l_maxExecute = max([ y.Execute[c_instrVal] for x,y in l_modeList ])
   %>
   <td>${c_instName}</td>
   % for c_modeName, c_modeVal in l_modeList:
    <td
       % if c_modeVal.Decode[c_instrVal] == l_minDecode:
         class=""
       % elif c_modeVal.Decode[c_instrVal] == l_maxDecode:
         class=""
       % endif
    >
       ${c_modeVal.Decode[c_instrVal]}
    </td>
    <td
       % if c_modeVal.Execute[c_instrVal] == l_minExecute:
         class="min"
       % elif c_modeVal.Execute[c_instrVal] == l_maxExecute:
         class="max"
       % endif
       >
      ${c_modeVal.Execute[c_instrVal]}</td>
   % endfor
  </tr>
% endfor

  <tr>
    <td>Sight</td>
    <%
      l_minSight = min([ y.Sight for x,y in l_modeList ])
      l_maxSight = max([ y.Sight for x,y in l_modeList ])
    %>
  % for c_modeName, c_modeVal in l_modeList:
    <td colspan="2"
       % if c_modeVal.Sight == l_minSight:
         class="max"
       % elif c_modeVal.Sight == l_maxSight:
         class="min"
       % endif
        >${c_modeVal.Sight}</td>
  % endfor
  </tr>

</table>
<br/>
<br/>



<h2>Jeu d'instructions détaillé</h2>

<p>
Sauf précision contraire spécifique à une instruction, toutes les instructions
affectent implicitement Z et S en mettant Z à 0 si le résultat du calcul est non
nul, à 1 s'il est nul, et S à 1 si le bit le plus fort du résultat du calcul est posé,
à 0 s'il ne l'est pas.
</p>
<p>
Attention. Pour simplifier l'écriture, nous utilisons ici l'expression "rx %
SIGHT" pour désigner le "modulo"" très particulier fait pour chaque accès
mémoire par la machine virtuelle. Il ne s'agit absolument pas d'un modulo
arithmétique habituel. Pour plus de détails, se référer à la section <a href="/rules/vm#sight">monde du relatif</a>
du fonctionnement de la machine virtuelle.
</p>

<h4><hr/> "<a id="and">and</a>" : AND register</h4>

<table class="instrd">
  <tr>    <td>Syntaxe : </td>                <td>and rx, ry</td>  </tr>
  <tr>    <td>Mise à jour des flags : </td>  <td> Z et S </td>    </tr>
  <tr>
    <td>Description : </td>
    <td>
      Cette instruction calcule le ET logique bit à bit entre rx et ry et stocke le
      résultat dans rx. L'effet est le même que celui de l'instruction C rx = rx & ry.
    </td>
  </tr>
  <tr>
    <td>Exemple : </td>
    <td>
      <pre>
ll r1, %1111000000001111
ll r2, %0011001110101010
and r1, r2               # r1 vaut %0011000000001010
      </pre>
    </td>
  </tr>
</table>


<h4><hr/> "<a id="or">or</a>" : OR register</h4>

<table class="instrd">
  <tr>    <td>Syntaxe : </td>                <td>or rx, ry</td>  </tr>
  <tr>    <td>Mise à jour des flags : </td>  <td> Z et S </td>    </tr>
  <tr>
    <td>Description : </td>
    <td>
      Calcule le OU logique bit à bit entre rx et ry et stocke le résultat dans rx.
      L'effet est le même que celui de l'instruction C rx = rx | ry.
    </td>
  </tr>
  <tr>
    <td>Exemple : </td>
    <td>
      <pre>
ll r1, %1111000000001111
ll r2, %0011001110101010
or r1, r2                # r1 vaut %1111001110101111
      </pre>
    </td>
  </tr>
</table>


<h4><hr/> "<a id="xor">xor</a>" : eXclusif OR register</h4>
<table class="instrd">
  <tr>    <td>Syntaxe : </td>                <td>xor rx, ry</td>  </tr>
  <tr>    <td>Mise à jour des flags : </td>  <td> Z et S </td>    </tr>
  <tr>
    <td>Description : </td>
    <td>
      Calcule le OU exclusif bit à bit entre rx et ry et stocke le résultat dans rx.
      L'effet est le même que celui de l'instruction C rx = rx ^ ry.
    </td>
  </tr>
  <tr>
    <td>Exemple : </td>
    <td>
      <pre>
ll r1, %1111000000001111
ll r2, %0011001110101010
xor r1 , r2              # r1 vaut %1100001110100101
      </pre>
    </td>
  </tr>
</table>


<h4><hr/> "<a id="not">not</a>" : NOT register</h4>
<table class="instrd">
  <tr>    <td>Syntaxe : </td>                <td>not rx, ry</td>  </tr>
  <tr>    <td>Mise à jour des flags : </td>  <td> Z et S </td>    </tr>
  <tr>
    <td>Description : </td>
    <td>
Calcule la négation binaire (complément à 1) de ry et la stocke dans rx.
L'effet est le même que celui de l'instruction C rx = ~ry.
    </td>
  </tr>
  <tr>
    <td>Exemple : </td>
    <td>
      <pre>
ll r2, %1111000010101111
not r1 , r2              # r1 vaut %0000111101010000
      </pre>
    </td>
  </tr>
</table>


<h4><hr/> "<a id="rol">rol</a>" : ROtation Left</h4>
<table class="instrd">
  <tr>    <td>Syntaxe : </td>                <td>rol rx, n</td>  </tr>
  <tr>    <td>Mise à jour des flags : </td>  <td> Z et S </td>    </tr>
  <tr>
    <td>Description : </td>
    <td>
      Effectue une rotation du registre rx de n bits vers la gauche. Les bits qui
      entrent à droite sont ceux qui sortent à gauche
    </td>
  </tr>
  <tr>
    <td>Exemple : </td>
    <td>
      <pre>
ll r1, %0000100000001111
rol r1 , 3               # r1 vaut %0010000001111000
      </pre>
    </td>
  </tr>
</table>


<h4><hr/> "<a id="asr">asr</a>" : Arithmetic Shift Right</h4>
<table class="instrd">
  <tr>    <td>Syntaxe : </td>                <td>asr rx, n</td>  </tr>
  <tr>    <td>Mise à jour des flags : </td>  <td> Z et S </td>    </tr>
  <tr>
    <td>Description : </td>
    <td>
      Effectue un décalage arithmétique du registre rx de n bits vers la droite : les
      bits entrants sont identiques au bit de signe.
    </td>
  </tr>
  <tr>
    <td>Exemple : </td>
    <td>
      <pre>
ll r1, %00110000000001111
asr r1 , 2                # r1 vaut %0000110000000011
ll r1, %1011000000001111
asr r1 , 2                # r1 vaut %1110110000000011
      </pre>
    </td>
  </tr>
</table>


<h4><hr/> "<a id="add">add</a>" : ADD register</h4>
<table class="instrd">
  <tr>    <td>Syntaxe : </td>                <td>add rx, ry</td>  </tr>
  <tr>    <td>Mise à jour des flags : </td>  <td> Z et S </td>    </tr>
  <tr>
    <td>Description : </td>
Additionne le contenu de ry à celui de rx et stocke le résultat dans rx. L'effet
est le même que celui de l'instruction C rx += ry.
    <td>
    </td>
  </tr>
</table>


<h4><hr/> "<a id="sub">sub</a>" : SUBstract register </h4>
<table class="instrd">
  <tr>    <td>Syntaxe : </td>                <td>sub rx, ry</td>  </tr>
  <tr>    <td>Mise à jour des flags : </td>  <td> Z et S </td>    </tr>
  <tr>
    <td>Description : </td>
    <td>
Soustrait le contenu de ry à celui de rx et stocke le résultat dans rx. L'effet
est le même que celui de l'instruction C rx -= ry.
    </td>
  </tr>
</table>


<h4><hr/> "<a id="cmp">cmp</a>" : CoMPare register</h4>
<table class="instrd">
  <tr>    <td>Syntaxe : </td>                <td>cmp rx, ry</td>  </tr>
  <tr>    <td>Mise à jour des flags : </td>  <td> Z et S </td>    </tr>
  <tr>
    <td>Description : </td>
    <td>
      Soustrait le contenu de ry à celui de rx et ne stocke pas le résultat.
      L'information intéressante se trouve dans les registres Z et S.
    </td>
  </tr>
</table>


<h4><hr/> "<a id="addi">addi</a>" : Add Integer</h4>
<table class="instrd">
  <tr>    <td>Syntaxe : </td>                <td>addi rx, n</td>  </tr>
  <tr>    <td>Mise à jour des flags : </td>  <td> Z et S </td>    </tr>
  <tr>
    <td>Description : </td>
    <td>
      Additionne la constante n (signée) au registre rx et stocke le résultat dans
      rx. L'effet est le même que celui de l'instruction C rx += n.
    </td>
  </tr>
</table>


<h4><hr/> "<a id="cmpi">cmpi</a>" CoMPare to Integer</h4>
<table class="instrd">
  <tr>    <td>Syntaxe : </td>                <td>cmpi rx, n</td>  </tr>
  <tr>    <td>Mise à jour des flags : </td>  <td> Z et S </td>    </tr>
  <tr>
    <td>Description : </td>
    <td>
      Soustrait la constante n (signée) à rx et ne stocke pas le résultat.
      L'information intéressante se trouve dans les registres Z et S.
    </td>
  </tr>
</table>


<h4><hr/> "<a id="neg">neg</a>" NEGate register</h4>
<table class="instrd">
  <tr>    <td>Syntaxe : </td>                <td>neg rx, ry</td>  </tr>
  <tr>    <td>Mise à jour des flags : </td>  <td> Z et S </td>    </tr>
  <tr>
    <td>Description : </td>
    <td>
Stocke dans rx l'opposé de ry. L'effet est le même que celui de l'instruction
C rx = -ry.
    </td>
  </tr>
</table>

<h4><hr/> "<a id="mov">mov</a>" : MOVe register</h4>
<table class="instrd">
  <tr>    <td>Syntaxe : </td>                <td>mov rx, ry</td>  </tr>
  <tr>    <td>Mise à jour des flags : </td>  <td>Aucune</td>    </tr>
  <tr>
    <td>Description : </td>
    <td>
      Copie le contenu de ry dans rx. L'effet est le même que celui de l'instruction
      C rx = ry.
    </td>
  </tr>
</table>


<h4><hr/> "<a id="swp">swp</a>" : SWaP register</h4>
<table class="instrd">
  <tr>    <td>Syntaxe : </td>                <td>swp rx, ry</td>  </tr>
  <tr>    <td>Mise à jour des flags : </td>  <td>Aucune</td>    </tr>
  <tr>
    <td>Description : </td>
    <td>
      Echange le contenu du registre rx avec celui de ry.
    </td>
  </tr>
  <tr>
    <td>Exemple : </td>
    <td>
      <pre>
ll r1, 2097
ll r2, 6100
swp r1 , r2 # r1 vaut 6100, r2 vaut 2097
      </pre>
    </td>
  </tr>
</table>


<h4><hr/> "<a id="lc">lc</a>" : Load Constant</h4>
<table class="instrd">
  <tr>    <td>Syntaxe : </td>                <td>lc rx, n</td>  </tr>
  <tr>    <td>Mise à jour des flags : </td>  <td>Aucune </td>    </tr>
  <tr>
    <td>Description : </td>
    <td>
      Charge n dans les 2 quartets de poids faible de rx et propage le bit de signe
      de ces 2 quartets dans les 2 quartets de poids fort de rx.
    </td>
  </tr>
  <tr>
    <td>Exemple : </td>
    <td>
      <pre>
lc r1, 10        # r1 vaut 10,  soit %0000000000001010
lc r2, -10       # r2 vaut -10, soit %1111111111110110
lc r3, %11110110 # r3 vaut -10 aussi
      </pre>
    </td>
  </tr>
</table>


<h4><hr/> "<a id="ll">ll</a>" : Load Long constant</h4>
<table class="instrd">
  <tr>    <td>Syntaxe : </td>                <td>ll rx, n</td>  </tr>
  <tr>    <td>Mise à jour des flags : </td>  <td>Aucune</td>    </tr>
  <tr>
    <td>Description : </td>
    <td>
      Charge n dans le registre rx entier.
    </td>
  </tr>
  <tr>
    <td>Exemple : </td>
    <td>
      <pre>
ll r1, 10        # r1 vaut 10, soit  %0000000000001010
ll r2, -10       # r2 vaut -10, soit %1111111111110110
ll r3, %11110110 # r3 vaut %0000000011110110 , soit 246
      </pre>
    </td>
  </tr>
</table>


<h4><hr/> "<a id="ldr">ldr</a>" : LoaD Register</h4>
<table class="instrd">
  <tr>    <td>Syntaxe : </td>                <td>ldr rx, [ry]</td>  </tr>
  <tr>    <td>Mise à jour des flags : </td>  <td>Aucune</td>    </tr>
  <tr>
    <td>Description : </td>
    <td>
      Charge les 4 quartets stockés à l'adresse PC + (ry % SIGHT) dans rx.
      ry est signé et utilisé en entier.
    </td>
  </tr>
  <tr>
    <td>Temps d'execution</td>
    <td>
T (en fonction du mode) cycles par quartet à charger. On considère que le
quartet est lu au dernier cycle de son propre délai. Le processeur lit les quartets
du poids faible au poids fort de la constante.
Par exemple, si T vaut 5, au premier cycle d'exécution il ne se passe rien,
aux deuxième, troisième et quatrième cycle non plus, puis au
cinquième cycle il lit le quartet de poids faible de la constante dans la mémoire;
il attendra encore jusqu'au dixième cycle du temps d'exécution pour lire le
quartet de rang un, au quinzième pour lire le quartet de rang deux, et jusqu'au
vingtième pour lire le quartet de rang trois, c'est-à-dire le quartet de poids le
plus fort.<br/>
A la fin du vingtième cycle, le registre est chargé et l'instruction rend
la main immédiatement. Si un autre processeur venait à écrire dans la mémoire sur la constante,
par exemple, au dix-huitième cycle d'exécution, il faut que les trois quartets de
poids faible chargé à l'arrivée dans le registre soient ceux d'origine, alors que le
quartet de poids fort sera celui d'après l'écriture.
    </td>
  </tr>
</table>


<h4><hr/> "<a id="str">str</a>" : STore Register</h4>
<table class="instrd">
  <tr>    <td>Syntaxe : </td>                <td>str [rx], ry</td>  </tr>
  <tr>    <td>Mise à jour des flags : </td>  <td>Aucune</td>    </tr>
  <tr>
    <td>Description : </td>
    <td>
      Stocke les 4 quartets de ry dans les 4 quartets stockes à l'adresse PC + (rx
      %% SIGHT). rx est signé et utilisé en entier.
    </td>
  </tr>
  <tr>
    <td>Temps d'exécution</td>
    <td>
      Exactement la même chose que pour LDR.
      Bien sûr, l'instruction str écrit dans la mémoire au lieu d'y lire.
    </td>
  </tr>
</table>


<h4><hr/> "<a id="ldb">ldb</a>" : LoaD Buffer</h4>
<table class="instrd">
  <tr>    <td>Syntaxe : </td>                <td>ldb [rx], n, m</td>  </tr>
  <tr>    <td>Mise à jour des flags : </td>  <td>Aucune</td>    </tr>
  <tr>
    <td>Description : </td>
    <td>
    Lit à partir de l'adresse PC + rx les m premiers quartets et les stocke à partir
    de l'offset n du tampon. Le tampon est circulaire, donc si m est plus grand que
    la taille entre l'offset n et la fin du tampon, les quartets surnuméraires seront
    écrits au début du tampon.
    </td>
  </tr>
  <tr>
    <td>Temps d'éxécution : </td>
    <td>
      Exactement la même chose que pour LDR.
      Bien sûr, l'instruction ldb est susceptible de lire bien plus de quatre quartets :
      ainsi le temps d'exécution de l'instruction ldb [r1], 0, 14 sera de 14 * T
      (T en fonction du mode).
    </td>
  </tr>
</table>


<h4><hr/> "<a id="stb">stb</a>" : STore Buffer</h4>
<table class="instrd">
  <tr>    <td>Syntaxe : </td>                <td>stb [rx], n, m</td>  </tr>
  <tr>    <td>Mise à jour des flags : </td>  <td> Z et S </td>    </tr>
  <tr>
    <td>Description : </td>
    <td>
      Écrit à l'adresse PC + rx les m premiers quartet à partir de l'offset n du tampon.
      Le tampon est circulaire, donc si m est plus grand que la taille entre l'offset
      n et la fin du tampon, les quartets surnuméraires seront lus au début du tampon.
    </td>
  </tr>
  <tr>
    <td>Temps d'éxécution : </td>
    <td>
      Exactement la même chose que pour STB, en écriture bien entendu.
    </td>
  </tr>
</table>


<h4><hr/> "<a id="b">b</a>" : Branch</h4>
<table class="instrd">
  <tr>    <td>Syntaxe : </td>                <td>b rx</td>  </tr>
  <tr>    <td>Mise à jour des flags : </td>  <td>Aucune</td>    </tr>
  <tr>
    <td>Description : </td>
    <td>
      Effectue un saut relatif inconditionnel de rx quartets (PC = PC + rx, conditionné
      par SIGHT). rx est signé et utilisé en entier.
    </td>
  </tr>
</table>


<h4><hr/> "<a id="bz">bz</a>" : Branch if Zero</h4>
<table class="instrd">
  <tr>    <td>Syntaxe : </td>                <td>bz rx</td>  </tr>
  <tr>    <td>Mise à jour des flags : </td>  <td>Aucune</td>    </tr>
  <tr>
    <td>Description : </td>
    <td>
      Effectue un saut relatif de rx quartets si le flag Z vaut 1 (PC = PC + rx conditionné
      par SIGHT)). rx est signé et utilisé en entier.
    </td>
  </tr>
</table>


<h4><hr/> "<a id="bnz">bzn</a>" : Branch if Not Zero</h4>
<table class="instrd">
  <tr>    <td>Syntaxe : </td>                <td>bnz rx</td>  </tr>
  <tr>    <td>Mise à jour des flags : </td>  <td>Aucune</td>    </tr>
  <tr>
    <td>Description : </td>
    <td>
    Effectue un saut relatif de rx quartets si Z = 0 (PC = PC + rx conditionné
    par SIGHT)). rx est signé et utilisé en entier.
    </td>
  </tr>
</table>


<h4><hr/> "<a id="bs">bs</a>" : Branch if Signed</h4>
<table class="instrd">
  <tr>    <td>Syntaxe : </td>                <td>bs rx</td>  </tr>
  <tr>    <td>Mise à jour des flags : </td>  <td>Aucune</td>    </tr>
  <tr>
    <td>Description : </td>
    <td>
      Effectue un saut relatif de rx quartets si S = 1 (PC = PC + rx conditionné
      par SIGHT)). rx est signé et utilisé en entier.
    </td>
  </tr>
</table>


<h4><hr/> "<a id="crash">crash</a>"</h4>
<table class="instrd">
  <tr>    <td>Syntaxe : </td>                <td>crash</td>  </tr>
  <tr>    <td>Mise à jour des flags : </td>  <td>Aucune </td>    </tr>
  <tr>
    <td>Description : </td>
    <td>
      Tout processeur qui exécute cette instruction est détruit instantanément.
    </td>
  </tr>
</table>


<h4><hr/> "<a id="write">write</a>"</h4>
<table class="instrd">
  <tr>    <td>Syntaxe : </td>                <td>write rx</td>  </tr>
  <tr>    <td>Mise à jour des flags : </td>  <td>Aucune</td>    </tr>
  <tr>
    <td>Description : </td>
    <td>
      Affiche sur la sortie standard le quartet de poids faible du registre rx.
      Utile pour debugguer son vaisseau.
    </td>
  </tr>
</table>


<h4><hr/> "<a id="stat">stat</a>"</h4>
<table class="instrd">
  <tr>    <td>Syntaxe : </td>                <td>stat rx, n</td>  </tr>
  <tr>    <td>Mise à jour des flags : </td>  <td>Aucune</td>    </tr>
  <tr>
    <td>Description : </td>
    <td>
      Charge une statistique de la machine virtuelle dans un des registres du processeur exécutant stat.
      <ul>
        <li>0 : met rx à 0 vector</li>
        <li>1 : charge dans rx le mode de fonctionnement du vaisseau (voir 4.1.2 pour les valeurs entières des modes)</li>
        <li>2 : copie dans rx le contenu du PC</li>
        <li>3 : copie dans rx le contenu du W'O''</li>
        <li>4 : copie dans rx le nombre de checkpoints validés par le processeur depuis le départ</li>
        <li>5 : copie dans rx l'adresse de départ du processeur</li>
        <li>6 : copie dans rx la taille en quartet de la mémoire de la vm</li>
        <li>7 : copie dans rx le nombre de tours à réaliser</li>
        <li>8 : copie dans rx le nombre de checkpoints par tour</li>
        <li>9 : copie dans rx la taille en quartet d'une étape</li>
        <li>10 : copie dans rx le nombre maximum de cycles pour valider une étape</li>
        <li>11 : copie dans rx le nombre de cycles restant pour faire un check avant que le vaisseau ne soit détruit</li>
        <li>12 : copie dans rx la place du processeur (1 si le processeur est premier, 2 s'il est deuxième, etc.)</li>
        <li>13 : charge dans rx la distance signée la plus petite en valeur absolue entre le PC du processeur courant et celui du processeur locké</li>
        <li>14 : charge dans rx le mode du processeur locké</li>
        <li>15 : copie dans le bit 0 (le bit de poids le plus faible) de rx le contenu de Z et dans le bit 1 le contenu de S.</li>
      </ul>
    </td>
  </tr>
</table>


<h4><hr/> "<a id="check">check</a>"</h4>
<table class="instrd">
  <tr>    <td>Syntaxe : </td>                <td>check</td>  </tr>
  <tr>    <td>Mise à jour des flags : </td>  <td>Z </td>    </tr>
  <tr>
    <td>Description : </td>
    <td>
      Tente de valider une étape. Le fonctionnement n'affecte pas S. Z est posé si
      le check a réussi, effacé s'il a échoué.
    </td>
  </tr>
</table>


<h4><hr/> "<a id="mode">mode</a>"</h4>
<table class="instrd">
  <tr>    <td>Syntaxe : </td>                <td>mode m</td>  </tr>
  <tr>    <td>Mise à jour des flags : </td>  <td>Aucune</td>    </tr>
  <tr>
    <td>Description : </td>
    <td>
      Demande un changement de mode, avec M # {feisar, goteki45, agsystems, auricom, assegai, piranha, qirex, icaras, rocket, missile, mines, plasma}.
      Si m est supérieur à 11, cette instruction est sans effet, mais consomme tout de même ses temps de décodage et d'exécution.
    </td>
  </tr>
</table>


<h4><hr/> "<a id="fork">fork</a>"</h4>
<table class="instrd">
  <tr>    <td>Syntaxe : </td>                <td>fork</td>  </tr>
  <tr>    <td>Mise à jour des flags : </td>  <td>Z</td>    </tr>
  <tr>
    <td>Description : </td>
    <td>
      Demande la duplication d'un processeur. Z vaut 1 dans un de deux  processeurs et 0 dans l'autre.
    </td>
  </tr>
</table>


<h4><hr/> "<a id="nop">nop</a>" : Not an OPeration</h4>
<table class="instrd">
  <tr>    <td>Syntaxe : </td>                <td>nop</td>  </tr>
  <tr>    <td>Mise à jour des flags : </td>  <td>Aucune</td>    </tr>
  <tr>
    <td>Description : </td>
    <td>
      Ne fait rien (peut être utilisé pour padder du code)
    </td>
  </tr>
</table>

