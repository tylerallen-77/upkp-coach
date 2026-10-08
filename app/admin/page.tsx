'use client'
import {useEffect,useState} from 'react'
import {api} from '../../lib/api'

type Tab='overview'|'users'|'learning'|'quality'|'audit'

export default function Admin(){
 const [me,setMe]=useState<any>(null),[users,setUsers]=useState<any[]>([]),[reports,setReports]=useState<any[]>([]),[cal,setCal]=useState<any[]>([]),[audit,setAudit]=useState<any[]>([]),[counts,setCounts]=useState<any>({}),[detail,setDetail]=useState<any>(null),[tab,setTab]=useState<Tab>('overview'),[err,setErr]=useState('')
 async function load(){
  try{
   const m=await api('/api/auth/me');setMe(m.user);if(m.user.role!=='admin')throw new Error('Admin only')
   const [u,r,c,o,a]=await Promise.all([api('/api/admin/users'),api('/api/admin/reports'),api('/api/admin/calibration'),api('/api/admin/data/overview'),api('/api/admin/audit')])
   setUsers(u.users);setReports(r.reports);setCal(c.items);setCounts(o.counts||{});setAudit(a.items||[])
  }catch(e:any){setErr(e.message)}
 }
 useEffect(()=>{load()},[])
 async function toggle(u:any){await api(`/api/admin/users/${u.id}/disable?disabled=${!u.disabled}`,{method:'POST'});await load()}
 async function resetPassword(u:any){const p=prompt(`Password baru untuk @${u.username} (min. 8 karakter)`);if(!p)return;await api(`/api/admin/users/${u.id}/reset-password`,{method:'POST',body:JSON.stringify({password:p})});alert('Password direset dan semua sesi login user tersebut dicabut.');await load()}
 async function resetLearning(u:any){if(!confirm(`Reset seluruh riwayat pembelajaran @${u.username}? Akun tetap ada.`))return;await api(`/api/admin/users/${u.id}/reset-learning`,{method:'POST'});alert('Riwayat pembelajaran direset.');setDetail(null);await load()}
 async function inspect(u:any){const d=await api(`/api/admin/data/users/${u.id}`);setDetail(d);setTab('learning')}
 async function quarantine(sig:string,active:boolean){await api(`/api/admin/quarantine/${sig}?active=${active}`,{method:'POST'});await load()}
 async function cleanup(){const d=await api('/api/admin/maintenance',{method:'POST'});alert(JSON.stringify(d.cleanup));await load()}
 const highSignal=cal.filter((x:any)=>x.attempts>=5).sort((a:any,b:any)=>Math.abs(b.empirical_level-b.authored_level)-Math.abs(a.empirical_level-a.authored_level)).slice(0,40)
 const tabs:[Tab,string][]=[['overview','Overview'],['users','Users'],['learning','Learning Data'],['quality','Question Quality'],['audit','Audit Log']]
 return <main style={{maxWidth:1180,margin:'30px auto',padding:18,fontFamily:'system-ui',color:'#172033'}}>
  <a href="/">← Kembali ke UPKP Coach</a>
  <div style={{display:'flex',justifyContent:'space-between',gap:16,alignItems:'center',flexWrap:'wrap'}}><div><h1 style={{marginBottom:4}}>Admin Console</h1><p style={{marginTop:0,color:'#71809b'}}>Safe database console · tidak mengekspos credential, password hash, atau raw SQL.</p></div><button onClick={cleanup}>Cleanup expired data</button></div>
  <div style={{display:'flex',gap:8,flexWrap:'wrap',margin:'18px 0'}}>{tabs.map(([id,label])=><button key={id} onClick={()=>setTab(id)} style={{padding:'9px 12px',borderRadius:10,border:'1px solid #dfe5ee',background:tab===id?'#0f1f3d':'white',color:tab===id?'white':'#172033'}}>{label}</button>)}</div>
  {err?<p style={{color:'#c94455'}}>{err}</p>:<>
   {tab==='overview'&&<><div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit,minmax(150px,1fr))',gap:10}}>{Object.entries(counts).map(([k,v])=><div key={k} style={card}><small style={{color:'#71809b'}}>{k}</small><b style={{fontSize:28,display:'block'}}>{String(v)}</b></div>)}</div><div style={{...card,marginTop:14}}><h3>Production data access</h3><p style={{color:'#71809b'}}>Gunakan tab Users, Learning Data, Question Quality, dan Audit Log untuk inspect/edit data dengan guardrails. Untuk perubahan schema tetap gunakan migration SQL yang versioned.</p></div></>}
   {tab==='users'&&<div style={{display:'grid',gap:10}}>{users.map(u=><div key={u.id} style={{...card,display:'flex',justifyContent:'space-between',alignItems:'center',gap:12,flexWrap:'wrap'}}><div><b>@{u.username}</b><div style={{fontSize:12,color:'#71809b'}}>{u.role} · {u.attempts} attempts · {u.disabled?'DISABLED':'active'}</div></div><div style={{display:'flex',gap:7,flexWrap:'wrap'}}><button onClick={()=>inspect(u)}>Inspect</button><button onClick={()=>resetPassword(u)}>Reset password</button><button onClick={()=>resetLearning(u)}>Reset learning</button>{u.id!==me?.id&&<button onClick={()=>toggle(u)}>{u.disabled?'Enable':'Disable'}</button>}</div></div>)}</div>}
   {tab==='learning'&&<>{!detail?<div style={card}><h3>Pilih user</h3><p style={{color:'#71809b'}}>Buka tab Users lalu klik Inspect untuk melihat sessions dan attempts.</p></div>:<><div style={card}><h2>@{detail.user.username}</h2><p style={{color:'#71809b'}}>{detail.sessions.length} recent sessions · {detail.attempts.length} recent attempts loaded</p><button onClick={()=>resetLearning(detail.user)}>Reset learning history</button></div><h3>Sessions</h3><div style={{display:'grid',gap:8}}>{detail.sessions.map((x:any)=><div key={x.id} style={card}><b>{x.title}</b><div style={meta}>{x.track} · {x.kind} · {new Date(x.started*1000).toLocaleString('id-ID')} · {x.ended?'closed':'active'}</div><pre style={pre}>{JSON.stringify(x.summary,null,2)}</pre></div>)}</div><h3>Recent attempts</h3><div style={{overflowX:'auto',...card}}><table style={table}><thead><tr><th>Time</th><th>Track</th><th>Skill</th><th>Question</th><th>Result</th></tr></thead><tbody>{detail.attempts.map((x:any)=><tr key={x.id}><td>{new Date(x.ts*1000).toLocaleString('id-ID')}</td><td>{x.track}</td><td>{x.skill}</td><td>{x.question_id}</td><td>{x.payload?.correct?'✓':'×'}</td></tr>)}</tbody></table></div></>}</>}
   {tab==='quality'&&<><h2>Question reports</h2>{reports.length===0?<p>Belum ada laporan.</p>:<div style={{display:'grid',gap:8}}>{reports.slice(0,80).map((r:any,i)=><div key={i} style={card}><b>{r.reason}</b> · @{r.username}<div style={meta}>{r.signature} · {r.question_id} · reports {r.report_count}</div>{r.detail&&<p>{r.detail}</p>}<button onClick={()=>quarantine(r.signature,!r.quarantined)}>{r.quarantined?'Release':'Quarantine'}</button></div>)}</div>}<h2 style={{marginTop:28}}>Empirical difficulty watch</h2><div style={{overflowX:'auto',...card}}><table style={table}><thead><tr><th>Skill</th><th>N</th><th>Authored</th><th>Empirical</th><th>Accuracy</th><th>Skip</th><th>Mean</th></tr></thead><tbody>{highSignal.map((x:any)=><tr key={x.signature}><td>{x.skill}</td><td>{x.attempts}</td><td>{x.authored_level}</td><td>{x.empirical_level}</td><td>{Math.round(x.accuracy*100)}%</td><td>{Math.round(x.skip_rate*100)}%</td><td>{Math.round(x.mean_ms/1000)}s</td></tr>)}</tbody></table></div></>}
   {tab==='audit'&&<div style={{display:'grid',gap:8}}>{audit.length===0?<p>Belum ada audit event.</p>:audit.map((x:any)=><div key={x.id} style={card}><b>{x.action}</b><div style={meta}>{new Date(x.created_at*1000).toLocaleString('id-ID')} · actor {x.actor_user_id} · {x.target_type}:{x.target_id}</div>{Object.keys(x.detail||{}).length>0&&<pre style={pre}>{JSON.stringify(x.detail,null,2)}</pre>}</div>)}</div>}
  </>}
 </main>
}
const card:any={background:'white',border:'1px solid #dfe5ee',borderRadius:12,padding:14}
const meta:any={fontSize:12,color:'#71809b',marginTop:4}
const pre:any={whiteSpace:'pre-wrap',fontSize:11,background:'#f6f8fc',padding:10,borderRadius:8,overflow:'auto'}
const table:any={width:'100%',borderCollapse:'collapse',textAlign:'left'}
