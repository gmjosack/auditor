
.PHONY: all coffee handlebars

all: coffee handlebars

coffee:
	coffee --join auditor.js --output static/js --compile coffee/*.coffee

handlebars:
	@for template in handlebars/*.handlebars; do \
		echo handlebars $$template -mf static/$${template%.handlebars}.min.js; \
		handlebars $$template -mf static/$${template%.handlebars}.min.js; \
	done
