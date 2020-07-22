const loadRevisionItem=()=>{
    let url = '/api/revision/';
     fetch(url)
      .then(response=>{
          
          return response.json();
      })
      .then(res=>{
          $('#tags').empty();
          let tags = res['tags'];
          if (tags.length)
          {
            $('#tags').empty();
            $.each(tags, function( index, value ) {
                  $('#tags').append(`<div><h5><span class="badge badge-info mr-2" >${value}</span><h5></div>`);
                  });
          }
          $(".modal-body-revision").html(res["content"]);
          $("#model_id").html(res["pk"]);
          upd = res["updated"]
          $("#last_upd").html(upd.split("T")[0]);
         
      });
    
   
  }
   const NextRevisionItem=()=>{
      let id = $("#model_id").html();
      let url = `/api/revision/${id}/`;
        
      fetch(url)
      .then(response=>{
        return response.json();
      })
      .then(res=>{
        
      });
      loadRevisionItem(); // load new questions
    }
  
    const EditRevisionItem=()=>{
      let id = $("#model_id").html();
      let url = `/comments/update/${id}/`;
      window.open(url, "_blank"); 
    }

    const updateActivityStatu = (pk) =>{
        fetch(`/api/activities/done/${pk}/`)
        .then(response=>{
            return response.json();
        })
        .then(res=>{
            if (res =='Done')
            {
                /** redirect to Activity list */
                window.location = "/activity/"; 
            }
            else
            {
                console.log(res);
            }
            
        });
    }