const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [svg,out,w,h]=process.argv.slice(2);const b=await chromium.launch();
const p=await b.newPage({viewport:{width:+w,height:+h}});
await p.setContent('<html><body style="margin:0">'+fs.readFileSync(svg,'utf8')+'</body></html>');
await p.waitForTimeout(200);await p.screenshot({path:out});await b.close();})();
