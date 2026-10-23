import assert from 'node:assert/strict';
import {mkdir,writeFile} from 'node:fs/promises';
const base='https://emergency-ready-stem-knowledge.netlify.app';
const evidence={captured_at:new Date().toISOString(),base,kind:'actual public HTTPS protocol calls, not LLM or classroom evaluation',checks:[]};
async function record(label,method,params={}){
 const r=await fetch(base+'/mcp',{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json, text/event-stream'},body:JSON.stringify({jsonrpc:'2.0',id:1,method,params}),signal:AbortSignal.timeout(30000)});
 const data=await r.json();evidence.checks.push({label,status:r.status,request:{method,params},response:data});assert.equal(r.status,200);return data;
}
const h=await fetch(base+'/health',{signal:AbortSignal.timeout(30000)});assert.equal(h.status,200);evidence.health=await h.json();assert.equal(evidence.health.status,'ok');assert.equal(evidence.health.items,12);
await record('initialize','initialize',{protocolVersion:'2025-03-26',capabilities:{},clientInfo:{name:'emergency-stem-release-check',version:'0.4.0'}});
const tools=await record('discover','tools/list');assert.deepEqual(tools.result.tools.map(x=>x.name).sort(),['get_reference','list_collections','search_references']);
const scope=await record('source provenance','tools/call',{name:'list_collections',arguments:{}});assert.equal(scope.result.structuredContent.items,12);
const search=await record('search low-tech guidance','tools/call',{name:'search_references',arguments:{query:'ออฟไลน์',limit:3}});assert.ok(search.result.structuredContent.results.some(x=>x.id==='ER-02'));
const read=await record('read original guidance','tools/call',{name:'get_reference',arguments:{id:'ER-02'}});assert.equal(read.result.structuredContent.source_type,'original-guidance');
const example=await record('read labeled example','tools/call',{name:'get_reference',arguments:{id:'ER-04'}});assert.equal(example.result.structuredContent.source_type,'synthetic-example');
const missing=await record('unknown source stays missing','tools/call',{name:'get_reference',arguments:{id:'ER-99'}});assert.equal(missing.result.structuredContent.found,false);
const invalid=await record('reject arbitrary URL','tools/call',{name:'get_reference',arguments:{id:'https://private.invalid'}});assert.ok(invalid.error||invalid.result?.isError);
const unknown=await record('reject nonexistent write tool','tools/call',{name:'delete_file',arguments:{}});assert.ok(unknown.error||unknown.result?.isError);
const get=await fetch(base+'/mcp');assert.equal(get.status,405);evidence.checks.push({label:'GET is not SSE',status:get.status});
const origin=await fetch(base+'/mcp',{method:'POST',headers:{Origin:'https://untrusted.invalid'}});assert.equal(origin.status,403);evidence.checks.push({label:'unapproved origin rejected',status:origin.status});
evidence.passed=true;
await mkdir(new URL('../../docs/submission/evidence/',import.meta.url),{recursive:true});
await writeFile(new URL('../../docs/submission/evidence/live-https.json',import.meta.url),JSON.stringify(evidence,null,2)+'\n');
console.log(JSON.stringify({passed:true,checks:evidence.checks.length,items:evidence.health.items,sha256:evidence.health.sha256,captured_at:evidence.captured_at}));
