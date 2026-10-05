import {chromium} from 'playwright';
import {spawnSync} from 'node:child_process';
import {mkdirSync, rmSync, writeFileSync} from 'node:fs';
import {resolve, dirname} from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';

const here=dirname(fileURLToPath(import.meta.url));
const root=resolve(here,'../../../..');
const out=resolve(root,'.cloud-render');
const frames=resolve(here,'.frames');
const quality=process.env.QUALITY || 'preview';
const isFinal=quality==='final';
// Visual QA must happen at delivery geometry/frame rate. Preview may render
// faster elsewhere, but it must not hide raster, timing or color defects.
const fps=60;
const width=1080;
const height=1920;
const scale=1;
const duration=18.0;
const totalFrames=Math.round(duration*fps);

rmSync(frames,{recursive:true,force:true});
mkdirSync(frames,{recursive:true});
mkdirSync(out,{recursive:true});

function wav(path){
  const sr=48000,n=Math.floor(duration*sr);
  const data=new Float32Array(n);
  let seed=20260928;
  const rnd=()=>{seed=(1664525*seed+1013904223)>>>0;return seed/4294967296*2-1};
  const add=(start,dur,fn,gain=1)=>{
    const a=Math.max(0,Math.floor(start*sr)),b=Math.min(n,Math.floor((start+dur)*sr));
    for(let i=a;i<b;i++) data[i]+=fn((i-a)/sr,(i-a)/(b-a))*gain;
  };
  const chords=[[130.81,164.81,196],[116.54,146.83,174.61],[130.81,155.56,196],[146.83,174.61,220]];
  for(let bar=0;bar<8;bar++){
    const start=bar*2;
    const chord=chords[bar%chords.length];
    add(start,2.05,(t,p)=>{
      const env=Math.min(1,t/.28)*Math.min(1,(2.05-t)/.35);
      return chord.reduce((s,f)=>s+Math.sin(2*Math.PI*f*t),0)/chord.length*env;
    },.075);
  }
  for(let beat=0;beat<Math.ceil(duration/.5);beat++){
    add(beat*.5,.18,(t)=>Math.sin(2*Math.PI*(58+42*Math.exp(-25*t))*t)*Math.exp(-20*t),beat<7?.07:.12);
  }
  [0.65,0.83,1.01,1.19,1.37,1.55,1.73,1.91,2.09,2.27].forEach(t=>
    add(t,.028,x=>(Math.sin(2*Math.PI*1150*x)+.25*Math.sin(2*Math.PI*1720*x))*Math.exp(-145*x),.03)
  );
  [3.58,10.78].forEach(t=>add(t-.22,.46,(x,p)=>rnd()*Math.sin(Math.PI*p)*Math.sin(Math.PI*p),.035));
  [3.08].forEach(t=>add(t,.07,x=>Math.sin(2*Math.PI*540*x)*Math.exp(-55*x),.08));
  let peak=1e-6;for(const v of data) peak=Math.max(peak,Math.abs(v));
  const gain=.82/peak;
  const bytes=Buffer.alloc(44+n*2);
  bytes.write('RIFF',0);bytes.writeUInt32LE(36+n*2,4);bytes.write('WAVE',8);bytes.write('fmt ',12);
  bytes.writeUInt32LE(16,16);bytes.writeUInt16LE(1,20);bytes.writeUInt16LE(1,22);bytes.writeUInt32LE(sr,24);
  bytes.writeUInt32LE(sr*2,28);bytes.writeUInt16LE(2,32);bytes.writeUInt16LE(16,34);bytes.write('data',36);bytes.writeUInt32LE(n*2,40);
  for(let i=0;i<n;i++) bytes.writeInt16LE(Math.round(Math.max(-1,Math.min(1,data[i]*gain))*32767),44+i*2);
  writeFileSync(path,bytes);
}

const audio=resolve(here,'score.wav');
wav(audio);

const browser=await chromium.launch({headless:true});
const page=await browser.newPage({viewport:{width,height},deviceScaleFactor:1});
await page.goto(pathToFileURL(resolve(here,'index.html')).href,{waitUntil:'load'});
await page.evaluate(async(s)=>{
  document.getElementById('stage').style.transform='scale('+s+')';
  await Promise.all(Array.from(document.images).map(img=>img.complete?Promise.resolve():new Promise(r=>{img.onload=r;img.onerror=r})));
  if (document.fonts && document.fonts.ready) await document.fonts.ready;
},scale);

for(let i=0;i<totalFrames;i++){
  const t=i/fps;
  await page.evaluate(v=>window.seek(v),t);
  const name='frame-'+String(i).padStart(5,'0')+'.png';
  await page.screenshot({path:resolve(frames,name),type:'png'});
  if(i%60===0) console.log('[render] frame '+i+'/'+totalFrames);
}
await browser.close();

const video=resolve(out,'preview.mp4');
const args=[
  '-y','-v','error','-framerate',String(fps),'-i',resolve(frames,'frame-%05d.png'),
  '-i',audio,'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset',isFinal?'medium':'veryfast',
  '-crf',isFinal?'14':'16','-tune','animation','-pix_fmt','yuv420p',
  '-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-color_range','tv',
  '-c:a','aac','-b:a','192k','-ar','48000','-ac','2',
  '-af','loudnorm=I=-14:TP=-1.5:LRA=7','-t',String(duration),'-movflags','+faststart',video
];
const ff=spawnSync('ffmpeg',args,{stdio:'inherit'});
if(ff.status!==0) process.exit(ff.status||1);
console.log('[render] '+video);
