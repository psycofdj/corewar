#!/usr/bin/python -O
# -*-coding:UTF-8 -*
#---------------------------------------------------------------------------#

import json
import sys

from pyscript                 import exceptions, config
from pyscript.config          import init_config
from pyscript.logger          import init_logging, get_logger

import corewar
import corewar.core
import corewar.core.vm
import corewar.core.pit

from corewar.core.data.ship        import Ship
from corewar.webserver.application import WebApplication

#---------------------------------------------------------------------------#




def process():
    if config.get("__internal", "compile") == True:
        for c_shipSource in config.get("__internal", "ships"):
            corewar.core.pit.pit.Pit().buildShipSource(c_shipSource, 0)
        if corewar.core.pit.pit.Pit().hasError():
            sys.exit(1)
        sys.exit(0)

    if config.get("general", "league") == 'race':
        l_type = corewar.core.vm.VirtualMachine.League.Race
    else:
        l_type = corewar.core.vm.VirtualMachine.League.Fight

    l_vm = corewar.core.vm.VirtualMachine(l_type)
    for c_shipSource in config.get("__internal", "ships"):
        l_vm.addShipSource(c_shipSource)

    if not l_vm.initialize():
        sys.exit(1)

    l_ships = l_vm.run()
    l_ships = l_vm.filterResults(l_ships, config.get("general", "result"))

    if config.get("general", "dump"):
        print json.dumps({"init" : l_vm.m_dataInit, "cycles" : l_vm.m_dataCycle, "finish" : l_vm.m_dataFinish}, sort_keys=True)
    else:
        print l_vm.printResult(l_ships)

def main():
    try:
        init_config(corewar.GLOBAL_CONFIG,
                    corewar.validation_handler,
                    corewar.cmdline_init_handler,
                    corewar.cmdline_process_handler)
        init_logging("%(asctime)s : %(message)s", "%d-%m-%y@%H:%M:%S")
    except exceptions.ConfigException, e:
        print str(e)
        sys.exit(1)

    l_webApp = WebApplication()
    if config.get("web", "action") == "start":
        if not l_webApp.start():
            sys.exit(1)
    elif config.get("web", "action") == "stop":
        if not l_webApp.stop():
            sys.exit(1)
    elif config.get("web", "action") == "restart":
        if not l_webApp.restart():
            sys.exit(1)
    else:
        process()
    sys.exit(0)


#---------------------------------------------------------------------------#

if __name__ == "__main__":
    main()

#---------------------------------------------------------------------------#
