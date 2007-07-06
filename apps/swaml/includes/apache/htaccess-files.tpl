# SWAML htaccess rules

# FIXME: customize base URI
# FIXME: dynamic customize of last rule

RewriteEngine On

RewriteBase /demos/swaml-devel/

AddType application/rdf+xml .rdf

Options -MultiViews

RewriteRule ^forum$ forum.rdf [R=303]
RewriteRule ^subscribers$ subscribers.rdf [R=303]
RewriteRule ^subscriber/(s[0-9]+)$ subscribers.rdf#$1 [R=303,NE]
RewriteRule ^post/([0-9]{4})-([A-Za-z]+)/([0-9]+)$ $1-$2/post-$3.rdf [R=303]
