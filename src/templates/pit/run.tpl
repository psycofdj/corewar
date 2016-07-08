<style>
  #container {
    width:100%;
    max-width:400px;
    margin:0px auto;
  }
  .form td { width:50% !important; }
  .other { font-size: 12px; padding-top:10px;}
  #go {
    padding:0px;
    border:1px #c0c0c0 dashed;;
    width:250px;
  }
  #go.load {
    background-image: url('/img/loader.gif');
    background-repeat: no-repeat;
    background-position: 50% 50%;
    border:0px;
    background-color:inherit;
  }
  table.form tr:nth-child(n+2) td:nth-child(2) { font-size: 12px; }
  pre.active {
    border:1px #c0c0c0 dashed;
    background-color:#101010;
    color: #ddd;
    padding:5px;
    overflow-y:scroll;
    overflow-x:visible;
    font-family: "Lucida Console", Monospace;
  }
</style>

<script type="text/javascript">
  var l_data = null;

  $(document).ready(function() {
    $("input[type=radio]:nth-child(2)").attr("checked", true);
    $("#all").click(function() {
      $("tr input[type=radio]:first-child").attr("checked", true);
    });
    $("#none").click(function() {
      $("tr input[type=radio]:nth-child(2)").attr("checked", true);
    });

    $("#go").click(function() {
      var l_lastLoaded = 0;

      $("#log").text("");
      $("#go").addClass("load");
      $("pre").addClass("active");
      $("#go").val("");
      $("#go").attr("disabled", false);
      $("html").focus();

      $.ajax({
        type: "POST",
        url: "/pit/run/",
        data: {
           "run"     : "true",
           "shipID"  : "${shipID}",
           "init"    : $("input[name=init]:first-child").attr("checked"),
           "cycle"   : $("input[name=cycle]:first-child").attr("checked"),
           "read"    : $("input[name=read]:first-child").attr("checked"),
           "fetch"   : $("input[name=fetch]:first-child").attr("checked"),
           "delay"   : $("input[name=delay]:first-child").attr("checked"),
           "execute" : $("input[name=execute]:first-child").attr("checked"),
           "write"   : $("input[name=write]:first-child").attr("checked"),
           "other"   : $("input[name=other]:first-child").attr("checked")
        },
        xhr: function() {
          var xhr = new window.XMLHttpRequest();
          xhr.addEventListener("progress", function (p_event) {
            var l_loaded = p_event.loaded;
            $("#log").append(p_event.target.responseText.substring(l_lastLoaded, l_loaded));
            l_lastLoaded = l_loaded;
            $(window).scrollTop($(document).height());
          }, false);
          return xhr;
        },

        success: function(p_data, p_status, p_http) {
          $("#go").attr("disabled", false);
          $("#go").removeClass("load");
          $("#go").val("Go!");
        }
      });
      return false;
    });
  });
</script>

<div id="container">


  <table class="form">
    <caption>Paramètres de course</caption>
    <tr>
      <td>Vaisseau :</td>
      <td>  <b>${ship["name"]}</b> </td>
    </tr>
    <tr>
      <td>Log :</td>
      <td> <input id="all" name="all" type="radio"/> on <input id="none" name="all" type="radio"/> off</td>
    </tr>
    <tr>
      <td>init Log :</td>
      <td><input type="radio" name="init"/> on <input type="radio" name="init"/> off</td>
    </tr>
    <tr>
      <td>cycle Log :</td>
      <td><input type="radio" name="cycle"/> on <input type="radio" name="cycle"/> off</td>
    </tr>
    <tr>
      <td>lecture Log :</td>
      <td><input type="radio" name="read"/> on <input type="radio" name="read"/> off</td>
    </tr>
    <tr>
      <td>instruction Log :</td>
      <td><input type="radio" name="fetch"/> on <input type="radio" name="fetch"/> off</td>
    </tr>
    <tr>
      <td>délai Log :</td>
      <td><input type="radio" name="delay"/> on <input type="radio" name="delay"/> off</td>
    </tr>
    <tr>
      <td>éxécution Log :</td>
      <td><input type="radio" name="execute"/> on <input type="radio" name="execute"/> off</td>
    </tr>
    <tr>
      <td>écritures Log :</td>
      <td><input type="radio" name="write"/> on <input type="radio" name="write"/> off</td>
    </tr>
    <tr>
      <td>autre Log :</td>
      <td><input type="radio" name="other"/> on <input type="radio" name="other"/> off</td>
    </tr>

    <tr>
      <td colspan="2">
        <input id="go" type="button" value="Go !"/>
      </td>
    </tr>
  </table>

</div>
<br/><br/>
<pre style="font-size:10px;"  id="log"></pre>
