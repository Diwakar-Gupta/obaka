
                    let infiniteLoopWorking = false;
                    document.getElementById('content').onscroll= function(){
                        c=document.getElementById('content')
                        if(c.scrollHeight -c.offsetHeight -c.scrollTop <=0 && infiniteLoopWorking==false && document.getElementById('allBook').children.length>=20){
                            infiniteLoopWorking = true;
                            setTimeout(function(){
                                        infiniteLoopWorking = false
                                    },3000);
                            let form=$('#table-form')[0]
                            $.ajax({
                                type: 'GET',
                                url: '',
                                data: {
                                    'have':document.getElementById('allBook').children.length
                                },
                                success: function (data) {
                                    list = JSON.parse(data);
                                    table = document.getElementById('allBook');
                                    if(list == false){
                                        makeToast('No more queries');
                                    }        
                                    else{
                                        
                
                                        list.forEach(function(e){
                                            table.innerHTML += '<tr><td>'+e.isbn+'</td><td>'+e.title+'</td><td>'+e.author +'</td><td>'+e.quantity+'</td><td>'+e.issued+'</td><td>'+e.deactive +'</td></tr>'
                                        })
                                    }
                
                                    setTimeout(function(){
                                        infiniteLoopWorking = false
                                    },500);
                                },
                                error: function (data) {
                                    makeToast('Cant connect to server','error');
                                }
                    });
                        }
                    }
