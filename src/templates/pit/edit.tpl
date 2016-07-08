<style>
	td#content_page_cell {
    padding-right:20px !important;
    padding-left:20px !important;
  }

  #editor {
    height:500px;
  }

  #editor > tbody > tr > td { vertical-align:top; }
  #editor > tbody > tr >  td:first-child { width: 20%; }
  #editor > tbody > tr >  td:nth-child(2) { width: 60%; padding:10px; }
  #editor > tbody > tr >  td:nth-child(3) { padding:10px; width: 20%; }

  #code {
    resize:none;
    width:100%;
    height:100%;
    overflow:visible;
  }

  #toolbar {
    text-align:center;
  }

  #toolbar input[type=submit] {
     background-size:24px 24px;
     width:32px;
     height:32px;
     background-repeat:no-repeat;
     background-position:center center;
     -webkit-border-radius: 5px;
     -moz-border-radius: 5px;
     border-radius: 5px;
     border:1px black solid;
     background-color:#e0e0e0;
     -webkit-box-shadow:  3px 3px 7px 1px ;
     box-shadow:  3px 3px 7px 1px ;
     margin:10px;
  }

 .ui-autocomplete {
    max-height: 400px;
    overflow-y: auto;
    /* prevent horizontal scrollbar */
    overflow-x: hidden;
    font-size:12px;
  }

  #toolbar input[type=submit]:hover { background-color:#f0f0f0; }
  #undo    { background-image: url('/img/undo.png');    }
  #redo    { background-image: url('/img/redo.png');    }
  #compile { background-image: url('/img/compile.png'); }
  #save    { background-image: url('/img/save.png');    }
  #close   { background-image: url('/img/close.png');   }
  #autosave{ background-image: url('/img/check.png');   }
  #autosave.pressed{ background-image: url('/img/checked.png');   }
  #codeeditor{ background-image: url('/img/check.png');   }
  #codeeditor.pressed{ background-image: url('/img/checked.png');   }
  #lastsave { font-size: 10px; }

  #container {
    width:100%;
    max-width:600px;
    margin:0px auto;
  }
  .other { font-size: 12px; padding-top:10px;}

  #instr_data { font-size: 14px;   min-width:280px; }
  #instr_data > tbody > tr > td:nth-child(n+2) > input { width:100%; }
  #instr_data > tbody > tr > td:first-child { text-align:right; padding:5px 10px; width:40%; }
  #instr_data > tbody > tr > td:noth-child(n+2) { width:60%; }


  #instr_code { font-size: 12px; cell-spacing:0px; border-spacing:0px; }
  #instr_code > tbody > tr > td { width:14.28%; text-align:center; border:1px #c0c0c0 dashed; }
  #instr_code > tbody > tr:nth-child(n+2) > td { width:14.28%; border-top:none; }
  #instr_code > tbody > tr:first-child > td { font-weight:bold; }

  #hexgo, #decgo, #bingo { width: 45px; }
  #hex,   #dec,   #bin   { text-align:right; text-transform:uppercase;}


  .errormsg, .successmsg, .warningmsg { margin-bottom:15px; font-size:14px; }
  .warningmsg { text-align:left; padding-left:40px }

  div.loader {
     top:0px;
     left:0px;
     position:fixed;
     z-index:1;
     background-image:url('/img/loader-big.gif');
     background-repeat:no-repeat;
     background-position:50% 50%;
     height:100%;
     width:100%;
     opacity:1;
  }

  div.loader div {
     width:100%;
     height:100%;
     opacity:0.5;
     background:#000000;
  }

</style>

<script type="text/javascript">

  var instructions = [
    ["crash", "",           "Destruction",                                         "0000"],
    ["nop",   "",           "No operation",                                        "0001"],
    ["and",   "rx, ry",     "ET logique registre à registre",                      "0010 rx ry"],
    ["or",    "rx, ry",     "OU logique registre à registre",                      "0011 rx ry"],
    ["xor",   "rx, ry",     "OU exclusif registre à registre",                     "0100 rx ry"],
    ["not",   "rx, ry",     "Négation binaire de registre à registre",             "0101 rx ry"],
    ["rol",   "rx, n",      "Rotation à gauche d'un registre",                     "0110 rx n"],
    ["asr",   "rx, n",      "Décalage arithmétique à droite d'un registre",        "0111 rx n"],
    ["add",   "rx, ry",     "Addition registre à registre",                        "1000 rx ry"],
    ["sub",   "rx, ry",     "Soustraction registre à registre",                    "1001 rx ry"],
    ["cmp",   "rx, ry",     "Comparaison registre à registre",                     "1010 rx ry"],
    ["neg",   "rx, ry",     "Calcul de l'opposé de registre à registre",           "1011 rx ry"],
    ["mov",   "rx, ry",     "Déplacement de données registre à registre",          "1100 rx ry"],
    ["ldr",   "rx, [ry]",   "Chargement de données mémoire à registre",            "1101 rx ry"],
    ["str",   "[rx], ry",   "Stockage de données registre à mémoire",              "1110 rx ry"],
    ["ldb",   "[rx], n, m", "Chargement du tampon",                                "1111 0000 rx n0 n1 m0 m1"],
    ["stb",   "[rx], n, m", "Ecriture du tampon",                                  "1111 0001 rx n0 n1 m0 m1"],
    ["lc",    "rx, n",      "Chargement de données immédiates courtes à registre", "1111 0010 rx n0 n1"],
    ["ll",    "rx, n",      "Chargement de données immédiates longues à registre", "1111 0011 rx n0 n1 n2 n3"],
    ["swp",   "rx, ry",     "Echange de contenu de registre",                      "1111 0100 rx ry"],
    ["addi",  "rx, n",      "Addition immédiate à registre",                       "1111 0101 rx n"],
    ["cmpi",  "rx, n",      "Comparaison immédiate à registre",                    "1111 0110 rx n"],
    ["b",     "rx",         "Saut inconditionnel",                                 "1111 0111 rx"],
    ["bz",    "rx",         "Saut conditionnel (si Z posé)",                       "1111 1000 rx"],
    ["bnz",   "rx",         "Saut conditionnel (si Z non posé)",                   "1111 1001 rx"],
    ["bs",    "rx",         "Saut conditionnel (si S posé)",                       "1111 1010 rx"],
    ["stat",  "rx, n",      "Chargement de statistique dans un registre special",  "1111 1011 rx n"],
    ["check", "",           "Validation d'une étape",                              "1111 1100"],
    ["mode",  "m",          "Changement de mode",                                  "1111 1101 m"],
    ["fork",  "",           "Demande d'entrée en duplication",                     "1111 1110"],
    ["write", "rx",         "Affchage d'un registre sur la sortie standard",       "1111 1111 rx"]
  ]

  function clock() {
    var l_text  = $("#lastsave").find("span").html();
    var l_parts = l_text.split(":");
    var l_date = new Date(0);
    l_date.setHours(parseInt(l_parts[0]));
    l_date.setMinutes(parseInt(l_parts[1]));
    l_date.setSeconds(parseInt(l_parts[2]) + 1);
    var l_newText = sprintf("%02d:%02d:%02d", l_date.getHours(), l_date.getMinutes(), l_date.getSeconds());
    $("#lastsave").find("span").html(l_newText);
  }

  function displayInfo(p_instrName) {
    var l_instr = null;
    for (var i = 0; i < instructions.length; i++)
      if (p_instrName == instructions[i][0])
         l_instr = instructions[i];

    $("#instr_syn").html("<a href='/rules/instructions#" + l_instr[0] + "'>" + l_instr[0] + "</a> " + l_instr[1]);
    $("#instr_descr").html(l_instr[2]);
    l_parts = l_instr[3].split(" ");
    for (var i = 0; i < 7; i++)
      $("#instr_code" + i).html("");
    for (var i = 0; i < l_parts.length; i++)
      $("#instr_code" + i).html(l_parts[i]);
  }

  function saveCode(p_code, p_location) {
      $("#errors,#success,#warnings").hide().html("");
      $("#loader").addClass("loader");
      $.ajax({
        type  : "POST",
        url   : "/pit/save",
        cache : false,
        data  : { "p_shipID" : $("#shipid").val(),
                  "p_shipCode" : p_code }
      }).fail(function(p_http, p_error, p_exception) {
        $("#errors").append(p_error);
        $("#errors").fadeIn();
        $("#loader").removeClass("loader");
      }).done(function(p_data, p_status, p_http) {
        if (p_data["errors"].length == 0) {
          $("#shipid").val(p_data["id"]);
          $("#success").append("Le vaisseau a été sauvegardé.");
          $("#success").fadeIn();
          $("#lastsave").find("span").html("00:00:00");
          if (p_location != null) {
            window.setTimeout(function() {
              window.location.href = p_location;
            }, 2000);
          }
        }
        else {
          for (var i = 0; i < p_data["errors"].length; i++) {
            if (p_data["errors"][i] == "duplicate")
              $("#errors").append("Ce nom de vaisseau est déjà utilisé");
            else if (p_data["errors"][i] == "noname")
              $("#errors").append("Vous devez donner un nom a votre vaisseau avec la directive .name");
            $("#errors").fadeIn();
          }
        }
        for (var i = 0; i < p_data["messages"].length; i++)
        {
           if (p_data["messages"][i][0] == "error") {
              $("#warnings").append(p_data["messages"][i][1]);
              $("#warnings").append("<br/>");
              $("#warnings").fadeIn();
           }
        }
        $("#loader").removeClass("loader");
      });
  }


  function compileCode(p_code) {
      $("#errors,#warnings,#success").hide().html("");
      $("#loader").addClass("loader");
      $.ajax({
        type  : "POST",
        url   : "/pit/compile",
        cache : false,
        data  : { "p_shipCode" : p_code }
      }).fail(function(p_http, p_error, p_exception) {
        $("#errors").append(p_error);
        $("#errors").fadeIn();
        $("#loader").removeClass("loader");
      }).done(function(p_data, p_status, p_http) {
        for (var i = 0; i < p_data["messages"].length; i++)
        {
           $("#warnings").append(p_data["messages"][i]);
           $("#warnings").append("<br/>");
           $("#warnings").fadeIn();
        }
        if (p_data["messages"].length == 0) {
           $("#success").append("Assemblage du vaisseau réussi.");
           $("#success").fadeIn();
        }
        $("#loader").removeClass("loader");
      });
  }



  $(document).ready(function() {
    $("#errors,#success,#warnings").hide().html("");
    var instr = [];
    for (var i = 0; i < instructions.length; i++)
      instr.push(instructions[i][0]);
    instr.sort();
    $("#instr").autocomplete({
        source : instr,
        minLength : 0,
        select : function(p_event, p_ui) { displayInfo(p_ui.item.value); }
    });

    $("#instr").focus(function() {
       $(this).autocomplete("search");
    }).click(function() {
       $(this).select();
    });


    function getCode() {
      if (true == $("#codeeditor").hasClass("pressed"))
        return myCodeMirror.getValue();
      return $("#code").val();
    }

    window.setInterval(function() {
      if (true == $("#autosave").hasClass("pressed"))
        saveCode(getCode());
    }, 60000);

    $("#undo").click(function() {
      var l_doc = myCodeMirror.getDoc();
      l_doc.undo();
    });

    $("#redo").click(function() {
      var l_doc = myCodeMirror.getDoc();
      l_doc.redo();
    });

    $("#close").click(function() {
      saveCode(getCode(), "/pit/list");
    });

    $("#save").click(function() {
      saveCode(getCode(), null);
    });

    $("#compile").click(function() {
      compileCode(getCode());
    });

    $("#autosave").click(function() {
       $(this).toggleClass("pressed");
    });

    $("#codeeditor").click(function() {
       $(this).toggleClass("pressed");
       if (false == $(this).hasClass("pressed")) {
         $("#undo,#redo").fadeOut();
         myCodeMirror.toTextArea();
       }
       else {
         el = document.getElementById("code");
         myCodeMirror =
              CodeMirror.fromTextArea(el, {
                  lineNumbers   : true,
                  undoDepth     : 9999,
                  smartIndent   : false,
                  electricChars : false });
         myCodeMirror.setSize("100%", "100%");
         $("#undo,#redo").fadeIn();
       }
    });

    $("#hexgo").click(function() {
      var l_val = parseInt($("#hex").val(), 16);
      $("#dec").val(l_val.toString(10));
      $("#bin").val(l_val.toString(2));
    });

    $("#decgo").click(function() {
      var l_val = parseInt($("#dec").val(), 10);
      $("#hex").val(l_val.toString(16));
      $("#bin").val(l_val.toString(2));
    });

    $("#bingo").click(function() {
      var l_val = parseInt($("#bin").val(), 2);
      $("#hex").val(l_val.toString(16));
      $("#dec").val(l_val.toString(10));
    });


    if ($("#code").val().length < 5000)
      $("#codeeditor").click();

    window.setInterval(clock, 1000);
  });
</script>

<h2 style="padding:0px;">Édition de vaisseau</h2>


<table id="editor">
  <tr>
    <td>
      <div id="toolbar">
        <input type="submit" id="codeeditor" title="Éditeur"                value=""/><br/>
        <input type="submit" id="undo"       title="Défaire"                value=""/><br/>
        <input type="submit" id="redo"       title="Refaire"                value=""/><br/>
        <input type="submit" id="compile"    title="Compiler"               value=""/><br/>
        <input type="submit" id="save"       title="Sauvegarder"            value=""/><br/>
        <input type="submit" id="close"      title="Sauvegarder & Fermer"   value=""/><br/>
        <input type="submit" id="autosave"   title="Sauvegarde automatique" value=""/><br/>
        <span id="lastsave"> Dernière sauvegarde :<br/> <span>00:00:00</span> </span>
      </div>
    </td>
    <td>
<div class="errormsg"   id="errors"></div>
<div class="successmsg" id="success"></div>
<div class="warningmsg"   id="warnings"></div>

<input id="shipid" type="hidden"
% if ship:
value="${ship['id']}"
% else:
value="0"
% endif
/>

<div id="loader">
  <div>
  </div>
</div>


<textarea name="p_shipCode" id="code">
% if ship:
${ship["code"]}
% else:
.name    "nom du vaisseau"
.comment "commentaire"
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
% endif
</textarea>
    </td>
    <td>
      <table id="instr_data">
        <tr>
          <td><input type="submit" id="hexgo" value="hex"/> : </td>
          <td><input type="text" id="hex" value=""/> </td>
        </tr>
        <tr>
          <td><input type="submit" id="decgo" value="dec"/> : </td>
          <td><input type="text" id="dec" value=""/> </td>
        </tr>
        <tr>
          <td><input type="submit" id="bingo" value="bin"/> : </td>
          <td><input type="text" id="bin" value=""/> </td>
        </tr>
        <tr>
          <td>Recherche : </td>
          <td><input id="instr"/></td>
        </tr>
        <tr>
          <td>Syntaxe : </td>
          <td id="instr_syn"></td>
        </tr>
        <tr>
          <td>Description :</td>
          <td id="instr_descr"></td>
        </tr>
        <tr>
          <td>Codage : </td>
          <td>
            <table id="instr_code">
              <tr>
                <td>q0</td>
                <td>q1</td>
                <td>q2</td>
                <td>q3</td>
                <td>q4</td>
                <td>q5</td>
                <td>q6</td>
              </tr>
              <tr>
                <td id="instr_code0"></td>
                <td id="instr_code1"></td>
                <td id="instr_code2"></td>
                <td id="instr_code3"></td>
                <td id="instr_code4"></td>
                <td id="instr_code5"></td>
                <td id="instr_code6"></td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
