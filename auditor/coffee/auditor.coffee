window.auditor = {}

class Attribute
    constructor: (@name, @values) ->

window.auditor.atBottom = (elem) ->
    return (elem[0].scrollHeight - elem.scrollTop()) == elem.innerHeight()

Handlebars.registerHelper 'ifEmpty', (context, options) ->
    if $.isEmptyObject context
        return options.fn this
    return options.inverse this

Handlebars.registerHelper 'first', (context, options) ->
    if context == 0
        return options.fn this
