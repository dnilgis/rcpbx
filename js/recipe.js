(function(){
  // Ingredient checking
  const ingList = document.querySelector('.ingredients-list');
  if(ingList) ingList.addEventListener('click',e=>{const li=e.target.closest('li');if(li)li.classList.toggle('checked');});
  
  // Step highlighting
  const steps = document.querySelector('.steps-list');
  if(steps) steps.addEventListener('click',e=>{
    const li = e.target.closest('li');
    if(!li)return;
    const all = steps.querySelectorAll('li');
    const isActive = li.classList.contains('active');
    all.forEach(s=>s.classList.remove('active','dimmed'));
    if(!isActive){li.classList.add('active');all.forEach(s=>{if(s!==li)s.classList.add('dimmed');});}
  });
  
  // Scaling
  const orig = [];
  document.querySelectorAll('.ingredients-list .amount').forEach((el,i)=>{orig[i]=parseAmt(el.textContent);});
  document.querySelectorAll('.scale-btn').forEach(btn=>{
    btn.addEventListener('click',function(){
      const scale = parseFloat(this.dataset.scale);
      document.querySelectorAll('.scale-btn').forEach(b=>b.classList.remove('active'));
      this.classList.add('active');
      document.querySelectorAll('.ingredients-list .amount').forEach((el,i)=>{if(orig[i]!==null)el.textContent=fmtAmt(orig[i]*scale);});
    });
  });
  
  function parseAmt(s){
    const frac={'½':.5,'⅓':.333,'⅔':.667,'¼':.25,'¾':.75,'⅛':.125};
    const m=s.match(/^(\d+)\s*([\u00BC-\u00BE\u2150-\u215E])/);
    if(m)return parseInt(m[1])+(frac[m[2]]||0);
    for(let[f,v]of Object.entries(frac))if(s.includes(f))return v;
    const n=parseFloat(s);return isNaN(n)?null:n;
  }
  function fmtAmt(n){
    if(n===null)return'';
    const frac=[[.125,'⅛'],[.25,'¼'],[.333,'⅓'],[.5,'½'],[.667,'⅔'],[.75,'¾']];
    const w=Math.floor(n),d=n-w;let f='';
    for(let[v,s]of frac)if(Math.abs(d-v)<.05){f=s;break;}
    if(w===0&&f)return f;if(f)return w+f;
    if(n<1)return n.toFixed(2).replace(/\.?0+$/,'');
    return n%1===0?n.toString():n.toFixed(1).replace(/\.0$/,'');
  }
  
  // Wake lock
  const wl = document.getElementById('wake-lock');
  let lock = null;
  if(wl && 'wakeLock' in navigator){
    wl.parentElement.style.display='flex';
    wl.addEventListener('change',async function(){
      if(this.checked){try{lock=await navigator.wakeLock.request('screen');this.parentElement.classList.add('active');}catch(e){this.checked=false;}}
      else{if(lock)lock.release();lock=null;this.parentElement.classList.remove('active');}
    });
  }
})();

// Keyboard shortcuts
(function(){
  const steps = document.querySelectorAll('.steps-list li');
  const ings = document.querySelectorAll('.ingredients-list li');
  if(!steps.length) return;
  
  let currentStep = -1;
  let currentIng = 0;
  
  function highlightStep(i){
    steps.forEach((s,idx)=>{
      s.classList.remove('active','dimmed');
      if(i>=0){
        if(idx===i){s.classList.add('active');s.scrollIntoView({behavior:'auto',block:'center'});}
        else{s.classList.add('dimmed');}
      }
    });
    currentStep = i;
  }
  
  document.addEventListener('keydown', e=>{
    // Ignore if typing in input
    if(e.target.tagName==='INPUT'||e.target.tagName==='TEXTAREA') return;
    
    // j = next step
    if(e.key==='j'){
      e.preventDefault();
      highlightStep(Math.min(currentStep+1, steps.length-1));
    }
    // k = prev step
    if(e.key==='k'){
      e.preventDefault();
      highlightStep(Math.max(currentStep-1, -1));
    }
    // space = check ingredient
    if(e.key===' '&&ings.length){
      e.preventDefault();
      if(currentIng<ings.length){
        ings[currentIng].classList.add('checked');
        currentIng++;
      }
    }
    // r = reset
    if(e.key==='r'){
      highlightStep(-1);
      currentIng=0;
      ings.forEach(i=>i.classList.remove('checked'));
    }
  });
})();
