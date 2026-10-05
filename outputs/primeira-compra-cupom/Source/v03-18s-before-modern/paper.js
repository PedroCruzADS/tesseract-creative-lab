/* A single paper texture on a continuous, articulated cylindrical surface. */
window.makePaper=async function(page){
  await Promise.all([document.fonts.load('700 100px Bai'),document.fonts.load('600 54px Bai')]);
  const logo=document.querySelector('#pl'); await logo.decode();
  const c=document.createElement('canvas'); c.width=1080;c.height=1920;
  const ctx=c.getContext('2d'),g=ctx.createLinearGradient(0,0,1080,0);
  g.addColorStop(0,'#fbf8f3');g.addColorStop(1,'#f3ecdf');ctx.fillStyle=g;ctx.fillRect(0,0,1080,1920);
  for(let i=0;i<22000;i++){const x=((i*73856093)>>>0)%1080,y=((i*19349663)>>>0)%1920;ctx.fillStyle=i%2?'rgba(98,72,35,.023)':'rgba(255,255,255,.12)';ctx.fillRect(x,y,1,1)}
  ctx.drawImage(logo,72,330,290,290*logo.naturalHeight/logo.naturalWidth);
  ctx.fillStyle='#E50914';ctx.fillRect(72,488,70,8);
  ctx.textBaseline='top';ctx.fillStyle='#14110f';ctx.font='700 96px Bai';
  ctx.fillText('Ainda não comprou',72,530);ctx.fillText('com a gente?',72,633);
  ctx.fillStyle='#6b6262';ctx.font='600 54px Bai';ctx.fillText('Ganhe',72,832);
  ctx.fillStyle='#E50914';ctx.font='700 244px Bai';ctx.fillText('5% OFF',62,904);
  ctx.fillStyle='#14110f';ctx.font='700 64px Bai';ctx.fillText('na sua primeira compra.',72,1200);
  const url=c.toDataURL('image/png');
  page.querySelector('#front').style.opacity='0';page.querySelector('#back').style.opacity='0';
  const strips=[];
  for(let i=0;i<18;i++){
    const s=document.createElement('div');s.className='paper-strip';
    const f=document.createElement('div');f.className='strip-front';f.style.backgroundImage='url('+url+')';f.style.backgroundPosition=(-i*60)+'px 0';
    const light=document.createElement('div');light.className='strip-light';f.append(light);
    const b=document.createElement('div');b.className='strip-back';s.append(f,b);page.append(s);strips.push({s,light});
  }
  return strips;
};
window.posePaper=function(strips,angle){
  let x=0,z=0;
  const bend=14+26*Math.sin(angle*Math.PI/180);
  strips.forEach(({s,light},i)=>{
    const theta=angle+bend*Math.pow((i+.5)/18,3),r=theta*Math.PI/180;
    s.style.transform='translate3d('+x+'px,0,'+z+'px) rotateY('+(-theta)+'deg)';
    light.style.opacity=Math.min(.26,.015+Math.abs(Math.sin(r))*.20);
    x+=60*Math.cos(r);z+=60*Math.sin(r);
  });
};
