# SWAML htaccess rules

# FIXME: customize base URI
# FIXME: dynamic customize of last rule

RewriteEngine On

RewriteRule ^forum$ http://swaml.berlios.de/demos/swaml-devel/forum.rdf [R=303]
RewriteRule ^subscribers$ http://swaml.berlios.de/demos/swaml-devel/subscribers.rdf [R=303]
RewriteRule ^subscriber/(s[0-9]+)$ http://swaml.berlios.de/demos/swaml-devel/subscribers.rdf#$1 [R=303,NE]
RewriteRule ^post/([0-9]{4})-([A-Za-z]+)/([0-9]+)$ http://swaml.berlios.de/demos/swaml-devel/$1-$2/post-$3.rdf [R=303]

AddType application/rdf+xml .rdf


