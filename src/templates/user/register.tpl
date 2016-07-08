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
    <caption>Inscription</caption>
    <tr>
      <td>Prénom Nom :</td>
      <td><input class="required" type="text" name="p_name"/></td>
    </tr>
    <tr>
      <td>Pseudo :</td>
      <td><input class="required" type="text" name="p_nickname"/></td>
    </tr>
    <tr>
      <td>eMail : </td>
      <td> <input class="required" type="email" name="p_mail"/> </td>
    </tr>
    <tr>
      <td>Mot de passe : </td>
      <td> <input class="required" type="password" name="p_password"/> </td>
    </tr>

    <tr>
      <td colspan="2">
        <input type="submit" value="Envoyer"/><br/>
        <div class="other">
          - Seul le pseudo apparaîtra sur le site web mais les vrais noms des vainqueurs seront dévoilés<br/>
          - Le mail sert de login et à se faire envoyer un nouveau mot de passe. (100% nospam)<br/>
          - Les mots de passes de stockés cryptés en base.<br/>
        </div>
      </td>
    </tr>
  </table>
</form>

% if duplicate:
<div class="errormsg">
  L'utilisateur existe déjà (nom, pseudo et/ou mail)
</div>
% endif


</div>
