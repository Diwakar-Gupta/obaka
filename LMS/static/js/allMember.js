
document.querySelector('#table-form > div > ul > li:nth-child(2) > input').onkeyup=function(){
    let key = this.value.toLowerCase()
    if(key.length>0)
    $.ajax({
                type: 'POST',
                url: '/member/name',
                data: {
                    'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
                    'name':key
                    },
                success: function (data) {
                    datas = JSON.parse(data)
                    if(datas['requested']==key){
                        let datalist=$(document.querySelector('#name'));
                        datalist.empty();
                        let list = datas['names']
                        list.forEach(e=>datalist.append('<option>'+e+'</option>'))
                        
                    }
                },
            });
};

    let infiniteLoopWorking = false;
    let lastScrollTop = 0;
    document.getElementById('content').onscroll = function () {
        c = document.getElementById('content')
        if (lastScrollTop != c.scrollTop && infiniteLoopWorking == false && c.scrollHeight - c.offsetHeight - c.scrollTop <= 0 &&  document.getElementById('allMember').children.length>=20) {
            lastScrollTop = c.scrollTop;
            infiniteLoopWorking = true;
            let form = $('#table-form')[0]
            $.ajax({
                type: 'GET',
                url: '',
                data: {
                    'have': document.getElementById('allMember').children.length
                },
                success: function (data) {
                    list = JSON.parse(data);

                    if (list == false)
                        makeToast('No more queries');
                    else {
                        table = document.getElementById('allMember');
                            table.innerHTML += data
                    }

                    setTimeout(function () {
                        infiniteLoopWorking = false
                    }, 500);
                },
                error: function (data) {
                    makeToast('Cant connect to server','error');
                }
            });
        }
    }
