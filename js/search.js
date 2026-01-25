(function(){
  let fuse;
  fetch('js/recipes.json').then(r=>r.json()).then(data=>{
    fuse = new Fuse(data, {keys:['title','category','ingredients'],threshold:0.3});
  }).catch(()=>{});
  
  const input = document.getElementById('search');
  const results = document.getElementById('search-results');
  if(!input||!results)return;
  
  let timer;
  input.addEventListener('input', function(){
    clearTimeout(timer);
    timer = setTimeout(()=>{
      const q = this.value.trim();
      if(q.length<2){results.classList.remove('active');results.innerHTML='';return;}
      if(!fuse)return;
      const r = fuse.search(q).slice(0,8);
      if(!r.length){results.innerHTML='<div class="search-result-item"><span class="title">No recipes found</span></div>';results.classList.add('active');return;}
      results.innerHTML = r.map(x=>`<a href="recipes/${x.item.slug}/" class="search-result-item"><span class="title">${x.item.title}</span><span class="category">${x.item.category}</span></a>`).join('');
      results.classList.add('active');
    },150);
  });
  
  document.addEventListener('click',e=>{if(!input.contains(e.target)&&!results.contains(e.target))results.classList.remove('active');});
  input.addEventListener('keydown',e=>{if(e.key==='Escape'){results.classList.remove('active');input.blur();}if(e.key==='Enter'){const a=results.querySelector('a');if(a)location.href=a.href;}});
})();
