import { build } from 'esbuild';
await build({entryPoints:['netlify/functions/mcp.mjs','netlify/functions/health.mjs'],outdir:'dist/functions',bundle:true,platform:'node',target:'node22',format:'esm',outExtension:{'.js':'.mjs'},logLevel:'info'});
