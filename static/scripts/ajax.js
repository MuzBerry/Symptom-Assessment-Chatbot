$(document).ready(function(){
    const userimg = "/static/user.png"
    const botimg = "/static/doctor.png"
    let choice = "yes"
    let model_no = ""
    const m = "menu"
    // let after_opt = ["Enter symptoms to get medicine","Enter Medicine Name", "Enter the symptoms"]
    
    
    $(".input-area").submit(function(e){
        let text = $(".input-text").val();
        text = text.trim();
        document.getElementById("input-area").reset();
        
        if (text === m ){
            choice = "yes"
            model_no = ""
            msg_append("Choices resseted",botimg,"left","Medico");
            console.log(choice);
            console.log(model_no)
            
        }

        else if(!text){
            alert("Gotta enter a text!!")
            console.log(choice);
        }
        
        else if((text === "1" || text === "2" || text === "3" || text == "4") && choice === "yes"){
            const after_opt = ["Enter symptoms to get medicine","Enter Medicine Name", "Enter the symptoms","Name a Disease"]
            model_no = text
            msg_append(text,userimg,"right","Me")
            msg_append(after_opt[parseInt(model_no)-1],botimg,"left","Medico")
            choice = "no"
            console.log(choice)
        }
       
        else if((model_no === "1" || model_no === "2" || model_no === "3" || model_no == "4") && choice === "no"){
            msg_append(text,userimg,"right","Me");
            total = model_no +"." + text
            totals = "Send from front end"
            console.log(choice);
            console.log(model_no)
            $.ajax({
                type: "POST",
                url: "/res", 
                data: {
                       msg:total, 
                },
                
                
               
                
            }).done(function(data){
                if (data.modelno === "1"){
                    if(data.response.length === 1){
                        msg_append("One medicine found in our database", botimg, "left", "Medico")
                        medicine_append(data.response , botimg, "left", "Medico",1)
                    }
                    else if (data.response.length > 1){
                        msg_append("More than one medicine found in our database ", botimg, "left", "Medico")
                        medicine_append(data.response,botimg,"left","Medico",1)
                    }
                    else {
                        msg_append("No medicine found, try being more specific ", botimg, "left", "Medico")
                    }
                }
                else if (data.modelno === "2"){
                    
                    if (data.response.length === 1){
                        msg_append("One medicine found in our database", botimg, "left", "Medico")
                        medicine_append(data.response , botimg, "left", "Medico",2)
                    }
                    else if (data.response.length > 1){
                        msg_append("More than one medicine found in our database ", botimg, "left", "Medico")
                        medicine_append(data.response,botimg,"left","Medico",2)
                    }
                    else {
                        msg_append("No medicine found, try being more specific ", botimg, "left", "Medico")
                    }
                    }
                else if (data.modelno === "3"){
                    if (data.response.length === 1){
                    msg_append("The predicted disease is: "+ data.response[0]["Disease"],botimg,"left","Medico")
                    }
                    else if (data.response.length > 1){
                    dis = []
                    msg_append("More than one disease was predicted. Prediction is given in decending order of probablity" ,botimg,"left","Medico")
                    for (let i = 0; i < data.response.length; i++){
                        dis.push(data.response[i]["Disease"])
                    }
                    
                    msg_append("The predicted diseases are: "+ dis.toString() ,botimg,"left","Medico")
                    }
                    else{
                        msg_append("No disease found, try entering some more symptoms",botimg,"left","Medico")
                    }
                    }
                else if(data.modelno === "4"){
                    if (data.response.length === 1){
                        msg_append("Following are the symptoms for "+ data.response[0]["Disease"],botimg,"left","Medico")
                        symptom_append(data.response,botimg,"left","Medico")
                    }
                    else if (data.response.length > 1){
                        msg_append("More than one disease was predicted for the following query found" ,botimg,"left","Medico")
                        symptom_append(data.response,botimg,"left","Medico")

                    }
                    else{
                        msg_append("No disease found in the database, try beign more specific" ,botimg,"left","Medico")
                    }
                }
                
                
            });
        
             
            
            
        }
       
        else {
            msg_append(text,userimg,"right","Me")
            msg_append("You need to select what you want!!",botimg,"left","Medico");
        }

    
    
        
         
        console.log(text);
        e.preventDefault();
        
    });
    function msg_append(text,img,side,who){
        let todayDate = new Date()
        let todayTime = todayDate.getHours()+ ":" + todayDate.getMinutes()

        const common_msg = `
        <div class="msg ${side}-chat">
                        <div class="chat-image-container">
                             <img src=${img} alt="" class="chat-image">
                        </div>
                        <div class="chat-box">
                          <div class="chatter">
                              <div class="chatter-name">${who}</div>
                              <div class="chatter-time">${todayTime}</div>
                          </div>
                          <div class="chat-text">${text}</div>
                        </div>
      
      
                  </div>`;
          $(".chat").append(common_msg);
      
      }
      function medicine_append(res,img,side,who,model){
        let todayDate = new Date()
        let todayTime = todayDate.getHours()+ ":" + todayDate.getMinutes()
          if(model === 2){  
            for(let i =0; i< res.length; i++){
            let med_name = res[i]["Medicine Name"][0]
            let uses = res[i]["Uses"]
            let pres = res[i]["Prescription"]
            if (pres === "N"){
                pres = "Not required"
            }
            let mrp = res[i]["MRP"]

            const common_msg = `
            <div class="msg ${side}-chat">
                            <div class="chat-image-container">
                                <img src=${img} alt="" class="chat-image">
                            </div>
                            <div class="chat-box">
                            <div class="chatter">
                                <div class="chatter-name">${who}</div>
                                <div class="chatter-time">${todayTime}</div>
                            </div>
                            <div class="chat-text">
                            <ol>
                            
                            <li>Medicine Name: ${med_name}</li>
                            <li>Uses: ${uses.toString()}</li>
                            <li>Prescription: ${pres}</li>
                            <li>MRP: ${mrp}</li>
                            
                            </ol>

                            </div>
                            </div>
        
        
                    </div>`;
            $(".chat").append(common_msg);

            }
          }
          else{
            for(let i =0; i< res.length; i++){
                let med_name = res[i]["Medicine Name"]
                let pres = res[i]["Prescription"]
                if (pres === "N"){
                    pres = "Not required"
                }
                let mrp = res[i]["MRP"]
    
                const common_msg = `
                <div class="msg ${side}-chat">
                                <div class="chat-image-container">
                                    <img src=${img} alt="" class="chat-image">
                                </div>
                                <div class="chat-box">
                                <div class="chatter">
                                    <div class="chatter-name">${who}</div>
                                    <div class="chatter-time">${todayTime}</div>
                                </div>
                                <div class="chat-text">
                                <ol>
                                
                                <li>Medicine Name: ${med_name}</li>
                                
                                <li>Prescription: ${pres}</li>
                                <li>MRP: ${mrp}</li>
                                
                                </ol>
    
                                </div>
                                </div>
            
            
                        </div>`;
                $(".chat").append(common_msg);
    
                }
          }
        // let med_name = res[0]["Medicine Name"][0]
        // let uses = res[0]["Uses"]
        // let pres = res[0]["Prescription"]
        // if (pres === "N"){
        //     pres = "Not required"
        // }
        // let mrp = res[0]["MRP"]

        // const common_msg = `
        // <div class="msg ${side}-chat">
        //                 <div class="chat-image-container">
        //                      <img src=${img} alt="" class="chat-image">
        //                 </div>
        //                 <div class="chat-box">
        //                   <div class="chatter">
        //                       <div class="chatter-name">${who}</div>
        //                       <div class="chatter-time">${todayTime}</div>
        //                   </div>
        //                   <div class="chat-text">
        //                   <ol>
                          
        //                   <li>Medicine Name: ${med_name}</li>
        //                   <li>Uses: ${uses.toString()}</li>
        //                   <li>Prescription: ${pres}</li>
        //                   <li>MRP: ${mrp}</li>
                          
        //                  </ol>

        //                   </div>
        //                 </div>
      
      
        //           </div>`;
        //   $(".chat").append(common_msg);
      
      }
      function symptom_append(res,img,side,who){

        let todayDate = new Date()
        let todayTime = todayDate.getHours()+ ":" + todayDate.getMinutes()
        for(let i=0;i< res.length; i++ ){
            let disease = res[i]["Disease"]
            let symptoms =  res[i]["Symptoms"]

        

        const common_msg = `
        <div class="msg ${side}-chat">
                        <div class="chat-image-container">
                            <img src=${img} alt="" class="chat-image">
                        </div>
                        <div class="chat-box">
                        <div class="chatter">
                            <div class="chatter-name">${who}</div>
                            <div class="chatter-time">${todayTime}</div>
                        </div>
                        <div class="chat-text">
                        <ul>
                        
                        <li>Disease Name: ${disease}</li>
                         <li>Symptoms: <ol>${symptoms.map(symptom => `<li>   ${symptom}</li>`).join("")}</li> </ol>
                      
                         
                        </ul>

                        </div>
                        </div>
    
    
                </div>`;
        $(".chat").append(common_msg);
        }
      }
   
    

})

// function msg_append(text,img,side){
//   const common_msg = `
//   <div class="msg ${side}-chat">
//                 <div class="chat-image">
 
//                 </div>
//                 <div class="chat-box">
//                     <div class="chatter">
//                         <div class="chatter-name">Me</div>
//                         <div class="chatter-time">23:35</div>
//                     </div>
//                     <div class="chat-text">${text}</div>
//                 </div>


//             </div>`;
//     $(".chat").append(common_msg);
    
// }







 
