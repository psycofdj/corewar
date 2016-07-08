<html>
  <head>
    <title> Corewar : Championnats F6100 </title>
    <link rel="stylesheet" type="text/css" href="/css/style.css">
    <script type="text/javascript" src="/js/jquery.js"></script>
    <script type="text/javascript" src="/js/sprintf.js"></script>
    <script type="text/javascript" src="/js/jquery.validate.js"></script>
    <script type="text/javascript" src="/js/localization/messages_fr.js"></script>
    <script src="/js/codemirror.js"></script>
    <link rel="stylesheet" href="/css//codemirror.css">
    <script src="/js/f6100.js"></script>
    <link rel="stylesheet" href="/css/ui-lightness/jquery-ui-1.10.3.custom.min.css" />
    <script src="/js/jquery-ui-1.10.3.custom.min.js"></script>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <link rel="icon" type="image/gif" href="/img/favicon.gif">
  </head>
  <body>
    <table id="main_table">
      <tr>
        <td id="main_header_cell">
          <%include file="header.tpl"/>
        </td>
      </tr>
      <tr>
        <td id="main_content_cell">
          <table id="content_table">
            <tr>
              <td id="content_menu_cell">
                <%include file="menu.tpl"/>
              </td>
              <td id="content_page_cell">
                <%include file="${page}"/>
              </td>
            </tr>
          </table>
        </td>
      </tr>
      <tr>
        <td id="main_footer_cell">
          <%include file="footer.tpl"/>
        </td>
      </tr>
    </table>
  </body>
</html>
