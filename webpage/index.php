<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
  <head>
    <title>SWAML - Semantic Web Archive of Mailing Lists</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
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
        <acronym title="Semantic Web Archive of Mailing Lists">SWAML</acronym>, pronounced 
        <em>[sw&aelig;ml]</em>, is  a research project around the semantic web technologies 
        to publish the mailing lists' archives into a 
        <acronym title="Resource Description Framework">RDF</acronym> format. It has been
        developed by the <a href="http://www.fundacionctic.org/"><abbr 
        title="Centro Tecnológico de la Información y la Comunicación"
        xml:lang="es">CTIC</abbr> Foundation</a> and the
        <a href="http://weso.sourceforge.net/"><abbr 
        title="Semantic Web Oviedo Research Group">WESO-RG</abbr></a>
        at <a href="http://www.euitio.uniovi.es/">University of Oviedo</a> (Spain). 
        You can visit the 
        <a href="http://developer.berlios.de/projects/swaml/">project page at BerliOS</a> 
        for more details.
      </p>

      <img src="images/swaml.png" width="400" height="336" alt="SWAML process description" id="process" />

      <p>
     	<acronym title="Semantic Web Archive of Mailing Lists">SWAML</acronym> reads a 
        collection of email messages stored in a mailbox (from a mailing list compatible 
        with <acronym title="Request For Comments">RFC</acronym> 4155) and generates a 
        <acronym title="Resource Description Framework">RDF</acronym> description. It is 
     	written in Python using <acronym title="Semantically-Interlinked Online Communities ">SIOC</acronym> as 
     	the main ontology to represent in <acronym title="Resource Description Framework">RDF</acronym>
        a mailing list.     	
      </p>

      <p>
        In the project we're involved:
      </p>
      <ul id="members">
     	<li>
     	  <a href="http://www.wikier.org/">Sergio Fernández</a> (maintainer),
     	  <a href="http://www.wikier.org/foaf.rdf#wikier"><img src="images/foaf.gif" width="26" height="14" alt="foaf" /></a>
     	</li>
     	<li>
     	  <a href="http://www.berrueta.net/">Diego Berrueta</a>,
     	  <a href="http://www.berrueta.net/foaf.rdf#me"><img src="images/foaf.gif" width="26" height="14" alt="foaf" /></a>
     	</li>
     	<li>
     	  <a href="http://www.di.uniovi.es/~labra">Jose E. Labra</a>,
     	  <a href="http://www.di.uniovi.es/~labra/labraFoaf.rdf"><img src="images/foaf.gif" width="26" height="14" alt="foaf" /></a>
     	</li>
     	<li>
     	  <a href="http://www.asturlinux.org/comunidad/blog/frade">Iván Frade</a>,
     	  <a href="http://frade.no-ip.info:2080/~ivan/foaf.rdf"><img src="images/foaf.gif" width="26" height="14" alt="foaf" /></a>
     	</li>
     	<li>
     	  <a href="http://criptonita.com/~nacho">Nacho Barrientos</a> (debian package),
     	  <a href="http://criptonita.com/~nacho/foaf.rdf"><img src="images/foaf.gif" width="26" height="14" alt="foaf" /></a>
     	</li>
      </ul>

      <p>
        Mainly it's formed by two components:
      </p>
      <ul>
     	<li id="swaml">
          <strong><acronym title="Semantic Web Archive of Mailing Lists">SWAML</acronym></strong>, 
          the core process that exports a mailing list in 
          <acronym title="Resource Description Framework">RDF</acronym>.
        </li>
     	<li id="buxon">
          <strong>Buxon</strong>, a 
          <acronym title="Semantically-Interlinked Online Communities ">sioc</acronym>:Forum
          browser.
        </li>
      </ul>

      <p>
     	And it has some <strong>features</strong>:
      </p>
      <ul>
      	<li>platform independent (written in <a href="http://www.python.org/">python</a>)</li>
     	<li>shell mode (to use manually or by cron script)</li>
     	<li>compatible with <a href="http://rfc.net/rfc4155.html"><acronym title="Request For Comments">RFC</acronym> 4155</a></li>
     	<li>serialize <acronym title="Resource Description Framework">RDF</acronym> to disk</li>
     	<li>reusability of <a href="wiki/index.php/Ontologies">ontologies</a> already extended, mainly <a href="http://sioc-project.org/"><acronym title="Semantically-Interlinked Online Communities ">SIOC</acronym></a></li>
     	<li>enrichment using <a href="http://www.foaf-project.org/"><acronym title="Friend of a Friend">FOAF</acronym></a></li>
     	<li><a href="http://earth.google.com/kml/whatiskml.html"><acronym title="Keyhole Markup Language">KML</acronym></a> support</li>
     	<li>browser in <acronym title="GIMP Tool Kit">GTK</acronym></li>
     	<li>free software (under <acronym title="GNU is Not Unix">GNU</acronym> General Public License, <a href="http://www.gnu.org/licenses/gpl.html"><acronym title="GNU General Public License">GPL</acronym></a> <abbr title="version 2">v2</abbr> or later)</li>
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
      <p style="text-align:right;">
        <a href="/news">read more news...</a>
      </p>

      <p>
        Also you could find all news/comments related with the project in a wiki page 
        called <a href="/wiki/index.php/SWAML-o-sphere">SWAML-o-sphere</a>. Feel free 
        to add any other entry.
      </p>

      <h2 id="files">Files</h2>
      <p>
        There are some <a href="/files">files</a> (and a <a href="/releases">mirror</a> of it) until the moment:
      </p>
      <dl>
        <dt>
          <acronym title="Semantic Web Archive of Mailing Lists">SWAML</acronym>:
        </dt>
        <dd>
          <a href="http://prdownload.berlios.de/swaml/swaml-0.0.5.tar.gz">swaml-0.0.5.tar.gz</a>
          and
          <a href="http://prdownload.berlios.de/swaml/swaml_0.0.5-2_all.deb">swaml_0.0.5-2_all.deb</a>
          (28/12/2006)
        </dd>
        <dd>
          <a href="http://prdownload.berlios.de/swaml/swaml-0.0.4.tar.gz">swaml-0.0.4.tar.gz</a>
          (21/11/2006)
        </dd>
        <dd>
          <a href="http://prdownload.berlios.de/swaml/swaml-0.0.3.tar.gz">swaml-0.0.3.tar.gz</a>
          (01/11/2006)
        </dd>
        <dd>
          <a href="http://prdownload.berlios.de/swaml/swaml-0.0.2.tar.gz">swaml-0.0.2.tar.gz</a>
          (13/10/2006)
        </dd>
        <dd>
          <a href="http://prdownload.berlios.de/swaml/swaml-0.0.1.tar.gz">swaml-0.0.1.tar.gz</a>
          (02/10/2006)
        </dd>
        <dt>
          Buxon:
        </dt>
        <dd>
          <a href="http://prdownload.berlios.de/swaml/buxon-0.0.3.tar.gz">buxon-0.0.3.tar.gz</a>
          and
          <a href="http://prdownload.berlios.de/swaml/buxon_0.0.3-2_all.deb">buxon_0.0.3-2_all.deb</a>
          (28/12/2006)
        </dd>
      </dl>

      <p>
        If you use any <a href="http://www.debian.org/">Debian</a>-based 
        <abbr title="GNU is Not Unix">GNU</abbr>/Linux distribution, you could 
        install it using <abbr title="Advanced Packaging Tool">APT</abbr> tools
        (<span class="console">apt-get install swaml</span> and 
        <span class="console">apt-get install buxon</span>).
        All packages depends on <a href="http://rdflib.net/">RDFLib</a>.
        You can see a <a href="/demo">demo</a> of which 
        <acronym title="Semantic Web Archive of Mailing Lists">SWAML</acronym> makes.
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
        Also the <a href="doc/">online documentation for developers</a>, it's available 
        to download another documents about the project:
      </p>

      <dl>
        <dt><a href="http://prdownload.berlios.de/swaml/propuesta.pdf">propuesta.pdf</a>:</dt>
        <dd>original document in spanish with the idea that motivated this project</dd>

        <dt><a href="http://prdownload.berlios.de/swaml/proposal.pdf">proposal.pdf</a>:</dt>
        <dd>translation with the idea that motivated this project</dd>

        <dt><a href="http://prdownload.berlios.de/swaml/swaml-pfc.pdf">swaml-pfc.pdf</a>:</dt>
        <dd>a book (in Spanish) about the SWAML project for Sergio's degree dissertation</dd>
      </dl>

      <p id="publications">
        The research activity in the project produces some <strong>scientist publications</strong>:
      </p>
      <ul>
        <li>
          Sergio Fernández, Diego Berrueta, José E. Labra,
          <a href="http://sunsite.informatik.rwth-aachen.de/Publications/CEUR-WS//Vol-245/paper4.pdf"><em>Mailing 
          lists meet the Semantic Web</em></a>, in Proceedings of the 
          <a href="http://bis.kie.ae.poznan.pl/10th_bis/"><abbr title="Business Information Systems">BIS</abbr> 2007</a> 
          Workshop on <a href="http://integror.net/saw/">Social Aspects of the Web</a>, 
          <abbr title="International Standard Book Number">ISBN</abbr> 83-916842-4-2, 
          <abbr title="pages">pp.</abbr> 45-52, Poznan, Poland, April 27, 2007.
        </li>
      </ul>

      <p>
        And we made some presentations about the project around the world:
      </p>
      <dl>
        <dt>
          <a href="http://prdownload.berlios.de/swaml/20070511-swaml-concurso-software-libre.pdf"><acronym 
          title="Semantic Web Archive of Mailing Lists">SWAML</acronym>,
          Semantic Web Archive of Mailing Lists</a>:
        </dt>
        <dd>
          11 of May of 2007 in Seville (Spain) on the final phase of the 
          <a href="http://concurso-softwarelibre.us.es/"><span 
          xml:lang="es"><abbr title="primer">I</abbr> Concurso Universitario de Software 
          Libre</span></a>
        </dd>
 
        <dt>
          <a href="http://prdownload.berlios.de/swaml/SAW2007-Mailing-Lists-Meet-The-Semantic-Web.pdf">Mailing Lists Meet The Semantic Web</a>:
        </dt>
        <dd>
          27 of April of 2007 in Poznan (Poland) on the workshop of Social Aspects of 
          the Web (<a href="http://integror.net/saw"><abbr title="Social Aspects of the Web">SAW</abbr>2007</a>),
          in conjunction with <abbr title="tenth">10<sup>th</sup></abbr> International
          Conference on Business Information Systems 
          (<a href="http://bis.kie.ae.poznan.pl/10th_bis"><abbr title="Business Information
          Systems">BIS</abbr>2007</a>), in co-operation with
          <abbr title="Association for Computing Machinery" xml:lang="en">ACM</abbr>
          <abbr title="Special Interest Groups in Management Information Systems">SIGMIS</abbr>
        </dd>

        <dt>
          <a href="http://prdownload.berlios.de/swaml/20061220-pfc-swaml.pdf"><span
          xml:lang="es"><acronym title="Semantic Web Archive of Mailing Lists">SWAML</acronym>,
          publicación de listas de correo en Web Semántica</span></a>:
        </dt>
        <dd>
          20 of December of 2006 in Oviedo (Spain) for Sergio's degree dissertation
        </dd>
      </dl>

      <h2 id="contact">Contact</h2>
      <p>
        You can contact with the <a href="/members-list">members of project</a> 
        in the <a href="/lists/devel">developers mailing list</a>
        (<a href="http://lists.berlios.de/pipermail/swaml-devel/">archives</a> are
        public). Also, you can <a href="/bugs">report a bug</a> or send a 
        <a href="/features">feature request</a> without you need to subscribe of 
        any of <a href="/lists">project mailing lists</a>.
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
    <script type="text/javascript">_uacct = "UA-599301-2";urchinTracker();</script>
    <script type="text/javascript" src="http://embed.technorati.com/embed/4y8uh7tpy.js"></script>

  </body>

</html>
