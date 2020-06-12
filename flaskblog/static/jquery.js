   $(document).ready(function(){
        
        $(document).on("click", "#target", function() {
        	//check is an array of integers which i am converting to an array of strings and then to String data type
            check.push(show2);
            console.log("p is"+p);
            check.map(String);
        	var check2=check.toString();
            
            //alert(check2); 
            console.log(typeof check2);
            var s=0;
            for(var i=0;i<check.length-1;i++){
                        if(check[i]>=0 && check[i]<=39)
                            s=s+r2;
                        else if(check[i]<=199 && check[i]>=160)
                            s=s+c3;
                        else 
                            s=s+p;
                    }
                    
            //console.log(show2)
             $.ajax({
			    
			     type: "GET",
			     url: "http://localhost:5000/process",
			     //url: "{{url_for('process')}}"			     
			     //data: JSON.stringify(check2),

			     data :{check2: check2},
			     //dataType: 'json',
			     //contentType: "application/json;charset=utf-8",
			     success: function() {
                    alert("Total cost of seats is: "+ s);
	            },
	            error: function() {
	                console.log("not done");
	            }

			}); 
            window.location.href="/"
        });
    });