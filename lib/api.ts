export async function api<T=any>(path:string,init?:RequestInit):Promise<T>{
  const r=await fetch(path,{credentials:'include',...init,headers:{'Content-Type':'application/json',...(init?.headers||{})}})
  const d=await r.json().catch(()=>({}))
  if(!r.ok)throw new Error(d.detail||d.error||'Request gagal')
  return d
}
export const pct=(x:number)=>Math.round((x||0)*100)+'%'
export const sec=(ms:number)=>ms?Math.round(ms/1000)+'s':'—'
