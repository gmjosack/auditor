window.auditor = {}

class Attribute
    constructor: (@name, @values) ->

window.auditor.atBottom = (elem) ->
    return (elem[0].scrollHeight - elem.scrollTop()) == elem.innerHeight()


window.auditor.updateRow = (row, event) ->
    row.find('td').each (idx, elem) ->
        td = $(elem)

        if td.hasClass("event-expander")
            td.find("a").attr("data-target", "#toggle-details-" + event.id)

        if td.hasClass("event-summary")
            td.html(event.summary or "")
        if td.hasClass("event-user")
            td.html(event.user or "")
        if td.hasClass("event-tags")
            td.html(event.tags or "")
        if td.hasClass("event-level")
            td.html(event.level or "")

        if td.hasClass("event-start")
            if event.start
                td.html(moment(event.start).format())
            else
                td.html("")

        if td.hasClass("event-end")
            if event.end
                td.html(moment(event.end).format())
            else
                td.html("")


window.auditor.addAttribute = (data) ->
    elem = $("#event-attributes-#{data.event_id}")
    if elem.hasClass("no-attributes")
        elem.html("")
        elem.removeClass("no-attributes")

    # attribute-event_id-key has been moved to data attribtues.
    $.each data.data, (key, value) ->
        span = elem.find("span#attribute-#{data.event_id}-#{key}")
        if not span.length
            elem.append("<div><b>#{key}:</b> <span id='attribute-#{data.event_id}-#{key}'></span></div>")

        span = elem.find("span#attribute-#{data.event_id}-#{key}")

        if data.op_type == "append"
            if !!span.html().length
                span.append(", ")
            span.append(value)
        else
            span.html(value)

Handlebars.registerHelper 'ifEmpty', (context, options) ->
    if $.isEmptyObject context
        return options.fn this
    return options.inverse this

Handlebars.registerHelper 'first', (context, options) ->
    if context == 0
        return options.fn this
