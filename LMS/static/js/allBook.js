
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
                                    table = document.getElementById('allBook');
                                    if(data == "false"){
                                        makeToast('No more queries');
                                    }        
                                    else{
                                        table.innerHTML += data
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
