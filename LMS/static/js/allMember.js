
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
    document.getElementById('content').onscroll = function () {
        c = document.getElementById('content')
        if (c.scrollHeight - c.offsetHeight - c.scrollTop == 0 && infiniteLoopWorking == false) {
            infiniteLoopWorking = true;
            let form = $('#table-form')[0]
            $.ajax({
                type: 'GET',
                url: '/member',
                data: {
                    'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
                    'membertype': document.getElementsByName('membertype')[0].value,
                    'idrangemin': document.getElementsByName('idrangemin')[0].value,
                    'idrangemax': document.getElementsByName('idrangemax')[0].value,
                    'active': document.getElementsByName('active')[0].value,
                    'issued': document.getElementsByName('issued')[0].value,
                    'fine': document.getElementsByName('fine')[0].value,
                    'overdue': document.getElementsByName('overdue')[0].value,
                    'have': document.getElementById('allMember').children.length
                },
                success: function (data) {
                    list = JSON.parse(data);

                    if (list == false)
                        return
                    else {
                        table = document.getElementById('allMember');

                        list.forEach(function (e) {
                            table.innerHTML += '<tr>' +
                                '<td><a href="/' + e.type + '/' + e.id + '">' + e.id + '</a></td>\n' +
                                '<td>' + e.name + '</td>\n' +
                                '<td><a target="_blank" href="/admin/LMS/userbasicsetting/' + e.type + '/change">' + e.type + '</a></td>\n' +
                                '<td>' + e.active + '</td>\n' +
                                '<td>' + e.issued + '</td>\n' +
                                '</tr>'
                        })
                    }

                    setTimeout(function () {
                        infiniteLoopWorking = false
                    }, 500);
                },
                error: function (data) {
                }
            });
        }
    }