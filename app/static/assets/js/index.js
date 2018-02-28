/* globals console,document */

var tmpl_list = function(id,title,desc,category,favorite){
    return [
'<li class="list-group-item">',
'    <a href="/notes/get/',id,'" title="',title,'">',
'        <div>',title,'</div>',
'       <div>',
'           <small><em>',desc,'</em></small>',
'        </div>',
'    </a>',
'</li>'].join('');
}


var site = (function(){
   return {
       list: function(){
           $('.menu .list-group').html(tmpl_list(0,'loading...','..'));
           $.get(site_url+'notes/get/all',function(resolve){
               var data = JSON.parse(resolve),
                   template = '';
               $.each(data,function(i,r){
                   template += tmpl_list(r.uid,r.title,r.desc,r.category);
               });
               $('.menu .list-group').html(template);
           });
       },
       search: function(name){
           $('.menu .list-group').html(tmpl_list(0,'loading...','..'));
           $.get(site_url+'notes/search/'+name,function(resolve){
               var data = JSON.parse(resolve),
                   template = '';
               $.each(data,function(i,r){
                   template += tmpl_list(r.uid,r.title,r.desc);
               });
               $('.menu .list-group').html(template);
           });   
       }
   } 
})();



$(document).ready(function(){
    site.list();
    $('#search').on('submit',function(e){
        e.preventDefault();
        if($('#name').val().trim() === ''){
            site.list();
        }else{
            site.search($('#name').val().trim());    
        }
        return false;
    });
    $('#name').on('keypress',function(e){
        if($('#name').val().trim() === ''){
            site.list();
        }
    })
});