# SWAML htaccess rules

RewriteEngine On
RewriteBase {BASE}
AddType application/rdf+xml .rdf
#Options -MultiViews

# Rewrite rule to serve forum instance
RewriteRule ^forum$ forum.rdf [R=303]

# Rewrite rule to serve subscriber instance
RewriteRule ^subscribers/(.*)$ subscribers.rdf [R=301]
RewriteRule ^subscriber$ subscribers.rdf [R=303]

# Rewrite rule to serve HTML content with a post intance
RewriteCond %{HTTP_ACCEPT} text/html [OR]
RewriteCond %{HTTP_ACCEPT} application/xhtml\+xml [OR]
RewriteCond %{HTTP_USER_AGENT} ^Mozilla/.*
RewriteRule ^{POSTURI}$ {POSTFILE}.html [R=303]

# Rewrite rule to serve RDF/XML content with a post intance
RewriteCond %{HTTP_ACCEPT} application/rdf\+xml
RewriteRule ^{POSTURI}$ {POSTFILE}.rdf [R=303]

