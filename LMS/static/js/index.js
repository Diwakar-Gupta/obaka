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

$('th').click(sortThis);
$('th').append('<i class="fas fa-long-arrow-alt-down sorted"></i>');
$('.searchTable').on('keyup',searchTable);

$('.changelist-filter .yesnoall>span').not("span.active").on('click',function(){
    parent=this.parentNode
    input=parent.querySelector('input[type=hidden]')
    input.value=this.innerText
    input.form.submit();
});

function makeToast(message="",header=""){
    let toast = document.getElementById('message')
    toast.getElementsByClassName("header")[0].innerText = header
    toast.getElementsByClassName("toast-body")[0].innerText = message
    $(toast).toast('show');
    //setInterval(function(){$(toast).toast('hide');},3500)
  }