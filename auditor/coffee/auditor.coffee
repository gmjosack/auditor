auditor = {}

window.auditor = auditor


auditor.atBottom = (elem) ->
    return (elem[0].scrollHeight - elem.scrollTop()) == elem.innerHeight()


auditor.updateRow = (row, event) ->
    row.find("td").each (idx, elem) ->
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


auditor.addAttribute = (data) ->
    elem = $("#event-attributes-#{data.event_id}")
    if elem.hasClass("no-attributes")
        elem.html("")
        elem.removeClass("no-attributes")

    $.each data.data, (key, value) ->
        span = elem.find("span[data-attribute-key='#{key}'][data-id='#{data.event_id}']")
        if not span.length
            elem.append("""
                <div>
                    <b>#{key}:</b>
                    <span data-attribute-key="#{key}" data-id="#{data.event_id}" class="event-attribute"></span>
                </div>
            """)

        span = elem.find("span[data-attribute-key='#{key}'][data-id='#{data.event_id}']")

        if data.op_type == "append"
            if !!span.html().length
                span.append(", ")
            span.append(value)
        else
            span.html(value)


auditor.addStream = (data) ->
    active = ""
    no_text = $("span.event-stream-text.no-text[data-id='#{data.event_id}']")
    if no_text.length
        no_text.remove()
        active = "active"

    new_stream = false
    elem = $(".event-stream-text[data-id='#{data.event_id}'][data-name='#{data.data.name}']")
    if not elem.length
        new_stream = true
        $("#event-details-#{data.event_id} .nav-tabs").append("""
            <li class="#{active}">
              <a href="#event-stream-#{data.event_id}-#{data.data.name}" data-toggle="tab">#{data.data.name}</a>
            <li>
        """)

        $("#event-details-#{data.event_id} .tab-content").append("""
            <div class="tab-pane #{active}" id="event-stream-#{data.event_id}-#{data.data.name}">
                <pre data-id="#{data.event_id}" data-name="#{data.data.name}" class="event-stream-text">#{data.data.text}</pre>
            </div>
        """)

    elem = $(".event-stream-text[data-id='#{data.event_id}'][data-name='#{data.data.name}']")

    atBottom = false
    if auditor.atBottom(elem)
        atBottom = true

    if not new_stream
        if data.op_type == "set"
            elem.html(data.data.text)
        else if data.op_type == "append"
            elem.append(data.data.text)

    if atBottom
        elem.stop().scrollTop(elem[0].scrollHeight)


Handlebars.registerHelper "ifEmpty", (context, options) ->
    if $.isEmptyObject context
        return options.fn this
    return options.inverse this


Handlebars.registerHelper "first", (context, options) ->
    if context == 0
        return options.fn this


Handlebars.registerHelper "join", (context, options) ->
    if _.isString(context)
        context = [context]
    return context.join(options.hash.delimeter)
