# SWAML htaccess rules

RewriteEngine On
RewriteBase {BASE}
AddType application/rdf+xml .rdf
#Options -MultiViews

# Rewrite rule to serve forum instance
RewriteRule ^forum$ forum.rdf [R=303]

# Rewrite rule to serve subscribers instances
RewriteRule ^subscribers$ subscribers.rdf [R=303]

# Rewrite rule to serve subscriber instance
RewriteRule ^subscriber/(s[0-9]+)$ subscribers.rdf#$1 [R=303,NE]

# Rewrite rule to serve HTML content with a post intance
RewriteCond %{HTTP_ACCEPT} text/html [OR]
RewriteCond %{HTTP_ACCEPT} application/xhtml\+xml [OR]
RewriteCond %{HTTP_USER_AGENT} ^Mozilla/.*
RewriteRule ^{POSTURI}$ {POSTFILE}.xhtml [R=303]

# Rewrite rule to serve RDF/XML content with a post intance
RewriteCond %{HTTP_ACCEPT} application/rdf\+xml
RewriteRule ^{POSTURI}$ {POSTFILE}.rdf [R=303]
