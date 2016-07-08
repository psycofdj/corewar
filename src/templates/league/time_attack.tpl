<style>
  img.status { width:24px; }
  #result { max-width: 800px; margin:0px auto; font-size:14px;}

  #result caption { font-size: 22px; font-weight:bold;  font-family:impact; text-transform:uppercase;color:#355f7c; padding-bottom:20px; }
  #result > tbody > tr > th { text-align:center; border:1px #c0c0c0 dashed; padding:10px; border-right:0px; font-size:18px; }
  #result > tbody > tr > td { text-align:center; border:1px #c0c0c0 dashed; border-top:0px; border-right:0px; padding:1px;}
  #result > tbody > tr > th:last-child,
  #result > tbody > tr > td:last-child { border-right:1px #c0c0c0 dashed; }
  #result > tbody > tr:nth-child(2) > td:first-child { border-top:1px #c0c0c0 dashed; }
  #result > tbody > tr > td:last-child {  }
  #result > tbody > tr > td:last-child form { display:inline; }
  #result > tbody > tr > td:last-child input { font-size:12px; padding:0px; }
  #result > tbody > tr > td:last-child select { font-size:12px; width:100px; margin-left:25px; color:#355f7c;border:1px #c0c0c0 solid; background:none; }
  #result > tbody > tr > td:last-child input[type=submit] { color:#355f7c;border:0px;background:none; font-size:14px; }
  #result > tbody > tr > td:last-child input[type=submit]:hover { text-decoration:underline; }

  form.log img { cursor:pointer; }
  #legend img { margin-bottom:-11px; padding-top:11px;width:32px;padding-left:15px; }
</style>

<script type="text/javascript">
  $(document).ready(function() {
    $("form.log img").click(function() {
      $(this).parents("form").first().submit();
    });
  });
</script>


<table id="result">
  <caption>Résultats de course<caption>
  <tr>
    <th></th>
    <th>Pilote</th>
    <th>Vaisseau</th>
    <th>Date</th>
    <th>Terminé</th>
    <th>Cycles</th>
    <th>Logs</th>
  </tr>
% for c_result in results:
  <tr>
    <td>
      % if not c_result["finished"]:
        <img class="status" src="/img/poop.png" title="Boouuuuhhhh !"/>
      % elif c_result["cycles"] < 3000:
       <img class="status" src="/img/nadeo.png" title="Médaille d'honneur ! Moins de 3000 cycles."/>
      % elif c_result["cycles"] < 10000:
       <img class="status" src="/img/gold.png" title="Médaille d'or ! Moins de 10000 cycles."/>
      % elif c_result["cycles"] < 15000:
       <img class="status" src="/img/silver.png" title="Médaille d'argent ! Moins de 15000 cycles."/>
      % elif c_result["cycles"] < 25000:
       <img class="status" src="/img/bronze.png" title="Médaille de bronze ! Moins de 25000 cycles."/>
      % else:
       <img class="status" src="/img/chocolat.png" title="Médaille en chocolat... peut mieux faire !"/>
      % endif
    </td>
    <td> ${c_result["nickname"]} </td>
    <td> ${c_result["name"]} </td>
    <td> ${c_result["date"].date()} </td>
    <td>
      % if c_result["finished"]:
        <img class="status" src="/img/ok.png" title="Ce vaisseau a terminé la course !"/>
      % else:
        <img class="status" src="/img/warning.png" title="Ce vaisseau n'a pas terminé la course."/>
      % endif
    </td>
    <td> ${c_result["cycles"]} </td>
    <td>
      % if c_result["uid"] == p_uid:
        <form action="/league/log" method="post" class="log">
          <input type="hidden" name="p_rid" value="${c_result['id']}"/>
          <img class="status" src="/img/log.png" title="Télécharger"/>
        </form>
      % else:
        &nbsp;
      % endif
    </td>
  </tr>
% endfor
</table>


<div id="legend" style="text-align:center;padding-top:20px;">
<span  style="text-align:left;display:inline-block;font-size:12px;">
<img class="status" src="/img/nadeo.png"    /> : 3000 cycles
<img class="status" src="/img/gold.png"     /> : 10000 cycles
<img class="status" src="/img/silver.png"   /> : 15000 cycles<br/>
<img class="status" src="/img/bronze.png"   /> : 25000 cycles
<img class="status" src="/img/chocolat.png" /> : Termine la course
<img class="status" src="/img/poop.png"     /> : Explose en plein vol<br/>
</span>
</div>
