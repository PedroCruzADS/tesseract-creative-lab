import {createHash} from 'node:crypto';
import {mkdirSync, writeFileSync} from 'node:fs';
import {resolve} from 'node:path';

const assetsDir=resolve(process.cwd(),'assets');
mkdirSync(assetsDir,{recursive:true});

const assets=[
  {
    id:'logo',
    file:'logo.svg',
    source:'https://www.leforzz.com/',
    url:'https://leforzzfast.vtexassets.com/assets/vtex.file-manager-graphql/images/b06c8cca-c045-4bce-b458-e79d5b4b2b56___789404fe5348f153a3b0f0ce755fbaf9.svg?width=140&aspect=true'
  },
  {
    id:'runverse',
    file:'runverse.jpg',
    source:'https://www.leforzz.com/esteira-ergometrica-le-forzz-runverse-touch-screen-330/p',
    url:'https://leforzzfast.vtexassets.com/assets/vtex.file-manager-graphql/images/8d8d63a0-5096-4d00-a37c-ce33fdce01f5___55a44aad14400296204070a4c4db0a6f.jpg?aspect=true&width=600'
  },
  {
    id:'runverse-hero',
    file:'runverse-hero.webp',
    source:'https://www.leforzz.com/esteira-ergometrica-le-forzz-runverse-touch-screen-330/p',
    url:'https://leforzzfast.vtexassets.com/arquivos/ids/158995-1920-auto/topo-desktop2.webp?v=639184414216430000'
  },
  {
    id:'konnect-leg-press',
    file:'konnect-leg-press.png',
    source:'https://www.leforzz.com/leg-press-digital-touchscreen-10-1-konnect-le-forzz-lfk-b12/p',
    url:'https://leforzzfast.vtexassets.com/assets/vtex.file-manager-graphql/images/bfe572b2-4e1a-444d-aca7-67f67bbbf08c___b2bdc0c431ad2b8b964bc86751a9a2e7.png?aspect=true&width=600'
  },
  {
    id:'konnect-chest-press',
    file:'konnect-chest-press.png',
    source:'https://www.leforzz.com/supino-vertical-digital-unilateral-konnect-le-forzz-lfk-c33/p',
    url:'https://leforzzfast.vtexassets.com/assets/vtex.file-manager-graphql/images/d8fe75df-6051-423e-b8bc-3e1a2d75f37a___37e159483c48cee1308128cbeca82c05.png?aspect=true&width=600'
  }
];

function sha256(buf){return createHash('sha256').update(buf).digest('hex')}

async function download(item){
  const res=await fetch(item.url,{headers:{'user-agent':'Mozilla/5.0 TesseractCreativeLab/1.0'}});
  if(!res.ok) throw new Error(`asset ${item.id}: HTTP ${res.status}`);
  const body=Buffer.from(await res.arrayBuffer());
  if(body.length<800) throw new Error(`asset ${item.id}: suspiciously small (${body.length} bytes)`);
  writeFileSync(resolve(assetsDir,item.file),body);
  return {...item,bytes:body.length,sha256:sha256(body),contentType:res.headers.get('content-type')};
}

const captured=[];
for(const item of assets) captured.push(await download(item));
const manifest={
  capturedAt:new Date().toISOString(),
  brand:'Le Forzz',
  officialHomepage:'https://www.leforzz.com/',
  instagram:'https://www.instagram.com/leforzzofficial/',
  assets:captured
};
writeFileSync(resolve(assetsDir,'capture.json'),JSON.stringify(manifest,null,2));
console.log(JSON.stringify(manifest,null,2));
