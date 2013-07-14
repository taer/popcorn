<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
  <head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <title>Circle Overlay</title>

    <style type="text/css" MEDIA="screen, projection">
	  #map {
        width: 1024px;
        height: 768px;
      }
    </style>

	<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js"></script>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
	
    <script type="text/javascript">
        function byte2Hex(b){
        var hexes="0123456789ABCDEF"
        return String(hexes.substr((b>>4) &0x0F,1)) + hexes.substr(b&0x0F,1); 
        }
        function RGB2Color(r,g,b){
            return '#'+ byte2Hex(r)+ byte2Hex(g) +byte2Hex(b);
            }
            $(function() {
		
  var txt=document.getElementById("bar")

    for (var i = 0; i < 20; ++i)
    {
txt.innerHTML+=  '<font color="' + getColor(i/20) + '">&#9608;</font>';
    }

			// **** CREATE GOOGLE MAP ****
			var mapCenter = new google.maps.LatLng(30.507166,-97.716084);
			var map = new google.maps.Map(document.getElementById('map'), {
				'zoom': 12,
				'center': mapCenter,
				'mapTypeId': google.maps.MapTypeId.ROADMAP
			});
   $.ajax({
                type: "GET",
                url: "/data/{{pack}}",   
                dataType: 'json',
                success: function(data) {
                    data.data.map(function(point){
                        drawProjectOnMap(map, point);
                   });
                    data.centers.map(function(center){
                        drawCircleOnMap(map, center);
                    });
                },
                error: function() {
                    handleError("Could not load XML file - local file access may be restricted (use IE).")
                }
            });

            function drawProjectOnMap(map, data)
                    {
                    var marker = new google.maps.Marker({
                      map: map,
                      position: new google.maps.LatLng(data[0], data[1]),
                      title: data[0] + ":" + data[1]
                    });

}
 function getColor(num)
  {
    var len = 20;
    var center = 128;
    var width = 127;
    frequency1 =.1
    frequency2=.1
    frequency3=.1
    phase1=0
    phase2=2
    phase3=4
       var red = Math.sin(frequency1*num*len + phase1) * width + center;
       var grn = Math.sin(frequency2*num*len + phase2) * width + center;
       var blu = Math.sin(frequency3*num*len + phase3) * width + center;
    return RGB2Color(red,grn,blu);   
    
  }
            function drawCircleOnMap(map, center)
                    {
                    var data=center.center
                    var red=255*center.weight
                    var color= RGB2Color(red,0,0) //'#AA0000' 
                    var circle = new google.maps.Circle({
                      map: map,
                            center:  new google.maps.LatLng(data[0],data[1]),
                      radius: 3000 ,
                      //fillColor: '#AA0000' 
                      //fillColor: color
                      fillColor: getColor(center.weight)
                    });

}

		});


    </script>
  </head>
  <body>
    <h1>{{pack}} locations for 2012</h1>
    <div id="bar"></div>
    <div id="map"></div>
  </body>
</html>
