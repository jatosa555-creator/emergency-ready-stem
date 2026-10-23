import items from '../data/catalog.json' with {type:'json'};
import { createHash } from 'node:crypto';

export const VERSION='0.4.0';
export const SNAPSHOT='2026-10-23';
export const digest=createHash('sha256').update(JSON.stringify(items)).digest('hex');
const allowedTopics=new Set(['continuity','access','lesson','inclusion','wellbeing','recovery','quality','reflection','sources','usage']);
const ids=new Set();
for(const x of items){
  if(ids.has(x.id)||!/^ER-\d{2}$/.test(x.id)||!allowedTopics.has(x.topic)||!['original-guidance','synthetic-example'].includes(x.source_type)||x.version!==VERSION||x.snapshot_date!==SNAPSHOT||!x.url.startsWith('https://github.com/jatosa555-creator/emergency-ready-stem/blob/main/knowledge/')) throw Error('Invalid publication catalog');
  ids.add(x.id);
}
export function listCollections(){return {service:'emergency-ready-stem-knowledge',version:VERSION,snapshot_date:SNAPSHOT,sha256:digest,items:items.length,topics:[...allowedTopics],source_types:['original-guidance','synthetic-example'],scope:'Original project guidance and invented teaching examples. Not current official policy, live Drive, or third-party checklist text. No private data or write access.'};}
export function searchReferences({query,topic,limit=3}){
  const terms=query.toLocaleLowerCase().trim().split(/\s+/u).filter(Boolean);
  const results=items.filter(x=>!topic||x.topic===topic).map(x=>({x,score:terms.reduce((n,t)=>n+(`${x.id} ${x.title} ${x.keywords} ${x.text}`.toLocaleLowerCase().includes(t)?1:0),0)})).filter(x=>x.score>0).sort((a,b)=>b.score-a.score||a.x.id.localeCompare(b.x.id)).slice(0,limit).map(({x})=>({id:x.id,title:x.title,topic:x.topic,source_type:x.source_type,snapshot_date:x.snapshot_date,excerpt:x.text.slice(0,150),url:x.url}));
  return {results,count:results.length,scope:'Read selected exact IDs with get_reference before quoting. No matches means only that this bounded library had no match.'};
}
export function getReference(id){const x=items.find(x=>x.id===id);return x?{found:true,...x,citation:`[${x.id}: ${x.title}](${x.url}) (project ${x.source_type}; snapshot ${SNAPSHOT}; v${VERSION})`}:{found:false,id,message:'No such item in this bounded public snapshot.'};}
