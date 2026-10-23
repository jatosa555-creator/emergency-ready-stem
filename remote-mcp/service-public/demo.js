const steps={scope:['Inspect the public source scope','list_collections',{}],search:['Search: ออฟไลน์ (offline)','search_references',{query:'ออฟไลน์',limit:3}],read:['Read exact original guidance: ER-02','get_reference',{id:'ER-02'}],example:['Read a clearly labeled synthetic example: ER-04','get_reference',{id:'ER-04'}],missing:['Unknown source ER-99 stays missing','get_reference',{id:'ER-99'}],reject:['A write tool does not exist','delete_file',{}]};
for(const b of document.querySelectorAll('button[data-step]'))b.addEventListener('click',async()=>{
 const [title,name,args]=steps[b.dataset.step];document.querySelector('#heading').textContent=title;
 document.querySelector('#meta').textContent='Calling actual production endpoint…';document.querySelector('#output').textContent='';
 for(const x of document.querySelectorAll('button')){x.disabled=true;x.setAttribute('aria-pressed',String(x===b));}
 try{const r=await fetch('/mcp',{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json, text/event-stream'},body:JSON.stringify({jsonrpc:'2.0',id:1,method:'tools/call',params:{name,arguments:args}})});const data=await r.json();const d=data.result?.structuredContent;
 document.querySelector('#meta').textContent=`Actual HTTPS response · HTTP ${r.status} · ${new Date().toISOString()} · ${name}`;
 document.querySelector('#output').textContent=d?.text?`${d.id} — ${d.title}\n${d.source_type} · v${d.version} · snapshot ${d.snapshot_date}\n\n${d.text}\n\n${d.citation}`:JSON.stringify(d??data,null,2);
 }catch(e){document.querySelector('#meta').textContent='Connection failed; no source is fabricated.';document.querySelector('#output').textContent=String(e);}
 finally{for(const x of document.querySelectorAll('button'))x.disabled=false;}
});
