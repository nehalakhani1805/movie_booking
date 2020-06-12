var c=['A','B','C','D','E','F','G','H','I','J'];var clicks=0;
 //var arr =[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
 var check=[]; var show2=0;var p=0;var r2=0;var c3=0;
    function buttons(arr,selected,show,tr,tp,tc)
    {    
         show2=show     
         console.log(show2)
         p=tp;
         r2=tr;
         c3=tc;
         document.getElementById("clickme").style.display = "none";
         //document.getElementById("plus").style.display = "none";
         //document.getElementById("minus").style.display = "none";
         //document.getElementById("clicks").style.display = "none";
         var newline; var tab;
         var docFrag = document.createDocumentFragment();
         var test=document.createElement('h6');
                 test.innerHTML='PREMIUM '+'Rs.'+p;
                 test.style.marginLeft='700px';
        var test2=document.createElement('h6');
                 test2.innerHTML='RECLINER '+'Rs.'+r2;
                 test2.style.marginLeft='700px';
        var test3=document.createElement('h6');
                 test3.innerHTML='CLASSIC '+'Rs.'+c3;
                 test3.style.marginLeft='700px';
                 var test4=document.createElement('h6');
                 test4.innerHTML='ALL EYES THIS WAY';
                 test4.style.marginLeft='680px';
         //docFrag.appendChild(test);
         var k=selected;var k2=-1;var j;
         for (var i=0; i < 10; i++){
             for(j=0;j<20;j++){
                 k2++;
                 var elem = document.createElement('input');
                 newline = document.createElement('p');
                 tab = document.createElement('p');
                 var row = document.createElement('input');
                 
                 tab.value="\t\t\t\t\t\t";
                 row.value=c[9-i];
                 row.disabled=true;
                 row.type = 'button';
                 row.style.marginLeft='250px';
                 elem.type = 'button';
                 elem.value = "  "+(j+1)+"  ";
                 elem.id=k2;

                 if(arr[k2]=='1'){
                    elem.style.backgroundColor='black';
                    elem.disabled=true;
                 }
                 else
                 {
                    if(i==0||i==1)
                        elem.style.backgroundColor='#0CCCE1';
                    else if(i==9||i==8)
                        elem.style.backgroundColor='#FE7281  ';
                    else
                        elem.style.backgroundColor='#60EE3C ';
                 }
                //if(i==0){
                    //elem.style.marginTop='0px';
                    //row.stlye.marginTop='0px';
                    
                //} 

                 elem.onclick = function() {
                    //var tid=this.id;
                    //alert(tid);
                    if(this.style.backgroundColor=='grey'){
                        console.log("k here is"+k)
                        //alert("hi");#87898C
                        var a=this.id;
                        //var b=this.id[this.id.length-1];
                        //alert(a+b);
                        arr[a]='0';
                        check.pop(a);
                        if(a>=0&&a<=39)
                        this.style.backgroundColor='#0CCCE1';
                        else if(a>=40&&a<=159)
                        this.style.backgroundColor='#60EE3C';
                        else
                        this.style.backgroundColor='#FE7281';
                        //this.disabled=true;
                        k++;
                        
                    }
                    else //if(this.style.backgroundColor=='#0CCCE1'||this.style.backgroundColor=='#60EE3C'||this.style.backgroundColor=='#FE7281')
                    {
                        var a=this.id;
                        //var b=this.id[this.id.length-1];
                        //alert(a+b);
                        
                        if(k!=0)
                        {
                            this.style.backgroundColor='grey';
                            //this.disabled=true;
                            arr[a]='1';
                            check.push(a);
                            console.log(check[0]);
                            k--;
                            console.log("k="+k)
                        }
                        else
                        {
                            alert("Ticket limit exceeded!");
                        }
                    }
                };
                 newline.value='\n';
                 if(i==2&&j==0)
                    docFrag.appendChild(test);
                if(i==0&&j==0)
                    docFrag.appendChild(test2);
                if(i==8&&j==0)
                    docFrag.appendChild(test3);

                 if(j==0){
                    //row.value=c[i];
                    //c++;

                    //docFrag.appendChild(test);
                    docFrag.appendChild(tab);
                    docFrag.appendChild(row);
                 }
                    
                docFrag.appendChild(elem);
             }
 //document.body.appendChild("\n");
            docFrag.appendChild(newline);
            c.value++;
           
        }
        var sub = document.createElement('input');
        sub.type = 'button';
        sub.value = "Done";
        sub.style.padding='5px';
        sub.style.paddingLeft='8px';
        sub.style.paddingRight='8px';
        sub.style.color='white';
        sub.style.backgroundColor='#1D14CD  '
        sub.style.marginLeft='1300px';
        sub.setAttribute("id","target");
        docFrag.appendChild(sub);

        //test4.style.marginTop='30px';
        docFrag.appendChild(test4);
        var line = document.createElement('hr');
        line.style.borderTop="3px solid black";
        line.style.marginLeft='50px';
        line.style.marginRight='50px';
        
        //line.style.color='black';
        //line.style.display='block';
        docFrag.appendChild(line);


        //nl = document.createElement('p');
        //nl.value="\n\n";
        //docFrag.appendChild(nl);
        
        console.log(arr[0]);

        document.body.appendChild(docFrag);
}
        
