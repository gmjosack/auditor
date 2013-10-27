// Generated by CoffeeScript 1.6.1
(function() {
  var auditor;

  auditor = {};

  window.auditor = auditor;

  auditor.atBottom = function(elem) {
    return (elem[0].scrollHeight - elem.scrollTop()) === elem.innerHeight();
  };

  auditor.updateRow = function(row, event) {
    return row.find("td").each(function(idx, elem) {
      var td;
      td = $(elem);
      if (td.hasClass("event-expander")) {
        td.find("a").attr("data-target", "#toggle-details-" + event.id);
      }
      if (td.hasClass("event-summary")) {
        td.html(event.summary || "");
      }
      if (td.hasClass("event-user")) {
        td.html(event.user || "");
      }
      if (td.hasClass("event-tags")) {
        td.html(event.tags || "");
      }
      if (td.hasClass("event-level")) {
        td.html(event.level || "");
      }
      if (td.hasClass("event-start")) {
        if (event.start) {
          td.html(moment(event.start).format());
        } else {
          td.html("");
        }
      }
      if (td.hasClass("event-end")) {
        if (event.end) {
          return td.html(moment(event.end).format());
        } else {
          return td.html("");
        }
      }
    });
  };

  auditor.addAttribute = function(data) {
    var elem;
    elem = $("#event-attributes-" + data.event_id);
    if (elem.hasClass("no-attributes")) {
      elem.html("");
      elem.removeClass("no-attributes");
    }
    return $.each(data.data, function(key, value) {
      var span;
      span = elem.find("span[data-attribute-key='" + key + "'][data-id='" + data.event_id + "']");
      if (!span.length) {
        elem.append("<div>\n    <b>" + key + ":</b>\n    <span data-attribute-key=\"" + key + "\" data-id=\"" + data.event_id + "\" class=\"event-attribute\"></span>\n</div>");
      }
      span = elem.find("span[data-attribute-key='" + key + "'][data-id='" + data.event_id + "']");
      if (data.op_type === "append") {
        if (!!span.html().length) {
          span.append(", ");
        }
        return span.append(value);
      } else {
        return span.html(value);
      }
    });
  };

  auditor.addStream = function(data) {
    var active, atBottom, elem, new_stream, no_text;
    active = "";
    no_text = $("span.event-stream-text.no-text[data-id='" + data.event_id + "']");
    if (no_text.length) {
      no_text.remove();
      active = "active";
    }
    new_stream = false;
    elem = $(".event-stream-text[data-id='" + data.event_id + "'][data-name='" + data.data.name + "']");
    if (!elem.length) {
      new_stream = true;
      $("#event-details-" + data.event_id + " .nav-tabs").append("<li class=\"" + active + "\">\n  <a href=\"#event-stream-" + data.event_id + "-" + data.data.name + "\" data-toggle=\"tab\">" + data.data.name + "</a>\n<li>");
      $("#event-details-" + data.event_id + " .tab-content").append("<div class=\"tab-pane " + active + "\" id=\"event-stream-" + data.event_id + "-" + data.data.name + "\">\n    <pre data-id=\"" + data.event_id + "\" data-name=\"" + data.data.name + "\" class=\"event-stream-text\">" + data.data.text + "</pre>\n</div>");
    }
    elem = $(".event-stream-text[data-id='" + data.event_id + "'][data-name='" + data.data.name + "']");
    atBottom = false;
    if (auditor.atBottom(elem)) {
      atBottom = true;
    }
    if (!new_stream) {
      if (data.op_type === "set") {
        elem.html(data.data.text);
      } else if (data.op_type === "append") {
        elem.append(data.data.text);
      }
    }
    if (atBottom) {
      return elem.stop().scrollTop(elem[0].scrollHeight);
    }
  };

  Handlebars.registerHelper("ifEmpty", function(context, options) {
    if ($.isEmptyObject(context)) {
      return options.fn(this);
    }
    return options.inverse(this);
  });

  Handlebars.registerHelper("first", function(context, options) {
    if (context === 0) {
      return options.fn(this);
    }
  });

  Handlebars.registerHelper("join", function(context, options) {
    if (_.isString(context)) {
      context = [context];
    }
    return context.join(options.hash.delimeter);
  });

}).call(this);
