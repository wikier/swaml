<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
 <head>
  <title>SWAML - Semantic Web Archive of Mailing Lists</title>
  <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
  <meta name="robots" content="index,follow" />
  <meta name="keywords" content="SWAML, semantic web, mailing lists, python" />
  <meta name="language" content="es" />
  <link rel="stylesheet" type="text/css" charset="iso-8859-1" href="style.css" />
  <link rel="shortcut icon" href="favicon.ico" />
  <link rel="meta" title="DOAP" type="application/rdf+xml" href="doap.rdf" />
  <link rel="alternate" type="application/rss+xml" title="SWAML RSS" href="/rss/news" />
 </head>

 <body>
  <div id="header"> 
   <table summary="logo" width="100%" cellpadding="0" cellspacing="0" border="0">
    <tr valign="middle">
     <td>
      <div id="logo">
       <a href="/">SWAML</a>
      </div>
     </td>
     <td>
      <div id="berlios"> 
       <a href="http://developer.berlios.de/"><img src="images/berlios.png" width="132" height="50"
       alt="proyect hosted by BerliOS"/></a>
      </div>
     </td>
    </tr>
   </table>
  </div>

  <!-- toolbar -->
  <div class="toolbar">
   <div id="navbuttons">
    <a href="/" class="wiki">Home</a> &nbsp;|&nbsp;
    <a href="#news" class="wiki">News</a> &nbsp;|&nbsp;
    <a href="#doc" class="wiki">Documentation</a> &nbsp;|&nbsp;
    <a href="#files" class="download">Files</a> &nbsp;|&nbsp;
    <a href="/wiki" class="wiki">Wiki</a> &nbsp;|&nbsp;
    <a href="#contact" class="wiki">Contact</a>
   </div>
   <div id="search">
    <form action="http://www.google.es/search" method="get">
     <img src="/images/search.png" class="wiki-button" alt="search" width="22" height="22" />
     <input type="text" name="q" value="" />
     <input name="sitesearch" value="swaml.berlios.de" type="hidden" />
    </form>
   </div>
  </div>

  <br/><br/><br/>

  <!-- Page content -->
  <div id="content">

   <p id="icons">
     <a href="http://www.w3.org/RDF/" title="Powered by RDF"><img src="images/rdf.gif" width="88" height="96" alt="RDF Resource Description Framework" /></a>
     <a href="http://www.python.org/" title="Powered by Python"><img src="images/python.png" width="100" height="103" alt="Python" /></a>
   </p>

   <p>
     <acronym title="Semantic Web Archive of Mailing Lists">SWAML</acronym>, pronounced <em>[sw&aelig;ml]</em>,
     is  a research project around the semantic web technologies to publish the mailing lists&acute;s 
     archive into an <acronym title="Resource Description Framework">RDF</acronym> format, developed at 
     <a href="http://www.euitio.uniovi.es/">University of Oviedo</a> (Spain). You can visit the 
     <a href="http://developer.berlios.de/projects/swaml/">project page at BerliOS</a> for more details.
   </p>

   <p id="advertisement">
     This project is still on development phase, not to be used without careful considerations.
   </p>

   <p>
     In the project the're involved:
   </p>
   <ul>
     <li><a href="http://www.wikier.org/">Sergio Fdez</a> (maintainer)</li>
     <li><a href="http://www.berrueta.net/">Diego Berrueta</a></li>
     <li><a href="http://www.di.uniovi.es/~labra/">Jose E. Labra</a></li>
   </ul>

   <p>
     It has some <strong>features</strong>:
   </p>
   <ul>
     <li>platform independent (written in <a href="http://www.python.org/">python</a>)</li>
     <li>shell mode (to use manually or by cron script)
     <li>serialize <acronym title="Resource Description Framework">RDF</acronym> to disk</li>
     <li>reusability of <a href="wiki/index.php/Ontologies">ontologies</a> already extended</li>
     <li>enrichment using <a href="http://www.foaf-project.org/"><acronym title="Friend of a Friend">FOAF</acronym></a>
     <li><a href="http://earth.google.com/kml/kml_intro.html"><acronym title="Keyhole Markup Language">KML</acronym></a> support</li>
     <li>free software (under GNU General Public License, <acronym title="GNU General Public License">GPL</acronym>)</li>
   </ul>

   <h2 id ="news">
     <a href="/rss/news" type="application/rss+xml" title="read SWAML's news in your favourite feed reader"><img src="images/rss.png" width="28" height="28" alt="RSS" id="feed-icon" /></a>
     News
   </h2>
   <div class="wikitext">
    <?php
	include('functions.php');
	$swaml = new SWAML();
	echo $swaml->parse_rss();
    ?>
   </div>

   <h2 id="doc">Documentation</h2>
   <div class="wikitext">
    <dl>
     <dt><a href="http://download.berlios.de/swaml/propuesta.pdf">propuesta.pdf</a>:</dt>
     <dd>a document in spanish with the initial idea that reason the development of this project</dd>
    </dl>  
   </div>

   <h2 id="files">Files</h2>
   <div class="wikitext">
    <p>There are not <a href="/files">files</a> until the moment.</p>
    <p><!--If you would like to stay up to date with development -->While you can check out the latest version via the 
    <a href="http://subversion.tigris.org/">subversion</a> version control system:</p>
    <p class="svn">svn checkout <a href="/wsvn">http://svn.berlios.de/svnroot/repos/swaml/trunk</a> swaml</p>
   </div>

   <h2 id="contact">Contact</h2>
   <div class="wikitext">
    <p>You can contact any <a href="/members-list"> members of project</a>. Also you have a several 
    <a href="/lists">mailing lists</a>:</p>
    <ul>
     <li><a href="/lists/devel">Developers mailing list</a></li>
     <li><a href="/lists/users">Users mailing list</a></li>
     <li><a href="/lists/spanish">Spanish Users mailing list</a></li>
    </ul>
    <br/><p>Also, you can <a href="/bugs">report a bug</a> or sending a <a href="/features">feature request</a> 
    without you need to subscribe of any of <a href="/lists">project mailing lists</a>.</p>
   </div>

  </div>

  <div id="footer">
     <a href="/doap.rdf" type="application/rdf+xml"><img src="images/rdfmeta.png" alt="RDF Meta" /></a>
     <a href="http://validator.w3.org/check/referer"><img src="images/xhtml.png" alt="Valid XHTML" /></a>
     <a href="http://jigsaw.w3.org/css-validator/check/referer"><img src="images/css.png" alt="Valid CSS" /></a>
     <a href="http://developer.berlios.de" title="BerliOS Developer"> <img src="http://developer.berlios.de/bslogo.php?group_id=4806" width="62px" height="16px" border="0" alt="BerliOS Developer Logo"></a>
  </div>

 </body>
</html>
