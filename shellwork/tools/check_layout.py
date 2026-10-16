"""Playwright check: filter rail/title/controls never overlap the Rolodex (768-1920 wide, 700/900 tall).
Run against a dev server: python shellwork/tools/check_layout.py [base_url]"""
import sys
from playwright.sync_api import sync_playwright
B=sys.argv[1] if len(sys.argv)>1 else "http://127.0.0.1:8030/shellwork/";bad=[]
with sync_playwright() as p:
  b=p.chromium.launch()
  for w in list(range(768,1921,64))+[1024,1280,1440]:
    for h in (700,900):
      pg=b.new_page(viewport={"width":w,"height":h});pg.goto(B);pg.wait_for_timeout(250)
      r=pg.evaluate("""()=>{const R=s=>[...document.querySelectorAll(s)].map(e=>e.getBoundingClientRect());
       const L=[...R('.filters'),...R('.ctl'),...R('.hero__brand')],D=[...R('.base'),...R('.knob'),...R('.rc')].filter(r=>r.width>0);
       const hit=(a,b)=>a.left<b.right-1&&b.left<a.right-1&&a.top<b.bottom-1&&b.top<a.bottom-1;
       const rcs=R('.rc').filter((r,i)=>getComputedStyle(document.querySelectorAll('.rc')[i]).opacity!=='0');
       return {o:L.some(a=>[...R('.base'),...R('.knob'),...rcs].some(d=>hit(a,d))),sx:document.documentElement.scrollWidth>innerWidth}}""")
      if r['o'] or r['sx']:bad.append((w,h,r))
      pg.close()
  b.close()
print("problems:",bad)
