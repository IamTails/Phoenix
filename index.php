<?php 

function parse_path() {
  $path = array();
  if (isset($_SERVER['REQUEST_URI'])) {
    $request_path = explode('?', $_SERVER['REQUEST_URI']);

    $path['base'] = rtrim(dirname($_SERVER['SCRIPT_NAME']), '\/');
    $path['call_utf8'] = substr(urldecode($request_path[0]), strlen($path['base']) + 1);
    $path['call'] = utf8_decode($path['call_utf8']);
    if ($path['call'] == basename($_SERVER['PHP_SELF'])) {
      $path['call'] = '';
    }
    $path['call_parts'] = explode('/', $path['call']);

    $path['query_utf8'] = urldecode($request_path[1]);
    $path['query'] = utf8_decode(urldecode($request_path[1]));
    $vars = explode('&', $path['query']);
    foreach ($vars as $var) {
      $t = explode('=', $var);
      $path['query_vars'][$t[0]] = $t[1];
    }
  }
return $path;
}

$path_info = parse_path();

function url_origin( $s, $use_forwarded_host = false )
{
    $ssl      = ( ! empty( $s['HTTPS'] ) && $s['HTTPS'] == 'on' );
    $sp       = strtolower( $s['SERVER_PROTOCOL'] );
    $protocol = substr( $sp, 0, strpos( $sp, '/' ) ) . ( ( $ssl ) ? 's' : '' );
    $port     = $s['SERVER_PORT'];
    $port     = ( ( ! $ssl && $port=='80' ) || ( $ssl && $port=='443' ) ) ? '' : ':'.$port;
    $host     = ( $use_forwarded_host && isset( $s['HTTP_X_FORWARDED_HOST'] ) ) ? $s['HTTP_X_FORWARDED_HOST'] : ( isset( $s['HTTP_HOST'] ) ? $s['HTTP_HOST'] : null );
    $host     = isset( $host ) ? $host : $s['SERVER_NAME'] . $port;
    return $protocol . '://' . $host;
}

function full_url( $s, $use_forwarded_host = false )
{
    return url_origin( $s, $use_forwarded_host ) . $s['REQUEST_URI'];
}

$absolute_url = full_url( $_SERVER );

$content = $_SERVER['REMOTE_ADDR'] . " - " . date("Y-m-d\TH:i:s", $_SERVER['REQUEST_TIME']) . "[" . $absolute_url . "]";

$file = '/var/www/access.log';
$handle_w = fopen($file, 'a') or die('Cannot open file:  '.$file);
fwrite($handle_w, $content . PHP_EOL);
fclose($handle_w);


switch ($path_info['call_parts'][0]) {
	case 'docs':
		if ($path_info['call_parts'][1] == "") {
			include_once("includes/header.html"); 
			include_once("includes/docs.html"); 
			include_once("includes/footer.html"); 
		} else {
			include_once("includes/header.html"); 
			include_once('includes/docs_' . $path_info['call_parts'][1] . '.html'); 
			include_once("includes/footer.html");
		}
		break;
	case 'gallery':
		include_once("includes/header.html"); 
		include_once("includes/gallery.html"); 
		include_once("includes/footer.html"); 
		break;
	case 'ui':
		include_once("ui.php");
		break;
	default:
		include_once("includes/header.html"); 
		include_once("includes/index.html"); 
		include_once("includes/footer.html"); 
		break;
}

     

?>