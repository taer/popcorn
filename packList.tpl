<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
  <head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <title>Circle Overlay</title>

    <style type="text/css" MEDIA="screen, projection">
	  #map {
        width: 800px;
        height: 600px;
      }
    </style>

  </head>
  <body>
  <ul>
  %for row in rows:
  <li><a href="/pack/{{row}}">{{row}}</a></li>
    %end
  </ul>
  </body>
</html>
