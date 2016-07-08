# -*-coding:UTF-8 -*
#---------------------------------------------------------------------------#

import re
import logging
import random
import time
import os
import cherrypy
import signal

from pyscript               import config
from pyscript.tools         import daemonize
from pyscript.logger.object import LoggingObject

from corewar.webserver import home, news, rules, user, league, pit, about

#---------------------------------------------------------------------------#

class WebApplication(LoggingObject):

    class LoggerFilter(logging.Filter):
        def __init__(self, p_webapp, p_handler):
            self.m_app = p_webapp
            self.m_handler = p_handler

        def filter(self, x):
            l_message = re.sub(r".*\]", "", x.msg)
            if x.levelno < config.get("log", "web-level"):
                return False
            if x.levelno == 10:
                self.m_app.debug(self.m_handler, l_message)
            elif x.levelno == 20:
                self.m_app.info(self.m_handler, l_message)
            elif x.levelno == 30:
                self.m_app.warning(self.m_handler, l_message)
            elif x.levelno == 40:
                self.m_app.error(self.m_handler, l_message)
            elif x.levelno == 50:
                self.m_app.exception(self.m_handler, l_message)
            return False

    def __init__(self):
        LoggingObject.__init__(self, "webapp")
        self.registerHandler("engine", "[engine]")
        self.registerHandler("request", "[req]")

    def __buildConfig(self):
        l_appPath = os.path.dirname(os.path.realpath(__file__))
        l_appPath = os.path.dirname(l_appPath)
        l_appPath = os.path.dirname(l_appPath)
        l_config = {
            'global':
                {
                'server.socket_host' : config.get("web", "host"),
                'server.socket_port' : config.get("web", "port"),
                'server.thread_pool' : config.get("web", "threads"),
                'log.screen' : True,
                'log.access_file' : config.get("log", "file") + ".access",
                'log.error_file'  : config.get("log", "file") + ".error",
                'tools.sessions.on' : True,
                'tools.sessions.storage_type' : "file",
                'tools.sessions.storage_path' : config.get("web", "session-path"),
                'tools.sessions.timeout' : 60*24*365,
                'tools.encode.on' : True,
                'tools.encode.encoding' : 'utf8',
                'tools.encode.debug' : True,
                'tools.gzip.on': True,
                },
            '/pit/run':
                {
                'response.stream': True
                },
            '/css' :
                {
                'tools.staticdir.on' : True,
                'tools.staticdir.dir' : os.path.join(l_appPath, "css"),
                'tools.sessions.on' : False,
                },
            '/js' :
                {
                'tools.staticdir.on' : True,
                'tools.staticdir.dir' : os.path.join(l_appPath, "js"),
                'tools.sessions.on' : False,
                },
            '/include' :
                {
                'tools.staticdir.on' : True,
                'tools.staticdir.dir' : os.path.join(l_appPath, "include"),
                'tools.sessions.on' : False,
                },
            '/img' :
                {
                'tools.staticdir.on' : True,
                'tools.staticdir.dir' : os.path.join(l_appPath, "img"),
                'tools.sessions.on' : False,
                },
            }
        return l_config

    def getQuote(self):
        l_quotes = [
            """Tout ça pour une instruction en trop...
               J'ai perdu un cycle dans une boucle critique et tous mes espoirs se sont envolés.
               Je ne suis pas digne d'être un pilote.<br/>
               - Daniel Chang""",
            """Ça y est, tu t'es bien amusé ? Viens avec moi maintenant,
               je vais te montrer comment pilote un champion.<br/>
               - Kel Solaar""",
            """Les intructions, tu as toujours l'impression qu'il n'y en a pas assez.
               Toujours. Jusqu'a ce qu'un jour tu comprennes.<br/>
               - Anastasia Cherovosky""",
            """Ah ah ah ! Mais tu as vu comment tu l'as écrit ton vaisseau ? Tu peux
               même pas t'assoir de dans ! Je suis sûre qu'il ne compile même pas ! ...<br/>
               mais à quoi ils pensent chez Auricom, c'est pas avec un nul comme ça
               comme partenaire que je pourrai battre ma soeur...<br/>
               - Arian Tetsuo""",
            """Aaaaah, mon nouveau bébé doit être prêt... ... comment ça "invalid operand" ???<br/>
               - Anastasia Cherovosky""",
            """Le circuit, y'a des moments ou tu l'aimes et des moments ou tu le détestes
               C'est ton meileur complice et en même temps ton pire ennemi. C'est comme si t'étais
               amoureuse de lui.<br/>
               - Arian Tetsuo""",
            """Tu mets le contact, tu fais chauffer les réacteurs, tu mets les gaz et ensuite seulement
               tu appuies sur l'accelérateur. Il faut faire les choses dans l'ordre. Et après
               tu recommences.<br/>
               - Paul Jackson""",
            """C'est ça que j'aime, tu te mesures avec tes adversaires d'homme à homme, personne
               n'est avantagé.<br/>
               - John Dekka""",
            """Quand tu prends le rail, tu sens l'accélération d'un coup. Tu sens le danger,
               ton vaisseau qui tremble, prêt à se disloquer. Tu sens vraiment que tu pourrais
               tout péter d’une seconde à l'autre.<br/>
               Je suis peut-être un malade, mais c’est ça que j’aime. Tu vois, la course,
               c'est ma raison de vivre. Le rail, ça pourrait bien être ma raison de mourir. <br/>
               - Kel Solaar""",
            """Et le spectacle ? Si le public ne voit rien, ça ne sert à rien. <br/>
               - Arian Tetsuo""",
            """Toi, moi, la course. Je suis plus rapide que toi, et je vais te le prouver.<br/>
               - Kel Solaar""",
            """Une balle tombe, une goupille tombe, une homme chute. La gravité est la colle
               qui nous lie tous à notre planète. <br/>
               Nous somme sur le point d'utiliser un solvant qui va libérér notre espèce
               pour l'éternité.<br/>
               - Pierre Belmondo""",
            """Chez Auricom, ils utilisent la ruse. Chez nous on appel ça la peur.<br/>
               - Zala Wollf""",
            """Pense à boucler ta ceinture avant le départ, parce que quand on aura démarrré,<br/>
               l'accélération t’empêchera de bouger les bras.<br/>
               - Sophia de la Rente""",
            """La course, c'est le pilote, mais surtout le vaisseau ! Le meileur pilote ne fera rien<br/>
               sans un bon vaisseau. C'est pour ça qu'ils sont si importants, eux, les techniciens.<br/>
               Ce sont eux qui construisent ton vaisseau. Quand tu franchis la ligne en tête, c'est surtout<br/>
               eux qui ont gagné.<br/>
               - Kel Solaar""",
            """Regarde-moi ce bolide... C'est quand même autre chose qu'une bagnole... Les gens<br/>
               disent qu'ils veulent des sensations mais ils savent pas de quoi ils parlent. Ils ne sauront<br/>
               pas jusqu'à ce qu'ils aient les tripes de prendre le manche d'une de ces beautés.<br/>
               - Paul Jackson""",
            """Aaaah, mon nouveau bébé doit être prêt...<br/>
               ...comment ça ``Invalid operand'' ? ? ?<br/>
               - Anastasia Cherovoski""",
            """Regarde. Elle, c'est Sophia de la Rente. Elle court pour Feisar. Chez Feisar, ils<br/>
               sont moins rapides mais ils sont plus fourbes. Quand tu as l'un d'eux au cul, tu ne<br/>
               sais jamais quand tu vas prendre un missile. Et lui là-bas, c'est Kel Solaar, de chez<br/>
               Qirex. Méfie-toi de lui. C'est le genre de mec qui te foncera dessus parce qu'il sait qu'il<br/>
               peut compter sur sa coque, et qui te pulvérisera au passage. Et après il ira faire une<br/>
               belle gerbe de feu dans le mur. Ils contrôlent pas leurs vaisseaux. C'est eux les plus dangereux.<br/>
               - John Dekka""",
            """Recommences.<br/>
               - Paul Jackson"""
            ]
        l_idx = random.randint(0, len(l_quotes) - 1)
        return l_quotes[l_idx].decode('utf8')

#     def __initLogging(self):
#         l_app = self
#         class LoggerWrapper(logging.Logger):
#             def __init__(self, p_name):
#                 logging.Logger.__init__(self, p_name)
#                 if p_name.find("cherrypy") != -1:
#                     self.addFilter(WebApplication.LoggerFilter(l_app, "request"))
#         logging.setLoggerClass(LoggerWrapper)

#         logging.getLogger("cherrypy.error").addFilter(WebApplication.LoggerFilter(l_app, "engine"))
#         logging.getLogger("cherrypy.access").addFilter(WebApplication.LoggerFilter(l_app, "engine"))

    def __launch(self):
        #self.__initLogging()
        l_webTree        = home.Page(self)
        l_webTree.user   = user.Page(self)
        l_webTree.news   = news.Page(self)
        l_webTree.rules  = rules.Page(self)
        l_webTree.league = league.Page(self)
        l_webTree.pit    = pit.Page(self)
        l_webTree.about  = about.Page(self)
        l_config = self.__buildConfig()
        cherrypy.quickstart(l_webTree, "", l_config)

    def restart(self):
        if not self.stop():
            return False
        if not self.start():
            return False
        return True

    def stop(self):
        self.info("engine", "stopping web server")
        l_pidFile = config.get("web", "pid-file")
        l_pid     = daemonize.get_pid_from_file(l_pidFile)
        if not daemonize.is_running(l_pid):
            self.error("engine", "webserver not started")
            return False
        os.kill(l_pid, signal.SIGKILL)
        time.sleep(2)
        return True

    def start(self):
        self.info("engine", "starting web server")
        l_pidFile = config.get("web", "pid-file")
        l_pid     = daemonize.get_pid_from_file(l_pidFile)
        if daemonize.is_running(l_pid):
            self.error("engine", "webserver already started")
            return False
        if config.get("web", "daemonize"):
            daemonize.daemonize(l_pidFile)
        self.__launch()
        return True
#---------------------------------------------------------------------------#
