import {createHash} from 'node:crypto';
import {mkdirSync,writeFileSync} from 'node:fs';
import {resolve} from 'node:path';

const assetsDir=resolve(process.cwd(),'assets');
mkdirSync(assetsDir,{recursive:true});
const sha256=buf=>createHash('sha256').update(buf).digest('hex');

const assets=[
 {id:'logo',file:'logo.svg',source:'https://www.leforzz.com/',url:'https://leforzzfast.vtexassets.com/assets/vtex.file-manager-graphql/images/b06c8cca-c045-4bce-b458-e79d5b4b2b56___789404fe5348f153a3b0f0ce755fbaf9.svg?width=140&aspect=true'},
 {id:'konnect-1',file:'konnect-1.source',line:'KONNECT',name:'Cadeira Flexora Extensora',source:'https://www.leforzz.com/cadeira-flexora-extensora-digital-konnect-le-forzz-lfk-b16-1510/p',url:'https://leforzzfast.vtexassets.com/assets/vtex.file-manager-graphql/images/37f9afbc-7dd9-4f19-a276-6c46e2d66db3___2feb8be8e1ad069dd19d4e69ce43cc41.png?aspect=true&width=600'},
 {id:'konnect-2',file:'konnect-2.source',line:'KONNECT',name:'Multi Press',source:'https://www.leforzz.com/multi-press-supino-desenvolvimento-digital-le-forzz-lfk-a01-1518/p',url:'https://leforzzfast.vtexassets.com/assets/vtex.file-manager-graphql/images/5458e55b-5bfa-4136-b34f-2b82a6229728___9c139025faf2e47a230090c17cf24729.png?aspect=true&width=600'},
 {id:'konnect-3',file:'konnect-3.source',line:'KONNECT',name:'Desenvolvimento Ombros',source:'https://www.leforzz.com/desenvolvimento-ombros-digital-unilateral-le-forzz-lfk-c32-1514/p',url:'https://leforzzfast.vtexassets.com/assets/vtex.file-manager-graphql/images/4d8c94f6-b607-452b-ad78-04ab9bba5ae9___c933abc513aae07ef619f7c13f382ae7.png?aspect=true&width=600'},
 {id:'strong-1',file:'strong-1.source',line:'STRONG',name:'Iso Row',source:'https://www.leforzz.com/remada-articulada-iso-row-strong-le-forzz-lfs-014-816/p',url:'https://leforzzfast.vtexassets.com/assets/vtex.file-manager-graphql/images/773de62b-b191-4053-81b0-f33927b6343c___dd148b394278040e000b94eb39b87751.png?aspect=true&width=600'},
 {id:'strong-2',file:'strong-2.source',line:'STRONG',name:'Supino Inclinado Iso Lateral',source:'https://www.leforzz.com/supino-inclinado-iso-lateral-strong-le-forzz-lfs-001/p',url:'https://leforzzfast.vtexassets.com/assets/vtex.file-manager-graphql/images/de3f71b3-e620-4641-858b-de13e65ce6e5___51a0f06dd75308d6f9b580ebe4c640c1.png?aspect=true&width=600'},
 {id:'strong-3',file:'strong-3.source',line:'STRONG',name:'Pullover',source:'https://www.leforzz.com/pullover-articulado-strong-le-forzz-lfs-020-817/p',url:'https://leforzzfast.vtexassets.com/assets/vtex.file-manager-graphql/images/e28f1366-199f-468d-ad22-14f28f683c51___f6135eaaab47b269cce9ff46678ccb3f.png?aspect=true&width=600'},
 {id:'zenith-1',file:'zenith-1.source',line:'ZENITH',name:'Leg Curl',source:'https://www.leforzz.com/cadeira-flexora-le-forzz-zenith-lfz-013-leg-curl-541/p',url:'https://leforzzfast.vtexassets.com/assets/vtex.file-manager-graphql/images/a9eed466-b83d-48c2-a318-b8a55fb854c8___7e6daadc7d9a6e224d3565af6aed6343.png?aspect=true&width=600'},
 {id:'zenith-2',file:'zenith-2.source',line:'ZENITH',name:'Lat Pull Down',source:'https://www.leforzz.com/puxada-alta-maquina-le-forzz-zenith-lfz-012-lat-pull-down-542/p',url:'https://leforzzfast.vtexassets.com/assets/vtex.file-manager-graphql/images/c1771dca-1fed-4423-b3f5-d2c6f4abafac___7b5b55c53eca5e854f02149d6bac0e6e.png?aspect=true&width=600'},
 {id:'zenith-3',file:'zenith-3.source',line:'ZENITH',name:'Chest Press',source:'https://www.leforzz.com/supino-reto-maquina-le-forzz-zenith-lfz-001-chestpress-554/p',url:'https://leforzzfast.vtexassets.com/assets/vtex.file-manager-graphql/images/2e5babd2-8429-43f3-aa23-a34584bd858a___4397f369ebb82e266e8fed6da4dbe014.png?aspect=true&width=600'},
 {id:'intensity-1',file:'intensity-1.source',line:'INTENSITY',name:'Vertical Bench',source:'https://www.leforzz.com/banco-de-desenvolvimento-le-forzz-lfi-025b-vertical-bench-286/p',url:'https://leforzzfast.vtexassets.com/assets/vtex.file-manager-graphql/images/aa1ae3c4-95d3-4bd0-b3c5-eb5dc5b741aa___fbce9f0c916a61897cebc50357c7626c.png?aspect=true&width=600'},
 {id:'intensity-2',file:'intensity-2.source',line:'INTENSITY',name:'Functional Trainer',source:'https://www.leforzz.com/crossover-angular-le-forzz-lfi-005a-fuctional-trainer-320/p',url:'https://leforzzfast.vtexassets.com/assets/vtex.file-manager-graphql/images/5b748b45-5077-4a1d-a781-611b52328d67___d51bee4ec5938b0b3952c01de509c7a6.png?aspect=true&width=600'},
 {id:'intensity-3',file:'intensity-3.source',line:'INTENSITY',name:'Smith',source:'https://www.leforzz.com/smith-le-forzz-lfi-020a-v2-smith-293/p',url:'https://leforzzfast.vtexassets.com/assets/vtex.file-manager-graphql/images/449ef9f3-852f-4495-a55c-bfc0a2e80fa0___9376a01910dcbb2a5f0fc0f894313724.png?aspect=true&width=600'}
];

async function download(item){
 const res=await fetch(item.url,{headers:{'user-agent':'Mozilla/5.0 TesseractCreativeLab/1.0'}});
 if(!res.ok) throw new Error(`HTTP ${res.status}: ${item.url}`);
 const body=Buffer.from(await res.arrayBuffer());
 if(body.length<800) throw new Error(`Suspicious asset ${item.id} (${body.length} bytes)`);
 writeFileSync(resolve(assetsDir,item.file),body);
 return {...item,bytes:body.length,sha256:sha256(body),contentType:res.headers.get('content-type')};
}
const captured=[]; for(const item of assets) captured.push(await download(item));
const manifest={capturedAt:new Date().toISOString(),brand:'Le Forzz',officialHomepage:'https://www.leforzz.com/',partnersUsedAsTypographicProof:['Bodytech','Cia Athletica','NitroGym','Fluminense FC'],assets:captured};
writeFileSync(resolve(assetsDir,'capture.json'),JSON.stringify(manifest,null,2));
console.log(JSON.stringify(manifest,null,2));