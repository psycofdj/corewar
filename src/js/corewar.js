var g_const;

var Core = new function() {
  var self = this;

  self.background = function(p_options) {
      p_options       = p_options       || {};
      p_options.func  = p_options.func  || function() {};
      p_options.pre   = p_options.pre   || function() {};
      p_options.post  = p_options.post  || function() {};
      p_options.begin = p_options.begin || 0;
      p_options.end   = p_options.end   || 0;

      if (true == p_options.func(p_options))
      {
        setTimeout(function() {
          self.background(p_options);
        }, g_const.m_timeScale);
      } else {
        p_options.post();
      }
  };

  self.colorLuminance = function(hex, lum) {
    // validate hex string
    hex = String(hex).replace(/[^0-9a-f]/gi, '');
    if (hex.length < 6) {
      hex = hex[0]+hex[0]+hex[1]+hex[1]+hex[2]+hex[2];
      }
    lum = lum || 0;

    // convert to decimal and change luminosity
    var rgb = "#", c, i;
    for (i = 0; i < 3; i++) {
      c = parseInt(hex.substr(i*2,2), 16);
      c = Math.round(Math.min(Math.max(0, c + (c * lum)), 255)).toString(16);
      rgb += ("00"+c).substr(c.length);
      }

    return rgb;
  };
};

Const = function(p_canvas_) {
  var self = this;

  self.construct = function(p_canvas) {
    self.m_repaintScale = 1;
    self.m_memorySize   = 65536;
    self.m_segmentSize  = 12;
    self.m_timeScale    = 0;
    self.m_menuWidth    = 420;
    self.m_width        = p_canvas_.width();
    self.m_pad          = 10;
    self.m_width        = $(window).width() - self.m_menuWidth;
    self.m_printWidth   = self.m_width - 2 * self.m_pad;
    self.m_nbCols       = Math.floor(self.m_printWidth / self.m_segmentSize);
    self.m_nbRows       = Math.ceil(self.m_memorySize / self.m_nbCols);
    self.m_printHeight  = (self.m_nbRows) * self.m_segmentSize;
    self.m_height       = self.m_printHeight + 2 * self.m_pad;
    self.m_segmentWidth = self.m_segmentSize - 1;
  };

  self.coordToAddr = function(p_left, p_top) {
    p_left -= (self.m_pad + self.m_menuWidth);
    p_top  -= self.m_pad;
    if ((p_left < 0) || (p_top < 0) ||
        (p_left > self.m_printWidth) || (p_top > self.m_printHeight))
      return null;
    var l_col = Math.floor(p_left / self.m_segmentSize);
    var l_row = Math.floor(p_top / self.m_segmentSize);
    return l_row * self.m_nbCols + l_col;
  };

  self.setSegmentSize = function(p_newSize) {
    self.m_segmentSize = p_newSize;
    self.m_nbCols      = Math.floor(self.m_printWidth / self.m_segmentSize);
    self.m_nbRows      = Math.ceil(self.m_memorySize / self.m_nbCols);
    self.m_printHeight = (self.m_nbRows) * self.m_segmentSize;
    self.m_height      = self.m_printHeight + 2 * self.m_pad;

    if (self.m_segmentSize < 7) {
      self.m_segmentWidth = self.m_segmentSize;
    } else {
      self.m_segmentWidth = self.m_segmentSize - 1;
    }
  };

  self.construct(p_canvas_);
};

var Status = function(p_corewar_) {
  var self = this;

  self.construct = function(p_corewar) {
    self.m_corewar = p_corewar;

  };

  self.construct(p_corewar_);
};

MemoryChunk = function(p_addr_) {
  var self = this;

  self.construct = function(p_addr) {
    self.m_readers     = null;
    self.m_color       = "#ffffff";
    self.m_baseColor   = "#ffffff";
    self.m_readColor   = "#ffffff";
    self.m_selectColor = "#00ff00";
    self.m_value       = 0;
    self.m_addr        = p_addr;
    self.m_row         = Math.floor(p_addr / g_const.m_nbCols);
    self.m_col         = p_addr % g_const.m_nbCols;
    self.m_selected    = false;
    self.m_read        = false;
  };

  self.startRead = function(p_ship) {
    self.m_read = true;
    self.updateColor();
  };

  self.stopRead = function(p_ship) {
    self.m_read = false;
    self.updateColor();
  };

  self.setOwner = function(p_ship) {
    self.m_baseColor = p_ship.m_writeColor;
    self.m_readColor = p_ship.m_pcColor;
    self.updateColor();
  };

  self.select = function() {
    self.m_selected = true;
    self.updateColor();
  };

  self.unselect = function() {
    self.m_selected = false;
    self.updateColor();
  };

  self.updateColor = function() {
    if (self.m_selected) {
      self.m_color = self.m_selectColor;
    } else if (self.m_read) {
      self.m_color = self.m_readColor;
    } else {
      self.m_color = self.m_baseColor;
    }
  };

  self.repaint = function(p_gui) {
    self.m_row   = Math.floor(self.m_addr / g_const.m_nbCols);
    self.m_col   = self.m_addr % g_const.m_nbCols;
    self.paint(p_gui);
  };

  self.paint = function(p_gui) {
    p_gui.fillStyle = self.m_color;
    p_gui.fillRect(g_const.m_pad + (self.m_col * g_const.m_segmentSize),
                   g_const.m_pad + (self.m_row * g_const.m_segmentSize),
                   g_const.m_segmentWidth,
                   g_const.m_segmentWidth);
  };

  self.construct(p_addr_);
};


Memory = function() {
  var self = this;

  self.construct = function() {
    self.m_size     = g_const.m_memorySize;
    self.m_items    = new Array();
    self.m_changes  = new Set();
    self.m_targetID  = null;

    for (var c_idx = 0; c_idx < self.m_size; c_idx++)
    {
      var l_chunk = new MemoryChunk(c_idx);
      self.m_items.push(l_chunk);
      self.m_changes.add(c_idx);
    }
  };

  self.setSelection = function(p_addr) {
    var l_res = null;

    if (self.m_targetID != null) {
      self.write(self.m_targetID).unselect();
    }
    if (p_addr != null) {
      l_res = self.write(p_addr);
      l_res.select();
    }
    self.m_targetID = p_addr;
    return l_res;
  };

  self.read = function(p_addr) {
    p_addr = p_addr % self.m_size;
    return self.m_items[p_addr];
  };

  self.write = function(p_addr) {
    p_addr = p_addr % self.m_size;
    self.m_changes.add(p_addr);
    return self.m_items[p_addr];
  };

  self.paint = function(p_gui) {
    for (var c_addr of self.m_changes) {
      self.m_items[c_addr].paint(p_gui);
    }
    self.m_changes.clear();
  };

  self.repaint = function(p_gui) {
    for (var c_item of self.m_items) {
      c_item.repaint(p_gui);
    }
    self.m_changes.clear();
  };

  self.construct();
};

Ship = function(p_map_, p_id_, p_name_, p_pos_, p_code_, p_status_) {
  var self = this;

  var WRITE_COLORS = [
    "#F78181", "#F7BE81", "#F3F781", "#BEF781", "#81F7F3", "#9F81F7", "#F781D8", "#FA5882"
  ];

  var PC_COLORS = [
    "#F55151", "#F39A39", "#EDF339", "#8DF221", "#21F2EB", "#5621F2", "#F221BA", "#E40742"
  ];

  self.construct = function(p_map, p_id, p_name, p_pos, p_code, p_status) {
    self.m_map             = p_map;
    self.m_id              = p_id;
    self.m_name            = p_name;
    self.m_pos             = p_pos;
    self.m_pc              = p_pos;
    self.m_code            = p_code;
    self.m_status          = p_status;
    self.m_state           = "reading";
    self.m_mode            = "Feisar";
    self.m_instr           = null;
    self.m_decodeDelay     = 0;
    self.m_execDelay       = 0;
    self.m_queue           = [];
    self.m_buffer          = new Array(64);
    self.m_writeColor      = WRITE_COLORS[self.m_id % WRITE_COLORS.length];
    self.m_pcColor         = PC_COLORS[self.m_id % PC_COLORS.length];
    self.m_s               = 0;
    self.m_z               = 0;
    self.m_registerChanged = true;
    self.m_bufferChanged   = true;
    self.m_queueChanged    = true;
    self.m_minCheck        = 8192;
    self.m_maxCheck        = 2 * 8192;
    self.m_checkChanged    = true;

    for (var c_idx = 0; c_idx < self.m_buffer.length; c_idx++) {
      self.m_buffer[c_idx] = 0;
    }
  };

  self.writeCode = function() {
    for (var c_idx = 0; c_idx < self.m_code.length; c_idx++) {
      var l_chunk = self.m_map.write(self.m_pc + c_idx);
      l_chunk.m_value = self.m_code[c_idx];
      l_chunk.setOwner(self);
    }
  };

  self.setDead = function() {
    self.m_map.write(self.m_pc).stopRead(self);
    self.m_status = "dead";
  };

  self.updatePC = function(p_newPC) {
    self.m_map.write(self.m_pc).stopRead(self);
    self.m_pc = p_newPC;
    self.m_map.write(self.m_pc).startRead(self);
  };

  self.construct(p_map_, p_id_, p_name_, p_pos_, p_code_, p_status_);
};



Corewar = function(p_canvasID_, p_data_) {
  var self = this;

  self.construct = function(p_canvasID, p_data) {
    self.m_data   = p_data;
    self.m_canvas = $("#" + p_canvasID);
    g_const       = new Const(self.m_canvas);
    self.m_canvas
      .css ("width",  g_const.m_width)
      .attr("width",  g_const.m_width)
      .css ("height", g_const.m_height)
      .attr("height", g_const.m_height)
    ;
    self.m_canvas[0].width = g_const.m_width;
    self.m_canvas[0].height = g_const.m_height;

    self.m_status       = new Gui();
    self.m_status.construct(self);

    self.m_gui      = self.m_canvas[0].getContext('2d');
    self.m_map      = new Memory();
    self.m_ships    = new Array(8);
    self.m_curCycle = 0;
    self.m_pause    = false;
    self.m_breakpoints = new Set([]);

    self.m_canvas.click(function(p_event) {
      var l_addr = g_const.coordToAddr(p_event.pageX, p_event.pageY);
      self.setSelection(l_addr);
      self.paint();
    });

    self.load();
  };

  self.setBreakpoints = function(p_bps) {
    self.m_breakpoints = new Set(p_bps);
  };

  self.addBreakpoint = function(p_bp) {
    self.m_breakpoints.add(p_bp);
  };

  self.deleteBreakpoint = function(p_bp) {
    self.m_breakpoints.delete(p_bp);
  };

  self.paint = function() {
    self.m_gui.beginPath();
    self.m_map.paint(self.m_gui);
    self.m_gui.stroke();
    self.m_status.paint();
  };

  self.repaint = function() {
    self.m_gui.beginPath();
    self.m_map.repaint(self.m_gui);
    self.m_gui.stroke();
    self.m_status.paint();
  };

  self.setSegmentSize = function(p_newSize) {
    g_const.setSegmentSize(p_newSize);
    self.m_canvas
      .css ("height", g_const.m_height)
      .attr("height", g_const.m_height)
    ;
    self.m_canvas[0].height = g_const.m_height;
    self.repaint();
  };

  self.setSelection = function(p_addr) {
    var l_chunk = self.m_map.setSelection(p_addr);
    self.m_status.m_vm.setSelection(l_chunk);
  };

  self.setTimeScale = function(p_value) {
    g_const.m_timeScale = p_value;
  };

  self.setRepaintScale = function(p_value) {
    g_const.m_repaintScale = p_value;
  };

  self.loadShip = function(p_data) {
    var l_ship = new Ship(self.m_map,
                          p_data.id,
                          p_data.name,
                          p_data.start_pos,
                          p_data.code,
                          p_data.status);

    l_ship.writeCode(self.m_map);
    l_ship.updatePC(l_ship.m_pc, self.m_map);
    self.m_ships[l_ship.m_id] = l_ship;
    self.m_status.addShip(l_ship);
  };

  self.step = function() {
    self.m_pause = false;
    self.m_status.m_vm.setStatus("Running");
    self.run({
      data :  self.m_data.cycles,
      begin : self.m_curCycle,
      end   : self.m_curCycle + 1
    });
    self.paint();
  };

  self.pause = function() {
    self.m_pause = true;
  };

  self.test = function() {
    requestAnimationFrame(self.test);
    self.run(self.m_opt);
  };

  self.play = function() {
    self.m_pause = false;
    self.m_status.m_vm.setStatus("Running");
    Core.background({
      data  : self.m_data.cycles,
      func  : self.run,
      post  : self.paint,
      begin : self.m_curCycle,
      end   : self.m_data.cycles.length
    });
  };

  self.load = function() {
    var l_init = self.m_data["init"];
    for (var c_item of l_init) {
      self.loadShip(c_item);
    }
    self.paint();
    self.m_status.m_vm.setStatus("Ready");
  };

  self.run = function(p_options) {
    var l_speeder = g_const.m_repaintScale;

    while ((l_speeder > 0) &&
           (false == self.m_pause) &&
           (p_options.begin < p_options.end))
    {
      var c_item = p_options.data[p_options.begin];
      for (var c_shipID in c_item.ships)
      {
        var l_ship = self.m_ships[c_shipID];
        var l_data = c_item.ships[c_shipID];

        if ((undefined != l_data.pc) && (l_ship.m_pc != l_data.pc)) {
          l_ship.updatePC(l_data.pc, self.m_map);
          l_ship.m_wo = l_data.wo;
        }

        for (var c_action of l_data.actions)
        {
          if (c_action.action == "write") {
            var l_chunk = self.m_map.write(c_action.chunk);
            l_chunk.m_value = c_action.value;
            l_chunk.setOwner(l_ship);
          }
          else if (c_action.action == "fetch") {
            l_ship.m_instr       = c_action.instr;
            l_ship.m_decodeDelay = c_action.decode;
            l_ship.m_execDelay   = c_action.execute;
          } else if (c_action.action == "state") {
            l_ship.m_state       = c_action.state;
            if (l_ship.m_state == "reading") {
              l_ship.m_instr       = null;
              l_ship.m_execDelay   = 0;
              l_ship.m_decodeDelay = 0;
            } else if (l_ship.m_state == "executing") {
              l_ship.m_decodeDelay = 0;
            }
          } else if (c_action.action == "decoding") {
            l_ship.m_decodeDelay = c_action.left;
          } else if (c_action.action == "executing") {
            l_ship.m_execDelay   = c_action.left;
          } else if (c_action.action == "read") {
            l_ship.m_queue         = c_action.queue;
            l_ship.m_queueChanged = true;
          } else if (c_action.action == "mode") {
            l_ship.m_mode       = c_action.value;
          } else if (c_action.action == "dead") {
            l_ship.setDead();
          } else if (c_action.action == "sz") {
            l_ship.m_z       = c_action.z;
            l_ship.m_s       = c_action.s;
          } else if (c_action.action == "write_buffer") {
            l_ship.m_buffer[c_action.offest] = c_action.value;
            l_ship.m_bufferChanged = true;
          } else if (c_action.action == "check") {
            l_ship.m_minCheck = c_action.next_min_check;
            l_ship.m_maxCheck = c_action.next_max_check;
            l_ship.m_checkChanged = true;
          } else if (c_action.action == "register") {
            var l_reg = null;
            if (c_action.name      == "r0")  l_ship.m_r0   = c_action.value;
            else if (c_action.name == "r1")  l_ship.m_r1   = c_action.value;
            else if (c_action.name == "r2")  l_ship.m_r2   = c_action.value;
            else if (c_action.name == "r3")  l_ship.m_r3   = c_action.value;
            else if (c_action.name == "r4")  l_ship.m_r4   = c_action.value;
            else if (c_action.name == "r5")  l_ship.m_r5   = c_action.value;
            else if (c_action.name == "r6")  l_ship.m_r6   = c_action.value;
            else if (c_action.name == "r7")  l_ship.m_r7   = c_action.value;
            else if (c_action.name == "r8")  l_ship.m_r8   = c_action.value;
            else if (c_action.name == "r9")  l_ship.m_r9   = c_action.value;
            else if (c_action.name == "r10") l_ship.m_r10  = c_action.value;
            else if (c_action.name == "r11") l_ship.m_r11  = c_action.value;
            else if (c_action.name == "r12") l_ship.m_r12  = c_action.value;
            else if (c_action.name == "r13") l_ship.m_r13  = c_action.value;
            else if (c_action.name == "r14") l_ship.m_r14  = c_action.value;
            else if (c_action.name == "r15") l_ship.m_r15  = c_action.value;
            l_ship.m_registerChanged = true;
          }
        }
      }
      if (self.m_breakpoints.has(self.m_curCycle)) {
        self.m_status.m_vm.pause();
      }

      p_options.begin += 1;
      self.m_curCycle = p_options.begin;
      l_speeder -= 1;
    }

    if (self.m_curCycle >= p_options.data.length)
      self.finish();
    self.paint();
    return (false == self.m_pause) && (p_options.begin < p_options.end);
  };

  self.reload = function() {
    self.m_status.clear();
    self.m_map      = new Memory();
    self.m_ships    = new Array(8);
    self.m_curCycle = 0;
    self.m_pause  = false;
    self.load();
  };

  self.finish = function() {
    var l_init = self.m_data["finish"];
    for (var c_item of l_init) {
      self.m_ships[c_item.id].m_status = c_item.status;
    }
    self.m_status.m_vm.pause();
    self.m_status.m_vm.setStatus("Finished");
    self.paint();
  };

  self.construct(p_canvasID_, p_data_);
};
