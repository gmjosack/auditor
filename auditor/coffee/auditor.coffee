window.auditor = {}

class Attribute
    constructor: (@name, @values) ->

window.auditor.atBottom = (elem) ->
    return (elem[0].scrollHeight - elem.scrollTop()) == elem.innerHeight();



Handlebars.registerHelper 'ifEmpty', (context, options) ->
    if $.isEmptyObject context
        return options.fn this
    else
        return options.inverse this
