function searchTable(){
    let searchText = this.value.toLowerCase();
    let tbody = $(this.attributes['data-target'].value);
    let tr = tbody.find('tr');
    for (i = 0; i < tr.length; i++) {
        if (tr[i].textContent.toLowerCase().indexOf(searchText) == -1)
            tr[i].hidden = true;
        else tr[i].hidden = false;
    }
}

function sortThis(){

    let parent = $($(this).parent());
    dtype = $(this).attr('dtype')
    index = parent.children().index(this);
    target = $(parent.parent()).next();
    //target.fadeOut('slow');
    children = $(target).children();
    if(dtype=='int')
    children.sort(function (a, b) {
        first = parseInt($(a).children()[index].textContent)
        second = parseInt($(b).children()[index].textContent)
        result = first < second
        return result * -1
    });
    else
    children.sort(function (a, b) {
        return $(a).children()[index].textContent.toLowerCase().localeCompare($(b).children()[index].textContent.toLowerCase())
    });

    $(children[0]).insertBefore($($(target).children[0]))
    for(i=1;i<children.length;i++){
        $(children[i]).insertAfter($(children[i-1]));
    };
    //target.fadeIn()

    $(parent.find('th .sorted')).css('display','none')
    $($(this).find('.sorted')).css('display','inline')
}

$('thead td input[type=checkbox] ').on('change',function(){
    ar = $($(this).parent().parent().parent().next()).find('input[type=checkbox]')
    if(this.checked){
        for(i=0;i<ar.length;i++)
        ar[i].checked=true
    }
    else {
        for(i=0;i<ar.length;i++)
    ar[i].checked=false
    }
});

$('.js-sort th').click(sortThis);
$('.js-sort th').append('<i class="fas fa-long-arrow-alt-down sorted"></i>');
$('.searchTable').on('keyup',searchTable);

$('.changelist-filter .yesnoall>span').not("span.active").on('click',function(){
    parent=this.parentNode
    input=parent.querySelector('input[type=hidden]')
    input.value=this.innerText
});


function makeToast(message,type="success"){
    if(type=='success')
        type="alert-success"
    else
        type='alert-warning'
    let content = document.getElementById('messages');
    let elem = document.createElement('div')
    let ele = $(elem)
    ele.addClass('alert '+type+' alert-dismissible')
    ele.append('<button type="button" class="close" data-dismiss="alert">&times;</button><strong >'+message+'</strong>')
    content.prepend(elem)
    setInterval(function(){ele.fadeOut('')},3000)
}
