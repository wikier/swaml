<?php

// PHP utils functions to SWAML webpage
//*************************************

class SWAML {

	function make_clickable($text) {

		$ret = " " . $text;

		// matches a "http://yyyy"
		$ret = preg_replace("#([\n ])(http|https)://([a-z0-9\-\.,\?!%\*_\#:;~\\&$@\/=\+]+)#i", "\\1<a href=\"\\2://\\3\">\\2://\\3</a>", $ret);

		// matches a "www.xxxx.yyyy[/zzzz]"
		$ret = preg_replace("#([\n ])www\.([a-z0-9\-]+)\.([a-z0-9\-.\~]+)((?:/[a-z0-9\-\.,\?!%\*_\#:;~\\&$@\/=\+]*)?)#i", "\\1<a href=\"http://www.\\2.\\3\\4\">www.\\2.\\3\\4</a>", $ret);

		$ret = substr($ret, 1);

		return($ret);
	}

	function acronyms_replace($text) {

		$acronyms = array(	'SWAML', 'RDF', 'URL', 'URI', 'OWL', 'SIOC', 'RFC');
		$titles   = array(	'Semantic Web Archive of Mailing Lists',
					'Resource Description Framework',
					'Uniform Resource Locator',
					'Uniform Resource Identifier',
					'Ontology Web Languaje',
					'Semantically-Interlinked Online Communities',
					'Request for Comments'
				);

		for ($i=0; $i<count($acronyms); $i++) {
			$acronym = $acronyms[$i];
			$title = $titles[$i];
			$text = str_replace(
					' '.$acronym.' ',
					' <acronym title="'.$title.'">'.$acronym.'</acronym> ',
					$text);
		}
		
		return $text;

	}

	function parse_rss() {

		$months = array("Jan" => "01",
                           	"Feb" => "02",
                           	"Mar" => "03",
                           	"Apr" => "04",
                           	"May" => "05",
                           	"Jun" => "06",
                           	"Jul" => "07",
                           	"Aug" => "08",
                           	"Sep" => "09",
                           	"Oct" => "10",
                           	"Nov" => "11",
                           	"Dec" => "12"
                    		);

		require_once('./magpierss/rss_fetch.inc');
          	$url = 'http://developer.berlios.de/export/rss20_bsnews.php?group_id=4806';

          	$rss = fetch_rss($url);

          	if ( $rss and !$rss->ERROR) {

	    		$num_items = 10;
	    		$items = array_slice($rss->items, 0, $num_items);
	    		
			$ret = '<dl>';

	    		foreach ($items as $item) {
	      			$title = $item[title];
	      			$link  = $item[link];
	      			$parted = explode('=', $link);
	      			if ($parted[1]!=22514 && $parted[1]!=22842 && $parted[1]!=22843) {
	      			 $description = $item[description];
	      			 $description = $this->acronyms_replace($description);
	      			 $description = $this->make_clickable($description);
	      			 $pubDate  = $item[pubdate];
	      			 $date = explode(" ", $pubDate);
	      			 $ret .= '<dt>['.$date[1].'-'.$months[$date[2]].'-'.$date[3].'] ';
              			 $ret .= '<a href="'.$link.'"><strong>'.$title.'</strong></a></dt>';
	      			 $ret .= '<dd>'.$description.'</dd>';
	      			}
	    		}

	    		$ret .= '</dl>';

          	} else { 
			$ret = 'Error: ' . $rss->ERROR; 
		}

		return $ret;

	}

}

?>
