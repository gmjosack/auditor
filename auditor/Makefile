
.PHONY: all coffee handlebars

all: coffee handlebars

coffee:
	coffee --join auditor.js --output static/js --compile coffee/*.coffee

handlebars:
	handlebars -mf static/js/hb_templates.min.js handlebars/*.handlebars
