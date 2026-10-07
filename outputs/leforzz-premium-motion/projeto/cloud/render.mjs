import {chromium} from 'playwright';
import {spawnSync} from 'node:child_process';
import {mkdirSync,rmSync} from 'node:fs';
import {resolve,dirname} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
const here=dirname(fileURLToPath(import.meta.url)),root=resolve(here,'../../../..'),out=resolve(root,'.cloud-render'),frames=resolve(here,'.frames');
const fps=30,width=1080,height=1920,duration=6.4,total=Math.round(duration*fps),quality=process.env.QUALITY||'preview',dsf=2;
rmSync(frames,{recursive:true,force:true});mkdirSync(frames,{recursive:true});mkdirSync(out,{recursive:true});
const browser=await chromium.launch({headless:true});const page=await browser.newPage({viewport:{width,height},deviceScaleFactor:dsf});
await page.goto(pathToFileURL(resolve(here,'index.html')).href,{waitUntil:'load'});
await page.evaluate(async()=>{await Promise.all(Array.from(document.images).map(img=>img.complete?Promise.resolve():new Promise((ok,fail)=>{img.onload=ok;img.onerror=fail})));if(document.fonts?.ready)await document.fonts.ready;});
for(let i=0;i<total;i++){await page.evaluate(t=>window.seek(t),i/fps);await page.screenshot({path:resolve(frames,`frame-${String(i).padStart(5,'0')}.png`),type:'png'});if(i%30===0)console.log(`[render 2x] ${i}/${total}`)}
await browser.close();
const video=resolve(out,'preview.mp4');
const vf='scale=1080:1920:flags=lanczos+accurate_rnd+full_chroma_int,format=yuv420p';
const ff=spawnSync('ffmpeg',['-y','-v','error','-framerate',String(fps),'-i',resolve(frames,'frame-%05d.png'),'-vf',vf,'-c:v','libx264','-preset',quality==='final'?'slow':'medium','-crf',quality==='final'?'12':'14','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-movflags','+faststart','-t',String(duration),video],{stdio:'inherit'});
if(ff.status!==0)process.exit(ff.status||1);console.log(video);