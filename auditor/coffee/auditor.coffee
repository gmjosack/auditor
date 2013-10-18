window.auditor = {}

class Attribute
    constructor: (@name, @values) ->

window.auditor.atBottom = (elem) ->
    return (elem[0].scrollHeight - elem.scrollTop()) === elem.innerHeight();

