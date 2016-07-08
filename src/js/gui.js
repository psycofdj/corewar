function intToBin(p_value) {
  var l_int = parseInt(p_value);
  var l_bin = l_int.toString(2);
  var l_binStr = $.sprintf("%04d", parseInt(l_bin));
  return $.sprintf("[%s] (%d)", l_binStr, l_int);
}


GuiVm = function(p_corewar_) {
  var self = this;

  self.construct = function(p_corewar) {
    self.m_corewar       = p_corewar;
    self.m_container     = $("#vm");
    self.m_status        = $("#vm_status");
    self.m_segmentSize   = $("#vm_segment");
    self.m_timeScale     = $("#vm_scale");
    self.m_repaintScale  = $("#vm_repaint");
    self.m_cycle         = $("#vm_cycle");
    self.m_play          = $("#vm_play");
    self.m_step          = $("#vm_step");
    self.m_pause         = $("#vm_pause");
    self.m_reload        = $("#vm_reload");
    self.m_selection     = null;
    self.m_selectionAddr = $("#vm_selection_addr");
    self.m_selectionVal  = $("#vm_selection_value");

    self.m_breakpoints      = $("#vm_breakpoints");
    self.m_breakpointVal    = $("#vm_breakpoint_value");
    self.m_breakpointAdd    = $("#vm_breakpoint_add");
    self.m_breakpointDelete = $("#vm_breakpoint_delete");

    self.m_breakpointAdd.click(self.breakpointAdd);
    self.m_breakpointDelete.click(self.breakpointDeleteAll);

    self.m_segmentSize.slider ({ tooltip_position : "top"      });
    self.m_timeScale.slider   ({ tooltip_position : "bottom" });
    self.m_repaintScale.slider({ tooltip_position : "bottom" });

    self.m_pause.prop("disabled", true);
    self.m_reload.prop("disabled", true);

    self.m_segmentSize.on("slideStop", function(p_data) {
      self.m_corewar.setSegmentSize(p_data.value);
    });
    self.m_timeScale.on("slideStop", function(p_data) {
      self.m_corewar.setTimeScale(p_data.value);
    });
    self.m_repaintScale.on("slideStop", function(p_data) {
      self.m_corewar.setRepaintScale(p_data.value);
    });
    self.m_play.click(self.play);
    self.m_step.click(self.step);
    self.m_pause.click(self.pause);
    self.m_reload.click(self.reload);
  };

  self.breakpointAdd = function() {
    var l_value = parseInt(self.m_breakpointVal.val(), 10);
    if (false == isNaN(l_value)) {
      self.m_corewar.addBreakpoint(l_value);
      var l_item = $("<button>", {
        "class"          : "btn btn-sm btn-danger bp",
        "data-toggle"    : "tooltip",
        "data-placement" : "top",
        "title"          : "Remove breakpoint"
      });

      l_item.tooltip({ container : "body" });
      l_item.text(l_value);
      l_item.click(function() {
        self.breakpointDelete($(this), l_value);
      });
      self.m_breakpoints.append(l_item);
      self.m_breakpointVal.val("");
    }
  };

  self.breakpointDelete = function(p_obj, p_val) {
    p_obj.remove();
    self.m_corewar.deleteBreakpoint(p_val);
  };

  self.breakpointDeleteAll = function() {
    self.m_breakpoints.empty();
    self.m_corewar.setBreakpoints([]);
  };

  self.play = function() {
    self.m_play.prop("disabled", true);
    self.m_step.prop("disabled", true);
    self.m_reload.prop("disabled", true);
    self.m_pause.prop("disabled", false);
    self.m_corewar.play();
  };

  self.step = function() {
    self.m_play.prop("disabled", false);
    self.m_step.prop("disabled", false);
    self.m_reload.prop("disabled", false);
    self.m_pause.prop("disabled", true);
    self.m_corewar.step();
  };

  self.pause = function() {
    self.m_play.prop("disabled", false);
    self.m_step.prop("disabled", false);
    self.m_reload.prop("disabled", false);
    self.m_pause.prop("disabled", true);
    self.m_corewar.pause();
  };

  self.reload = function() {
    self.m_play.prop("disabled", false);
    self.m_step.prop("disabled", false);
    self.m_reload.prop("disabled", true);
    self.m_pause.prop("disabled", true);
    self.m_corewar.reload();
  };

  self.hide = function() {
    self.m_container.hide();
  };

  self.show = function() {
    self.m_container.show();
  };

  self.setStatus = function(p_status) {
    self.m_status.text(p_status);
  };

  self.paint = function() {
    self.m_cycle.text(self.m_corewar.m_curCycle - 1);
    if (self.m_selection != null) {
      self.m_selectionAddr.text("address : " + self.m_selection.m_addr);
      self.m_selectionVal.text("value : " + intToBin(self.m_selection.m_value));
    } else {
      self.m_selectionAddr.text("");
      self.m_selectionVal.text("");
    }
  };

  self.setSelection = function(p_chunk) {
    self.m_selection = p_chunk;
  };

  self.construct(p_corewar_);
};

GuiShip = function(p_corewar_) {
  var self = this;

  self.construct = function(p_corewar) {
    self.m_hidden      = false;
    self.m_corewar     = p_corewar;
    self.m_container   = $("#ship .panel-body");
    self.m_target      = null;
    self.m_id          = $("#ship_id");
    self.m_name        = $("#ship_name");
    self.m_status      = $("#ship_status");
    self.m_state       = $("#ship_state");
    self.m_instr       = $("#ship_instr");
    self.m_decodeDelay = $("#ship_decode_delay");
    self.m_execDelay   = $("#ship_execution_delay");
    self.m_mode        = $("#ship_mode");
    self.m_wo          = $("#ship_wo");
    self.m_pc          = $("#ship_pc");
    self.m_z           = $("#ship_z");
    self.m_s           = $("#ship_s");
    self.m_r0          = $("#ship_r0");
    self.m_r1          = $("#ship_r1");
    self.m_r2          = $("#ship_r2");
    self.m_r3          = $("#ship_r3");
    self.m_r4          = $("#ship_r4");
    self.m_r5          = $("#ship_r5");
    self.m_r6          = $("#ship_r6");
    self.m_r7          = $("#ship_r7");
    self.m_r8          = $("#ship_r8");
    self.m_r9          = $("#ship_r9");
    self.m_r10         = $("#ship_r10");
    self.m_r11         = $("#ship_r11");
    self.m_r12         = $("#ship_r12");
    self.m_r13         = $("#ship_r13");
    self.m_r14         = $("#ship_r14");
    self.m_r15         = $("#ship_r15");
    self.m_queue       = $("#ship_queue");
    self.m_buffer      = $("#ship_buffer");
    self.m_minCheck    = $("#ship_min_check");
    self.m_maxCheck    = $("#ship_max_check");
  };

  self.hide = function() {
    self.m_container.hide();
    self.m_hidden = true;
  };

  self.show = function() {
    self.m_container.show();
    self.m_hidden = false;
  };

  self.registerToStr = function(p_value) {
    var l_q0 = ((p_value >> 0)  & 0x000F).toString(2);
    var l_q1 = ((p_value >> 4)  & 0x000F).toString(2);
    var l_q2 = ((p_value >> 8)  & 0x000F).toString(2);
    var l_q3 = ((p_value >> 12) & 0x000F).toString(2);
    return $.sprintf("[%04d][%04d][%04d][%04d]", l_q3, l_q2, l_q1, l_q0);
  };

  self.writeBuffer = function(p_addr, p_text, p_val) {
    var l_row     = Math.floor(p_addr / 8);
    var l_col     = p_addr % 8;
    var l_fmtRow  = $.sprintf("tbody tr:nth-child(%d)", l_row + 1);
    var l_fmtCell = $.sprintf("td:nth-child(%d)", l_col + 2);
    var l_cRow    = $(l_fmtRow, self.m_buffer);
    var l_cell    = $(l_fmtCell, l_cRow);


    l_cell.data("toggle", "tooltip");
    l_cell.data("placement", "top");
    l_cell.attr("title", p_val);
    l_cell.tooltip({
      container : "body"
    });
    l_cell.text(p_text);
  };

  self.update = function() {
    if (self.m_hidden) {
      return;
    }

    if (self.m_target == null) {
      return;
    }

    self.m_id.text(self.m_target.m_id);
    self.m_name.text(self.m_target.m_name);
    self.m_pc.text(self.m_target.m_pc);
    self.m_wo.text(self.m_target.m_wo);
    self.m_status.text(self.m_target.m_status);
    self.m_state.text(self.m_target.m_state);
    self.m_decodeDelay.text(self.m_target.m_decodeDelay);
    self.m_execDelay.text(self.m_target.m_execDelay);
    self.m_mode.text(self.m_target.m_mode);
    self.m_z.text(self.m_target.m_z);
    self.m_s.text(self.m_target.m_s);

    if (self.m_target.m_queueChanged) {
      var l_queue = [];
      for (var c_idx = 0; c_idx < self.m_target.m_queue.length; c_idx++)
        l_queue.push($.sprintf("[%04d]", self.m_target.m_queue[c_idx].toString(2)));
      self.m_queue.text(l_queue.join(""));
      self.m_target.m_queueChanged = false;
    };

    if (self.m_target.m_bufferChanged) {
      for (var c_idx = 0; c_idx < self.m_target.m_buffer.length; c_idx++) {
        self.writeBuffer(c_idx,
                         $.sprintf("[%04d]", self.m_target.m_buffer[c_idx].toString(2)),
                         $.sprintf("offset : %s, value : %d", c_idx, self.m_target.m_buffer[c_idx]));
      }
      self.m_target.m_bufferChanged = false;
    }

    if (self.m_target.m_checkChanged) {
      self.m_minCheck.text(self.m_target.m_minCheck);
      self.m_maxCheck.text(self.m_target.m_maxCheck);
    }

    if (self.m_target.m_registerChanged) {
      self.m_r0.text(self.registerToStr(self.m_target.m_r0));
      self.m_r1.text(self.registerToStr(self.m_target.m_r1));
      self.m_r2.text(self.registerToStr(self.m_target.m_r2));
      self.m_r3.text(self.registerToStr(self.m_target.m_r3));
      self.m_r4.text(self.registerToStr(self.m_target.m_r4));
      self.m_r5.text(self.registerToStr(self.m_target.m_r5));
      self.m_r6.text(self.registerToStr(self.m_target.m_r6));
      self.m_r7.text(self.registerToStr(self.m_target.m_r7));
      self.m_r8.text(self.registerToStr(self.m_target.m_r8));
      self.m_r9.text(self.registerToStr(self.m_target.m_r9));
      self.m_r10.text(self.registerToStr(self.m_target.m_r10));
      self.m_r11.text(self.registerToStr(self.m_target.m_r11));
      self.m_r12.text(self.registerToStr(self.m_target.m_r12));
      self.m_r13.text(self.registerToStr(self.m_target.m_r13));
      self.m_r14.text(self.registerToStr(self.m_target.m_r14));
      self.m_r15.text(self.registerToStr(self.m_target.m_r15));
      self.m_registerChanged = false;
    }

    if (self.m_target.m_instr) {
      self.m_instr.text(self.m_target.m_instr);
    } else {
      self.m_instr.text("");
    }

  };

  self.setTarget = function(p_target) {
    self.m_target = p_target;
    self.paint();
  };

  self.paint = function() {
    self.update();
  };

  self.construct(p_corewar_);
};

Gui = function() {
  var self = this;

  self.construct = function(p_corewar) {
    self.m_corewar  = p_corewar;
    self.m_vm       = new GuiVm(p_corewar);
    self.m_ship     = new GuiShip(p_corewar);
    self.m_mode     ="vm";
    self.m_ships    = $("#vm_ships");
    $('[data-toggle="tooltip"]').tooltip({
      container : "body"
    });


    self.m_ship.hide();

    self.m_ships.change(function() {
      $("option:selected", $(this)).each(function() {
        var l_id = $(this).attr("id");
        self.selectShip(l_id);
      });
    });

    $("#vm .panel-heading").click(function() {
      $("#vm .panel-body").toggle();
      $("#vm .panel-footer").toggle();
    });

    $("#vm_ships .panel-heading").click(function() {
      $("#vm_ships .panel-body").toggle();
      $("#vm_ships .panel-footer").toggle();
    });
  };

  self.selectShip = function(p_id) {
    var l_ship = null;
    if (p_id != undefined) {
      self.m_ship.show();
      l_ship = self.m_corewar.m_ships[p_id];
    } else {
      self.m_ship.hide();
    }
    self.m_ship.setTarget(l_ship);
  };

  self.addShip = function(p_ship) {
    var l_opt = $("<option>", { "id" : p_ship.m_id });
    l_opt.text(p_ship.m_name + "(" + p_ship.m_id + ")");
    self.m_ships.append(l_opt);
  };

  self.clear = function() {
    $("option[id]", self.m_ships).remove();
    self.selectShip(undefined);
  };

  self.paint = function() {
    self.m_vm.paint();
    self.m_ship.paint();
  };

};
