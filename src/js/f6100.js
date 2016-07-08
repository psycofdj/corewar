CodeMirror.defineMode("f6100", function () {
  var keyword_regex1 = /^(add|addi|and|asr|b|bnz|bs|bz|check|cmp|cmpi|crash|fork|lc|ldb|ldr|ll|mode|mov|neg|nop|not|or|rol|stat|stb|str|sub|swp|write|xor)(\b|,)/ig;
  var register       = /^(r0|r1|r2|r3|r4|r5|r6|r7|r8|r9|r10|r11|r12|r13|r14|r15)(,|\b)/ig;
  var registerderef  = /^(\[r0\]|\[r1\]|\[r2\]|\[r3\]|\[r4\]|\[r5\]|\[r6\]|\[r7\]|\[r8\]|\[r9\]|\[r10\]|\[r11\]|\[r12\]|\[r13\]|\[r14\]|\[r15\])(,|\b)/ig;
  var modes          = /^(feisar|goteki45|agsystems|auricom|assegai|piranha|qirex|icaras|rocket|missile|mine|plasma)(,|\b)/ig;

  return {
    startState: function () {
      return {
        inString: false,
        beforeTag: true,
        justMatchedKeyword: false,
        afterParen: false
      };
    },
    token: function (stream, state) {
      //check for state changes
      if (!state.inString && (stream.peek() == '"')) {
        stream.next(); // Skip quote
        state.inString = true; // Update state
      }
      //return state
      if (state.inString)
      {
        stream.skipTo('"');
        stream.next(); // Skip quote
        state.inString = false; // Clear flag
        return "string"; // Token style
      }
      else if (stream.match(/^([a-zA-Z][a-zA-Z0-9_]*[a-zA-Z0-9]:)/)) {
        return "def";
      }
      else if (stream.match(keyword_regex1)) {
        return "keyword";
      }
      else if (stream.match(registerderef)) {
        return "atom";
      }
      else if (stream.match(register)) {
        return "meta";
      }
      else if (stream.match(/^([-+]?%[01_]*[01])/)) {
        return "number";
      }
      else if (stream.match(/^([-+]?0x[a-fA-F0-9_]*[a-fA-F0-9])/)) {
        return "number";
      }
      else if (stream.match(/^([-+]?[0-9_]*[0-9])/)) {
        return "number";
      }
      else if (stream.match(modes)) {
        return "attribute";
      }
      else if (stream.match(/^#.*/)) {
        return "comment";
      }
      else if (stream.match(/^\.[a-zA-Z]+/)) {
        return "builtin";
      }
      else if (stream.match(/^([^\s]+)\s/i)) {
        return null;
      }
      stream.next();
      return null;
    }
  };
});

CodeMirror.defineMIME('text/x-6100', 'f6100');
