<style>
  img.status { width:24px; }
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
  }

  div.loader div {
     width:100%;
     height:100%;
     opacity:0.5;
     background:#000000;
  }

  #ships { max-width: 800px; margin:0px auto; }
  #ships > tbody > tr > th { text-align:center; border:1px #c0c0c0 dashed; padding:10px; border-right:0px; font-size:18px; }
  #ships > tbody > tr > td { text-align:center; border:1px #c0c0c0 dashed; border-top:0px; border-right:0px; padding:5px; }

  #ships > tbody > tr > th:last-child,
  #ships > tbody > tr > td:last-child { border-right:1px #c0c0c0 dashed; }
  #ships > tbody > tr:nth-child(2) > td:first-child { border-top:1px #c0c0c0 dashed; }

  #ships > tbody > tr > td:nth-child(4) {  }
  #ships > tbody > tr > td:nth-child(4) form { display:inline; }
  #ships > tbody > tr > td:nth-child(4) input { font-size:12px; padding:0px; }
  #ships > tbody > tr > td:nth-child(4) select { font-size:12px; width:100px; margin-left:25px; color:#355f7c;border:1px #c0c0c0 solid; background:none; }

  #ships > tbody > tr > td:nth-child(4) input[type=submit] { color:#355f7c;border:0px;background:none; font-size:14px; }
  #ships > tbody > tr > td:nth-child(4) input[type=submit]:hover { text-decoration:underline; }
</style>

<script type="text/javascript">
  $(document).ready(function() {
    $("form.run").submit(function() {
      $("#loader").addClass("loader");
    });

    $("form.delete").submit(function() {
      var l_name = $(this).parents("tr").first()
                     .find("td:first-child").text();
      l_name = $.trim(l_name);
      return confirm("Êtes vous certain de vouloir supprimer le vaisseau '" + l_name + "' ?");
    });
  });
</script>

<h2>Liste de vos vaisseaux</h2>

<div id="loader">
  <div>
  </div>
</div>

% if "duplicate" in errors:
  <br/>
  <div class="errormsg" id="errors">
   Ce vaisseau a déjà participé à cette course.<br/>
   Veuillez utiliser un autre vaisseau ou modifier les plans de celui-ci.
  </div>
  <br/>
% endif

<a class="racename" href="/pit/edit">Nouveau vaisseau</a>
<br/>
<br/>
<table id="ships">
  <tr>
    <th></th>
    <th>Nom</th>
    <th>Dernière modification</th>
    <th>Actions</th>
  </tr>
% for c_ship in ships:
  <tr>
    <td>
      % if c_ship["compiles"] == 0:
        <img class="status" src="/img/warning.png" title="Ce vaisseau ne compile pas !"/>
      % else:
        <img class="status" src="/img/ok.png" title="Ce vaisseau ne compile pas !"/>
      % endif
    </td>
    <td> ${c_ship["name"]} </td>
    <td> ${c_ship["date"]} </td>
    <td>

      <form action="/pit/run" method="post">
        <input type="hidden" name="shipID" value="${c_ship['id']}"/>
      % if c_ship["compiles"] == 1:
        <input class="racename" type="submit" value="Essayer"/>
      % else:
        <input class="racename" type="submit" value="Essayer" disabled="disabled" style="color:#a0a0a0;"/>
      % endif
      </form>

      <form action="/pit/run_gui" method="post" target="_blank">
        <input type="hidden" name="shipID" value="${c_ship['id']}"/>
      % if c_ship["compiles"] == 1:
        <input class="racename" type="submit" value="Visualiser"/>
      % else:
        <input class="racename" type="submit" value="Visualiser" disabled="disabled" style="color:#a0a0a0;"/>
      % endif
      </form>

      <form action="/pit/edit" method="post">
        <input type="hidden" name="p_shipID" value="${c_ship['id']}"/>
        <input class="racename" type="submit" value="Modifier"/>
      </form>
      <form action="/pit/delete" method="post" class="delete">
        <input type="hidden" name="p_shipID" value="${c_ship['id']}"/>
        <input class="racename" type="submit" value="Supprimer"/>
      </form><br/>
      <form class="run" action="/pit/apply" method="post">
        <input type="hidden" name="p_shipID" value="${c_ship['id']}"/>
        <select name="p_leagueType" class="racename">
          <option value="time">Time attack</option>
          <option disabled="disabled" value="dirtyrace">Dirty Race</option>
          <option disabled="disabled" value="viralexpansion">Viral Expansion</option>
          <option disabled="disabled" value="totalannihilation">Total annihilation</option>
        </select>
        % if c_ship["compiles"] == 0:
          <input class="racename" type="submit" value="Concourir" disabled="disabled"  style="color:#a0a0a0;"/>
        % else:
          <input class="racename" type="submit" value="Concourir"/>
        % endif
      </form>
    </td>
  </tr>
% endfor
</table>
