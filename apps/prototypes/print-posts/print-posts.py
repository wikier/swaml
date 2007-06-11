#
# A simple program showing how to read the RDF data,
# retrieve additional RDF files (if necessary), and
# querying the data with SPARQL
#
# Diego Berrueta, 2.006
#

import rdflib
import sys
from rdflib import sparql

SIOC = rdflib.Namespace(u'http://rdfs.org/sioc/ns#')

def loadMailingList(mailingListUri):
    graph = rdflib.Graph()

    print "Getting mailing list data (", mailingListUri, ")...",
    graph.parse(mailingListUri)
    print "OK, loaded", len(graph), "triples"
    return graph


def loadAdditionalData(graph, mailingListUri):

    for post in graph.objects(mailingListUri, SIOC["container_of"]):
        if not hasValueForPredicate(graph, post, SIOC["title"]):
            print "Resolving reference to get additional data (", post, ")...",
            graph.parse(post)
            print "OK, now", len(graph), "triples"

    for user in graph.objects(mailingListUri, SIOC["has_subscriber"]):
        if not hasValueForPredicate(graph, user, SIOC["email_sha1sum"]):
            print "Resolving reference to get additional data (", user, ")...",
            graph.parse(user)
            print "OK, now", len(graph), "triples"


def hasValueForPredicate(graph, subject, predicate):
    return (len([x for x in graph.objects(subject, predicate)]) > 0)


def printPosts(graph, posts):
    print """
    FORUM POSTS:
    ============
    """
    
    for (title, userName) in posts:
        print "==>", title, "by", userName

############################################################
            
if __name__ == '__main__':

    if len(sys.argv) > 1:
        mailingListUri = sys.argv[1]
    else:
        print 'you must to indicate a mailing list URI'
        sys.exit()

    graph = loadMailingList(mailingListUri)
    loadAdditionalData(graph, mailingListUri)

    sparqlGr = sparql.sparqlGraph.SPARQLGraph(graph)
    select = ("?postTitle", "?userName")
    where  = sparql.GraphPattern(
        [("?x",    SIOC["container_of"], "?post"),
         ("?post", SIOC["title"],        "?postTitle"),
         ("?post", SIOC["has_creator"],  "?user")])
    opt    = sparql.GraphPattern(
        [("?user", SIOC["name"],         "?userName")])
    posts  = sparqlGr.query(select, where, opt)
    
    printPosts(graph, posts)
