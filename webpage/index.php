<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
  <head>
    <title>SWAML - Semantic Web Archive of Mailing Lists</title>
    <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
    <meta name="robots" content="index,follow" />
    <meta name="keywords" content="SWAML, semantic web, mailing lists, python, sioc" />
    <meta name="language" content="en" />
    <link rel="stylesheet" type="text/css" charset="utf-8" href="style.css" />
    <link rel="shortcut icon" href="favicon.ico" />
    <link rel="meta" title="DOAP" type="application/rdf+xml" href="doap.rdf" />
    <link rel="alternate" type="application/rss+xml" title="SWAML RSS" href="/rss/news" />
  </head>

  <body>

    <div class="accessibility">
		<a href="#content" accesskey="c" title="Go to content">Go to content</a>
    </div>

    <h1 id="head">
		<a href="http://developer.berlios.de/"><img src="images/berlios.png" width="132" height="50" alt="Project hosted by BerliOS" /></a>
		<a href="http://swaml.berlios.de/"><acronym title="Semantic Web Archive of Mailing Lists">swaml</acronym></a>
    </h1>

    <div id="menu">
	  <ul>
		<li><a href="/" accesskey="1" title="go SWAML home">Home</a></li>
		<li><a href="#news" accesskey="2" title="read SWAML news">News</a></li>
 		<li><a href="#files" accesskey="3" title="download SWAML files">Files</a></li>
		<li><a href="#doc" accesskey="4" title="see SWAML documentation">Documentation</a></li>
 		<li><a href="/wiki" accesskey="5" title="go SWAML wiki">Wiki</a></li>
		<li class="last"><a href="#contact" accesskey="6" title="contact with SWAML team">Contact</a></li>
	  </ul>
    </div>

    <div id="content">
	  <p>
		<acronym title="Semantic Web Archive of Mailing Lists">SWAML</acronym>, pronounced <em>[sw&aelig;ml]</em>,
		is  a research project around the semantic web technologies to publish the mailing lists&acute;s 
		archive into a <acronym title="Resource Description Framework">RDF</acronym> format, developed at 
		<a href="http://www.euitio.uniovi.es/">University of Oviedo</a> (Spain). You can visit the 
		<a href="http://developer.berlios.de/projects/swaml/">project page at BerliOS</a> for more details.
	  </p>

      <img src="images/swaml.png" width="400" height="336" alt="SWAML process description" id="process" />

      <p id="advertisement">
     	This project is still on development phase, not to be used without careful considerations.
      </p>

      <p>
     	<acronym title="Semantic Web Archive of Mailing Lists">SWAML</acronym> reads a collection of email messages 
     	stored in a mailbox (from a mailing list compatible with <acronym title="Request For Comments">RFC</acronym> 
     	4155) and generates a <acronym title="Resource Description Framework">RDF</acronym> description. It is 
     	written in Python using <acronym title="Semantically-Interlinked Online Communities ">SIOC</acronym> as 
     	the main ontology to represent in <acronym title="Resource Description Framework">RDF</acronym> a mailing 
     	list.     	
      </p>

      <p>
		In the project we're involved:
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
     	<li>shell mode (to use manually or by cron script)</li>
     	<li>compatible with <a href="http://rfc.net/rfc4155.html"><acronym title="Request For Comments">RFC</acronym> 4155</a></li>
     	<li>serialize <acronym title="Resource Description Framework">RDF</acronym> to disk</li>
     	<li>reusability of <a href="wiki/index.php/Ontologies">ontologies</a> already extended, mainly <a href="http://sioc-project.org/"><acronym title="Semantically-Interlinked Online Communities ">SIOC</acronym></a></li>
     	<li>enrichment using <a href="http://www.foaf-project.org/"><acronym title="Friend of a Friend">FOAF</acronym></a></li>
     	<li>rich visor in <acronym title="GIMP Tool Kit">GTK</acronym></li>
     	<li><a href="http://earth.google.com/kml/kml_intro.html"><acronym title="Keyhole Markup Language">KML</acronym></a> support</li>
     	<li>free software (under <acronym title="GNU is Not Unix">GNU</acronym> General Public License, <a href="http://www.gnu.org/licenses/gpl.html"><acronym title="GNU General Public License">GPL</acronym></a> <abbr title="version 2">v2</abbr>)</li>
      </ul>

      <h2 id ="news">
     	<a href="/rss/news" type="application/rss+xml" title="read SWAML's news in your favourite feed reader"><img src="images/rss.png" width="28" height="28" alt="RSS" id="feed-icon" /></a>
     	News
      </h2>
    	<?php
		  include('functions.php');
		  $swaml = new SWAML();
		  echo $swaml->parse_rss();
    	?>
		<p style="text-align:right;"><a href="/news">read more news...</a></p>

      <h2 id="files">Files</h2>
    	<p>
		  There are some <a href="/files">files</a> (and a <a href="/releases">mirror</a> of it) until the moment:
		</p>
    	<dl>
    	 <dt>
    	  	<acronym title="Semantic Web Archive of Mailing Lists">SWAML</acronym>
    	 </dt>
    	 <dd>
			<a href="http://prdownload.berlios.de/swaml/swaml-0.0.4.tar.gz">swaml-0.0.4.tar.gz</a>
    	 </dd>
    	 <dd>
		<a href="http://prdownload.berlios.de/swaml/swaml-0.0.3.tar.gz">swaml-0.0.3.tar.gz</a>
    	 </dd>
    	 <dd>
			<a href="http://prdownload.berlios.de/swaml/swaml-0.0.2.tar.gz">swaml-0.0.2.tar.gz</a>
    	 </dd>
   	 	 <dd>
			<a href="http://prdownload.berlios.de/swaml/swaml-0.0.1.tar.gz">swaml-0.0.1.tar.gz</a>
    	 </dd>
   	 	</dl>

    	<p>
		  You can see <a href="/demo">demo</a> of which <acronym title="Semantic Web Archive of Mailing Lists">SWAML</acronym> makes.
		</p>

    	<p>
		  If you would like to stay up to date with development you can check out the latest version via the 
    	  <a href="http://subversion.tigris.org/">subversion</a> version control system:
		</p>
    	<p class="svn">
		  svn checkout <a href="/wsvn">http://svn.berlios.de/svnroot/repos/swaml/trunk</a> swaml
		</p>

      <h2 id="doc">Documentation</h2>
    	<p>
     	  Also the <a href="doc/">online documentation for developers</a>, it's available to download
     	  another documents about the project:
    	</p>
    	<dl>
   		  <dt><a href="http://prdownload.berlios.de/swaml/propuesta.pdf">propuesta.pdf</a>:</dt>
     	  <dd>original document in spanish with the idea that motivated this project</dd>
     	  <dt><a href="http://prdownload.berlios.de/swaml/proposal.pdf">proposal.pdf</a>:</dt>
     	  <dd>translation with the idea that motivated this project</dd>
     	  <dt><a href="http://prdownload.berlios.de/swaml/swaml-pfc.pdf">swaml-pfc.pdf</a>:</dt>
     	  <dd>a book (in Spanish) about the SWAML project for Sergio's degree dissertation</dd>
    	</dl>  

      <h2 id="contact">Contact</h2>
    	<p>
		  You can contact any <a href="/members-list">members of project</a>. Also you have a several 
    	  <a href="/lists">mailing lists</a>:
		</p>
    	<ul>
    	 <li><a href="/lists/devel">Developers mailing list</a></li>
    	 <li><a href="/lists/users">Users mailing list</a></li>
    	 <li><a href="/lists/spanish">Spanish Users mailing list</a></li>
    	</ul>

		<p>
		  Also, you can <a href="/bugs">report a bug</a> or sending a <a href="/features">feature request</a> 
    	  without you need to subscribe of any of <a href="/lists">project mailing lists</a>.
		</p>

    </div>

    <div id="foot">
	  <ul>
		<li><a href="doap.rdf" type="application/rdf+xml"><img src="images/rdfmeta.png" alt="RDF Meta" /></a></li>
		<li><a href="http://validator.w3.org/check/referer"><img src="images/xhtml.png" alt="Valid XHTML" /></a></li>
		<li><a href="http://jigsaw.w3.org/css-validator/check/referer"><img src="images/css.png" alt="Valid CSS" /></a></li>
 		<li><a href="http://developer.berlios.de" title="BerliOS Developer"> <img src="http://developer.berlios.de/bslogo.php?group_id=4806" width="62px" height="16px" alt="BerliOS Developer Logo" /></a></li>
	  </ul>
    </div>


    <script src="http://www.google-analytics.com/urchin.js" type="text/javascript"></script>
    <script type="text/javascript">
		_uacct = "UA-599301-2";
		urchinTracker();
    </script>

    <script type="text/javascript" src="http://embed.technorati.com/embed/4y8uh7tpy.js"></script>

  </body>

</html>
