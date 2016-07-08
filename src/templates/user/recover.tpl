<style>
  #container {
    width:100%;
    max-width:600px;
    margin:0px auto;
  }
  .other { font-size: 10px; padding-top:10px;}
</style>


<script type="text/javascript">
  $(document).ready(function() {
    $("form").validate();
  });
</script>

<div id="container">
<form action="" method="post">
  <table class="form">
    <caption>Regénération du mot de passe</caption>
      <td>eMail : </td>
      <td> <input class="required" type="email" name="p_mail"/> </td>
    </tr>
    <tr>
      <td colspan="2">
        <input type="submit" value="Envoyer"/><br/>
      </td>
    </tr>
  </table>
</form>

% if unknown:
<div class="errormsg">
  Cette adresse mail n'éxiste pas.
</div>
% endif

% if sent:
<div class="successmsg">
  Un nouveau mot de passe a été envoyé à l'adresse donnée.
</div>
% endif


</div>
