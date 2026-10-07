import {createHash} from 'node:crypto';
import {mkdirSync,writeFileSync} from 'node:fs';
import {resolve} from 'node:path';
import {chromium} from 'playwright';

const assetsDir=resolve(process.cwd(),'assets');
mkdirSync(assetsDir,{recursive:true});
const sha256=buf=>createHash('sha256').update(buf).digest('hex');

const fixed=[
 {id:'logo',file:'logo.svg',source:'https://www.leforzz.com/',url:'https://leforzzfast.vtexassets.com/assets/vtex.file-manager-graphql/images/b06c8cca-c045-4bce-b458-e79d5b4b2b56___789404fe5348f153a3b0f0ce755fbaf9.svg?width=140&aspect=true'}
];

const products=[
 {id:'konnect-1',line:'KONNECT',name:'Cadeira Flexora Extensora',page:'https://www.leforzz.com/cadeira-flexora-extensora-digital-konnect-le-forzz-lfk-b16-1510/p'},
 {id:'konnect-2',line:'KONNECT',name:'Multi Press',page:'https://www.leforzz.com/multi-press-supino-desenvolvimento-digital-le-forzz-lfk-a01-1518/p'},
 {id:'konnect-3',line:'KONNECT',name:'Desenvolvimento Ombros',page:'https://www.leforzz.com/desenvolvimento-ombros-digital-unilateral-le-forzz-lfk-c32-1514/p'},
 {id:'strong-1',line:'STRONG',name:'Iso Row',page:'https://www.leforzz.com/remada-articulada-iso-row-strong-le-forzz-lfs-014-816/p'},
 {id:'strong-2',line:'STRONG',name:'Supino Reto Deitado',page:'https://www.leforzz.com/supino-reto-deitado-articulado-strong-le-forzz-lfs-018-814/p'},
 {id:'strong-3',line:'STRONG',name:'Pullover',page:'https://www.leforzz.com/pullover-articulado-strong-le-forzz-lfs-020-817/p'},
 {id:'zenith-1',line:'ZENITH',name:'Leg Curl',page:'https://www.leforzz.com/cadeira-flexora-le-forzz-zenith-lfz-013-leg-curl-541/p'},
 {id:'zenith-2',line:'ZENITH',name:'Lat Pull Down',page:'https://www.leforzz.com/puxada-alta-maquina-le-forzz-zenith-lfz-012-lat-pull-down-542/p'},
 {id:'zenith-3',line:'ZENITH',name:'Chest Press',page:'https://www.leforzz.com/supino-reto-maquina-le-forzz-zenith-lfz-001-chestpress-554/p'},
 {id:'intensity-1',line:'INTENSITY',name:'Vertical Bench',page:'https://www.leforzz.com/banco-de-desenvolvimento-le-forzz-lfi-025b-vertical-bench-286/p'},
 {id:'intensity-2',line:'INTENSITY',name:'Functional Trainer',page:'https://www.leforzz.com/crossover-angular-le-forzz-lfi-005a-fuctional-trainer-320/p'},
 {id:'intensity-3',line:'INTENSITY',name:'Smith',page:'https://www.leforzz.com/smith-le-forzz-lfi-020a-v2-smith-293/p'}
];

async function download(url,file,extra={}){
 const res=await fetch(url,{headers:{'user-agent':'Mozilla/5.0 TesseractCreativeLab/1.0'}});
 if(!res.ok) throw new Error(`HTTP ${res.status}: ${url}`);
 const body=Buffer.from(await res.arrayBuffer());
 if(body.length<800) throw new Error(`Suspicious asset ${url} (${body.length} bytes)`);
 writeFileSync(resolve(assetsDir,file),body);
 return {...extra,url,file,bytes:body.length,sha256:sha256(body),contentType:res.headers.get('content-type')};
}

const captured=[];
for(const item of fixed) captured.push(await download(item.url,item.file,item));

const browser=await chromium.launch({headless:true});
const page=await browser.newPage({viewport:{width:1440,height:1200}});
for(const item of products){
 await page.goto(item.page,{waitUntil:'domcontentloaded',timeout:45000});
 await page.waitForTimeout(1000);
 const src=await page.evaluate(()=>{
   const imgs=[...document.images];
   const byAlt=imgs.find(i=>(i.alt||'').toLowerCase().includes('imagem do produto'));
   const candidates=[byAlt,...imgs].filter(Boolean);
   const pick=candidates.find(i=>{
     const s=i.currentSrc||i.src||'';
     return /vtexassets\.com/.test(s) && !/icon|icone|logo/i.test(s);
   });
   return pick ? (pick.currentSrc||pick.src) : null;
 });
 if(!src) throw new Error(`No product image found: ${item.id} ${item.page}`);
 captured.push(await download(src,`${item.id}.source`,{...item,source:item.page}));
}
await browser.close();

const manifest={
 capturedAt:new Date().toISOString(),
 brand:'Le Forzz',
 officialHomepage:'https://www.leforzz.com/',
 partnersUsedAsTypographicProof:['Bodytech','Cia Athletica','NitroGym','Fluminense FC'],
 products:captured
};
writeFileSync(resolve(assetsDir,'capture.json'),JSON.stringify(manifest,null,2));
console.log(JSON.stringify(manifest,null,2));