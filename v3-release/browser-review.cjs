const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
(async()=>{
 const browser=await chromium.launch({headless:true});
 const out='browser-review'; fs.mkdirSync(out,{recursive:true});
 const issues=[],checks=[]; const origin='http://127.0.0.1:8765';
 const routes=['','migration/decree-702/','services/','for-business/','consultations/','contacts/','about/','knowledge/','knowledge/articles/rvp-shared-values-702/'];
 const sizes=[{width:390,height:844},{width:768,height:1024},{width:1440,height:900}];
 for(const lang of ['ru','en','fr']) for(const size of sizes){
  const page=await browser.newPage({viewport:size,deviceScaleFactor:1});
  const failures=[];page.on('pageerror',e=>failures.push('JS: '+e.message));
  page.on('response',r=>{if(r.url().startsWith(origin)&&r.status()>=400)failures.push('HTTP '+r.status()+' '+r.url());});
  page.on('requestfailed',r=>{if(r.url().startsWith(origin)&&r.failure()?.errorText!=='net::ERR_ABORTED')failures.push('Request: '+r.url());});
  for(const route of routes){
   failures.length=0;
   const label=lang+'/'+route+' @ '+size.width;
   try{
    const response=await page.goto(origin+'/'+lang+'/'+route,{waitUntil:'load',timeout:20000});
    await page.evaluate(()=>document.fonts.ready);
    const metrics=await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,h1:document.querySelector('h1')?.innerText,brokenImages:[...document.images].filter(i=>i.complete&&!i.naturalWidth).map(i=>i.src)}));
    if(!response?.ok()) issues.push({label,error:'HTTP navigation '+response?.status()});
    if(!metrics.h1) issues.push({label,error:'Missing visible H1'});
    if(metrics.scrollWidth>metrics.width+2) issues.push({label,error:'Horizontal overflow '+(metrics.scrollWidth-metrics.width)+'px'});
    for(const src of metrics.brokenImages) issues.push({label,error:'Broken image '+src});
    if(route===''&&size.width===390){
     const burger=page.locator('#burger');
     if(await burger.isVisible()){
      await burger.click();
      if(await burger.getAttribute('aria-expanded')!=='true'||!await page.locator('#navLinks').isVisible())issues.push({label,error:'Menu did not open'});
      await burger.click();
      if(await burger.getAttribute('aria-expanded')!=='false')issues.push({label,error:'Menu did not close'});
     } else issues.push({label,error:'Mobile burger not visible'});
    }
    if(route==='consultations/'){
     const groups=page.locator('details.sr-contact-details');
     if(await groups.count()!==6)issues.push({label,error:'Consultation category count != 6'});
     for(let i=0;i<await groups.count();i++){
      const g=groups.nth(i); const summary=g.locator('summary');
      if(!await g.evaluate(e=>e.open))await summary.click();
      if(!await g.evaluate(e=>e.open))issues.push({label,error:'Consultation accordion did not open'});
      for(const prefix of ['https://wa.me/','https://t.me/','mailto:'])if(!await g.locator('a[href^="'+prefix+'"]').count())issues.push({label,error:'Missing contact link '+prefix+' in category '+(i+1)});
      if(await g.evaluate(e=>e.open))await summary.click();
     }
    }
    if((route===''||route==='for-business/')&&(size.width===390||size.width===1440)){
     await page.screenshot({path:path.join(out,lang+'-'+(route?'b2b':'home')+'-'+size.width+'.png'),fullPage:true,animations:'disabled'});
    }
    if(route==='migration/decree-702/'){
     const target=lang==='ru'?'en':'ru';
     const switcher=page.locator('a[hreflang="'+target+'"]').first();
     const href=await switcher.getAttribute('href');
     const expected='/'+target+'/'+route;
     if(new URL(href,page.url()).pathname!==expected)issues.push({label,error:'Language switch wrong destination'});
    }
    failures.forEach(error=>issues.push({label,error}));
    checks.push({label,metrics});
   }catch(e){issues.push({label,error:String(e)});}
  }
  await page.close();
 }
 await browser.close();
 fs.writeFileSync(path.join(out,'report.json'),JSON.stringify({checks,issues},null,2));
 console.log('BROWSER_REVIEW '+JSON.stringify({pages:checks.length,issues}));
 if(issues.length)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1;});
