<html>
    <head>
<style type="text/css">
.styled-button-ON {
	background: #FEDA71;
	background: -moz-linear-gradient(top,#FEDA71 0%,#FEBB49 100%);
	background: -webkit-gradient(linear,left top,left bottom,color-stop(0%,#FEDA71),color-stop(100%,#FEBB49));
	background: -webkit-linear-gradient(top,#FEDA71 0%,#FEBB49 100%);
	background: -o-linear-gradient(top,#FEDA71 0%,#FEBB49 100%);
	background: -ms-linear-gradient(top,#FEDA71 0%,#FEBB49 100%);
	background: linear-gradient(top,#FEDA71 0%,#FEBB49 100%);
	filter: progid: DXImageTransform.Microsoft.gradient( startColorstr='#FEDA71',endColorstr='#FEBB49',GradientType=0);
	padding:8px 18px;
	color:#623F1D;
	font-family:'Helvetica Neue',sans-serif;
	font-size:12px;
	border-radius:48px;
	-moz-border-radius:48px;
	-webkit-border-radius:48px;
	border:1px solid #623F1D
}
.styled-button-OFF {
	background: #000000;
	background: -moz-linear-gradient(top,##000000 0%,#FEBB49 100%);
	background: -webkit-gradient(linear,left top,left bottom,color-stop(0%,#000000),color-stop(100%,#FEBB49));
	background: -webkit-linear-gradient(top,#000000 0%,#FEBB49 100%);
	background: -o-linear-gradient(top,#000000 0%,#FEBB49 100%);
	background: -ms-linear-gradient(top,#000000 0%,#FEBB49 100%);
	background: linear-gradient(top,#000000 0%,#FEBB49 100%);
	filter: progid: DXImageTransform.Microsoft.gradient( startColorstr='#FEDA71',endColorstr='#FEBB49',GradientType=0);
	padding:8px 18px;
	color:#623F1D;
	font-family:'Helvetica Neue',sans-serif;
	font-size:12px;
	border-radius:48px;
	-moz-border-radius:48px;
	-webkit-border-radius:48px;
	border:1px solid #623F1D
}  

</style>

<script>
    
$(document).ready(function(){  
    	alert("document ready");
    
   		$("#btn").click(function(){
   		var urll="https://dweet.io:443/dweet/for/smart_bed_status";
             	
   		if($("#btn").attr("value") == 'ON') {
            
            $("#btn").attr("value","OFF");
            $("#btn").attr("class","styled-button-OFF");
            $.post(urll,{status: "0"});
            $("#para").text("ALARM CLOCK IS NOT YET SET!");
       		
		} else if($("#btn").attr("value") == 'OFF'){
            var q=$("#ore").val();
        	var u=$("#minuti").val();
            if(q!="-"&&u!="-"){
                var h=document.getElementById("back_alarm");
                if(h.checked){
                    var z=$("#minuti_back_alarm").val();
                    if (z!="-"){
                        
                        $("#btn").attr("value","ON");
       					$("#btn").attr("class","styled-button-ON");
                    
                        $.post(urll,{status: "1",alarm_hour:q,alarm_min:u,smart_alarm:z});
                        $("#para").text("ALARM SET AT "+q+":"+u+". Smart Alarm:"+z);
            			alert("ALARM SET AT "+q+":"+u+". Smart Alarm:"+z);
                        
                    }else{
                        alert("Please set a correct smart alarm time!");
                        
                    }
       				
                }else{
                    $("#btn").attr("value","ON");
       				$("#btn").attr("class","styled-button-ON");
                    $.post(urll,{status: "1",alarm_hour:q,alarm_min:u,smart_alarm: "0"});
            		$("#para").text("ALARM SET AT "+q+":"+u);
            		alert("ALARM SET AT "+q+":"+u);
                }
            
        	}else{
            
    			alert("Please set a correct alarm time!");
			}
        }});

$("#btn").ready(function(){
    alert("I'm ready button");
	$.ajax({
   	type: 'GET',
    url: "https://dweet.io/get/latest/dweet/for/smart_bed_status",
    contentType: "application/json",
    dataType: 'json',
    success: function(json) {
        if(json["this"]=="failed"){
             alert("Valore ajax settato a OFF"); 
     		$("#btn").attr("value","OFF");
     		$("#btn").attr("class","styled-button-OFF");
        	$("#para").text("ALARM CLOCK IS NOT YET SET!");
     
        }else{
    		var val=JSON.stringify(json["with"][0]["content"]["status"]);
    		var h=JSON.stringify(json["with"][0]["content"]["alarm_hour"]); 
    		var m=JSON.stringify(json["with"][0]["content"]["alarm_min"]);
    		var z=JSON.stringify(json["with"][0]["content"]["smart_alarm"]);  
     		if(val==1){
        		alert("Valore ajax settato a ON");
     			$("#btn").attr("value","ON");
     			$("#btn").attr("class","styled-button-ON");
        		if(z==0){
        			$("#para").text("ALARM SET AT "+h+":"+m);
        		} else{
            		$("#para").text("ALARM SET AT "+h+":"+m+". Smart Alarm:"+z);
        		}
     		}else{
        		alert("Valore ajax settato a OFF"); 
     			$("#btn").attr("value","OFF");
     			$("#btn").attr("class","styled-button-OFF");
        		$("#para").text("ALARM CLOCK IS NOT YET SET!");
     		}
   
        }}
       
    });
});
    $("#ore").ready(function(){
    	alert("I'm ready ore");
        var a=document.getElementById("ore");
		var b=document.getElementById("minuti");
        var c=document.getElementById("minuti_back_alarm");

 		var opt = document.createElement('option');
    	opt.value = "-";
    	opt.innerHTML = "-";
    	a.appendChild(opt);
    
		for (var i = 0; i<24; i++){
    		var opt = document.createElement('option');
    		opt.value = i;
    		opt.innerHTML = i;
    		a.appendChild(opt);
		}
 		var opt = document.createElement('option');
    	opt.value = "-";
    	opt.innerHTML = "-";
    	b.appendChild(opt);

		for (var i = 0; i<60; i++){
    		var opt = document.createElement('option');
    		opt.value = i;
    		opt.innerHTML = i;
    		b.appendChild(opt);
		}
        
        var opt = document.createElement('option');
    	opt.value = "-";
    	opt.innerHTML = "-";
    	c.appendChild(opt);

		for (var i = 0; i<60; i++){
    		var opt = document.createElement('option');
    		opt.value = i;
    		opt.innerHTML = i;
    		c.appendChild(opt);
		}
   
    });   
});

      
</script>
</head>
<body>
    <br>
    <td valign="center">
    <div style="text-align:center">
        
    <input type="button" class="styled-button-ON" id="btn" value="" />
    </div>
    </td>
    <br>
    <div align="center">
    <select id="ore" style="height: 20%; width:30%;color : black; background-color: GhostWhite;"></select>
    : <select id="minuti" style="height: 20%; width:30%;color : black; background-color: GhostWhite;"></select>  

    <br>
    
	<p id="para" style="text-align: center;  font-family: Helvetica Neue; font-size: 100%;">ALARM CLOCK IS NOT YET SET!</p> 
    </div>
    
    <div align="center">
    <p>    Smart Wake Up Function:</p>
       
   <input name="back_alarm" id="back_alarm" type="checkbox" value="m"/>    
    <br>
    <br>  
       
    <select id="minuti_back_alarm" style="height: 20%; width:30%;color : black; background-color: GhostWhite;"/>  
    </div>

   
</body>
</html>
