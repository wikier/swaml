# SWAML htaccess rules

# FIXME: customize base URI
# FIXME: dynamic customize of last rule

RewriteEngine On

Options -MultiViews

RewriteRule ^(.*) http://wopr:8180/openrdf-http-server-2.0-beta5/repositories/prueba/?query=CONSTRUCT+{<http://swaml.berlios.de/demos/sioc-dev/$1>+?y+?z}+WHERE+{<http://swaml.berlios.de/demos/sioc-dev/$1>+?y+?z}&queryLn=sparql [R=303]
