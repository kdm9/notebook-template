all_html=$(patsubst %.md,www/%.html,$(wildcard */index.md))


all:$(all_html)
serve: $(all_html)
	@x-www-browser http://localhost:1313 &
	caddy file-server --browse --root www  --listen 0.0.0.0:1313

www/%/index.html: %/index.md
	@mkdir -p $(dir $@)
	./md2html $^ $(dir $@)
