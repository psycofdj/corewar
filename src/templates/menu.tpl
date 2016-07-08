<style>
 #connect { text-align:center; padding-bottom:15px;  }
</style>

<div id="connect">
% if logged:
  <a href="/user/logout"/> déconnexion </a>
% else:
  <a href="/user/login"/> connexion </a>
% endif
</div>

<div id="logo">
  <img id="logo" src="/img/logo_trans.png"/>
</div>



<ul>
  <li>
    <img src="/img/news.png"/>
    <a href="/news"> News </a><br/>
    <br/>
  </li>

  <li>
    <img src="/img/book.png"/>
    <a href="/rules"> Règles </a>
    <ul>
      <li> <a href="/rules/league">       - Epreuves       </a>  </li>
      <li> <a href="/rules/language">     - Language F6100 </a>  </li>
      <li> <a href="/rules/vm">           - Vm             </a>  </li>
      <li> <a href="/rules/instructions"> - Instructions   </a>  </li>
      <li> <a href="/rules/faq">          - F.A.Q.         </a>  </li>
    </ul>
    <br/>
  </li>

  <li>
    <img src="/img/cup.png"/>
    <a href="/league"> Compétitions </a>
    <ul>
      <li> <a href="/league/time_attack">        - Time         </a>  </li>
      <li> <a style="color:#a0a0a0;" disabled="disabled" href="/league/dirty_race">         - Race         </a>  </li>
      <li> <a style="color:#a0a0a0;" disabled="disabled" href="/league/viral_expansion">    - Viral        </a> </li>
      <li> <a style="color:#a0a0a0;" disabled="disabled" href="/league/total_annihilation"> - Annihilation </a> </li>
    </ul>
    <br/>
  </li>

  <li>
    <img src="/img/tools.png"/>
    <a href="/pit"> Stands </a>
    <br/><br/>
  </li>

  <li>
    <img src="/img/contact.png"/>
    <a href="/about"> A propos </a>
  </li>
</ul>



