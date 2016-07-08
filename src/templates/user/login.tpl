<style>
  #container {
    width:100%;
    max-width:600px;
    margin:0px auto;
  }
  .other { font-size: 12px; padding-top:10px;}
</style>

<script type="text/javascript">
  $(document).ready(function() {
    $("form").validate();
  });
</script>


<div id="container">
<form action="" method="post">
  <input type="hidden" name="p_dest" value="${p_dest}"/>
  <table class="form">
    <caption>Connexion</caption>
    <tr>
      <td>eMail :</td>
      <td><input class="required" type="email" name="p_mail"
                 % if p_mail:
                    value="${p_mail}"
                 % endif
                 /></td>
    </tr>
    <tr>
      <td>Mot de passe : </td>
      <td> <input class="required" type="password" name="p_password"
                  % if p_password:
                  value="${p_password}"
                  % endif
                  /> </td>
    </tr>
    <tr>
      <td colspan="2">
        <input type="submit" value="Envoyer"/><br/>
        <div class="other">
          Pas encore inscrit ? <a href="/user/register">c'est par là</a></br>
          Mot de passe perdu ? <a href="/user/recover">cliquez ici</a></br>
        </div>
      </td>
    </tr>
  </table>
</form>

% if error:
<div class="errormsg">
  Identifiants incorrects
</div>
% endif

</div>
