import { listCollections } from '../../lib/catalog.mjs';
export default async req=>{
 if(!['GET','HEAD'].includes(req.method))return new Response('Method not allowed',{status:405});
 return new Response(req.method==='HEAD'?null:JSON.stringify({status:'ok',...listCollections()}),{headers:{'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store','X-Content-Type-Options':'nosniff'}});
};
export const config={path:'/health'};
