<html>
  <head>
    <title> Corewar : Championnats F6100 </title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <link rel="icon" type="image/gif" href="/img/favicon.gif">
    <!-- bower:css -->
    <link rel="stylesheet" href="/include/seiyria-bootstrap-slider/dist/css/bootstrap-slider.css" />
    <link rel="stylesheet" href="/include/bootstrap-css/css/bootstrap.min.css" />
    <!-- endbower -->
    <!-- bower:js -->
    <script src="/include/jquery/dist/jquery.js"></script>
    <script src="/include/seiyria-bootstrap-slider/js/bootstrap-slider.js"></script>
    <script src="/include/bootstrap-css/js/bootstrap.min.js"></script>
    <!-- endbower -->
    <script src="/js/corewar.js"></script>
    <script src="/js/gui.js"></script>
    <script src="/js/sprintf.js"></script>
    <style>
     canvas {
       width: 100%;
       height: 100%
     }

     body {
       margin: 0px;
       background-color: white;
       font-size:12px;
     }

     .slider {
       margin:5px;
       width:100% !important;
     }

     body {

     }

     .buffer {
       font-size:12px;
     }

     #ship {
       font-size:10px;
     }

     .buffer > tbody > tr > th,
     .buffer > thead > tr > th {
       text-align:right;
       font-size:10px;
     }

     .buffer > tbody > tr > td {
       padding:0px 0px;
       text-align:center;
       width:12.5%;
       font-size:10px;
     }

     .buffer > tbody > tr > th,
     .buffer > thead > tr > th {
       padding:0px 10px;
       text-align:center;
     }

     .buffer > tbody > tr > td:hover {
       background-color:#99FFB3;
     }

     #ship_registers table > tbody > tr > td {
       padding:0px 0px;
       text-align:center;
       width:100%;
       font-size:10px;
     }

     #ship_registers table > tbody > tr > th {
       padding:0px 10px;
       font-size:10px;
     }

     .container-fluid {
       padding:0px;
     }

     .panel {
       margin-bottom:0px;
     }

     .bp {
       padding:0px;
       min-width:35px;
       margin-top:1px;
     }
    </style>
  </head>
  <body style="margin:0; overflow:scroll;">
    <script>
      $(document).ready(function() {
       var l_corewar = new Corewar("container", ${data});
      });
    </script>
    <div class="container-fluid" style="padding:0px;">
      <div style="margin:0px;padding:0px;width:420;float:left;">
        <div id="vm" class="container-fluid col-lg-12">
          <div class="panel panel-primary">
            <div class="panel-heading"  style="padding:5px 15px;">
              <h3 class="panel-title" style="line-height:30px; height:30px">
                VM
              </h3>
            </div>
            <div class="panel-body">
              <div class="row">
                <div class="col-xs-4 text-right">Current cycle ID :</div>
                <div id="vm_cycle" class="col-xs-8">0</div>
              </div>
              <div class="row">
                <div class="col-xs-4 text-right">Race status :</div>
                <div id="vm_status" class="col-xs-8">Uninitialized</div>
              </div>
              <div class="row">
                <div class="col-xs-4 text-right">Display size (px) :</div>
                <div class="col-xs-8">
                  <input id="vm_segment" class="form-control"  data-slider-id='ex1Slider' type="text" data-slider-min="4" data-slider-max="30" data-slider-step="1" data-slider-value="12"/>
                </div>
              </div>
              <div class="row">
                <div class="col-xs-4 text-right">Cycle delay (ms) :</div>
                <div class="col-xs-8">
                  <input id="vm_scale" class="form-control" data-slider-id='ex1Slider' type="text" data-slider-min="0" data-slider-max="1000" data-slider-step="10" data-slider-value="0"/>
                </div>
              </div>
              <div class="row">
                <div class="col-xs-4 text-right">Repaint cycle : </div>
                <div class="col-xs-8">
                  <input id="vm_repaint" class="form-control" data-slider-id='ex1Slider' type="text" data-slider-min="1" data-slider-max="100" data-slider-step="1" data-slider-value="1"/>
                </div>
              </div>
              <div class="row">
                <div class="col-xs-4 text-right">Selected chunk  :</div>
                <div id="vm_selection_addr" class="col-xs-4"></div>
                <div id="vm_selection_value" class="col-xs-4"></div>
              </div>
              <div class="row">
                <div class="col-xs-4 text-right">Breakpoints  :</div>
                <div id="vm_breakpoints" class="col-xs-8">
                </div>
              </div>
            </div>
            <div class="panel-footer text-center" style="padding:2px;padding-bottom:3px;">
              <div class="row">
                <button id="vm_play"   type="button" class="btn btn-success glyphicon glyphicon-play"         data-toggle="tooltip" data-placement="top" title="Play"></button>
                <button id="vm_step"   type="button" class="btn btn-warning glyphicon glyphicon-arrow-right"  data-toggle="tooltip" data-placement="top" title="Step"></button>
                <button id="vm_pause"  type="button" class="btn btn-danger glyphicon glyphicon-stop"          data-toggle="tooltip" data-placement="top" title="Pause"></button>
                <button id="vm_reload" type="button" class="btn btn-primary glyphicon glyphicon-refresh"      data-toggle="tooltip" data-placement="top" title="Reload"></button>
              </div>
              <div class="row form-inline" style="padding-top:5px;">
                <input  id="vm_breakpoint_value"  class="form-control input-sm" style="" placeholder="Breakpoint to cycle..."/>
                <button id="vm_breakpoint_add"    class="btn btn-success btn-sm glyphicon glyphicon-plus"   data-toggle="tooltip" data-placement="top" title="Add breakpoint to cycle"></button>
                <button id="vm_breakpoint_delete" class="btn btn-danger btn-sm glyphicon glyphicon-refresh" data-toggle="tooltip" data-placement="top" title="Remove all breakpoints"></button>
              </div>
            </div>
          </div>
        </div>
        <div id="ship" class="container-fluid col-lg-12" style="margin-top:5px">
          <div class="panel panel-primary">
            <div class="panel-heading" style="padding:5px 15px;">
              <div class="row">
                <div class="col-xs-4 text-left">
                  <h3 class="panel-title" style="line-height:30px; height:30px">
                    Ship
                  </h3>
                </div>
                <div class="col-xs-8">
                  <select id="vm_ships" class="form-control input-sm">
                    <option>(none)</option>
                  </select>
                </div>
              </div>
            </div>
            <div class="panel-body">
              <div class="row">
                <div class="col-xs-4 text-right">Proc. ID : </div>
                <div id="ship_id" class="col-xs-8"></div>
              </div>
              <div class="row">
                <div class="col-xs-4 text-right">Name : </div>
                <div id="ship_name" class="col-xs-8"></div>
              </div>
              <div class="row">
                <div class="col-xs-4 text-right">Status : </div>
                <div id="ship_status" class="col-xs-8"></div>
              </div>
              <div class="row">
                <div class="col-xs-4 text-right">State : </div>
                <div id="ship_state" class="col-xs-8"></div>
              </div>
              <div class="row">
                <div class="col-xs-4 text-right">Mode : </div>
                <div id="ship_mode" class="col-xs-8"></div>
              </div>
              <div class="row">
                <div class="col-xs-4 text-right">WO : </div>
                <div id="ship_wo" class="col-xs-8"></div>
              </div>
              <div class="row">
                <div class="col-xs-4 text-right">PC : </div>
                <div id="ship_pc" class="col-xs-8"></div>
              </div>
              <div class="row">
                <div class="col-xs-4 text-right">Queue : </div>
                <div id="ship_queue" class="col-xs-8">  </div>
              </div>
              <div class="row">
                <div class="col-xs-4 text-right">Nect check (min) : </div>
                <div id="ship_min_check" class="col-xs-8">  </div>
              </div>
              <div class="row">
                <div class="col-xs-4 text-right">Next check (max) : </div>
                <div id="ship_max_check" class="col-xs-8">  </div>
              </div>
              <div class="row">
                <div class="col-xs-4 text-right">Bit registers : </div>
                <div id="" class="col-xs-8">
                  Z = <span id="ship_z"></span>
                  S = <span id="ship_s"></span>
                </div>
              </div>
              <div class="row">
                <div class="col-xs-4 text-right">Decode Delay : </div>
                <div id="ship_decode_delay" class="col-xs-8"></div>
              </div>
              <div class="row">
                <div class="col-xs-4 text-right">Exec Delay : </div>
                <div id="ship_execution_delay" class="col-xs-8"></div>
              </div>
              <div class="row">
                <div class="col-xs-4 text-right">Instruction : </div>
                <div id="ship_instr" class="col-xs-8" style="height:34px;"></div>
              </div>


              <div class="row">
                <div id="ship_registers" class="col-xs-12" style="padding:5px;">
                  <table class="table table-bordered table-condensed buffer" style="margin-bottom:0px;">
                    <caption class="text-center" style="padding:0px;"><u>Registers</u></caption>
                    <tbody>
                      <tr><th>r0</th><td id="ship_r0"></td></tr>
                      <tr><th>r1</th><td id="ship_r1"></td></tr>
                      <tr><th>r2</th><td id="ship_r2"></td></tr>
                      <tr><th>r3</th><td id="ship_r3"></td></tr>
                      <tr><th>r4</th><td id="ship_r4"></td></tr>
                      <tr><th>r5</th><td id="ship_r5"></td></tr>
                      <tr><th>r6</th><td id="ship_r6"></td></tr>
                      <tr><th>r7</th><td id="ship_r7"></td></tr>
                      <tr><th>r8</th><td id="ship_r8"></td></tr>
                      <tr><th>r9</th><td id="ship_r9"></td></tr>
                      <tr><th>r10</th><td id="ship_r10"></td></tr>
                      <tr><th>r11</th><td id="ship_r11"></td></tr>
                      <tr><th>r12</th><td id="ship_r12"></td></tr>
                      <tr><th>r13</th><td id="ship_r13"></td></tr>
                      <tr><th>r14</th><td id="ship_r14"></td></tr>
                      <tr><th>r15</th><td id="ship_r15"></td></tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <div class="row">
                <div id="ship_buffer" class="col-xs-12" style="padding:5px;">
                  <table class="table table-bordered table-condensed buffer"  style="margin-bottom:0px;">
                    <caption class="text-center" style="padding:0px;"><u>Buffer</u></caption>
                    <thead>
                      <tr>
                        <th></th>
                        <th>0</th>
                        <th>1</th>
                        <th>2</th>
                        <th>3</th>
                        <th>4</th>
                        <th>5</th>
                        <th>6</th>
                        <th>7</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <th>0+</th><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                      </tr>
                      <tr>
                        <th>8+</th><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                      </tr>
                      <tr>
                        <th>16+</th><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                      </tr>
                      <tr>
                        <th>24+</th><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                      </tr>
                      <tr>
                        <th>32+</th><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                      </tr>
                      <tr>
                        <th>40+</th><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                      </tr>
                      <tr>
                        <th>48+</th><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                      </tr>
                      <tr>
                        <th>56+</th><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div style="padding:0px;float:left;background-color:black;">
        <canvas id="container"></canvas>
      </div>
  </body>
</html>
