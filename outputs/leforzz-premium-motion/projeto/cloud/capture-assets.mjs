import {chromium} from 'playwright';
import {createHash} from 'node:crypto';
import {mkdirSync, readFileSync, writeFileSync} from 'node:fs';
import {resolve} from 'node:path';

const assetsDir=resolve(process.cwd(),'assets');
mkdirSync(assetsDir,{recursive:true});

const products=[
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
  if(body.length<2000) throw new Error(`asset ${item.id}: suspiciously small (${body.length} bytes)`);
  writeFileSync(resolve(assetsDir,item.file),body);
  return {...item,bytes:body.length,sha256:sha256(body),contentType:res.headers.get('content-type')};
}

async function captureLogo(){
  const browser=await chromium.launch({headless:true});
  try{
    const page=await browser.newPage({viewport:{width:1440,height:1000},deviceScaleFactor:2});
    await page.goto('https://www.leforzz.com/',{waitUntil:'domcontentloaded',timeout:90000});
    await page.waitForTimeout(2500);

    const candidates=await page.locator('header img, header svg, nav img, nav svg, a img, a svg').evaluateAll(nodes=>nodes.map((el,i)=>{
      const r=el.getBoundingClientRect();
      const text=[el.getAttribute('alt'),el.getAttribute('class'),el.getAttribute('src'),el.getAttribute('aria-label')].filter(Boolean).join(' ').toLowerCase();
      const ratio=r.height?r.width/r.height:0;
      let score=0;
      if(/logo|le\s*forzz|leforzz/.test(text)) score+=10;
      if(r.width>=90&&r.height>=18&&ratio>=2&&ratio<=12) score+=4;
      if(el.closest('header,nav')) score+=3;
      if(r.top<300) score+=1;
      return {i,tag:el.tagName.toLowerCase(),text,width:r.width,height:r.height,ratio,score,src:el.getAttribute('src')||'',outer:el.tagName.toLowerCase()==='svg'?el.outerHTML:''};
    }));
    const viable=candidates.filter(c=>c.width>40&&c.height>12).sort((a,b)=>b.score-a.score);
    if(!viable.length) throw new Error('official logo element not found on homepage');
    const winner=viable[0];

    const isolated=await browser.newPage({viewport:{width:1000,height:300},deviceScaleFactor:2});
    let markup='';
    if(winner.tag==='img'&&winner.src){
      const src=new URL(winner.src,page.url()).href;
      markup=`<img id="mark" src="${src}" style="display:block;max-width:860px;max-height:220px">`;
    }else if(winner.outer){
      markup=winner.outer.replace('<svg','<svg id="mark"');
    }else{
      throw new Error('logo candidate has no reusable source');
    }
    await isolated.setContent(`<html><head><style>html,body{margin:0;padding:20px;background:transparent}#mark{display:block}</style></head><body>${markup}</body></html>`,{waitUntil:'load'});
    await isolated.locator('#mark').waitFor({state:'visible',timeout:30000});
    const logoPath=resolve(assetsDir,'logo.png');
    await isolated.locator('#mark').screenshot({path:logoPath,omitBackground:true});
    const buf=readFileSync(logoPath);
    return {id:'logo',file:'logo.png',source:'https://www.leforzz.com/',discovery:winner,bytes:buf.length,sha256:sha256(buf)};
  } finally {
    await browser.close();
  }
}

const captured=[];
for(const item of products) captured.push(await download(item));
captured.push(await captureLogo());
const manifest={
  capturedAt:new Date().toISOString(),
  brand:'Le Forzz',
  officialHomepage:'https://www.leforzz.com/',
  instagram:'https://www.instagram.com/leforzzofficial/',
  assets:captured
};
writeFileSync(resolve(assetsDir,'capture.json'),JSON.stringify(manifest,null,2));
console.log(JSON.stringify(manifest,null,2));
