
$('.sort').append('<i class="fas fa-sort"></i><i class="fas fa-sort-up" style="display:none"></i><i class="fas fa-sort-down" style="display:none"></i>');

let sort = document.getElementsByName('sort')[0];
function sortDisp(){
    let type=sort.value.split('-')
    cont=document.querySelector('.sort[value='+type[0]+']')
    cont.querySelector('.fa-sort').style['display']='none'
    cont.querySelector('.fa-sort-'+type[1]).style['display']='inline-block'
};
if(sort.value)
sortDisp();
function clearSort(){
    $('thead .fas').css('display','none')
    $('thead .fa-sort').css('display','inline-block')
};
$('thead .fa-sort-up').on('click',function(){
    clearSort();
    this.parentElement.querySelector('.fa-sort').style['display']="none"
    this.parentElement.querySelector('.fa-sort-down').style['display']="inline-block"
    sort.value=$(this.parentElement).attr('value')+"-down"
    sort.form.submit()
});
$('thead .fa-sort').on('click',function(){
    clearSort();
    this.style['display']="none"
    this.parentElement.querySelector('.fa-sort-up').style['display']="inline-block"
    sort.value=$(this.parentElement).attr('value')+"-up"
    sort.form.submit()
});
$('thead .fa-sort-down').on('click',function(){
    clearSort();
    sort.value="";
    sort.form.submit()
});
