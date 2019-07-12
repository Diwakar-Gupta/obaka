let infiniteLoopWorking = false;
    document.getElementById('content').onscroll = function () {
        c = document.getElementById('content')
        if (c.scrollHeight - c.offsetHeight - c.scrollTop <= 0 && infiniteLoopWorking == false) {
            infiniteLoopWorking = true;
            $.ajax({
                type: 'GET',
                url: '',
                data: {
                    'have': document.getElementById('circulations').children.length
                },
                success: function (data) {
                    list = JSON.parse(data);
                    if (list == false)
                        makeToast('No more circulations');
                    else {
                        table = document.getElementById('circulations');

                        list.forEach(function (e) {
                            table.innerHTML += '<tr>'+
      '<td>'+
        '<span>'+e.date+'</span>'+
      '</td>'+
      '<td><a href="#">'+e.title+'</a></td>'+
      '<td>'+e.author+'</td>'+
      '<td><a target="_blank" href="/admin/LMS/isbn/'+ e.barcode +'/change">'+ e.barcode +'</a></td>'+
      '<td>'+e.countrenewal+'</td>'+
      '<td>'+
        '<span>'+ e.issued_time +'</span>'+
      '</td>'+
     '<td>'+ e.issuefrom +'</td>'+
      '<td>'+
        '<span>'+ e.duedate +'</span>'+
      '</td>'+
      '<td>'+
        e.return_date
      '</td>'+
    '</tr>'})
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
