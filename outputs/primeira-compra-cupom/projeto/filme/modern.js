/* Luz e profundidade das superficies (v04). Mesma ideia do light-sweep-pass, restrita aos cards. */
window.polishModern=function(tl){
  const root=document.querySelector('#root');
  const ambient=document.createElement('div');ambient.id='ambient-modern';ambient.dataset.layoutIgnore='true';root.prepend(ambient);
  const orbits=[];
  for(let i=0;i<2;i++){const el=document.createElement('div');el.className='modern-orbit'+(i?' small':'');el.dataset.layoutIgnore='true';root.insertBefore(el,document.querySelector('#s1logo'));orbits.push(el)}
  tl.to(ambient,{x:-38,y:35,duration:18,ease:'sine.inOut'},0);
  tl.to(orbits[0],{x:85,y:-80,scale:1.07,duration:18,ease:'sine.inOut'},0);
  tl.to(orbits[1],{x:-40,y:80,scale:.94,duration:18,ease:'sine.inOut'},0);

  /* cena 1: brilho passando no ticket e no painel do codigo */
  const tk=document.querySelector('#tk');
  const shine=document.createElement('div');shine.className='tk-shine';shine.dataset.layoutIgnore='true';tk.append(shine);
  tl.fromTo(shine,{x:0},{x:1500,duration:1.2,ease:'sine.inOut'},.5);
  const code=document.querySelector('#tkcode');
  const cs=document.createElement('div');cs.className='chip-shine';cs.dataset.layoutIgnore='true';code.append(cs);
  tl.fromTo(cs,{x:0},{x:1000,duration:.9,ease:'sine.inOut'},1.1);

  /* cena 2: brilho entra em cada card quando ele chega ao centro */
  const at=[3.4,5.2,6.8,8.4,10.0];
  document.querySelectorAll('.cc').forEach((card,i)=>{
    card.dataset.layoutAllowOverflow='true';
    card.querySelectorAll('.cat,.nm,.chips span').forEach(e=>e.dataset.layoutAllowOverflow='true');
    if(i<4){const sweep=document.createElement('div');sweep.className='card-sweep';sweep.dataset.layoutIgnore='true';card.append(sweep);
    tl.fromTo(sweep,{x:0},{x:1350,duration:1.15,ease:'sine.inOut'},at[i]);}
    const img=card.querySelector('.img');
    if(img) tl.fromTo(img,{y:8},{y:-6,duration:1.2,ease:'sine.inOut'},at[i]);
  });
  tl.fromTo('.more-grid span',{y:22,opacity:.5},{y:0,opacity:1,duration:.45,stagger:.07,ease:'power2.out'},10.1);

  /* cena 3 */
  const cart=document.querySelector('#cart');
  const sw=document.createElement('div');sw.className='card-sweep';sw.dataset.layoutIgnore='true';cart.append(sw);
  tl.fromTo(sw,{x:0},{x:1400,duration:.85,ease:'sine.inOut'},11.9);
  tl.fromTo('#ok i',{scale:.6,rotation:-20},{scale:1,rotation:0,duration:.35,ease:'power2.out'},14.12);

  /* cena 4 */
  const disc=document.createElement('div');disc.className='end-disc';disc.dataset.layoutIgnore='true';root.insertBefore(disc,document.querySelector('#cl'));
  tl.fromTo(disc,{opacity:0,scale:.84},{opacity:1,scale:1,duration:.7,ease:'sine.out'},15.55);
  tl.to(disc,{scale:1.05,y:-12,duration:1.8,ease:'sine.inOut'},16.2);
};
